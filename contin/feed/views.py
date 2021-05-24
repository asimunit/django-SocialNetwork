from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .forms import PostForm
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comments, Like
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json


class Home(ListView):
    model = Post
    template_name = 'feed/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    is_liked = Like.objects.filter(user=user, post=post)
    context = {'post': post}
    return render(request, 'feed/post_detail.html', context)


@login_required
def create_post(request):
    user = request.user
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.user_name = user
            data.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'feed/create_post.html', {'form': form})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['description']
    template_name = 'feed/create_post.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user_name = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user_name:
            return True
        return False


@login_required
def post_delete(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user == post.user_name:
        Post.objects.get(pk=pk).delete()
    return redirect('home')
