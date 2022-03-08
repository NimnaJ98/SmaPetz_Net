from django.db import models
from users.models import User

# Create your models here.


class Post(models.Model):
    picture = models.ImageField(upload_to='images', blank= True)
    caption = models.TextField()
    liked_by = models.ManyToManyField(User, default=None, blank=True, related_name='likes')
    tags = models.CharField(max_length=100, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authors')
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

    #get the users who liked a post
    def get_liked(self):
        return self.liked_by.all()

    #property = will be treated as a field
    @property
    def likes_count(self):
        return self.liked_by.all().count()

    #def user_liked_status(self, user):
        #pass

