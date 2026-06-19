from django.db import models


class createregister(models.Model):
    fullname = models.CharField(max_length=100, blank=False)
    adharnumber = models.CharField(max_length=14, blank=False)
    phonenumber = models.CharField(max_length=10, blank=False)
    birthdate = models.DateField(blank=False)
    address = models.CharField(max_length=100, blank=False)

    class Meta:
        db_table = "createregister_table"


class signup(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, blank=True, default="")
    aadhar = models.CharField(max_length=12, blank=True, default="")       # Optional
    voter_id = models.CharField(max_length=10, unique=True, blank=True, default="")  # NEW
    dob = models.DateField(null=True, blank=True)
    voted = models.BooleanField(default=False)
    voted_party = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        db_table = "signup_table"


class ActiveSession(models.Model):
    username = models.CharField(max_length=100)

    class Meta:
        db_table = "active_session_table"


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=15)
    email = models.CharField(max_length=100)
    issue = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "feedback_table"


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    party = models.CharField(max_length=100)

    class Meta:
        db_table = "candidate_table"


class Vote(models.Model):
    voter = models.OneToOneField(signup, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "vote_table"