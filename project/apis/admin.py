from django.contrib import admin
from .models import SocialProfile, AcceptdFriendRequests, PendingFriendRequests, RejectedFriendRequests
# Register your models here.


admin.site.register(SocialProfile)
admin.site.register(AcceptdFriendRequests)
admin.site.register(RejectedFriendRequests)
admin.site.register(PendingFriendRequests)
