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

    # Aggregate from signup.voted_party instead of Vote/Candidate tables —
    # castvote() only creates a Vote row if a matching Candidate exists in
    # the DB, which isn't guaranteed, so that table can stay empty even
    # after real votes are cast. signup.voted_party is always set on vote.
    party_votes = (
        signup.objects.filter(voted=True)
        .exclude(voted_party="")
        .values("voted_party")
        .annotate(total_votes=Count("voted_party"))
        .order_by("-total_votes")
    )

    party_votes = [
        {"party": row["voted_party"], "total_votes": row["total_votes"]}
        for row in party_votes
    ]

    total_voted = signup.objects.filter(voted=True).count()

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