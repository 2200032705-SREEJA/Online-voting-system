from django.shortcuts import render
from django.db.models import Count
from aminapp.models import signup, Vote

def aminhome(request):
    total_registered = signup.objects.count()
    total_voted      = signup.objects.filter(voted=True).count()
    total_not_voted  = total_registered - total_voted

    party_votes = (
        Vote.objects
        .values('candidate__party')
        .annotate(total_votes=Count('id'))
        .order_by('-total_votes')
    )

    context = {
        'total_registered': total_registered,
        'total_voted':      total_voted,
        'total_not_voted':  total_not_voted,
        'party_votes':      party_votes,
    }
    return render(request, "aminhome.html", context)