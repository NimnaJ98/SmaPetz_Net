from django.db import models
from users.models import User
from .validators import fileSize
from django.core.validators import FileExtensionValidator

# Create your models here.


class Post(models.Model):
    picture = models.ImageField(upload_to='images', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank= True)
    video =  models.FileField(upload_to='videos', blank= True, validators=[fileSize, FileExtensionValidator(['mp4'])])
    caption = models.TextField()
    liked_by = models.ManyToManyField(User, default=None, blank=True, related_name='likes')
    tags = models.CharField(max_length=100, blank=True)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.caption)

    #get the users who liked a post
    def get_liked(self):
        return self.liked_by.all()

    #property = will be treated as a field
    @property
    def likes_count(self):
        return self.liked_by.all().count()

    def num_comment(self):
        return self.comment_set.all().count()

    class Meta:
        ordering =('-created',)

    
class Comment(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.pk)

REACTIONS = (
    ('Love', 'Love'),
    ('Angry', 'Angry'),
    ('Surprise', 'Surprise'),
    ('Sad', 'Sad'),
    ('Sick', 'Sick'),
)

class Reaction(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value= models.CharField(choices=REACTIONS, max_length=10)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"

