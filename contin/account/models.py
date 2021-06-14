from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


# Create your models here.

class ProfileManager(models.Manager):

    def get_all_profiles_to_invite(self, sender):
        profiles = Profile.objects.select_related('user').prefetch_related(
            'friends').exclude(user=sender)
        profile = Profile.objects.select_related("user").get(sender)
        qs = Relationship.objects.filter(
            Q(sender=profile) | Q(receiver=profile)).select_related(
            'sender__user', 'receiver__user')

        accepted = []
        for rel in qs:
            if rel.status == 'accepted':
                accepted.append(rel.receiver)
                accepted.append(rel.sender)
        available = [profile for profile in profiles if
                     profile not in accepted]

        return available

    def get_all_profiles(self, me):
        profile = Profile.objects.select_related('user').exclude(user=me)
        return profile


class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField(auto_now=False, null=True)
    image = models.ImageField(upload_to='profile_pics')
    bio = models.TextField()
    friends = models.ManyToManyField(User, related_name='friends', blank=True)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now=True)

    objects = ProfileManager()

    def __str__(self):
        return str(self.user_id)


STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)


class Relationship(models.Model):
    sender = models.ForeignKey(Profile, related_name='senders',
                               on_delete=models.CASCADE)
    receiver = models.ForeignKey(Profile, related_name='receivers',
                                 on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender_id}-{self.receiver_id}-{self.status}"
