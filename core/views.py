from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import UserRegisterForm, JobForm, ApplicationForm
from .models import Job, Application
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages

User = get_user_model()  # This will get your custom core.User model

def home(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    if request.user.role == 'job_seeker':
        return render(request, 'dashboard/seeker_dashboard.html')
    elif request.user.role == 'employer':
        return render(request, 'dashboard/employer_dashboard.html')
    elif request.user.role == 'admin':
        return render(request, 'dashboard/admin_dashboard.html')
    else:
        return redirect('login')

@login_required
def job_posting_view(request):
    if request.user.role != 'employer':
        messages.error(request, "Unauthorized access.")
        return redirect('dashboard')
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request, "Job posted successfully.")
            return redirect('dashboard')
    else:
        form = JobForm()
    return render(request, 'job_posting.html', {'form': form})

@login_required
def job_search_view(request):
    if request.user.role != 'job_seeker':
        messages.error(request, "Unauthorized access.")
        return redirect('dashboard')
    jobs = Job.objects.all()
    # Add filtering logic here if needed
    return render(request, 'job_search.html', {'jobs': jobs})

@login_required
def apply_job_view(request, job_id):
    if request.user.role != 'job_seeker':
        messages.error(request, "Unauthorized access.")
        return redirect('dashboard')
    job = Job.objects.get(id=job_id)
    if request.method == 'POST':
        application = Application(job=job, applicant=request.user)
        application.save()
        messages.success(request, "Applied for job successfully.")
        return redirect('dashboard')
    return render(request, 'apply_job.html', {'job': job})

@login_required
def admin_manage_view(request):
    if request.user.role != 'admin':
        messages.error(request, "Unauthorized access.")
        return redirect('dashboard')
    users = User.objects.all()
    jobs = Job.objects.all()
    return render(request, 'dashboard/admin_manage_jobs.html', {'users': users, 'jobs': jobs})

def admin_manage_jobs(request):
    jobs = Job.objects.all().order_by('-date_posted')
    return render(request, 'dashboard/admin_manage_jobs.html', {'jobs': jobs})


@login_required
def manage_jobs(request):
    user = request.user

    if user.role == 'employer':
        if request.method == 'POST':
            title = request.POST['title']
            description = request.POST['description']
            salary = request.POST['salary']
            location = request.POST['location']
            category = request.POST['category']

            Job.objects.create(
                title=title,
                description=description,
                salary=salary,
                location=location,
                category=category,
                posted_by=user
            )
            messages.success(request, 'Job posted successfully!')

        jobs = Job.objects.filter(posted_by=user)

    elif user.role == 'admin':
        jobs = Job.objects.all()

    else:  # Job Seeker
        jobs = Job.objects.all()

    return render(request, 'manage_jobs.html', {'jobs': jobs})

def apply_job(request, job_id):
    job = Job.objects.get(id=job_id)
    
    # Optional: Check if already applied
    already_applied = Application.objects.filter(job=job, user=request.user).exists()
    if already_applied:
        messages.warning(request, "You have already applied for this job.")
        return redirect('job_detail', job_id=job.id)

    # Save application
    Application.objects.create(job=job, user=request.user)
    messages.success(request, "Successfully applied for the job!")
    return redirect('job_detail', job_id=job.id)

    