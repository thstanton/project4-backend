from rest_framework import authentication, permissions, generics
from rest_framework.decorators import api_view
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

# ! Group-related Views



# ! Context-related Views

# ? List all contexts created by the user
class ListContexts(generics.ListAPIView):
    serializer_class = ContextSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Context.objects.filter(author=user)

# ? GET - Context detail view (PK), DELETE - delete context (PK)   
class ContextDetail(generics.RetrieveDestroyAPIView):
    queryset = Context.objects.all()
    serializer_class = ContextSerializer
    permission_classes = [permissions.IsAuthenticated]

# ? Create a new context
class CreateContext(generics.CreateAPIView):
    queryset = Context.objects.all()
    serializer_class = ContextCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        print(f"User: {self.request.user}")
        serializer.save(author=self.request.user)

# ? Update a context (PK)
class UpdateContext(generics.UpdateAPIView):
    queryset = Context.objects.all()
    serializer_class = UpdateContextSerializer
    permission_classes = [permissions.IsAuthenticated]

# ? Assign/Unassign a context to/from a class
@api_view(['POST'])
def assoc_class_add(request, context_id, pupilclass_id):
    Context.objects.get(id=context_id).classes.add(pupilclass_id)
    return Response({ "message": f"Context {context_id} unassigned to class {pupilclass_id}" })

@api_view(['DELETE'])
def assoc_class_remove(request, context_id, pupilclass_id):
    Context.objects.get(id=context_id).classes.remove(pupilclass_id)
    return Response({ "message": f"Context {context_id} unassigned to class {pupilclass_id}" })

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



# ! Jotter-Related Views



