from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Blogpost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150,blank=False)
    description = RichTextUploadingField(null=True)
    short_description = models.TextField(default="")
    thumbnail=models.ImageField(upload_to="Blog/",default='thumbnail.jpeg')
    like = models.ManyToManyField(User,blank=True,related_name="like")
    viewer=models.ManyToManyField(User,related_name="viewer",blank=True)
    post_on=models.DateTimeField(auto_now=True,auto_now_add=False)

    def __str__(self):
        return '{}-{}'.format(self.title,self.author)

    def like_count(self):
        return self.like.all().count()


class Comment(models.Model):
    post = models.ForeignKey(Blogpost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    reply = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, related_name="replies")
    content = models.TextField(max_length=160)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.post, str(self.user))



class Branch(models.Model):
    name=models.CharField(max_length=200)
    president_image=models.ImageField(upload_to="Branch/",default="avatar7.png")
    president_message=models.TextField(max_length=1000)
    vicepresident_image=models.ImageField(upload_to="Branch/",default="avatar7.png")
    vicepresident_message=models.TextField(max_length=1000)
    created=models.DateTimeField(auto_now=True,auto_now_add=False)

    def __str__(self):
        return '{}-{}'.format(self.name,self.created.date())
