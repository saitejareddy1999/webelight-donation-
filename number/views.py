from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from Donation import settings
from accounts.models import Profile
from number.forms import NumberForm
from number.models import Order, Number
import razorpay

# Create your views here.
#
client = razorpay.Client(auth=(settings.razorpay_key, settings.razorpay_secret))


@login_required
def payment(request):
    form = NumberForm()
    if request.method == 'POST':
        form = NumberForm(request.POST)
        if form.is_valid():
            receiver_phone_number = form.cleaned_data['receiver_phone_number']
            amount = form.cleaned_data['amount']
            print(receiver_phone_number, amount)
            number = Number(receiver_phone_number=receiver_phone_number, amount=amount)
            number.save()
            amount_float = float(amount)
            client = razorpay.Client(auth=(settings.razorpay_key, settings.razorpay_secret))
            data = {
                'amount': amount_float * 100,  # Razorpay amount is in paisa
                'currency': 'INR',
                'receipt': 'order_receipt_' + str(receiver_phone_number),
                'payment_capture': 1  # Auto-capture payment
            }
            razorpay_order = client.order.create(data=data)
            order_id = razorpay_order['id']
            order = Order(user=request.user, razorpay_order_id=order_id)
            order.save()

            return render(request, 'Number/thanku.html', {'order_id': order_id})

    return render(request, 'Number/thanku.html', {'form': form})


@csrf_exempt
def handlerequest(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            order_db = Order.objects.get(razorpay_order_id=order_id)
            order_db.razorpay_payment_id = payment_id
            order_db.razorpay_signature = signature
            order_db.save()
            result = client.utility.verify_payment_signature(params_dict)
            if result is None:
                amount = order_db.amount * 100  # Convert amount to paisa
                try:
                    client.payment.capture(payment_id, amount)
                    order_db.payment_status = 1
                    order_db.save()
                    return render(request, 'Number/paymentsuccess.html', {'id': order_db.id})
                except razorpay.errors.BadRequestError as e:
                    # Handle error appropriately
                    order_db.payment_status = 2
                    order_db.save()
                    return render(request, 'Number/paymentfail.html')
            else:
                order_db.payment_status = 2
                order_db.save()
                return render(request, 'Number/paymentfail.html')
        except Order.DoesNotExist:
            return HttpResponse("505 Not Found")
        except Exception as e:
            # Handle other exceptions
            return HttpResponse("505 Internal Server Error")


def History(request):
    number = Number.objects.all().order_by('-created_at')[:3]
    profile = Profile.objects.all().order_by('-id')[:3]
    return render(request, 'Number/History.html', {'number': number, 'profiles': profile})
