from django.db import models
from django.db import models
from profiles.models import Profile
from .validators import fileSize
from django.core.validators import FileExtensionValidator

#Post Model
class Post(models.Model):
    picture = models.ImageField(upload_to='images/', null=True , blank= True)
    video =  models.FileField(upload_to='videos/', blank= True, validators=[fileSize, FileExtensionValidator(['mp4'])])
    caption = models.TextField()
    liked_by = models.ManyToManyField(Profile, default=None, blank=True, related_name='likes')
    tags = models.CharField(max_length=100, blank=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='posts')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.author)
    
#to grab the number of likes
    def num_likes(self):
        return self.liked_by.all().count()

#to grab the number of comments
    def num_comments(self):
        return self.comment_set.all().count()


#to create the ordering of the posts by time
    class Meta:
        ordering = ('-created',)


#Comment Model 
class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.pk)

#Reaction Model
LIKE_CHOICES = (
    
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"