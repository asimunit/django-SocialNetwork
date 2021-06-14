import numpy as np
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView

from .constant import THRESHOLD_SIMILARITY,comment_classes
from .forms import PostForm
from .models import Post, SimilarPost
from .utils import post_similarity, predict_class, stanford_ner, spacy_ner, ner


class Home(ListView, LoginRequiredMixin):
    model = Post
    template_name = 'feed/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            post = self.model.objects.filter(
                user_name=self.request.user).select_related(
                'user_name').order_by(
                '-date_posted')
            similar_posts = SimilarPost.objects.filter(
                user=self.request.user).select_related('post')
            context['posts'] = post
            context['similar_posts'] = similar_posts
        return context


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {'post': post}
    return render(request, 'feed/post_detail.html', context)


@login_required
def create_post(request):
    user = request.user
    if request.method == "POST":
        # remove request.FILES
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post_created = form.cleaned_data['description']
            predicted_class = predict_class(post_created)
            if predicted_class:
                predicted_class_list = [comment_classes[i] for i in
                                        predicted_class]
                messages.error(request,
                               "Cannot  post because your post contain "
                               "following categories{}".format(
                                   predicted_class_list))
                return redirect('home')

            all_posts = Post.objects.filter(user_name_id=request.user)
            similar_post_index = np.array([])
            similar_post_dict = {}
            if all_posts.exists():
                similar_post_dict = {}
                all_docs = [post.description for post in all_posts]
                similarity = post_similarity(post_created, all_docs)
                similar_post_index = np.argwhere(
                    similarity[0] > THRESHOLD_SIMILARITY
                )
                print(similar_post_index)
            # similar_post_dict = {
            #     all_posts[int(i)]: similarity[0][int(i)]
            #     for i in similar_post_index[0]
            # }
                a = "karan"
                print(type(similar_post_index))
                # if a == "karan":
                #     print("as")

            if similar_post_index.size != 0:
                print("asim")
                for i in similar_post_index[0]:
                     similar_post_dict[all_posts[int(i)]] = similarity[0][
                        int(i)]
                max_similarity = (
                    max(similar_post_dict, key=similar_post_dict.get)
                ).id

            if similar_post_dict:
                context = {
                    'similar_post_dict': similar_post_dict,
                    'post_created': post_created,
                    'max_similarity': max_similarity

                }
                return render(request, 'feed/similar_post.html', context)
            else:
                data = form.save(commit=False)
                data.user_name = user
                data.save()
                return redirect('home')
    else:
        form = PostForm()
    return render(request, 'feed/create_post.html', {'form': form})


def save_post(request):
    if request.method == "POST":
        max_similarity = request.POST.get('max_similarity')
        post_data = request.POST.get('post_data')
        post = Post.objects.get(id=max_similarity)
        SimilarPost.objects.create(user=request.user, post=post,
                                   duplicate=post_data)
        return redirect('home')
    return redirect('home')


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['description']
    template_name = 'feed/create_post.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        post_created = form.cleaned_data['description']
        predicted_class = predict_class(post_created)
        if predicted_class:
            predicted_class_list = [comment_classes[i] for i in
                                    predicted_class]
            messages.error(self.request,
                           "Cannot update the post because your post contain "
                           "following categories{}".format(
                               predicted_class_list))
            return super(PostUpdateView, self).form_invalid(form)
        else:

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


def name_entity_recognition_spacy(request, pk):
    post = Post.objects.get(pk=pk)
    response = spacy_ner(post.description)
    locations = response['location']
    names = response['name']
    organisations = response['organisation']
    Post.objects.filter(id=post.id).update(locations=str(locations),
                                           names=str(names),
                                           organisations=str(organisations))
    post_stanford_ner = post.description
    for name in names:
        post_stanford_ner = (post_stanford_ner.replace(name, '<span '
                                                             'style="color: '
                                                             '#4ef542">{'
                                                             '}</span>'.format(
            name)))
    for loc in locations:
        post_stanford_ner = (post_stanford_ner.replace(loc, '<span '
                                                            'style="color: '
                                                            '#ff0000">{'
                                                            '}</span>'.format(
            loc)))
    for org in organisations:
        post_stanford_ner = (post_stanford_ner.replace(org, '<span '
                                                            'style="color: '
                                                            '#3467eb">{'
                                                            '}</span>'.format(
            org)))

    context = {
        'post_stanford_ner': post_stanford_ner,

    }

    return render(request, 'feed/ner.html', context)


def name_entity_recognition_stanford(request, pk):
    post = Post.objects.get(pk=pk)
    response = stanford_ner(post.description)
    locations = response['location']
    names = response['name']
    organisations = response['organisation']
    Post.objects.filter(id=post.id).update(locations=str(locations),
                                           names=str(names),
                                           organisations=str(organisations))
    post_stanford_ner = post.description
    for name in names:
        post_stanford_ner = (post_stanford_ner.replace(name, '<span '
                                                             'style="color: '
                                                             '#4ef542">{'
                                                             '}</span>'.format(
                                                        name)))
    for loc in locations:
        post_stanford_ner = (post_stanford_ner.replace(loc, '<span '
                                                            'style="color: '
                                                            '#ff0000">{'
                                                            '}</span>'.format(
            loc)))
    for org in organisations:
        post_stanford_ner = (post_stanford_ner.replace(org, '<span '
                                                            'style="color: '
                                                            '#3467eb">{'
                                                            '}</span>'.format(
            org)))

    context = {
        'post_stanford_ner': post_stanford_ner,

    }

    return render(request, 'feed/ner.html', context)


def name_entity_recognition_cmd(request, pk):
    post = Post.objects.get(pk=pk)
    response = ner(post.description)
    locations = response['LOCATION']
    names = response['PERSON']
    organisations = response['ORGANIZATION']

    Post.objects.filter(id=post.id).update(locations=str(locations),
                                           names=str(names),
                                           organisations=str(organisations))
    post_stanford_ner = post.description
    for name in names:
        post_stanford_ner = (post_stanford_ner.replace(name, '<span '
                                                             'style="color: '
                                                             '#4ef542">{'
                                                             '}</span>'.format(
            name)))
    for loc in locations:
        post_stanford_ner = (post_stanford_ner.replace(loc, '<span '
                                                            'style="color: '
                                                            '#ff0000">{'
                                                            '}</span>'.format(
            loc)))
    for org in organisations:
        post_stanford_ner = (post_stanford_ner.replace(org, '<span '
                                                            'style="color: '
                                                            '#3467eb">{'
                                                            '}</span>'.format(
            org)))

    context = {
        'post_stanford_ner': post_stanford_ner,

    }

    return render(request, 'feed/ner.html', context)
