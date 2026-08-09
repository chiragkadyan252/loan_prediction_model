from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .models import Prediction

import joblib
import os


# =========================================================
# LOAD MACHINE LEARNING MODEL
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

model = joblib.load(
    os.path.join(BASE_DIR, "loan_approval_model.pkl")
)


# =========================================================
# HOME
# =========================================================

def index(request):
    return render(request, "index.html")


# =========================================================
# ABOUT
# =========================================================

def about(request):
    return render(request, "about.html")


# =========================================================
# CONTACT
# =========================================================

def contact(request):
    return render(request, "contact.html")


def signup(request):

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(
                request,
                "Account created successfully! Welcome to Loan Approval Prediction."
            )

            return redirect("home")

    else:

        form = UserCreationForm()

    return render(
        request,
        "signup.html",
        {"form": form}
    )
# =========================================================
# LOGIN
# =========================================================

def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # Login user
            login(request, user)

            # After login → Home page
            return redirect("home")

        else:

            return render(
                request,
                "login.html",
                {
                    "error": "Invalid Username or Password"
                }
            )

    return render(
        request,
        "login.html"
    )


# =========================================================
# LOGOUT
# =========================================================

def user_logout(request):

    logout(request)

    # After logout → Home
    return redirect("home")


# =========================================================
# DASHBOARD
# =========================================================

@login_required(login_url="login")
def dashboard(request):

    user_predictions = Prediction.objects.filter(
        user=request.user
    )

    recent_predictions = (
        user_predictions
        .order_by("-created_at")[:5]
    )

    total_predictions = (
        user_predictions.count()
    )

    approved = (
        user_predictions
        .filter(result="Approved")
        .count()
    )

    rejected = (
        user_predictions
        .filter(result="Rejected")
        .count()
    )

    if total_predictions > 0:

        approval_rate = round(
            (approved / total_predictions) * 100,
            2
        )

    else:

        approval_rate = 0

    context = {

        "total_predictions":
            total_predictions,

        "approved":
            approved,

        "rejected":
            rejected,

        "approval_rate":
            approval_rate,

        "recent_predictions":
            recent_predictions,
    }

    return render(
        request,
        "dashboard.html",
        context
    )


# =========================================================
# LOAN PREDICTION
# =========================================================

@login_required(login_url="login")
def prediction(request):

    result = None

    if request.method == "POST":

        # -------------------------------------------------
        # Education
        # -------------------------------------------------

        education = (
            1
            if request.POST.get("education") == "Graduate"
            else 0
        )

        # -------------------------------------------------
        # Self Employed
        # -------------------------------------------------

        self_employed = (
            1
            if request.POST.get("self_employed") == "Yes"
            else 0
        )

        # -------------------------------------------------
        # Input Values
        # -------------------------------------------------

        no_of_dependents = int(
            request.POST["no_of_dependents"]
        )

        income_annum = float(
            request.POST["income_annum"]
        )

        loan_amount = float(
            request.POST["loan_amount"]
        )

        loan_term = float(
            request.POST["loan_term"]
        )

        cibil_score = float(
            request.POST["cibil_score"]
        )

        residential_assets_value = float(
            request.POST[
                "residential_assets_value"
            ]
        )

        commercial_assets_value = float(
            request.POST[
                "commercial_assets_value"
            ]
        )

        luxury_assets_value = float(
            request.POST[
                "luxury_assets_value"
            ]
        )

        bank_asset_value = float(
            request.POST[
                "bank_asset_value"
            ]
        )

        # -------------------------------------------------
        # Prepare Data For ML Model
        # -------------------------------------------------

        data = [[
            no_of_dependents,
            education,
            self_employed,
            income_annum,
            loan_amount,
            loan_term,
            cibil_score,
            residential_assets_value,
            commercial_assets_value,
            luxury_assets_value,
            bank_asset_value
        ]]

        # -------------------------------------------------
        # Prediction
        # -------------------------------------------------

        prediction_result = model.predict(data)

        print(
            "MODEL PREDICTION:",
            prediction_result
        )

        # -------------------------------------------------
        # 0 = Approved
        # 1 = Rejected
        # -------------------------------------------------

        if prediction_result[0] == 0:

            result = {
                "status": "approved",
                "title": "Loan Approved",
                "message": (
                    "Congratulations! Based on the "
                    "provided details, the applicant "
                    "is eligible for loan approval."
                )
            }

            db_result = "Approved"

        else:

            result = {
                "status": "rejected",
                "title": "Loan Rejected",
                "message": (
                    "Sorry! Based on the provided "
                    "details, the applicant is not "
                    "eligible for loan approval."
                )
            }

            db_result = "Rejected"

        # -------------------------------------------------
        # Save Prediction
        # -------------------------------------------------

        Prediction.objects.create(

            user=request.user,

            no_of_dependents=no_of_dependents,

            education=education,

            self_employed=self_employed,

            income_annum=income_annum,

            loan_amount=loan_amount,

            loan_term=loan_term,

            cibil_score=cibil_score,

            residential_assets_value=(
                residential_assets_value
            ),

            commercial_assets_value=(
                commercial_assets_value
            ),

            luxury_assets_value=(
                luxury_assets_value
            ),

            bank_asset_value=(
                bank_asset_value
            ),

            result=db_result
        )

    return render(
        request,
        "prediction.html",
        {
            "result": result
        }
    )


