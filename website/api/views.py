from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .ai import sum_text, gen_quest, text_subject, text_quality

from .serializers import (
    AuthUserSerializer,
    AuthUserTokenObtainPairSerializer,
    UserSerializer,
)


class CurrentUserView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True)

    def get_object(self):
        return get_object_or_404(self.queryset, username=self.kwargs['username'])


@api_view(['GET'])
def user_search(request):
    NUM_USERS_MAX = 5
    LEN_QUERY_MIN = 3
    query = request.query_params.get('search_query')
    if not query:
        return Response({'data': []})

    qs = User.objects.filter(is_active=True)
    if len(query) < LEN_QUERY_MIN:
        users = qs.filter(username=query)[:1]
    else:
        users = qs \
            .filter(username__startswith=query) \
            .order_by('username')[:NUM_USERS_MAX + 1]  # ordering guarantees that first object is closest match (maybe)
        if len(users) > NUM_USERS_MAX:
            if users[0].username == query:
                # the closest match is an exact match, that's the only one we'll need
                users = [users[0]]
            else:
                users = []
    serializer = UserSerializer(users, many=True)
    return Response({'data': serializer.data})


@api_view(['POST'])
def register(request):
    serializer = AuthUserSerializer(data=request.data)

    if serializer.is_valid():
        # XXX: maybe use User.create_user instead
        serializer.validated_data['password'] = make_password(
            serializer.validated_data['password']
        )
        serializer.save()
        return Response(
            {'data': serializer.data, 'detail': 'User registered successfully'},
            status=status.HTTP_201_CREATED,
        )

    return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def summarize(request):
    if len(request.data['text']) < 50:
        return Response(
            {'message': 'Text too short for proper summarization'},
            status=status.HTTP_406_NOT_ACCEPTABLE
        )
    return Response(sum_text(request.data['text']))


class UserTokenPairView(TokenObtainPairView):
    serializer_class = AuthUserTokenObtainPairSerializer


@api_view(['POST'])
def genquest(request):
    return Response(gen_quest(request.data['text'], request.data['type']))


@api_view(['POST'])
def subject(request):
    return Response(text_subject(request.data['text']))


@api_view(['POST'])
def quality(request):
    return Response(text_quality(request.data['text']))
