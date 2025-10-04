from django.db import models
from django.contrib.auth.models import User
class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    def __str__(self):
        return str(self.id) + ' - ' + self.name
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie,
        on_delete=models.CASCADE)
    user = models.ForeignKey(User,
        on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name

class MovieRequest(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.id} - {self.name} (Requested by {self.user.username})"

class MoviePetition(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_petitions')
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.id} - {self.title} (by {self.created_by.username})"
    
    def get_vote_count(self):
        upvotes = self.votes.filter(vote_type='upvote').count()
        downvotes = self.votes.filter(vote_type='downvote').count()
        return upvotes - downvotes

class PetitionVote(models.Model):
    id = models.AutoField(primary_key=True)
    petition = models.ForeignKey(MoviePetition, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=10, choices=[
        ('upvote', 'Upvote'),
        ('downvote', 'Downvote')
    ])
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('petition', 'user')  # One vote per user per petition
    
    def __str__(self):
        return f"{self.user.username} {self.vote_type}d {self.petition.title}"