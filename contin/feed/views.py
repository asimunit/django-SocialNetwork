from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .forms import NewPostForm
from .models import Post


# Create your views here.
@login_required(login_url='/account/login/')
def create_post(request):
    user = request.user
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user_name = user
            data.save()
            return redirect('home')
    else:
        form = NewPostForm()
    return render(request, 'feed/create_post.html', {'form': form})


class Home(ListView):
    model = Post
    template_name = 'feed/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
