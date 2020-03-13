from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('lyrics/<artist>/<name>', views.lyrics, name="lyrics"),
    path('lyrics/<artist>/<name>/', views.lyrics, name="lyrics"),
    path('lyrics/<artist>',views.artist, name="artist"),
    path('lyrics/<artist>/',views.artist, name="artist"),
]

'''path('lyrics/<artist>/<name>/add', views.name_add_lyrics, name="name_add_lyrics"),
    path('lyrics/<artist>/<name>/add/', views.name_add_lyrics, name="name_add_lyrics"),
    path('lyrics/<artist>/<name>/add/success', views.lyric_added, name="lyric_added"),'''