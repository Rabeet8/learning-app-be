from django.db import models

class SpeechAttempt(models.Model):
    user_id = models.CharField(max_length=255)
    target_word = models.CharField(max_length=100)
    recognized_text = models.TextField()
    is_correct = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} - {self.target_word} - {self.is_correct}"