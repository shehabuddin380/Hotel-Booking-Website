from django.http import JsonResponse

def api_root_view(request):
    return JsonResponse({
        "message": "Welcome to Hotel Booking API",
        "endpoints": {
            "users": "/api/users/",
            "hotels": "/api/hotels/",
            "payments": "/api/payments/",
            "token": "/api/token/",
            "swagger": "/swagger/"
        }
    })
