from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_view, logout
from django.contrib.auth.decorators import login_required
from konrix.postman import send_email
import uuid
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from account.models import *
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now
from django.conf import settings
from django.core.files.storage import default_storage
from datetime import datetime, time

@login_required(login_url="login")
def home(request):
    return render(request, 'account/home.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    message = None

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login_view(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    context = {"message": message}
    return render(request, 'account/register/login.html', context)

def sign_up(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Username already taken.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
        else:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = full_name
            user.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
    return render(request, 'account/register/sign_up.html')

def forgot_password(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            if not User.objects.filter(email=email).first():
                messages.error(request, f'No Email Found With This {email}.')
                return redirect('forgot_password')

            user_obj = User.objects.get(email=email)
            profile_obj = Profile.objects.get(user=user_obj)
            token = str(uuid.uuid4())
            profile_obj.forget_password_token = token
            profile_obj.save()

            url = f"{request.get_host()}/account/change-password/{token}/"
            print(url)

            messages.success(request, 'Reset Your Password Please Check Your Email Inbox')
            return redirect('forgot_password')
    except Exception as e:
        print(e)
    return render(request, 'account/register/forgot_password.html')

def change_password(request, token):
    context = {}
    try:
        profile_obj = Profile.objects.filter(forget_password_token=token).first()
        context = {'user_id': profile_obj.user.id}
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confrom_password')
            user_id = request.POST.get('user_id')

            if user_id is None:
                messages.success(request, 'No user id found')
                return redirect(f'/change-password/{token}/')

            if password != confirm_password:
                messages.success(request, 'Both passwords should be equal')
                return redirect(f'/change-password/{token}/')

            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(password)
            user_obj.save()
            return redirect('login')
    except Exception as e:
        print(e)
    return render(request, 'account/register/change_password.html', context)

def reset_password(request, token):
    try:
        profile_obj = Profile.objects.filter(forget_password_token=token).first()
        if not profile_obj:
            messages.error(request, "Invalid or expired reset link.")
            return redirect('forgot_password')

        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect(f'/reset-password/{token}/')

            user = profile_obj.user
            user.set_password(password)
            user.save()

            profile_obj.forget_password_token = None
            profile_obj.save()

            messages.success(request, "Password reset successfully. You can now log in.")
            return redirect('login')
    except Exception as e:
        print(e)
    return render(request, 'customer/register/reset_password.html', {'token': token})

def logout_view(request):
    logout(request)
    return redirect('home')

def school_list(request):
    student_submission = StudentSubmissions.objects.all()
    context = {'student_submission': student_submission}
    return render(request, 'account/school_list.html', context)

def student_submission(request):
    school_list = Schools.objects.all()
    school = request.GET.get('school')
    issue_list = Issues.objects.all()
    selected_school = None

    if school:
        campus_list = Campuses.objects.filter(school__id=school)
        selected_school = Schools.objects.filter(id=school).first()
    else:
        campus_list = Campuses.objects.none()

    if request.method == 'POST':
        student_ids = request.POST.get('student_ids', '').strip()
        student_id_4 = request.POST.get('student_id_4', '').strip()
        school_id = request.POST.get('school', '').strip()
        campus_id = request.POST.get('campus', '').strip()
        issue_id = request.POST.get('issue', '').strip()
        raw_date = request.POST.get('date', '').strip()
        raw_in_time = request.POST.get('in_time', '').strip()
        raw_out_time = request.POST.get('out_time', '').strip()
        message = request.POST.get('message', '').strip()

        try:
            parsed_date = datetime.strptime(raw_date, "%Y-%m-%d").date() if raw_date else None
        except ValueError:
            messages.error(request, "Invalid date format. Use YYYY-MM-DD.")
            return redirect(request.path)

        try:
            parsed_in_time = datetime.strptime(raw_in_time, "%H:%M").time() if raw_in_time else None
        except ValueError:
            messages.error(request, "Invalid in-time format. Use HH:MM.")
            return redirect(request.path)

        try:
            parsed_out_time = datetime.strptime(raw_out_time, "%H:%M").time() if raw_out_time else None
        except ValueError:
            messages.error(request, "Invalid out-time format. Use HH:MM.")
            return redirect(request.path)

        new_submission = StudentSubmissions.objects.create(
            student_ids=student_ids,
            student_id_4=student_id_4,
            school=Schools.objects.filter(id=school_id).first() if school_id.isdigit() else None,
            campus=Campuses.objects.filter(id=campus_id).first() if campus_id.isdigit() else None,
            issue=Issues.objects.filter(id=issue_id).first() if issue_id.isdigit() else None,
            date=parsed_date,
            in_time=parsed_in_time,
            out_time=parsed_out_time,
            message=message
        )
        ticket_number = new_submission.id
        return redirect('submition_message', ticket_number=ticket_number)

    context = {
        "school_list": school_list,
        "campus_list": campus_list,
        "issue_list": issue_list,
        "selected_school": selected_school,
        "today": now(),
    }
    return render(request, 'account/student_submission.html', context)

def submition_message(request, ticket_number):
    return render(request, 'account/submition_message.html', {'ticket_number': ticket_number})

def chat_bot(request):
    return render(request, 'account/chat_bot.html')