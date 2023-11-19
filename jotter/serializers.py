from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Context, WordBank, Word, Jotter, PupilClass, Image

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['word']

class WordBankSerializer(serializers.ModelSerializer):
    words = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = WordBank
        fields = ['title', 'words']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['url']

class PupilClassSerializer(serializers.ModelSerializer):
    pupils = UserSerializer(many=True)
    teacher = UserSerializer()
    class Meta:
        model = PupilClass
        fields = ['name', 'teacher', 'year_group', 'access_key']

class ContextCreateSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    wordbanks = WordBankSerializer(many=True)
    images = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Context
        fields = ['title', 'prompt', 'instructions', 'images', 'wordbanks', 'author']

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])  # Provide a default empty list if 'images' is not present
        wordbanks_data = validated_data.pop('wordbanks', [])  # Provide a default empty list if 'wordbanks' is not present

        context = Context.objects.create(**validated_data)

        for wordbank_data in wordbanks_data:
            words_data = wordbank_data.pop('words', [])
            new_wordbank = WordBank.objects.create(context=context, **wordbank_data)

            for word_data in words_data:
                Word.objects.create(word_bank=new_wordbank, word=word_data)

        for image_data in images_data:
            Image.objects.create(context=context, url=image_data)

        return context
    
class ContextSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    wordbanks = WordBankSerializer(many=True)
    images = serializers.ListField(child=serializers.CharField())
    classes = PupilClassSerializer(many=True, required=False)

    class Meta:
        model = Context
        fields = ['title', 'prompt', 'instructions', 'images', 'wordbanks', 'author', 'classes']

class UpdateContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Context
        fields = ['title', 'prompt', 'instructions']

class JotterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jotter
        fields = '__all__'

