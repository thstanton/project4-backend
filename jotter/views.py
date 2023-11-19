from rest_framework import authentication, permissions, generics, status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.contrib.auth.models import User

from .serializers import *
from .models import *

# ! User-related Views

class ListUsers(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]

class CreateUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class EditUser(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# ! Context-related Views

# ? List all contexts created by the user
class ListContexts(generics.ListAPIView):
    serializer_class = ContextSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Context.objects.filter(author=user)

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
    PupilClass.objects.get(id=class_id).contexts.add(context_id)
    return Response({ "message": f"Context {context_id} assigned to class {class_id}" }).status_code(201)

@api_view(['DELETE'])
def assoc_class_remove(request, context_id, class_id):
    PupilClass.objects.get(id=class_id).contexts.remove(context_id)
    return Response({ "message": f"Context {context_id} unassigned to class {class_id}" }).status_code(202)

# ! Word and WordBank-Related Views

class WordBank(generics.RetrieveUpdateDestroyAPIView):
    queryset = WordBank.objects.all()
    serializer_class = WordBankSerializer
    permission_classes = [permissions.IsAuthenticated]

class SingleWord(generics.RetrieveUpdateDestroyAPIView):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    permission_classes = [permissions.IsAuthenticated]

# ! Class-Related Views

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
    
class ListOwnIncompleteJotters(generics.ListAPIView):
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
    
class ListContextJotters(generics.ListAPIView):
    serializer_class = JotterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        context = self.context['request'].parser_context['kwargs']['context_id']
        pupil_class = self.context['request'].parser_context['kwargs']['class_id']
        return Jotter.objects.filter(context=context, complete=True)