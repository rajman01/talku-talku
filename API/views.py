from django.shortcuts import render

# Create your views here.
from rest_framework import status, generics, filters
from rest_framework.reverse import reverse
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import (RegisterSerializer, UserSerializer, ProfileSerializer, LanguageSerializer,
                          StageSerializer, StudyMaterialSerializer, QuestionSerializer, AnswerSerializer,
                          ResultSerializer, CreateResultSerializer)
from rest_framework.authentication import TokenAuthentication
from user.models import Profile
from language.models import Language, Stage, StudyMaterial, Question, AnswerOptions, Result
from rest_framework.pagination import PageNumberPagination


@api_view(['GET'])
@permission_classes(())
def api_root(request, format=None):
    return Response({
        'users': reverse('api-users', request=request, format=format),
        'login': reverse('api-login', request=request, format=format),
        'register': reverse('api-register', request=request, format=format),
        'languages': reverse('api-languages', request=request, format=format),
        'create result': reverse('create-result', request=request, format=format),
    })


@api_view(['POST', ])
@permission_classes(())
def registration_view(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'successfully register a new user'
            data['email'] = account.email
            data['username'] = account.username
            token = Token.objects.create(user=account)
            data['token'] = token.key
        else:
            data = serializer.errors
        return Response(data, status=status.HTTP_201_CREATED)


class ObtainAuthTokenView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        context = {}
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        try:
            username = request.data['username']
            password = request.data['password']
        except KeyError:
            return Response({'error': 'Provide all credentials'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user:
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            context['response'] = 'Successfully authenticated.'
            context['pk'] = user.pk
            context['username'] = username
            context['token'] = token.key
        else:
            context['response'] = 'Error'
            context['error_message'] = 'Invalid credentials'
        return Response(context, status=status.HTTP_200_OK)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = PageNumberPagination


class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def put(self, request, *args, **kwargs):
        object = self.get_object()
        user = request.user
        if object != user:
            return Response({'response': 'you dont have permission to edit that'}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(object, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['success'] = 'update successful'
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def put(self, request, *args, **kwargs):
        object = self.get_object()
        user = request.user
        if object.user != user:
            return Response({'response': 'you dont have permission to edit that'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ProfileSerializer(object, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['success'] = 'update successful'
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LanguageList(generics.ListAPIView):
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = PageNumberPagination


class LanguageDetail(generics.RetrieveAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class StageView(generics.RetrieveAPIView):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class StudyMaterialView(generics.RetrieveAPIView):
    queryset = StudyMaterial.objects.all()
    serializer_class = StudyMaterialSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class QuestionView(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class AnswerView(generics.RetrieveAPIView):
    queryset = AnswerOptions.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class ResultView(generics.RetrieveUpdateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def put(self, request, *args, **kwargs):
        object = self.get_object()
        user = request.user
        if object.user != user:
            return Response({'response': 'you dont have permission to edit that'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ResultSerializer(object, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['success'] = 'update successful'
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def create_result_view(request):
    if request.method == 'POST':
        user1 = request.user
        username = request.data['username']
        try:
            user2 = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'response': 'user does not exist'}, status=status.HTTP_404_NOT_FOUND)
        if user1 != user2:
            return Response({'response': 'you dont have permission to do that'}, status=status.HTTP_403_FORBIDDEN)
        serializer = CreateResultSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            result = serializer.save()
            data['response'] = 'successfully created'
            data['username'] = result.user.username
            data['study_material_id'] = result.study_material.id
            data['score'] = result.score
        else:
            data = serializer.errors
        return Response(data)