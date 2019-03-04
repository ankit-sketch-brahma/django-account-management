from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

from test_project.config import *


USER_TYPE_CHOICES = (
    ('A', 'Admin'),
    ('H', 'HOD'),
    ('F', 'Faculity'),
    ('S', 'Student'),
)


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, full_name, password, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Email id is required')
        email=self.normalize_email(email)

        if is_superuser:
            user = self.model(
                email=self.normalize_email(email),
                full_name=full_name,
                is_superuser=True,
                user_type=USER_TYPE_CHOICES[0][0],
                is_staff=True,
                **extra_fields
            )
        else:
            user = self.model(
                email=self.normalize_email(email),
                full_name=full_name,
                **extra_fields
            )

        user.set_password(password)
        user.save(force_insert=True)
        return user

    def create_user(self, email, full_name, password=None, **extra_fields):
        return self._create_user(email, full_name, password, False, **extra_fields)

    def create_superuser(self, email, full_name, password, **extra_fields):
        user = self._create_user(email, full_name, password, True, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Create a custom user model by inheriting AbstractBaseUser
    """
    user_id = models.CharField(primary_key=True, default=generate_unique_object_id, editable=False, max_length=24)
    full_name = models.CharField(blank=True, null=True, max_length=100)
    email = models.EmailField(unique=True, max_length=254,)
    user_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=1, db_index=True)
    is_staff = models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(blank=True, null=True, db_index=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    # def save(self, *args, **kwargs):
    #     if self.user_type == 'I':
    #         self.profile_url = reverse('user_management:institute_profile', kwargs={
    #             'slug': slugify(self.full_name),
    #             'user_id': self.user_id
    #         })
    #     if self.user_type == 'S':
    #         self.profile_url = reverse('user_management:student_profile', kwargs={
    #             'slug': slugify(self.full_name),
    #             'user_id': self.user_id
    #         })
    #     super(CustomUser, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        try:
            return self.full_name.split(' ')[0]
        except:
            return ''

    @staticmethod
    def get_user_by_email(email_id):
        try:
            return CustomUser.objects.get(email_id=email_id)
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    def get_user_by_id(user_id):
        try:
            return CustomUser.objects.get(user_id=user_id)
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    def get_user_by_user_id(user_id):
        try:
            return CustomUser.objects.get(user_id=user_id)
        except CustomUser.DoesNotExist:
            return None

    def __str__(self):
        return self.email


class HOD(models.Model):
    id = models.CharField(default=generate_unique_object_id, max_length=24, primary_key=True)
    author = models.OneToOneField(CustomUser, related_name='hod', blank=True, null=True)

    class Meta:
        verbose_name = 'HOD'
        verbose_name_plural = 'HOD'

    def __str__(self):
        return str(self.author)

    @staticmethod
    def get_hod_by_id(hod_id):
        try:
            return HOD.objects.get(id=hod_id)
        except HOD.DoesNotExist:
            return None

class Faculity(models.Model):
    id = models.CharField(default=generate_unique_object_id, max_length=24, primary_key=True, blank=True)
    author = models.OneToOneField(CustomUser, related_name='faculity')
    added_by = models.ForeignKey(HOD, related_name='faculity_added', blank=True, null=True)

    class Meta:
        verbose_name = 'Faculity'
        verbose_name_plural = 'Faculities'

    def __str__(self):
        return str(self.author)

    @staticmethod
    def get_faculity_by_id(faculity_id):
        try:
            return Faculity.objects.get(id=faculity_id)
        except Faculity.DoesNotExist:
            return None


class Student(models.Model):
    id = models.CharField(default=generate_unique_object_id, max_length=24, primary_key=True)
    author = models.OneToOneField(CustomUser, related_name='student')
    added_by = models.ForeignKey(Faculity, related_name='student_added', blank=True, null=True)
    is_varified = models.BooleanField(default=False, blank=True)
    is_request_sent_for_varify = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return str(self.author)

    @staticmethod
    def get_student_by_id(student_id):
        try:
            return Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return None

class StudentMark(models.Model):
    id = models.CharField(default=generate_unique_object_id, max_length=24, primary_key=True)
    author = models.ForeignKey(Student, related_name='student_mark')
    subject = models.CharField(blank=True, null=True, max_length=100)
    mark = models.CharField(blank=True, null=True, max_length=10)

    def __str__(self):
        return '%s %s %s' % (self.subject, '->',  self.author.author.full_name)
