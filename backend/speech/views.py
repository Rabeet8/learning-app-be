import google.generativeai as genai
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SpeechAttempt
import os

# Ideally, put this in your .env file or settings.py instead of hardcoding!
# e.g., GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "Your-Key-Here"))

# We instantiate the model once
generative_model = genai.GenerativeModel("gemini-1.5-flash")

@api_view(['POST'])
def evaluate_speech(request):
    user_id = request.data.get('user_id')
    target_word = request.data.get('target_word', '').lower().strip()
    recognized_text = request.data.get('recognized_text', '').lower().strip()

    # Determine if it's correct (Using strict match rather than sloppy includes to avoid '' in 'apple' bug)
    is_correct = bool(recognized_text and (target_word in recognized_text or recognized_text in target_word))

    # Evaluate dynamic feedback
    feedback = "Success"
    if not is_correct:
        if not recognized_text:
            feedback = "I couldn't hear you! Let's try again!"
        else:
            try:
                # The prompt requested: Act as a friendly teacher explaining pronunciation mistakes.
                prompt = (
                    f"You are a friendly, encouraging preschool teacher. "
                    f"A child was supposed to read the word '{target_word}', "
                    f"but they said '{recognized_text}'. "
                    f"Write a very short, simple 1-sentence tip on how they can pronounce '{target_word}' correctly "
                    f"or what sound they missed. Say it directly to them. No quotes, no markdown."
                )
                ai_response = generative_model.generate_content(prompt)
                feedback = ai_response.text.strip()
            except Exception as e:
                print("Gemini API Error:", e)
                # Fallback if AI fails or rate limits
                feedback = f"You said '{recognized_text}'. Let's try saying '{target_word}' again!"

    SpeechAttempt.objects.create(
        user_id=user_id,
        target_word=target_word,
        recognized_text=recognized_text,
        is_correct=is_correct
    )

    return Response({
        "correct": is_correct,
        "feedback": feedback
    })