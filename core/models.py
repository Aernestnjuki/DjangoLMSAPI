from django.db import models
from django.utils.text import slugify
from shortuuid.django_fields import ShortUUIDField
from django.utils import timezone
from moviepy.editor import VideoFileClip

import math

from userAuth.models import User, Profile

LANGUAGE = (
    ('English', 'English'), # key , value
    ('Kiswahili', 'Kiswahili'),
    ('German', 'German')
)
LEVEL = (
    ('Beginner', 'Beginner'), 
    ('Intermediate', 'Intermediate'),
    ('Advanced', 'Advanced')
)
TEACHER_STATUS = (
    ('Draft', 'Draft'), 
    ('Disabled', 'Disabled'),
    ('Published', 'Published')
)
PLATFORM_STATUS = (
    ('Draft', 'Draft'), 
    ('Review', 'Review'),
    ('Rejected', 'Rejected'),
    ('Disabled', 'Disabled'),
    ('Published', 'Published')
)

class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to='lms-file', blank=True, null=True, default='default.jpg')
    full_name = models.CharField(max_length=100)
    bio = models.CharField(max_length=100, null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.full_name
    
    # get all stedents of a teacter
    def students(self):
        return CartOrderItem.objects.filter(teacter=self)
    
    # get total courses of ateacter
    def courses(self):
        return Course.objects.filter(teacher=self)
    
    # get total reviews of a teacher
    def reviews(self):
        return Course.objects.filter(teacher=self).count()

# category eg Python, Java, JavaScript etc
class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to='lms-file', default='default.jpg', null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    class Meta:
        verbose_name_plural  = 'Category'
        ordering = ['title'] # ascending order from A, B, ... Z

    def __str__(self):
        return self.title
    
    # count courses related to this category
    def course_count(self):
        return Course.objects.filter(category=self).count()
    
    # slugify the title
    def save(self, *args, **kwargs):
        if self.slug == '' or self.slug == None:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)


class Course(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    file = models.FileField(upload_to='lms-file', blank=True, null=True) # the intro video
    image = models.FileField(upload_to='lms-file', blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    language = models.CharField(max_length=100, choices=LANGUAGE, default='English')
    level = models.CharField(max_length=100, choices=LEVEL, default='Beginner')
    platform_status = models.CharField(max_length=100, choices=PLATFORM_STATUS, default='Published')
    teacher_course_status = models.CharField(max_length=100, choices=TEACHER_STATUS, default='Published')
    featured = models.BooleanField(default=False)
    course_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet='1234567890')
    slug = models.SlugField(unique=True, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug == '' or self.slug == None:
            self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)

    # get stuednts enrolled in a given course
    def students(self):
        return EnrolledCourse.objects.filter(course=self)
    
    # get all lesson parts in a course curriculum eg part a can have 5 lesson etc
    def curriculum(self):
        return VariantItem.objects.filter(variant__course=self)
    
    def lectures(self):
        return VariantItem.objects.filter(variant__course=self)
    
    # get average rating of a course
    def average_rating(self):
        average_rating = Review.objects.filter(course=self, active=True).aggregate(avg_rating=models.Avg('rating'))
        return average_rating['avg_rating']
    
    def rating_count(self):
        return Review.objects.filter(course=self, active=True).count()
    
    # get the reviews
    def reviews(self):
        return Review.objects.filter(course=self, active=True)
    

# variant model is like all the section in a full course containing videos related to that section
class Variant(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    variant_id = ShortUUIDField(unique=True, length=5, max_length=20, alphabet='1234567890')
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    # get all lession in that course section
    def variant_item(self):
        return VariantItem.ojects.filter(variant=self)
    
# model to hold all the lessons in the Variant course models
class VariantItem(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='variant_item')
    title = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='lms-file')
    duration = models.DurationField(null=True, blank=True)
    content_duration = models.CharField(max_length=1000, null=True, blank=True)
    preview = models.BooleanField(default=False)
    variant_item_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet='1234567890')
    data = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.variant.title} - {self.title}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # get the actual length of the uploaded video in min and sec
        if self.file:
            clip = VideoFileClip(self.file.path)
            deration_time = clip.duration
            minutes, remainder = divmod(deration_time, 60)
            minutes = math.floor(minutes)
            seconds = math.floor(remainder)

            self.content_duration = f'{minutes}m {seconds}s'
            super().save(update_fields=['content_duration'])


class Question_Answer(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    qa_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet='1234567890')
    data = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} = {self.course.title}'
    
    # order questions from newest to oldest
    class Meta:
        ordering = ['-date']

    def messages(self):
        return Question_Answer_Message.objects.filter(question=self)
    
    # get the user posting the questiion Profile pic
    def profile(self):
        return Profile.objects.get(user=self.user)
    
class Question_Answer_Message(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    question = models.ForeignKey(Question_Answer, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    qam_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet='1234567890')
    data = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} = {self.course.title}'
    
    # order messages from oldest to newest
    class Meta:
        ordering = ['date']
    
    # get the user posting the questiion Profile pic
    def profile(self):
        return Profile.objects.get(user=self.user)