# =========================================================
# HISTORY
# =========================================================

@login_required(login_url="login")
def history(request):

    predictions = Prediction.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "history.html",
        {
            "predictions": predictions
        }
    )


# =========================================================
# DOWNLOAD PDF REPORT
# =========================================================

@login_required(login_url="login")
def download_report(
    request,
    prediction_id
):

    prediction = Prediction.objects.get(
        id=prediction_id,
        user=request.user
    )

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'attachment; '
        f'filename="loan_report_'
        f'{prediction.id}.pdf"'
    )

    pdf = canvas.Canvas(response)

    pdf.setTitle(
        "Loan Prediction Report"
    )

    # -------------------------------------------------
    # Heading
    # -------------------------------------------------

    pdf.setFont(
        "Helvetica-Bold",
        20
    )

    pdf.drawCentredString(
        300,
        800,
        "LOAN PREDICTION REPORT"
    )

    # -------------------------------------------------
    # Details
    # -------------------------------------------------

    pdf.setFont(
        "Helvetica",
        12
    )

    y = 750

    pdf.drawString(
        60,
        y,
        f"Username: {request.user.username}"
    )

    y -= 30

    pdf.drawString(
        60,
        y,
        f"Dependents: "
        f"{prediction.no_of_dependents}"
    )

    y -= 25

    pdf.drawString(
        60,
        y,
        "Education: "
        + (
            "Graduate"
            if prediction.education == 1
            else "Not Graduate"
        )
    )

    y -= 25

    pdf.drawString(
        60,
        y,
        f"Annual Income: "
        f"{prediction.income_annum}"
    )

    y -= 25

    pdf.drawString(
        60,
        y,
        f"Loan Amount: "
        f"{prediction.loan_amount}"
    )

    y -= 25

    pdf.drawString(
        60,
        y,
        f"Loan Term: "
        f"{prediction.loan_term}"
    )

    y -= 25

    pdf.drawString(
        60,
        y,
        f"CIBIL Score: "
        f"{prediction.cibil_score}"
    )

    y -= 40

    # -------------------------------------------------
    # Result
    # -------------------------------------------------

    pdf.setFont(
        "Helvetica-Bold",
        16
    )

    pdf.drawString(
        60,
        y,
        f"Result: {prediction.result}"
    )

    y -= 40

    # -------------------------------------------------
    # Date
    # -------------------------------------------------

    pdf.setFont(
        "Helvetica",
        11
    )

    pdf.drawString(
        60,
        y,
        "Generated on: "
        + prediction.created_at.strftime(
            "%d-%m-%Y %H:%M"
        )
    )

    pdf.save()

    return response