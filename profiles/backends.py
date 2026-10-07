from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class EmailOrUsernameModelBackend(ModelBackend):
    """
    Custom authentication backend allowing users to log in 
    using either their username or email address.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        
        if username is None:
            username = kwargs.get('username')
            
        if not username or not password:
            return None

        try:
            # Query for exact match on username OR email (case-insensitive)
            user = User.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            user = User.objects.filter(
                Q(username__iexact=username) | Q(email__iexact=username)
            ).first()

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None