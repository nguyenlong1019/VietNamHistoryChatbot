from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# 1 user có nhiều Chat
# 1 chat có nhiều question


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=timezone.now)
    
    def __str__(self):
        return f"{self.pk}-{self.created_at}"

    # lấy các message thuộc về một chat cụ thể
    def get_messages(self):
        messages = list(self.message_set.all())
        return messages


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk}-{self.chat}-{self.created_at}"
