from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, MovieRequest, MoviePetition, PetitionVote
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = Movie.objects.all()
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html', {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

@login_required
def movie_requests(request):
    template_data = {}
    template_data['title'] = 'Movie Requests'
    
    # Get user's movie requests
    user_requests = MovieRequest.objects.filter(user=request.user).order_by('-date')
    template_data['user_requests'] = user_requests
    
    if request.method == 'POST':
        # Handle new movie request
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        
        if name and description:
            movie_request = MovieRequest()
            movie_request.name = name
            movie_request.description = description
            movie_request.user = request.user
            movie_request.save()
            return redirect('movies.movie_requests')
        else:
            template_data['error'] = 'Please fill in both movie name and description.'
    
    return render(request, 'movies/movie_requests.html', {'template_data': template_data})

@login_required
def delete_movie_request(request, request_id):
    movie_request = get_object_or_404(MovieRequest, id=request_id, user=request.user)
    movie_request.delete()
    return redirect('movies.movie_requests')

@login_required
def petition_list(request):
    template_data = {}
    template_data['title'] = 'Movie Petitions'
    
    # Get all petitions with vote counts
    petitions = MoviePetition.objects.all().order_by('-created_date')
    template_data['petitions'] = petitions
    
    if request.method == 'POST':
        # Handle new petition creation
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        
        if title and description:
            petition = MoviePetition()
            petition.title = title
            petition.description = description
            petition.created_by = request.user
            petition.save()
            return redirect('movies.petition_list')
        else:
            template_data['error'] = 'Please fill in both title and description.'
    
    return render(request, 'movies/petition_list.html', {'template_data': template_data})

@login_required
def vote_petition(request, petition_id):
    petition = get_object_or_404(MoviePetition, id=petition_id)
    vote_type = request.POST.get('vote_type')
    
    if vote_type in ['upvote', 'downvote']:
        # Check if user already voted
        existing_vote = PetitionVote.objects.filter(petition=petition, user=request.user).first()
        
        if existing_vote:
            # Update existing vote
            existing_vote.vote_type = vote_type
            existing_vote.save()
        else:
            # Create new vote
            vote = PetitionVote()
            vote.petition = petition
            vote.user = request.user
            vote.vote_type = vote_type
            vote.save()
    
    return redirect('movies.petition_list')

@login_required
def delete_petition(request, petition_id):
    petition = get_object_or_404(MoviePetition, id=petition_id, created_by=request.user)
    petition.delete()
    return redirect('movies.petition_list')