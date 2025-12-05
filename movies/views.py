from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Movie, Genre, Comment
from .forms import MovieForm, CommentForm


def movie_list(request):
    q = request.GET.get('q')
    genre_id = request.GET.get('genre')
    sort = request.GET.get('sort')

    movies = Movie.objects.all()

    # 🔍 Поиск
    if q:
        movies = movies.filter(title__icontains=q)

    # 🎞 Фильтр жанр
    if genre_id:
        movies = movies.filter(genre_id=genre_id)

    # ⭐ Сортировка
    if sort == 'rating':
        movies = movies.order_by('-rating')
    else:
        movies = movies.order_by('-id')

    # 📄 Пагинация
    paginator = Paginator(movies, 6)  # 6 фильмов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    genres = Genre.objects.all()

    return render(request, 'movies/movie_list.html', {
        'page_obj': page_obj,
        'genres': genres,
        'q': q,
        'selected_genre': genre_id,
        'sort': sort
    })


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    comments = Comment.objects.filter(movie=movie)

    # Комментарий
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.movie = movie
            new.save()
            return redirect('movie_detail', pk=movie.id)
    else:
        form = CommentForm()

    return render(request, 'movies/movie_detail.html', {
        'movie': movie,
        'comments': comments,
        'form': form
    })


def movie_create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = MovieForm()

    return render(request, 'movies/movie_form.html', {'form': form})
