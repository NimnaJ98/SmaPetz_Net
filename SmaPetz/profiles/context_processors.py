from .models import Profile, FriendRequest

def profile_pic(request):
    if request.user.is_authenticated:
        profile_obj = Profile.objects.get(user=request.user)
        pic = profile_obj.profilePic
        return {'picture':pic}
    return {}

def invitations_no(request):
    if request.user.is_authenticated:
        profile_obj = Profile.objects.get(user=request.user)
        qs_count = FriendRequest.objects.received_requests(profile_obj).count()
        return {'requests_no':qs_count}
    return {}

