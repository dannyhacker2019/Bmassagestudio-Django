from django.shortcuts import render
from django.http import JsonResponse
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


# Create your views here.
def home(request):
    return render(request, 'index.html')

def services(request):
    return render(request, 'service.html')

def contact(request):
    return render(request, 'contact.html')

def appointment(request):
    return render(request, 'appointment.html')

def pricing(request):
    return render(request, 'price.html')

def about(request):
    return render(request, 'about.html')


def booking(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        service = request.POST.get("service")
        date = request.POST.get("date")
        message = request.POST.get("message", "")

        if not name or not phone:
            return JsonResponse({"error": "Missing required fields"}, status=400)

        try:
            msg = Mail(
                from_email=os.getenv("SENDGRID_SENDER"),
                to_emails=os.getenv("SENDGRID_RECEIVER"),
                subject="New Massage Booking Request 💆‍♀️",
                html_content=f"""
                <p>Name: {name}</p>
                <p>Phone: {phone}</p>
                <p>Service: {service}</p>
                <p>Date: {date}</p>
                <p>Notes: {message}</p>
                """
            )
            sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
            sg.send(msg)
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return render(request, "booking.html")

