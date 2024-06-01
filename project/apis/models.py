from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class SocialProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Requests(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_sent_requests")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_received_requests")
    message = models.CharField(max_length=300)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.sender} {self.receiver}"


class AcceptdFriendRequests(Requests):
    def __str__(self):
        return f"{self.receiver} accepted a friend request from {self.sender}"


class PendingFriendRequests(Requests):
    def __str__(self):
        return f"{self.sender} sent a request to {self.receiver}"


class RejectedFriendRequests(Requests):
    def __str__(self):
        return f"{self.receiver} rejected a friend request from {self.sender}"
