from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.
class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self):
        return self.caption

class Author(models.Model):
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.firstName+" "+self.lastName
        # __str__(self) method tells how it's represented as a string in admin page

class Post(models.Model):
    title = models.CharField(max_length=30)
    excerpt = models.CharField(max_length=200)
    # imageName = models.CharField(max_length=100)
    image = models.ImageField(upload_to='posts', null=True)
    date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name="posts")
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

# images or files stored with the help of model have nested properties such as 'url' which gives url to that image

class Comment(models.Model):
    userName = models.CharField(max_length=120) # Your Name
    userEmail = models.EmailField() # Your Email
    text = models.TextField(max_length=400)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    