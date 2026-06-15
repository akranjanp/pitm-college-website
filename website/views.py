import json
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Course, Notice, GalleryImage, FacultyMember, ContactMessage, CarouselSlide

def home(request):
    notices = Notice.objects.filter(is_active=True)[:5]
    featured_courses = Course.objects.all()[:3]
    slides = CarouselSlide.objects.filter(is_active=True)
    return render(request, 'website/home.html', {
        'notices': notices,
        'courses': featured_courses,
        'slides': slides,
        'active_page': 'home'
    })

def about(request):
    faculty = FacultyMember.objects.all()
    return render(request, 'website/about.html', {
        'faculty': faculty,
        'active_page': 'about'
    })

def courses(request):
    all_courses = Course.objects.all()
    return render(request, 'website/courses.html', {
        'courses': all_courses,
        'active_page': 'courses'
    })

def gallery(request):
    images = GalleryImage.objects.all()
    categories = GalleryImage.CATEGORY_CHOICES
    return render(request, 'website/gallery.html', {
        'images': images,
        'categories': categories,
        'active_page': 'gallery'
    })

def contact(request):
    if request.method == 'POST':
        # Check if request is AJAX
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json'
        
        if is_ajax:
            try:
                data = json.loads(request.body)
                name = data.get('name', '').strip()
                email = data.get('email', '').strip()
                phone = data.get('phone', '').strip()
                subject = data.get('subject', '').strip()
                message = data.get('message', '').strip()
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid data submitted.'}, status=400)
        else:
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()
            subject = request.POST.get('subject', '').strip()
            message = request.POST.get('message', '').strip()

        # Basic Validation
        if not (name and email and phone and subject and message):
            err_msg = 'All fields are required.'
            if is_ajax:
                return JsonResponse({'status': 'error', 'message': err_msg}, status=400)
            messages.error(request, err_msg)
            return redirect('contact')

        # Save to Database
        contact_msg = ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )

        # Trigger Email Notification
        email_subject = f"NEW COLLEGE ENQUIRY: {subject}"
        email_body = f"""
Dear Admin,

You have received a new contact/admission enquiry form submission.

Sender Details:
Name: {name}
Email: {email}
Phone: {phone}
Subject: {subject}

Message:
--------------------------------------------------
{message}
--------------------------------------------------

You can view and export this submission at the Admin Dashboard:
{request.build_absolute_uri('/admin/website/contactmessage/')}

Regards,
PITM Notification Bot
"""
        try:
            send_mail(
                subject=email_subject,
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL_RECIPIENT],
                fail_silently=False,
            )
        except Exception as e:
            # We log the error but still proceed since database save was successful
            print(f"Failed to send email notification: {str(e)}")

        success_msg = 'Thank you! Your message has been sent successfully. We will contact you soon.'
        if is_ajax:
            return JsonResponse({'status': 'success', 'message': success_msg})
        
        messages.success(request, success_msg)
        return redirect('contact')

    return render(request, 'website/contact.html', {
        'active_page': 'contact'
    })
