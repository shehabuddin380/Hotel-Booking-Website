from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import redirect
from sslcommerz_lib import SSLCOMMERZ
from hotels.models import Room, Order
from decouple import config

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def payment_view(request):
    room_id = request.data.get("room_id")
    name = request.data.get("name")
    phone = request.data.get("phone")
    address = request.data.get("address")

    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        return Response({"error": "Room not found"}, status=404)

    order = Order.objects.create(
        name=name,
        phone=phone,
        address=address,
        room=room,
        amount=room.price,
    )

    sslcz_settings = {
        'store_id': config('SSLCZ_STORE_ID'),
        'store_pass': config('SSLCZ_STORE_PASS'),
        'issandbox': True
    }

    sslcz = SSLCOMMERZ(sslcz_settings)

    post_body = {
        'total_amount': room.price,
        'currency': "BDT",
        'tran_id': f"order_{order.id}",
        'success_url': "https://hotel-booking-website-zpp5.vercel.app/api/payments/payment/success/",
        'fail_url': "https://hotel-frontend-ot7v.vercel.app/fail",
        'cancel_url': "https://hotel-frontend-ot7v.vercel.app/fail",
        'emi_option': 0,
        'cus_name': name,
        'cus_email': request.user.email,
        'cus_phone': phone,
        'cus_add1': address,
        'cus_city': "Dhaka",
        'cus_country': "Bangladesh",
        'shipping_method': "NO",
        'num_of_item': 1,
        'product_name': room.name,
        'product_category': "Hotel Room",
        'product_profile': "general",
    }

    response = sslcz.createSession(post_body)

    if response.get('status') == 'SUCCESS':
        return Response({"payment_url": response['GatewayPageURL']})
    else:
        return Response({"error": "Payment initiation failed"}, status=400)


@api_view(["POST"])
@permission_classes([])
def payment_success(request):
    tran_id = request.data.get("tran_id", "")
    if tran_id.startswith("order_"):
        order_id = tran_id.split("_")[1]
        try:
            Order.objects.get(id=order_id)
        except:
            pass
    return redirect("https://hotel-frontend-ot7v.vercel.app/success")