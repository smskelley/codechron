from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    posts = models.IntegerField()
    email = models.EmailField(max_length=75)

    def __unicode__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=100)
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey(Author)
    body = models.TextField()
    published = models.BooleanField()

    def __unicode__(self):
        return self.title

class Comment(models.Model):
    pub_date = models.DateTimeField('date published')
    author = models.CharField(max_length=100)
    post = models.ForeignKey(Post)
    body = models.TextField()

    def __unicode__(self):
        return self.body
