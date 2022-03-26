from django.db import models
from users.models import User
from .validators import fileSize
from django.core.validators import FileExtensionValidator

# Create your models here.


class Post(models.Model):
    picture = models.ImageField(upload_to='images/', null=True , blank= True)
    video =  models.FileField(upload_to='videos/', blank= True, validators=[fileSize, FileExtensionValidator(['mp4'])])
    caption = models.TextField()
    liked_by = models.ManyToManyField(User, default=None, blank=True, related_name='likes')
    tags = models.CharField(max_length=100, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.author)

    #get the authors
    def get_author(self):
        return self.author.all()

    def get_author_list(self):
        author_list = [a for a in self.get_author()]
        return author_list

    #get the users who liked a post
    def get_liked(self):
        return self.liked_by.all()

    #property = will be treated as a field
    @property
    def likes_count(self):
        return self.liked_by.all().count()

    #get the number of comment in a post
    def num_comment(self):
        return self.comment_set.all().count()

    #get the number of reactions in a post
    def num_reaction(self):
        return self.reaction_set.all().count()
    
    #get the reactions in a post
    def reaction_value(self):
        posts = self.author.all()
        love = angry = surprise = sad = sick = 0
        for reaction in posts:
            if reaction.value == 'Love':
                love += 1
            elif reaction.value == 'Angry':
                angry += 1
            elif reaction.value == 'Surprise':
                surprise += 1
            elif reaction.value == 'Sad':
                sad += 1
            elif reaction.value == 'Sick':
                sick += 1
        return {'Love': love, 'Angry': angry, 'Surprise': surprise, 'Sad': sad, 'Sick':sick}

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

