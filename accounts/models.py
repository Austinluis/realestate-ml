from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = [('admin', 'Admin'), ('user', 'User')]

class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'accounts_user'

    def __str__(self):
        return self.email

    def is_admin(self):
        return self.role == 'admin'
