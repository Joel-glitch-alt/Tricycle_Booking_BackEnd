from django.shortcuts import render
import requests
import hmac
import hashlib
import json
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import status
from bookings.models import Booking


# Create your views here.

class InitializePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):  # ✅ Indented inside the class
        booking_id = request.data.get('booking_id')
        amount = request.data.get('amount')

        print(f"=== PAYMENT DEBUG ===")
        print(f"booking_id: {booking_id}")
        print(f"amount: {amount}")
        print(f"user: {request.user} ({request.user.id})")
        print(f"request data: {request.data}")
        print(f"====================")

        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
            print(f"Booking found: {booking}")
        except Booking.DoesNotExist:
            print("BOOKING NOT FOUND")
            return Response({'error': 'Booking not found'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

        try:
            amount_in_pesewas = int(float(amount) * 100)

            headers = {
                'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
                'Content-Type': 'application/json',
            }

            payload = {
                'email': request.user.email,
                'amount': amount_in_pesewas,
                'reference': f'booking_{booking.id}_{request.user.id}_{int(__import__("time").time())}',
                'callback_url': 'https://tricycle-booking-backend.onrender.com/api/payments/webhook/',
                'metadata': {
                    'booking_id': booking.id,
                    'user_id': request.user.id,
                }
            }

            response = requests.post(
                'https://api.paystack.co/transaction/initialize',
                headers=headers,
                json=payload
            )

            data = response.json()

            if data['status']:
                return Response({
                    'authorization_url': data['data']['authorization_url'],
                    'reference': data['data']['reference'],
                    'access_code': data['data']['access_code'],
                })
            else:
                return Response({'error': data.get('message', 'Payment initialization failed')}, status=400)

        except Exception as e:
            return Response({'error': str(e)}, status=400)

    # def post(self, request):
    #     booking_id = request.data.get('booking_id')           
    #     amount = request.data.get('amount')

    #     # ADD THESE DEBUG LINES
    #     print(f"=== PAYMENT DEBUG ===")
    #     print(f"booking_id: {booking_id}")
    #     print(f"amount: {amount}")
    #     print(f"user: {request.user}")
    #     print(f"user_id: {request.user.id}")
    #     print(f"request data: {request.data}")
    #     print(f"====================")

    #     try:
    #         booking = Booking.objects.get(id=booking_id, user=request.user)
    #     except Booking.DoesNotExist:
    #         print("BOOKING NOT FOUND!")  # ADD THIS
    #         return Response({'error': 'Booking not found'}, status=404)
        
         

        # try:
        #     booking = Booking.objects.get(id=booking_id, user=request.user)
        # except Booking.DoesNotExist:
        #     return Response({'error': 'Booking not found'}, status=404)

        # Paystack expects amount in pesewas (1 GHS = 100 pesewas)
        # amount_in_pesewas = int(float(amount) * 100)

        # headers = {
        #     'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        #     'Content-Type': 'application/json',
        # }

        # payload = {
        #     'email': request.user.email,
        #     'amount': amount_in_pesewas,
        #     'reference': f'booking_{booking.id}_{request.user.id}',
        #     'callback_url':  'https://tricycle-booking-backend.onrender.com/api/payments/webhook/',     
        #     # 'https://yourdomain.com/api/payments/callback/',
        #     'metadata': {
        #         'booking_id': booking.id,
        #         'user_id': request.user.id,
        #     }
        # }

        # response = requests.post(
        #     'https://api.paystack.co/transaction/initialize',
        #     headers=headers,
        #     json=payload
        # )

        # data = response.json()

        # if data['status']:
        #     return Response({
        #         'authorization_url': data['data']['authorization_url'],
        #         'reference': data['data']['reference'],
        #         'access_code': data['data']['access_code'],
        #     })
        # else:
        #     return Response({'error': 'Payment initialization failed'}, status=400)


class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, reference):
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        }

        response = requests.get(
            f'https://api.paystack.co/transaction/verify/{reference}',
            headers=headers
        )

        data = response.json()

        if data['status'] and data['data']['status'] == 'success':
            # Update booking status
            metadata = data['data']['metadata']
            booking_id = metadata.get('booking_id')

            Booking.objects.filter(id=booking_id).update(status='completed')

            return Response({'message': 'Payment verified', 'status': 'success'})
        else:
            return Response({'message': 'Payment not successful'}, status=400)


@api_view(['POST'])
def paystack_webhook(request):
    # Verify the webhook is from Paystack
    paystack_signature = request.headers.get('x-paystack-signature')
    secret = settings.PAYSTACK_SECRET_KEY.encode('utf-8')
    body = request.body

    computed = hmac.new(secret, body, hashlib.sha512).hexdigest()

    if computed != paystack_signature:
        return Response({'error': 'Invalid signature'}, status=400)

    payload = json.loads(body)
    event = payload.get('event')

    if event == 'charge.success':
        metadata = payload['data']['metadata']
        booking_id = metadata.get('booking_id')
        Booking.objects.filter(id=booking_id).update(status='completed')

    return Response({'status': 'ok'})
