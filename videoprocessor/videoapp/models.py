from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Subtitle(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    timestamp = models.CharField(max_length=20)  # To store time like "00:01:30"
    content = models.TextField()  # Subtitle text

    def __str__(self):
        return f"{self.timestamp} - {self.content[:30]}"
