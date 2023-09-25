from __future__ import annotations
from typing import TYPE_CHECKING, Optional

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


if TYPE_CHECKING:
    from students.models import Student
    from companies.models import Company


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user: User = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.company = None
        user.student = None
        user.save(using=self._db)
        return user


class User(AbstractUser):
    company: Optional[Company]
    student: Optional[Student]

    username = None
    first_name = None
    last_name = None
    email = models.EmailField(("Adresse mail"), max_length=100, unique=True)
    finished_inscription = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def is_student(self):
        return hasattr(self, "student")

    def is_company(self):
        return hasattr(self, "company")

    def __str__(self):
        return self.email

    class Meta:
        ordering = ["-date_joined", "email", "-last_login"]
        verbose_name_plural = "Utilisateurs"
        verbose_name = "Utilisateur"
