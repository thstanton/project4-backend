from rest_framework import permissions, generics, status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Q

from .serializers import *
from .models import *

# ! User-related Views

class ListUsers(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class CreateUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class EditUser(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class SelfUser(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        print(user)
        return User.objects.filter(username=user)

# ! Context-related Views

# ? List all contexts created by the user
class ListContexts(generics.ListAPIView):
    serializer_class = ContextListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Context.objects.filter(author=user)

# ? Show all contexts assigned to a particular pupil    
class AssignedContextsView(generics.ListAPIView):
    serializer_class = ContextSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Extract user from the request
        user = self.request.user

        # Get the PupilClasses associated with the user
        pupil_classes = PupilClass.objects.filter(pupils=user)

        # Get the Contexts assigned to those PupilClasses
        contexts = Context.objects.filter(assigned_classes__in=pupil_classes)

        # Exclude Contexts for which the user has already created a Jotter
        jotter_contexts = Jotter.objects.filter(author=user).values_list('context', flat=True)
        contexts = contexts.exclude(id__in=jotter_contexts)

        return contexts

# ? GET - Context detail view (PK), PUT - Edit (Title, Prompt, Instructions only), DELETE - delete context (PK)   
class ContextDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Context.objects.all()
    serializer_class = ContextSerializer
    permission_classes = [permissions.IsAuthenticated]

# ? Create a new context
class CreateContext(generics.CreateAPIView):
    queryset = Context.objects.all()
    serializer_class = ContextSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# ? Assign/Unassign a context to/from a class
@api_view(['POST'])
def assoc_class_add(request, context_id, class_id):
    pupil_class = PupilClass.objects.get(id=class_id)
    context = Context.objects.get(id=context_id)
    pupil_class.contexts.add(context)

    serializer = PupilClassSerializer(pupil_class)
    serialized_data = serializer.data

    return Response({ "message": f"Context {Context.objects.get(id=context_id)} assigned to class {pupil_class}", "pupil_class": serialized_data })

@api_view(['DELETE'])
def assoc_class_remove(request, context_id, class_id):
    pupil_class = PupilClass.objects.get(id=class_id)
    pupil_class.contexts.remove(context_id)
    return Response({ "message": f"Context {Context.objects.get(id=context_id)} unassigned to class {pupil_class}" })

# ! Word, WordBank & Image-Related Views
class CreateWordBank(generics.CreateAPIView):
    queryset = WordBank.objects.all()
    serializer_class = WordBankSerializer
    permission_classes = [permissions.IsAuthenticated]

class WordBank(generics.RetrieveUpdateDestroyAPIView):
    queryset = WordBank.objects.all()
    serializer_class = WordBankSerializer
    permission_classes = [permissions.IsAuthenticated]

class WordListCreate(generics.ListCreateAPIView):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return WordListSerializer
        return WordSerializer

class SingleWord(generics.RetrieveUpdateDestroyAPIView):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    permission_classes = [permissions.IsAuthenticated]

class CreateImage(generics.CreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

class SingleImage(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

# ! Class-Related Views

class ClassList(generics.ListAPIView):
    serializer_class = PupilClassSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return PupilClass.objects.filter(teacher=user)

class CreatePupilClass(generics.CreateAPIView):
    queryset = PupilClass.objects.all()
    serializer_class = PupilClassSerializer
    permission_classes = [permissions.IsAuthenticated]

class SingleClass(generics.RetrieveUpdateDestroyAPIView):
    queryset = PupilClass.objects.all()
    serializer_class = PupilClassSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['POST'])
@parser_classes([JSONParser])
def join_class(request):
    key = request.data['key']
    pupil_class = PupilClass.objects.get(access_key=key)
    pupil_class.pupils.add(request.user)
    return Response({ "message": f"User {request.user} added to class {pupil_class}"}, status=201)

@api_view(['DELETE'])
@parser_classes([JSONParser])
def remove_from_class(request, class_id, pupil_id):
    pupil_class = PupilClass.objects.get(id=class_id)
    pupil_class.pupils.remove(pupil_id)
    return Response({ "message": f"User {User.objects.get(id=pupil_id)} removed from class {pupil_class}"}, status=202)

# ! Jotter-Related Views

class CreateJotter(generics.CreateAPIView):
    queryset = Jotter.objects.all()
    serializer_class = JotterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        context_id = self.request.data.get('context')
        context_instance = Context.objects.get(pk=context_id)
        serializer.save(author=self.request.user, context=context_instance, complete=False)

class SingleJotter(generics.RetrieveUpdateDestroyAPIView):
    queryset = Jotter.objects.all()
    serializer_class = JotterSerializer
    permission_classes = [permissions.IsAuthenticated]

class ListOwnIncompleteJotters(generics.ListAPIView):
    serializer_class = JotterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Jotter.objects.filter(author=user, complete=False)
    
class ListOwnCompleteJotters(generics.ListAPIView):
    serializer_class = JotterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Jotter.objects.filter(author=user, complete=True)
    
class ListPupilJotters(generics.ListAPIView):
    serializer_class = JotterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        pupil = self.context['request'].parser_context['kwargs']['pupil_id']
        return Jotter.objects.filter(author=pupil, complete=True)
    
class ListClassContextJotters(generics.ListAPIView):
    serializer_class = JotterListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        context_id = self.kwargs.get('context_id')
        pupil_class_id = self.kwargs.get('class_id')
        queryset = Jotter.objects.filter(
            Q(context_id=context_id) &
            Q(complete=True) &
            Q(author__pupil_classes__id=pupil_class_id)
        ).order_by('author__first_name')

        return queryset

class ListContextJotters(generics.ListAPIView):
    serializer_class = JotterListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        context_id = self.kwargs.get('context_id')
        queryset = Jotter.objects.filter(
            Q(context_id=context_id) &
            Q(complete=True)
        ).order_by('author__pupil_classes__name')

        return queryset
    
