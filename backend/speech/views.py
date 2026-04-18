import google.generativeai as genai
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SpeechAttempt
import os

genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "Your-Key-Here"))

generative_model = genai.GenerativeModel("gemini-1.5-flash")

@api_view(['POST'])
def evaluate_speech(request):
    user_id = request.data.get('user_id')
    target_word = request.data.get('target_word', '').lower().strip()
    recognized_text = request.data.get('recognized_text', '').lower().strip()

    is_correct = bool(recognized_text and (target_word in recognized_text or recognized_text in target_word))

    feedback = "Success"
    if not is_correct:
        if not recognized_text:
            feedback = "I couldn't hear you! Let's try again!"
        else:
            try:
                prompt = (
                    f"You are a friendly, encouraging preschool teacher. "
                    f"A child was supposed to read the word '{target_word}', "
                    f"but they said '{recognized_text}'. "
                    f"If what they said sounds somewhat close or shares similar sounds, give them a short 1-sentence tip on what sound they missed and encourage them to try again. "
                    f"If what they said is entirely wrong, just say specifically: 'You said {recognized_text}, but the word is {target_word}. Let's try again!' "
                    f"Say it directly to them. No quotes, no markdown, keep it very simple."
                )
                ai_response = generative_model.generate_content(prompt)
                feedback = ai_response.text.strip()
            except Exception as e:
                print("Gemini API Error:", e)
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