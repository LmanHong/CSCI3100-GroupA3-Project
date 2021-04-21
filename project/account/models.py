from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# need to be extended if the base user is extended
class AccountManager(BaseUserManager):
    # method to create a user
    def create_user(self, email, username, password=None):
        # check format
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an username")
        
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )

        # update database
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # method to create a superuser
    def create_superuser(self, email, username, password=None):
        # call the normal user create function
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )

        # fields to be turned on for superusers
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        # update database
        user.save(using=self._db)
        return user
        
class Account(AbstractBaseUser):
    # fields for account module
    email = models.EmailField(verbose_name="email", max_length=64, unique=True)
    username = models.CharField(max_length=32, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # login field
    USERNAME_FIELD = 'email'

    # required fields, as the name suggests
    REQUIRED_FIELDS = ['username']

    objects = AccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

class Profile(models.Model):
    # choices tuple for valid gender choices stored in database
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Uncertain')
    )

    # fields for account module
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pictures/default.jpg', upload_to='profile_pictures')
    first_name = models.CharField(default=None, null=True, max_length=64)
    last_name = models.CharField(default=None, null=True, max_length=64)
    gender = models.CharField(default=None, null=True, max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(default=None, null=True, help_text='YYYY-MM-DD')
    job_title = models.CharField(default=None, null=True, max_length=128)
    passions = models.CharField(default=None, null=True, max_length=256, help_text='hiking, outdoors, cat lover')

    def __str__(self):
        return f'{self.user.username} Profile'

# called when a user is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# save the profile in database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()