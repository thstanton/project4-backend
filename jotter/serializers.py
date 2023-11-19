from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Context, WordBank, Word, Jotter, Image, PupilClass
import uuid

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    # Add users to the pupil or teacher group when account created
    def create(self, validated_data):
        group_id = self.context['request'].parser_context['kwargs']['group_id']
        print(group_id)

        user = super(UserSerializer, self).create(validated_data)

        group = Group.objects.get(id=group_id)
        user.groups.add(group)

        return user


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['word']

class WordBankSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    words = WordSerializer(many=True)

    class Meta:
        model = WordBank
        fields = ['title', 'words']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['url']
    
class ContextSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    wordbanks = WordBankSerializer(many=True)
    images = ImageSerializer(many=True)

    class Meta:
        model = Context
        fields = ['title', 'prompt', 'instructions', 'author', 'wordbanks', 'images']

    def create(self, validated_data):
        wordbanks_data = validated_data.pop('wordbanks', [])
        images_data = validated_data.pop('images', [])

        context = Context.objects.create(**validated_data)

        for wordbank_data in wordbanks_data:
            words_data = wordbank_data.pop('words', [])
            new_wordbank = WordBank.objects.create(context=context, **wordbank_data)

            for word_data in words_data:
                word_value = word_data['word']
                try:
                    Word.objects.create(word_bank=new_wordbank, word=word_value)
                except Exception as e:
                    print(f"Error creating Word: {e}")

        for image_data in images_data:
            Image.objects.create(context=context, url=image_data['url'])

        return context
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.prompt = validated_data.get('prompt', instance.prompt)
        instance.instructions = validated_data.get('instructions', instance.instructions)

        instance.save()
        return instance

class PupilClassSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)
    pupils = UserSerializer(many=True, read_only=True)
    contexts = ContextSerializer(many=True, read_only=True)

    class Meta:
        model = PupilClass
        fields = ['name', 'teacher', 'year_group', 'access_key', 'pupils', 'contexts']
        extra_kwargs = {'access_key': {'required': False}}

    def create(self, validated_data):
        teacher = self.context['request'].user
        access_key = uuid.uuid4().hex[:8]
        pupil_class = PupilClass.objects.create(teacher=teacher, access_key=access_key, **validated_data)
        pupil_class.save()

        return pupil_class
        
class JotterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jotter
        fields = '__all__'

