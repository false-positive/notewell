from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


def generate_jwt_token(user):
    return {
        "access": str(AccessToken.for_user(user)),
        "refresh": str(RefreshToken.for_user(user))
    }
