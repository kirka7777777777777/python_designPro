from django.shortcuts import render
from .models import Application
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ApplicationForm


def home(request):

    completed_applications = Application.objects.filter(status='completed')[:4]

    in_progress_count = Application.objects.filter(status='in_progress').count()

    context = {
        'completed_applications': completed_applications,
        'in_progress_count': in_progress_count,
    }
    return render(request, 'main/home.html', context)


@login_required
def profile(request):
    applications = Application.objects.filter(user=request.user)

    
    status_filter = request.GET.get('status')
    if status_filter:
        applications = applications.filter(status=status_filter)

    return render(request, 'main/profile.html', {
        'applications': applications,
        'status_filter': status_filter
    })


@login_required
def create_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            return redirect('profile')
    else:
        form = ApplicationForm()

    return render(request, 'main/create_application.html', {'form': form})


@login_required
def delete_application(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)

    if application.status != 'new':
        return redirect('profile')

    if request.method == 'POST':
        application.delete()
        return redirect('profile')

