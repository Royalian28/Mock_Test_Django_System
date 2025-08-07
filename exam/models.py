from django.db import models

class ExamSession(models.Model):
    exam_name = models.CharField(max_length=100)
    duration = models.IntegerField(help_text="Duration in minutes")
    json_file_name = models.CharField(max_length=255)
    started_at = models.DateTimeField(auto_now_add=True)

    # Result-related fields (to be filled after exam)
    marks_obtained = models.IntegerField(default=0)
    total_marks = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.exam_name} - {self.started_at.strftime('%Y-%m-%d %H:%M:%S')}"
