from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(
            self, email, date_of_birth,
            location, contact, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            name=name,
            location=location,
            contact=contact
            )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
            self, email, date_of_birth,
            location, name,  contact, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            contact=contact,
            date_of_birth=date_of_birth,
            location=location,
            name=name
            )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    name = models.CharField(max_length=40)
    contact = models.CharField('phone number', max_length=20)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True)
    location = models.CharField('your address', max_length=50)
    date_of_birth = models.DateField(help_text='YYYY-MM-DD')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth', 'name', 'contact', 'location']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    # use in terminal
    def __str__(self):
        return self.name
    
    # used in admin panel to display the name
    def get_username(self) -> str:
        return self.name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
