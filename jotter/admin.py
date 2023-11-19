from django.contrib import admin
from .models import Context, Jotter, WordBank, Word, Image, PupilClass

admin.site.register(PupilClass)
admin.site.register(Context)
admin.site.register(Image)
admin.site.register(WordBank)
admin.site.register(Word)
admin.site.register(Jotter)