from django.shortcuts import render, redirect
from django.db.models import Count
from aminapp.models import signup, Vote, Candidate
import datetime


def calculate_age(dob):
    if not dob:
        return "-"

    today = datetime.date.today()

    return today.year - dob.year - (
        (today.month, today.day) < (dob.month, dob.day)
    )


# ==========================
# ADMIN HOME DASHBOARD
# ==========================
def aminhome(request):

    if not request.session.get("admin_logged_in"):
        return redirect("adminlogin")

    total_registered = signup.objects.count()
    total_voted = signup.objects.filter(voted=True).count()
    total_not_voted = total_registered - total_voted

    return render(request, "aminhome.html", {
        "total_registered": total_registered,
        "total_voted": total_voted,
        "total_not_voted": total_not_voted,
    })


# ==========================
# PARTY VOTES PAGE
# ==========================
def partyvotes(request):

    if not request.session.get("admin_logged_in"):
        return redirect("adminlogin")

    party_votes = Candidate.objects.annotate(
        total_votes=Count('vote')
    ).order_by('-total_votes')

    total_voted = Vote.objects.count()

    return render(request, "partyvotes.html", {
        "party_votes": party_votes,
        "total_voted": total_voted,
    })


# ==========================
# VOTERS PAGE
# ==========================
def voters(request):

    if not request.session.get("admin_logged_in"):
        return redirect("adminlogin")

    voters = signup.objects.all().order_by('username')

    for voter in voters:
        voter.age = calculate_age(voter.dob)

    return render(request, "voters.html", {
        "voters": voters,
        "total_registered": voters.count(),
    })