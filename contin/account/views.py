from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from feed.models import Post

from .forms import UserRegisterForm, ProfileUpdateForm
from .models import Profile, Relationship

# Create your views here.

User = get_user_model()


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful Please Login')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'account/register.html', {'form': form})


@login_required(login_url='/account/login/')
def my_profile(request):
    profile = Profile.objects.select_related("user").prefetch_related(
        'friends').get(user=request.user)
    user_post = Post.objects.select_related('user_name').filter(
        user_name=request.user).order_by('-date_posted')
    context = {'profile': profile, 'user_post': user_post}
    return render(request, 'account/my_profile.html', context)


@login_required(login_url='/account/login/')
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES,
                                 instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('my_profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'form': form
    }
    return render(request, 'account/edit_profile.html', context)


@login_required(login_url='/account/login/')
def friend_list(request):
    friends = request.user.profile.friends.select_related('profile')
    context = {
        'friends': friends
    }
    return render(request, "account/friend_list.html", context)


@login_required(login_url='/account/login/')
def invites_received(request):
    profile = Profile.objects.select_related("user").get(user=request.user)
    qs = Relationship.objects.filter(receiver=profile,
                                     status='send').select_related(
        'sender__user', 'receiver__user')
    results = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(results) == 0:
        is_empty = True
    context = {
        'qs': results,
        'is_empty': is_empty,
    }
    return render(request, 'account/my_invites.html', context)


@login_required(login_url='/account/login/')
def accept_invitation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)

        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)

        if rel.status == 'send':
            rel.status = "accepted"
            rel.save()
    return redirect('my_invites_view')


@login_required(login_url='/account/login/')
def reject_invitation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('my_invites_view')


@login_required(login_url='/account/login/')
def profile_list(request):
    # import pdb;
    # pdb.set_trace()
    all_profile = Profile.objects.select_related('user').prefetch_related(
        'friends').exclude(user=request.user)
    profile = Profile.objects.select_related("user").get(user=request.user)
    all_relations = Relationship.objects.filter(
        Q(sender=profile) | Q(receiver=profile)).select_related(
        'sender__user', 'receiver__user')
    receivers = []
    senders = []
    for item in all_relations:
        senders.append(item.sender.user)
        receivers.append(item.receiver.user)

    is_empty = False
    if not all_profile:
        is_empty = False

    context = {
        'all_profile': all_profile,
        'rel_receiver': receivers,
        'rel_sender': senders,
        'is_empty': is_empty
    }
    return render(request, 'account/profile_list.html', context)


@login_required(login_url='/account/login/')
def add_friend(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        user = request.user
        # sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=user.profile,
                                          receiver=receiver, status='send')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('my_profile')


@login_required(login_url='/account/login/')
def remove_friend(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        user = request.user
        # sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get(
            (Q(sender=user.profile) & Q(receiver=receiver)) | (
                    Q(sender=receiver) & Q(receiver=user.profile)))
        rel.delete()

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('my_profile')


@login_required(login_url='/account/login/')
def search_users(request):
    query = request.GET.get('q')
    object_list = Profile.objects.select_related('user').prefetch_related(
        'friends').exclude(user=request.user).filter(
        user__username__icontains=query)
    profile = Profile.objects.select_related("user").get(user=request.user)
    all_relations = Relationship.objects.filter(
        Q(sender=profile) | Q(receiver=profile)).select_related(
        'sender__user', 'receiver__user')
    receivers = []
    senders = []
    for item in all_relations:
        senders.append(item.sender.user)
        receivers.append(item.receiver.user)

    is_empty = False
    if not object_list:
        is_empty = False

    context = {
        'all_profile': object_list,
        'rel_receiver': receivers,
        'rel_sender': senders,
        'is_empty': is_empty
    }
    # context = {
    #     'users': object_list
    # }
    return render(request, "account/search_users.html", context)


@login_required(login_url='/account/login/')
def user_profile(request):
    if request.method == "POST":

        pk = request.POST.get('profile_pk')
        print(pk)
        profile = Profile.objects.select_related("user").prefetch_related(
            'friends').get(pk=pk)
        user_post = Post.objects.select_related('user_name').filter(
            user_name=profile.user).order_by('-date_posted')
        context = {'profile': profile, 'user_post': user_post}
        return render(request, 'account/user_profile.html', context)
    return redirect(request.META.get('HTTP_REFERER'))
