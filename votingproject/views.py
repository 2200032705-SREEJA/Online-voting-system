import datetime
import json

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from aminapp.models import signup, createregister, ActiveSession, Feedback, Candidate, Vote


def calculate_age(birthdate):
    today = datetime.date.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))


def demofunctio(request):
    return render(request, "main.html")


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
    return redirect("login")


def createuser(request):
    if request.method == "POST":
        uid = request.POST["uid"]
        password = request.POST['password']
        email = request.POST['email']
        phone = request.POST.get('phone', '').strip()
        aadhar = request.POST.get('aadhar', '').strip()
        dob_str = request.POST.get('dob', '').strip()

        if not (phone and aadhar and dob_str):
            return render(request, 'signup.html', {'msg1': 'Phone number, Aadhar number, and date of birth are all required.'})
        if not (phone.isdigit() and len(phone) == 10):
            return render(request, 'signup.html', {'msg1': 'Enter a valid 10-digit phone number.'})
        if not (aadhar.isdigit() and len(aadhar) == 12):
            return render(request, 'signup.html', {'msg1': 'Enter a valid 12-digit Aadhar number.'})

        try:
            birthdate = datetime.date.fromisoformat(dob_str)
        except ValueError:
            return render(request, 'signup.html', {'msg1': 'Enter a valid date of birth.'})

        age = calculate_age(birthdate)
        if age < 18:
            return render(request, 'signup.html', {'msg1': f'You must be at least 18 years old to register. You are {age}.'})

        s = signup(username=uid, password=password, email=email, phone=phone, aadhar=aadhar, dob=birthdate)
        signup.save(s)
        msg = 'Registration is Succesful'
        return render(request, 'login.html', {'msg': msg})


def singup(request):
    return render(request, 'signup.html')


def submitfeedback(request):
    if request.method == "POST":
        Feedback.objects.create(
            name=request.POST.get('name'),
            number=request.POST.get('number'),
            email=request.POST.get('email'),
            issue=request.POST.get('issue'),
        )
        return render(request, "complaint.html", {"msg": "Thanks! Your feedback has been submitted."})
    return render(request, "complaint.html")


def createregister(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        adhar_number = request.POST.get('adhar_number')
        phone_number = request.POST.get('phone_number')
        birth_date = request.POST.get('birth_date')
        address = request.POST.get('address')

        new_registration = createregister(
            fullname=full_name,
            adharnumber=adhar_number,
            phonenumber=phone_number,
            birthdate=birth_date,
            address=address
        )
        new_registration.save()
        return redirect('success_page')

    return render(request, 'voterregistration.html')