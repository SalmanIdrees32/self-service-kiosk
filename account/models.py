from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django import forms
from datetime import date, datetime


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.FileField(upload_to='user/profile/images', blank=True, null=True)

    father_name = models.CharField(max_length=150,null=True, blank=True)
    mother_name = models.CharField(max_length=150,null=True, blank=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10,null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=100,null=True, blank=True)
    nid = models.CharField(max_length=20,null=True, blank=True)

    email_verification_code = models.CharField(max_length=6, blank=True, null=True)
    is_email_active = models.BooleanField(default=False)
    forget_password_token = models.CharField(max_length=100,blank=True, null=True )
    created_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if isinstance(self.birth_date, str):
            try:
                self.birth_date = datetime.strptime(self.birth_date, '%Y-%m-%d').date()
            except ValueError:
                self.birth_date = None

        if self.birth_date:
            today = date.today()
            self.age = today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        ordering = ('-id', )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Schools(models.Model):
    name = models.CharField(max_length=100 ,blank=True, null=True)
    address = models.CharField(max_length=200 , blank=True, null=True)
    icon = models.ImageField(upload_to='school/images' , blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='created_schools', blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True,blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='updated_schools', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "School"
        verbose_name_plural = "Schools"


class Campuses(models.Model):
    school = models.ForeignKey(Schools, on_delete=models.SET_NULL, related_name='campuses', blank=True, null=True)
    name = models.CharField(max_length=100 ,blank=True, null=True)
    address = models.CharField(max_length=200 , blank=True, null=True)
    icon = models.ImageField(upload_to='campus/images' , blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='created_campuses', blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True,blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='updated_campuses', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Campus"
        verbose_name_plural = "Campuses"


class Issues(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    icon = models.ImageField(upload_to='issue/images' , blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='created_issues', blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True,blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='updated_issues', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Issue"
        verbose_name_plural = "Issues"


class StudentSubmissions(models.Model):
    school = models.ForeignKey(Schools, on_delete=models.SET_NULL, related_name='student_submissions', blank=True, null=True)
    campus = models.ForeignKey(Campuses, on_delete=models.SET_NULL, related_name='student_submissions', blank=True, null=True)
    student = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='student_submissions', blank=True, null=True)
    issue = models.ForeignKey(Issues, on_delete=models.SET_NULL, related_name='student_submissions', blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    in_time = models.TimeField(blank=True, null=True)
    out_time = models.TimeField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    face_image = models.ImageField(upload_to='student/submissions', blank=True, null=True)
    attachment = models.FileField(upload_to='student/submissions', blank=True, null=True)
    student_ids = models.CharField(max_length=100, blank=True, null=True)
    student_id_4 = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='created_student_submissions', blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True,blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='updated_student_submissions', blank=True, null=True)

    class Meta:
        verbose_name = "Student Submission"
        verbose_name_plural = "Student Submissions"