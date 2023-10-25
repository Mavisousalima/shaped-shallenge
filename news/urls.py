from django.urls import path
from news.views import NewsAPIView, TemporaryLinkView

urlpatterns = [
    path("news/", NewsAPIView.as_view(), name="news-api"),
    path("news/<int:pk>/", NewsAPIView.as_view(), name="news-api-detail"),
    path("link/<int:news_id>/", TemporaryLinkView.as_view(), name="temporary-link-create"),
    path("link/<str:token>/", TemporaryLinkView.as_view(), name="temporary-link-view"),
]
