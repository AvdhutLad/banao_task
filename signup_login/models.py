from django.db import models

# Create your models here.

class User(models.Model):
    USER_TYPE_CHOICES = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to="profile_pics", default="")
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    user_type = models.CharField(max_length=7, choices=USER_TYPE_CHOICES)
    address_line1 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='blog_images/',default="")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blog_posts')
    summary = models.TextField(max_length=300)
    content = models.TextField()
    is_draft = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
