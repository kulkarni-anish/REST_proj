from django.contrib.auth.models import BaseUserManager

class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **other_fields):

        # other_fields.setdefault('is_staff',True)
        # other_fields.setdefault('is_superuser',True)
        # other_fields.setdefault('is_active',True)

        # if other_fields.get('is_staff') is not True:
        #     raise ValueError('Superuser must be assigned is_staff=True')

        # if other_fields.get('is_superuser') is not True:
        #     raise ValueError('Superuser must be assigned is_superuser=True')


        # return self.create_user(email, username, password, **other_fields)


        user = self.create_user(
            username,
            email,
            password,
        )
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user