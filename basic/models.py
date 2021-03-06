from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import MyUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.
class Workspace(models.Model):
    options = (
        ('personal', 'Personal'),
        ('collaborative', 'Collaborative'),
    )
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type       = models.CharField(max_length=50, choices=options)

class ToDo(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tasks', on_delete=models.CASCADE)
    name        = models.CharField(max_length=50)
    description = models.TextField(null=True)
    status      = models.BooleanField(default=False)
    date        = models.DateTimeField(auto_now=True,auto_now_add=False)
    updates     = models.IntegerField(default=0)
    deadline    = models.DateTimeField(default=timezone.now)
    workspace   = models.ForeignKey(Workspace, on_delete=models.PROTECT, default=None)

    def __str__(self):
        return self.name



class Notes(models.Model):
    title       = models.CharField(max_length=100)
    content     = models.TextField()
    date        = models.DateField(default=timezone.now)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    workspace   = models.ForeignKey(Workspace, on_delete=models.PROTECT, default=None)



class Journal(models.Model):
    name        = models.CharField(max_length=50)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notes       = models.ForeignKey(Notes, on_delete=models.PROTECT, default=None)
    workspace   = models.ForeignKey(Workspace, on_delete=models.PROTECT, default=None)
    







class MyUser(AbstractBaseUser, PermissionsMixin):

    username        = models.CharField(max_length=50)
    email           = models.EmailField(max_length=60,unique=True)
    profile_picture = models.ImageField(blank=True)
    is_admin        = models.BooleanField(default = False)
    is_active       = models.BooleanField(default = True)
    is_staff        = models.BooleanField(default = False)
    is_superuser    = models.BooleanField(default = False)
    date_joined     = models.DateTimeField(default=timezone.now)


    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']   

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')
        
    def __str__(self):
        return self.email

    #Does this user have permisssion to view this app? (ALWAYS YES FOR SIMPLICITY)
    # def has_module_perms(self, app_Label):
    #     return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)       #post_save is the signal
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)