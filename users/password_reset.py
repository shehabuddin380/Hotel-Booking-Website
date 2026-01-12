from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["POST"])
def password_reset(request):
    return Response({"message":"Reset link sent (demo)"})
