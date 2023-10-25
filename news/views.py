from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from news.models import News, TemporaryLink
from news.serializers import NewsSerializer, TemporaryLinkSerializer
from django.utils import timezone
from utils.generate_token import generate_token


class NewsAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, pk=None) -> Response:
        if pk:
            news = News.objects.get(pk=pk)
            serializer = NewsSerializer(news, many=False)
        else:
            news = News.objects.all()
            pagination = PageNumberPagination()
            page = pagination.paginate_queryset(news, request)
            serializer = NewsSerializer(page, many=True)
            
        return Response(serializer.data)

    def post(self, request) -> Response:
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            news_article = News.objects.get(pk=pk)
        except News.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = NewsSerializer(news_article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            news_article = News.objects.get(pk=pk)
        except News.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        news_article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class TemporaryLinkView(APIView):
    def post(self, request, news_id):
        try:
            news = News.objects.get(id=news_id)
        except News.DoesNotExist:
            return Response({"message": "News not found"}, status=status.HTTP_404_NOT_FOUND)
        
        token = generate_token()
        expiration_time = timezone.now() + timezone.timedelta(hours=1)
        
        TemporaryLink.objects.create(news=news, token=token, expiration_time=expiration_time)
        
        return Response({"link": f'http://localhost:8000/api/link/{token}', "expiration_time": expiration_time}, status=status.HTTP_201_CREATED)
    
    def get(self, request, token):
        try:
            temporary_link = TemporaryLink.objects.get(token=token, expiration_time__gt=timezone.now())
        except TemporaryLink.DoesNotExist:
            return Response({"message": "Temporary link not found or expired"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = NewsSerializer(temporary_link.news)
        return Response(serializer.data)