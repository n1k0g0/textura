from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
 
# importing views from views..py
from . import views


urlpatterns = [
    path('show_corpora', views.show_corpora, name='show_corpora'),
    path('analysis', views.analysis, name='analysis'),
    path('', views.upload_text, name='upload_text'),
    path('delete/<int:pk>/', views.delete_text, name='delete_text'),
    path('create', views.add_corpora_entity ),
    #re_path(r'^process/', views.process, name='process')   # likepost view at /likepost)
]

urlpatterns += static(settings.MEDIA_URL,
                        document_root=settings.MEDIA_ROOT)