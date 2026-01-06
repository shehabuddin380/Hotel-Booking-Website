from rest_framework.decorators import api_view
from rest_framework.response import Response
import uuid

@api_view(["POST"])
def payment(request):
    room_id = request.data.get("room_id")
    name = request.data.get("name")
    phone = request.data.get("phone")
    address = request.data.get("address")

    tran_id = str(uuid.uuid4())
    
    return Response({
        "payment_url": "http://localhost:5173/success"
        })
