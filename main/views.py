from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CategoryForm, ApplicationStatusForm, ApplicationForm
from .models import Category, Application

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


@staff_member_required
def admin_panel(request):
    applications = Application.objects.all()
    categories = Category.objects.all()

    category_form = CategoryForm()

    if request.method == 'POST' and 'add_category' in request.POST:
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            return redirect('admin_panel')

    return render(request, 'main/admin_panel.html', {
        'applications': applications,
        'categories': categories,
        'category_form': category_form,
    })


@staff_member_required
def change_application_status(request, pk):
    application = get_object_or_404(Application, pk=pk)

    if request.method == 'POST':
        form = ApplicationStatusForm(request.POST, request.FILES, instance=application)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = ApplicationStatusForm(instance=application)

    return render(request, 'main/change_status.html', {
        'form': form,
        'application': application
    })


@staff_member_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category.delete()
        return redirect('admin_panel')

    return render(request, 'main/confirm_delete_category.html', {'category': category})