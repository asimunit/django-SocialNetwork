from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


# Create your models here.

class ProfileManager(models.Manager):

    def get_all_profiles_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))

        accepted = []
        for rel in qs:
            if rel.status == 'accepted':
                accepted.append(rel.receiver)
                accepted.append(rel.sender)
        available = [profile for profile in profiles if profile not in accepted]

        return available

    def get_all_profiles(self, me):
        profile = Profile.objects.all().exclude(user=me)
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
        return str(self.user)


STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)


class RelationshipManager(models.Manager):
    def invitation_recieved(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='send')
        return qs


class Relationship(models.Model):
    sender = models.ForeignKey(Profile, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Profile, related_name='receiver', on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now=True)

    objects = RelationshipManager()

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
