from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CustomerSignUpForm, StaffSignUpForm
from .models import Artist, CompanyInfo, Department


def home(request):
    company_info = CompanyInfo.objects.first()
    departments = (
        Department.objects.prefetch_related("highlights")
        .all()
        .order_by("order", "name")
    )
    artists = Artist.objects.prefetch_related("stats").all().order_by("order", "name")

    context = {
        "company_name": company_info.name if company_info else "Nyalo Intelligence",
        "tagline": company_info.tagline
        if company_info
        else "Technology, creativity, and security working together for modern teams.",
        "mission": company_info.mission
        if company_info
        else "To integrate ICT support, security, engineering, and creativity into one reliable partner for modern businesses and artists.",
        "vision": company_info.vision
        if company_info
        else "To be the go-to intelligence hub in Africa and beyond for secure technology, powerful software, and inspiring entertainment.",
        "owners": [
            name
            for name in [
                getattr(company_info, "owner_primary", "") if company_info else "Munyaradzi Mutoo",
                getattr(company_info, "owner_secondary", "") if company_info else "Emmanuel Vincent Chikarati",
            ]
            if name
        ],
        "contact_email": company_info.email if company_info else "hello@nyalo.intel",
        "contact_phone": company_info.phone if company_info else "+000 000 0000",
        "contact_location": company_info.location
        if company_info
        else "Global • Remote-first",
        "departments": departments,
        "artists": artists,
    }
    return render(request, "core/home.html", context)


class CustomerLoginView(LoginView):
    template_name = "registration/customer_login.html"
    redirect_authenticated_user = True


class StaffLoginView(LoginView):
    template_name = "registration/staff_login.html"
    redirect_authenticated_user = True


def customer_signup(request):
    if request.method == "POST":
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data["email"]
            user.save()
            customers_group, _ = Group.objects.get_or_create(name="Customers")
            customers_group.user_set.add(user)
            login(request, user)
            return redirect("department_list")
    else:
        form = CustomerSignUpForm()
    return render(request, "registration/customer_signup.html", {"form": form})


def staff_signup(request):
    if request.method == "POST":
        form = StaffSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data["email"]
            # Staff candidates are normal users; you can promote them via admin.
            user.save()
            pending_group, _ = Group.objects.get_or_create(name="Staff Candidates")
            pending_group.user_set.add(user)
            login(request, user)
            return redirect("department_list")
    else:
        form = StaffSignUpForm()
    return render(request, "registration/staff_signup.html", {"form": form})


@login_required
def department_list(request):
    company_info = CompanyInfo.objects.first()
    departments = (
        Department.objects.prefetch_related("highlights")
        .all()
        .order_by("order", "name")
    )
    return render(
        request,
        "core/departments_list.html",
        {
            "company_name": company_info.name if company_info else "Nyalo Intelligence",
            "departments": departments,
        },
    )


@login_required
def department_detail(request, slug):
    company_info = CompanyInfo.objects.first()
    department = get_object_or_404(
        Department.objects.prefetch_related("highlights"), slug=slug
    )

    user_groups = set(request.user.groups.values_list("name", flat=True))
    is_customer = "Customers" in user_groups
    staff_group_name = f"{department.name} Staff"
    is_department_staff = staff_group_name in user_groups or request.user.is_staff

    template_map = {
        "ict-support": "core/departments/ict_support.html",
        "computer-hardware-repairs": "core/departments/hardware_repairs.html",
        "software-engineering": "core/departments/software_engineering.html",
        "cybersecurity": "core/departments/cybersecurity.html",
        "music-and-entertainment": "core/departments/music_entertainment.html",
        "graphic-design": "core/departments/graphic_design.html",
        "merchandise-sales": "core/departments/merchandise.html",
    }
    template_name = template_map.get(slug, "core/department_detail.html")

    return render(
        request,
        template_name,
        {
            "company_name": company_info.name if company_info else "Nyalo Intelligence",
            "department": department,
            "is_customer": is_customer,
            "is_department_staff": is_department_staff,
        },
    )
