from django.db import models
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self,email,password=None, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email , **kwargs)
        user.set_password(password=password)



    def normalize_email(self,email):
        return self.email.lower()