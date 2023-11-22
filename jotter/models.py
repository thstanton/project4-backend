from django.db import models
from django.contrib.auth.models import User

class Context(models.Model):
    title = models.CharField(max_length=100)
    prompt = models.CharField(max_length=200)
    instructions = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class PupilClass(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, related_name='classes_taught', on_delete=models.CASCADE)
    year_group = models.CharField(max_length=30)
    access_key = models.CharField(max_length=8)
    pupils = models.ManyToManyField(User, blank=True, related_name='pupil_classes')
    contexts = models.ManyToManyField(Context, related_name='assigned_classes', blank=True)

    def __str__(self):
        return self.name
    
class Image(models.Model):
    url = models.CharField(max_length=200)
    context = models.ForeignKey(Context, related_name='images', on_delete=models.CASCADE)

class Jotter(models.Model):
    context = models.ForeignKey(Context, on_delete=models.CASCADE)
    body = models.TextField(blank=True, null=True)
    complete = models.BooleanField(default=False)
    author = models.ForeignKey(User, related_name='owned_jotters', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.context}, {self.author}"

class WordBank(models.Model):
    title = models.CharField(max_length=100)
    context = models.ForeignKey(Context, related_name='wordbanks', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Word(models.Model):
    word = models.CharField(max_length=30)
    word_bank = models.ForeignKey(WordBank, related_name='words', on_delete=models.CASCADE)

    def __str__(self):
        return self.word
    
