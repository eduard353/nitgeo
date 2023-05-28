import hashlib

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string

from .validators import validate_birth_date

User = get_user_model()


class ActivationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='activation_token')
    token = models.CharField(max_length=32, default='', unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}\'s activate token'

    def save(self, *args, **kwargs):
        self.token = get_random_string(length=32)
        super(ActivationToken, self).save(*args, **kwargs)

    def verify_token(self):
        validate_exp = timezone.localtime(self.created) > timezone.now() - timezone.timedelta(days=1)
        if validate_exp:
            return True
        return False


class PasswordResetToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='password_reset_token')
    token = models.CharField(max_length=32, default='', unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}\'s password reset token'

    def save(self, *args, **kwargs):
        self.token = get_random_string(length=32)
        super(PasswordResetToken, self).save(*args, **kwargs)

    def verify_token(self):
        validate_exp = timezone.localtime(self.created) > timezone.now() - timezone.timedelta(days=1)
        if validate_exp:
            return True
        return False


class Profile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='profile')
    avatar = models.URLField(max_length=255, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(validators=[validate_birth_date])
    bio = models.TextField()
    info = models.CharField(max_length=255)

    def __str__(self):
        return f'Profile\'s of user {self.user.username}'

    def create_avatar(self):
        md5_hash = hashlib.md5(self.user.email.lower().encode('utf-8')).hexdigest()
        gravatar_url = f'https://www.gravatar.com/avatar/{md5_hash}?d=identicon&s={200}'
        self.avatar = gravatar_url

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
        if not self.avatar:
            self.create_avatar()
        super().save(*args, **kwargs)
