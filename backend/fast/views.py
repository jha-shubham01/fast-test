from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login
from rest_framework import viewsets, generics, mixins, status, permissions, authentication , filters
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post
from .serializers import LoginSerializer, PostSerializer, PostListSerializer
from .tasks import send_email_task
import logging

logger = logging.getLogger('history')

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.user
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)
            logger.info(f'{user} has logged in successfully')
            return Response({
                'token': token.key,
                'user_name': user.username,
                'email': user.email,
                'staff': user.is_staff
            })
        else:
            logger.info('Someone tried to login but failed at it')
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

class CreateListPost(viewsets.ViewSet):
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        print(self.request.user)
        return Post.objects.filter(post_posted_by=self.request.user.id)

    def create(self, request):
        request.data["post_posted_by"] = self.request.user.id
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f'{request.user.username} has created a new post')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = PostSerializer(queryset, many=True)
        logger.info(f'{request.user.username} has requested for list of post')
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostSerializer(post)
        logger.info(f'{request.user.username} has requested for detailed post')
        return Response(serializer.data)


class ListPostGAPIView(generics.ListAPIView):
    search_fields = ['post_title']
    filter_backends = (filters.SearchFilter,)
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.info(f'{request.user} has requested for list of post')
        return self.list(request)

@api_view(('GET','POST'))
@permission_classes([IsAuthenticated])
def send_email(request, by, to):
    send_email_task.delay(by, to)
    # send_email_task(by, to)
    logger.info(f'{request.user} contacted {to}')
    return Response({'message': 'Mail will be sent soon'}, status=status.HTTP_200_OK)