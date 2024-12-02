import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.conf import settings
from .models import Payment
from tourism.models import Tour, Purchase

class ZarinpalPaymentRequest(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, pk=None):
        # Parameters for the payment request
        merchant_id = settings.ZARINPAL_MERCHANT_ID  # Your merchant ID
        amount = request.data.get('amount')
        description = request.data.get('description')
        callback_url = request.data.get('callback_url')
        mobile = request.data.get('mobile')
        email = request.data.get('email')

        # Prepare the metadata field
        metadata = {}
        if mobile:
            metadata['mobile'] = str(mobile)  # Only add if mobile is provided
        if email:
            metadata['email'] = str(email)  # Only add if email is provided
        
        # Prepare the request payload
        payload = {
            'merchant_id': merchant_id,
            'amount': amount * 10,
            'callback_url': callback_url,
            'description': description,
            'metadata': metadata,
        }

        # Make POST request to Zarinpal API to request payment
        response = requests.post(
            'https://sandbox.zarinpal.com/pg/v4/payment/request.json',
            json=payload,
            headers={
                'accept': 'application/json',
                'content-type': 'application/json',
            }
        )

        # Log the response data for debugging
        data = response.json()

        if data['data']['code'] == 100:
            # Redirect URL for the payment
            authority = data['data']['authority']
            payment_url = f"https://sandbox.zarinpal.com/pg/StartPay/{authority}"

            # Create a Payment instance to track the payment request
            payment, created = Payment.objects.get_or_create(
                user=request.user,
                tour_id=pk,
                defaults={
                    'amount_paid': amount,
                    'ref_id': authority,  # Save the authority from Zarinpal for future reference
                    'payment_status': Payment.PENDING,  # Initial status is pending
                }
            )
            if not created:
                payment.amount_paid = amount
                payment.ref_id = authority
                payment.payment_status = Payment.PENDING
                payment.save()

            return Response({'payment_url': payment_url}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Payment request failed'}, status=status.HTTP_400_BAD_REQUEST)


class ZarinpalPaymentVerify(APIView):

    def post(self, request, pk):
        # Retrieve Authority and Amount from the request body
        authority = request.data.get('Authority')
        amount = request.data.get('Amount')

        if not authority or not amount:
            return Response({'error': 'Authority or Amount missing'}, status=status.HTTP_400_BAD_REQUEST)

        merchant_id = settings.ZARINPAL_MERCHANT_ID

        # Verify the payment with Zarinpal API
        payload = {
            'merchant_id': merchant_id,
            'amount': amount * 10,
            'authority': authority,
        }

        try:
            response = requests.post(
                'https://sandbox.zarinpal.com/pg/v4/payment/verify.json',
                json=payload,
                headers={'accept': 'application/json', 'content-type': 'application/json'}
            )
            data = response.json()

            if data['data']['code'] == 100:  # Payment successful
                # Find the payment instance based on the authority and update it
                payment = Payment.objects.get(ref_id=authority, tour_id=pk)
                payment.payment_status = Payment.SUCCESS
                payment.save()

                # Associate the user with the tour and decrease remaining seats
                tour = Tour.objects.get(id=pk)
                if tour.remaining_capacity > 0:
                    Purchase.objects.create(user=payment.user, tour=tour)
                    tour.remaining_capacity -= 1
                    tour.save()

                return Response({'message': 'Payment verified successfully'}, status=status.HTTP_200_OK)
            else:
                # Payment failed
                payment = Payment.objects.get(ref_id=authority, tour_id=pk)
                payment.payment_status = Payment.FAILED
                payment.save()

                return Response({'error': 'Payment verification failed'}, status=status.HTTP_400_BAD_REQUEST)

        except requests.exceptions.RequestException as e:
            return Response({'error': f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
