from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name



class Notes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    categories = models.ForeignKey(Categories,on_delete=models.CASCADE,null=True,blank=True)
    image = models.ImageField(upload_to="post/" ,null= True,blank= True)
    date = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField('auth.User', related_name='liked_students', through='Like')


    def __str__(self):
        return self.title


class NotesShearing(models.Model):
    notes = models.ForeignKey(Notes,on_delete=models.CASCADE)
    shared_by = models.OneToOneField(User,on_delete=models.CASCADE,related_name="by")
    shared_to = models.OneToOneField(User,on_delete=models.CASCADE,related_name="to")

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Notes,on_delete=models.CASCADE)
    comment = models.CharField(max_length=300)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Notes, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Follow(models.Model):
    followed_by = models.ForeignKey(User,on_delete=models.CASCADE , related_name='f_by')
    followed_to = models.ForeignKey(User,on_delete=models.CASCADE ,related_name='f_to')