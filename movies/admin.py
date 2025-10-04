from django.contrib import admin
from .models import Movie, Review, MovieRequest, MoviePetition, PetitionVote

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

class MovieRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'date']
    list_filter = ['date', 'user']
    search_fields = ['name', 'user__username']
    ordering = ['-date']

class MoviePetitionAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'created_date', 'get_vote_count']
    list_filter = ['created_date', 'created_by']
    search_fields = ['title', 'created_by__username']
    ordering = ['-created_date']
    
    def get_vote_count(self, obj):
        return obj.get_vote_count()
    get_vote_count.short_description = 'Vote Count'

class PetitionVoteAdmin(admin.ModelAdmin):
    list_display = ['petition', 'user', 'vote_type', 'created_date']
    list_filter = ['vote_type', 'created_date']
    search_fields = ['petition__title', 'user__username']
    ordering = ['-created_date']

admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
admin.site.register(MovieRequest, MovieRequestAdmin)
admin.site.register(MoviePetition, MoviePetitionAdmin)
admin.site.register(PetitionVote, PetitionVoteAdmin)