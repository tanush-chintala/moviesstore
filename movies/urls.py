from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='movies.index'),
    path('<int:id>/', views.show, name='movies.show'),
    path('<int:id>/review/create/', views.create_review, name='movies.create_review'),
    path('<int:id>/review/<int:review_id>/edit/', views.edit_review, name='movies.edit_review'),
    path('<int:id>/review/<int:review_id>/delete/', views.delete_review, name='movies.delete_review'),
    path('requests/', views.movie_requests, name='movies.movie_requests'),
    path('requests/<int:request_id>/delete/', views.delete_movie_request, name='movies.delete_movie_request'),
    path('petitions/', views.petition_list, name='movies.petition_list'),
    path('petitions/<int:petition_id>/vote/', views.vote_petition, name='movies.vote_petition'),
    path('petitions/<int:petition_id>/delete/', views.delete_petition, name='movies.delete_petition'),
]