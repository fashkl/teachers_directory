from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import unicodecsv as csv
import os

from .models import *
from .filters import TeacherFilter
from .forms import *


# authenticate views #
def logout_view(request):
    logout(request)
    return redirect('TeacherListView')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            return_value = authenticate(
                request=request,
                username=form.cleaned_data.get("username"),
                password=form.cleaned_data.get("password"))

            if return_value is not None:
                login(request, return_value)
                return redirect('TeacherListView')
            else:
                form.add_error("password", "Please check your credentials and try again")
        return render(request, "login.html", {"form": form})
    else:
        form = LoginForm()
        return render(request, "login.html", {"form": form})


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('TeacherListView')
    else:
        form = RegisterForm()
    return render(request, 'signup.html', {'form': form})


# authenticate views #


class TeacherListView(ListView):
    model = Teacher
    template_name = "listView.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = TeacherFilter(self.request.GET, queryset=self.get_queryset())
        return context


class TeacherDetailView(DetailView):
    model = Teacher
    template_name = "detailView.html"


class NewTeacher(CreateView):
    model = Teacher
    form_class = AddTeacherForm
    template_name = "add_teacher.html"


class NewSubject(CreateView):
    model = Subject
    form_class = AddSubjectForm
    template_name = "add_subject.html"


@login_required
def teacher_upload(request):
    template = 'teacher_upload.html'
    prompt = {
        # 'order': "Order should be  First Name - Last Name - Profile picture - Email Address - Phone Number - Room "
        #          "Number - Subjects taught "
    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'CSV file only allowed')

    file_lines = csv_file.read().splitlines()

    reader = csv.DictReader(file_lines)
    invalid_data = 0
    success_import = 0
    for row in reader:

        if row['First Name'].isspace() or row['First Name'] is None or len(row['First Name']) == 0:
            invalid_data += 1
            break

        if row['Last Name'].isspace() or row['Last Name'] is None or len(row['Last Name']) == 0:
            invalid_data += 1
            break

        if row['Email Address'].isspace() or row['Email Address'] is None or len(row['Email Address']) == 0:
            invalid_data += 1
            break

        if row['Phone Number'].isspace() or row['Phone Number'] is None or len(row['Phone Number']) == 0:
            invalid_data += 1
            break

        if row['Profile picture'].isspace() or row['Profile picture'] is None or len(
                row['Profile picture']) == 0 or os.path.isfile('images/images/' + row['Profile picture']) is False:
            row['Profile picture'] = 'default.jpg'

        # add a teacher if he/she has 5 subjects or less
        subjects = row['Subjects taught'].split(',')
        if len(subjects) > 5:
            failed = row['First Name'] + ' ' + row['Last Name'] + " has more than 5 subjects. "
            messages.error(request, failed)
            continue

        # get or create the Teacher if it's Email does not exist
        new_teacher, created = Teacher.objects.get_or_create(email=row['Email Address'])
        if created is False:
            failed = row['First Name'] + ' ' + row['Last Name'] + " has an email that already exists. "
            messages.error(request, failed)
            continue

        # get or create the subject if it does not exist
        subjects_per_line = []
        for subject in subjects:
            new_subject, subject_created = Subject.objects.get_or_create(name=subject.strip().capitalize())
            subjects_per_line.append(new_subject)

        new_teacher.first_name = row['First Name']
        new_teacher.last_name = row['Last Name']
        new_teacher.room_number = row['Room Number']
        new_teacher.phone_number = row['Phone Number']
        new_teacher.image = 'images/' + row['Profile picture']

        if len(subjects_per_line) > 0:
            for subject in subjects_per_line:
                new_teacher.subjects.add(Subject.objects.get(name=str(subject).strip().capitalize()))

        new_teacher.save()
        success_import += 1

    success_message = str(success_import) + " record(s) had successfully imported"
    # failed = str(invalid_data) + " record(s) has invalid data"

    # messages.error(request, failed)
    messages.success(request, success_message)

    context = {}
    return render(request, template, context)
