from django.db import models
from django.utils.text import slugify
from shortuuid.django_fields import ShortUUIDField
from django.utils import timezone

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
    language = models.CharField(choices=LANGUAGE, default='English')
    level = models.CharField(choices=LEVEL, default='Beginner')
    platform_status = models.CharField(choices=PLATFORM_STATUS, default='Published')
    teacher_course_status = models.CharField(choices=TEACHER_STATUS, default='Published')
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