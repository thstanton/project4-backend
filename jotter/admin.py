from django.contrib import admin
from .models import Context, Jotter, WordBank, Word, PupilClass, Image
# Register your models here.
admin.site.register(PupilClass)
admin.site.register(Context)
admin.site.register(Image)
admin.site.register(WordBank)
admin.site.register(Word)
admin.site.register(Jotter)