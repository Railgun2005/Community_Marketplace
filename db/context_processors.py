from .models import UserProfile

def profile_pic(request):
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            return {'profile_pic': profile.pfp.url}
        except UserProfile.DoesNotExist:
            return {'profile_pic': None}
    return {'profile_pic': None}