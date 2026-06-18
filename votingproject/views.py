import datetime
import json
import re

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from aminapp.models import signup, createregister as CreateRegister, ActiveSession, Feedback, Candidate, Vote


def calculate_age(birthdate):
    today = datetime.date.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))


def demofunctio(request):
    return render(request, "main.html")


def welcome(request):          # ← ADD THIS ENTIRE FUNCTION
    return render(request, "welcome.html")


def homefunction(request):
    return render(request, "index.html")


def voterregistratiofunction(request):
    return render(request, "voterregistratio.html")


def resultsfunction(request):
    return render(request, "results.html")


def candidateinformationfunction(request):
    return render(request, "candidateinformation.html")


def complaintfunction(request):
    return render(request, "complaint.html")


def login(request):
    return render(request, "login.html")

def adminlogin(request):
    return render(request, "adminlogin.html")


def adminauthenticate(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        # CHANGE THESE VALUES
        if username == "admin" and password == "admin123":

            request.session["admin_logged_in"] = True

            return redirect("aminhome")

    return render(
        request,
        "adminlogin.html",
        {"error": "Invalid Admin Credentials"}
    )

def voting(request):
    username = request.session.get("username")
    if not username:
        return redirect("login")
    user = signup.objects.filter(username=username).first()
    already_voted = user.voted if user else False
    voted_party = user.voted_party if user else ""
    return render(request, "voting.html", {
        "already_voted": already_voted,
        "voted_party": voted_party,
    })


@require_POST
def castvote(request):
    username = request.session.get("username")
    if not username:
        return JsonResponse({"status": "not_logged_in"}, status=401)

    user = signup.objects.filter(username=username).first()
    if not user:
        return JsonResponse({"status": "not_logged_in"}, status=401)

    # SERVER-SIDE guard — blocks vote even if someone bypasses the frontend
    if user.voted:
        return JsonResponse({"status": "already_voted", "party": user.voted_party})

    try:
        data = json.loads(request.body)
        party = data.get("party", "").strip()
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({"status": "invalid_data"}, status=400)

    if not party:
        return JsonResponse({"status": "no_party_selected"}, status=400)

    # Save vote record in Vote table
    candidate = Candidate.objects.filter(party=party).first()
    if candidate:
        Vote.objects.create(voter=user, candidate=candidate)

    # Mark user as voted AND record which party — prevents double voting
    user.voted = True
    user.voted_party = party  # ← THIS WAS THE MISSING LINE
    user.save()

    return JsonResponse({"status": "success", "party": party})


def checkaminlogin(request):
    if request.method != "POST":
        return redirect("login")

    aminuname = request.POST.get("uname")
    aminpwd = request.POST.get("pwd")

    matched_user = signup.objects.filter(
        username=aminuname,
        password=aminpwd
    ).first()

    if not matched_user:
        return render(request, "loginfail.html")

    request.session["username"] = aminuname

    return render(request, "index.html")


def logout_view(request):
    username = request.session.get("username")

    if username:
        ActiveSession.objects.filter(username=username).delete()

    request.session.flush()

    return redirect("welcome")
def forgotpassword(request):
    return render(request, "forgotpassword.html")


def resetpassword(request):
    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        new_password = request.POST.get("new_password")

        user = signup.objects.filter(
            username=username,
            email=email
        ).first()

        if not user:
            return render(
                request,
                "forgotpassword.html",
                {"msg": "Invalid Username or Email"}
            )

        user.password = new_password
        user.save()

        return render(
            request,
            "login.html",
            {"msg": "Password Reset Successful. Please Login."}
        )

    return redirect("forgotpassword")
import re

def createuser(request):
    if request.method == "POST":

        uid = request.POST["uid"].strip()
        password = request.POST['password'].strip()
        email = request.POST['email'].strip()
        phone = request.POST.get('phone', '').strip()
        aadhar = request.POST.get('aadhar', '').strip()
        dob_str = request.POST.get('dob', '').strip()

        if not uid:
            return render(request, 'signup.html', {'msg1': 'User ID is required.'})

        if not password:
            return render(request, 'signup.html', {'msg1': 'Password is required.'})

        if not email:
            return render(request, 'signup.html', {'msg1': 'Email is required.'})

        if not phone:
            return render(request, 'signup.html', {'msg1': 'Phone Number is required.'})

        if not aadhar:
            return render(request, 'signup.html', {'msg1': 'Aadhar Number is required.'})

        if not dob_str:
            return render(request, 'signup.html', {'msg1': 'Date of Birth is required.'})
        if not re.match(r'^[A-Za-z][A-Za-z0-9]*$', uid):
            return render(request, 'signup.html', {
        'msg1': 'Username must start with a letter and contain only letters and numbers.',
        'uid': uid,
        'email': email,
        'phone': phone,
        'aadhar': aadhar,
        'dob': dob_str
    })

        if not any(ch.isupper() for ch in uid):
            return render(request, 'signup.html', {
        'msg1': 'Username must contain at least one Capital Letter.',
        'uid': uid,
        'email': email,
        'phone': phone,
        'aadhar': aadhar,
        'dob': dob_str
    })

        if not any(ch.isupper() for ch in password):
            return render(request, 'signup.html',
                          {'msg1': 'Password must contain at least one Capital Letter.'})

        if sum(ch.isdigit() for ch in password) < 2:
            return render(request, 'signup.html',
                          {'msg1': 'Password must contain at least 2 numbers.'})

        if not any(ch in "@#$%^&*!?" for ch in password):
            return render(request, 'signup.html',
                          {'msg1': 'Password must contain at least one Special Character.'})

        if '@' not in email or '.' not in email:
            return render(request, 'signup.html',
                          {'msg1': 'Enter a valid Email Address.'})

        if not phone.isdigit() or len(phone) != 10:
            return render(request, 'signup.html',
                          {'msg1': 'Phone Number must be exactly 10 digits.'})

        if not aadhar.isdigit() or len(aadhar) != 12:
            return render(request, 'signup.html',
                          {'msg1': 'Aadhar Number must be exactly 12 digits.'})

        try:
            birthdate = datetime.date.fromisoformat(dob_str)
        except ValueError:
            return render(request, 'signup.html',
                          {'msg1': 'Enter a valid Date of Birth.'})

        age = calculate_age(birthdate)

        if age < 18:
            return render(request, 'signup.html',
                          {'msg1': 'You must be 18 years or older to register as a voter.'})
        if signup.objects.filter(username=uid).exists():
            return render(request, 'signup.html', {
        'msg1': 'Username already taken. Please choose another username.',
        'uid': uid,
        'email': email,
        'phone': phone,
        'aadhar': aadhar,
        'dob': dob_str
    })

        s = signup(
            username=uid,
            password=password,
            email=email,
            phone=phone,
            aadhar=aadhar,
            dob=birthdate
        )

        s.save()

        return render(request, 'login.html',
                      {'msg': 'Registration Successful'})

    return render(request, 'signup.html')


def singup(request):
    return render(request, 'signup.html')


def submitfeedback(request):
    if request.method == "POST":
        Feedback.objects.create(
            name=request.POST.get('name'),
            number=request.POST.get('number'),
            email=request.POST.get('email'),
            issue=request.POST.get('issue')
        )

        return render(
            request,
            "complaint.html",
            {"msg": "Thanks! Your feedback has been submitted."}
        )

    return render(request, "complaint.html")


def createregister(request):

    if request.method == 'POST':

        full_name = request.POST.get('full_name', '').strip()
        adhar_number = request.POST.get('adhar_number', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        birth_date = request.POST.get('birth_date', '').strip()
        address = request.POST.get('address', '').strip()

        if not full_name:
            return render(request, 'voterregistration.html',
                          {'msg': 'Full Name is required.'})

        if not adhar_number:
            return render(request, 'voterregistration.html',
                          {'msg': 'Aadhar Number is required.'})

        if not phone_number:
            return render(request, 'voterregistration.html',
                          {'msg': 'Phone Number is required.'})

        if not birth_date:
            return render(request, 'voterregistration.html',
                          {'msg': 'Date of Birth is required.'})

        if not address:
            return render(request, 'voterregistration.html',
                          {'msg': 'Address is required.'})

        if not phone_number.isdigit() or len(phone_number) != 10:
            return render(request, 'voterregistration.html',
                          {'msg': 'Phone Number must be exactly 10 digits.'})

        if not adhar_number.isdigit() or len(adhar_number) != 12:
            return render(request, 'voterregistration.html',
                          {'msg': 'Aadhar Number must be exactly 12 digits.'})

        try:
            dob = datetime.date.fromisoformat(birth_date)
        except ValueError:
            return render(request, 'voterregistration.html',
                          {'msg': 'Enter a valid Date of Birth.'})

        age = calculate_age(dob)

        if age < 18:
            return render(
                request,
                'voterregistration.html',
                {'msg': 'You must be 18 years or older to register as a voter.'}
            )

        new_registration = CreateRegister(
            fullname=full_name,
            adharnumber=adhar_number,
            phonenumber=phone_number,
            birthdate=dob,
            address=address
        )

        new_registration.save()

        return render(
            request,
            'voterregistration.html',
            {'msg': 'Registration Successful'}
        )

    return render(request, 'voterregistration.html')