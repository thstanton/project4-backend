from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Context, WordBank, Word, Jotter, Image, PupilClass
import uuid

class NestedTeacherUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

class NestedPupilClassSerializer(serializers.ModelSerializer):
    teacher = NestedTeacherUserSerializer(read_only=True)

    class Meta:
        model = PupilClass
        fields = ['name', 'teacher', 'year_group']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    pupil_classes = NestedPupilClassSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'groups', 'pupil_classes', 'email', 'password']
    
    extra_kwargs = {
        'password': {'write_only': True},
    }

    # Add users to the pupil or teacher group when account created
    def create(self, validated_data):
        group_id = self.context['request'].parser_context['kwargs']['group_id']
        password = validated_data.pop('password')
        user = super().create(validated_data)
        group = Group.objects.get(id=group_id)
        user.groups.add(group)
        user.set_password(password)
        user.save()
        return user
    
class PupilUserSerializer(serializers.ModelSerializer):
    pupil_classes = 'PupilClassSerializer(many=True)'
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'pupil_classes', 'groups']

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = '__all__'

class WordListSerializer(serializers.ListSerializer):
    child = WordSerializer()

class WordBankSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    words = WordSerializer(many=True, read_only=True)

    class Meta:
        model = WordBank
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
    
class ContextSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    wordbanks = WordBankSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    assigned_classes = NestedPupilClassSerializer(many=True, read_only=True)

    class Meta:
        model = Context
        fields = ['id', 'title', 'prompt', 'instructions', 'author', 'wordbanks', 'images', 'assigned_classes']
    
    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.prompt = validated_data.get('prompt', instance.prompt)
    #     instance.instructions = validated_data.get('instructions', instance.instructions)

    #     instance.save()
    #     return instance

class PupilClassSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)
    pupils = PupilUserSerializer(many=True, read_only=True)
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
    author = PupilUserSerializer(read_only=True)
    context = ContextSerializer(read_only=True)

    class Meta:
        model = Jotter
        fields = '__all__'

