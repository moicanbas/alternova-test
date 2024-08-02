from django.contrib.auth.models import AbstractUser
from django.db import models
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher_suite = Fernet(key)

class CustomUser(AbstractUser):
    identification = models.CharField(max_length=150)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False) 
    cellphone = models.CharField(max_length=150)
    
    class Meta:
        verbose_name = "Usuario"
        db_table = 'user_usuarios'
    
    def get_encrypted_field(self, field_value):
        return cipher_suite.encrypt(field_value.encode()).decode()

    def get_decrypted_field(self, encrypted_value):
        return cipher_suite.decrypt(encrypted_value.encode()).decode()
        
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.identification}"

    
    