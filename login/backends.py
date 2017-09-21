from django.contrib.auth.models import User

class LoginUsingEmailAsUsernameBackend(object):
  """
  Custom Authentication backend that supports using an e-mail address
  to login instead of a username.
  See: http://blog.cingusoft.org/custom-django-authentication-backend
  """
  supports_object_permissions = False
  supports_anonymous_user = False
  supports_inactive_user = False

  def authenticate(self, email=None, password=None):
    print("\n\nUsing custom authenticate function.\n\n")

    try:
      # Check if the user exists in Django's database
      user = User.objects.get(email=email)
    except User.DoesNotExist:
      return None

    # Check password of the user we found
    if user.check_password(password):
      return user
    return None

  # Required for the backend to work properly - unchanged in most scenarios
  def get_user(self, user_id):
    try:
      return User.objects.get(pk=user_id)
    except User.DoesNotExist:
      return None