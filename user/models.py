from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    """
    Gerenciador de usuário personalizado para o nosso modelo de usuário personalizado.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Cria e salva um usuário com o email e senha fornecidos.
        """
        if not email:
            raise ValueError('O email deve ser definido')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Cria e salva um superusuário com o email e senha fornecidos.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuário deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuário deve ter is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de usuário personalizado para nossa aplicação.
    """
    email = models.EmailField(unique=True)
    cpf_cnpj= models.TextField(max_length=40, unique=True)
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    nasc = models.DateField(null=True, blank=True)  # data de nascimento
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)  # Ex: 'SP', 'RJ'
    endereco = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Um administrador não é automaticamente um superusuário
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'sobrenome']  # Campos obrigatórios além do email e senha

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Retorna o nome completo do usuário.
        """
        return f"{self.nome} {self.sobrenome}"

    def get_short_name(self):
        """
        Retorna o nome abreviado do usuário.
        """
        return self.nome