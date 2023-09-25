from django.db import models

from students.models import Student
from companies.models import Job


class Like(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    student_liked = models.BooleanField(default=False)
    company_liked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"<Like> {self.student}: {self.student_liked} - {self.job}: {self.company_liked}"

    class Meta:
        ordering = ["-student_liked", "-company_liked"]
        verbose_name_plural = "Likes des utilisateurs"
        verbose_name = "Like"


class Chats(models.Model):
    chat = models.CharField(max_length=2000)
    date = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    by = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f"<Chat> {self.student} - {self.job}"

    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Messages échangés"
        verbose_name = "Message"
