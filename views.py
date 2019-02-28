# View.py
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from home.forms import StudentSignUpForm, TutorSignUpForm, BookingForm
from .models import Tutor, Instrument, Student, Hour, Availablity, Booking   # import all models
from django.db.models import Q # import for searching
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# functions to get objects, classname.objects - send to url, args
# url = reverse(view_name, args=args, kwargs=kwargs, current_app=current_app)

## HOME
@login_required(login_url="/accounts/login/")
def home(request):
    tutors = Tutor.objects.all()
    students = Student.objects.all()
    return render(request, 'home.html', {'tutors': tutors,'students': students,})


## FORMS
# sign up form
def StudentSignup(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            student = Student(
                user = authenticate(username=username, password=raw_password),
                profile_pic = form.cleaned_data.get('profile_pic'),
                name = (form.cleaned_data.get('first_name') + ' ' + form.cleaned_data.get('last_name')),
                about = form.cleaned_data.get('about'),
                instrument_req = form.cleaned_data.get('instrument_required'),
                instrument = form.cleaned_data.get('instrument'),
                )
            student.save()
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = StudentSignUpForm()
    return render(request, 'registration/studentsignup.html', {'form': form})





# tutor sign up form
def TutorSignup(request):
    if request.method == 'POST':
        form = TutorSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            tutor = Tutor(
                user = authenticate(username=username, password=raw_password),
                profile_pic = form.cleaned_data.get('profile_pic'),
                name = (form.cleaned_data.get('first_name') + ' ' + form.cleaned_data.get('last_name')),
                experience = form.cleaned_data.get('experience'),
                instrument_avail = form.cleaned_data.get('instrument_available'),
                instrument = form.cleaned_data.get('instrument'),
                price = form.cleaned_data.get('hourly_rate'),
                )
            tutor.save()
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = TutorSignUpForm()
    return render(request, 'registration/tutorsignup.html', {'form': form})

## PROFILE
# Logged In User Profile
@login_required(login_url="/accounts/login/")
def profile(request, id):
    user = User.objects.get(id=id)
    return render(request, 'home/profile.html', {'user': user})


## BOOKING
def schedule(request):
    all_instruments = Instrument.objects.all()
    tutors = Tutor.objects.all()
    all_hours = Hour.objects.all()
    return render(request, 'schedule.html', {'all_instruments': all_instruments, \
        'tutors': tutors, 'all_hours': all_hours})

def detail(request, instrument_type):
    all_instruments = Instrument.objects.all()
    all_tutors = Tutor.objects.all()
    all_availablitys = Availablity.objects.all()
    return render(request, 'instrument_timetable.html', \
        {'all_instruments': all_instruments, 'all_availablitys': all_availablitys, \
        'instrument_type': instrument_type, 'all_tutors': all_tutors,})

def BookingPage(request, booking_id):
    all_students = Student.objects.all()
    all_availablitys = Availablity.objects.all()
    for availablity in all_availablitys:
        availablity.pk = int(availablity.pk)
    passingBooking_id = booking_id
    booking_idx = int(passingBooking_id)
    if request.method == 'POST':
        form = BookingForm(request.POST, request.FILES)
        if form.is_valid():
            for student in all_students:   ## better comparing system can be added  in latter iterations
                if student.user == request.user:
                    stud_booking = student
            if stud_booking == None:
                return render(request, 'not-student.html')
            for availablity in all_availablitys:
                if availablity.pk == booking_idx:
                    avail_page = availablity
            avail_page.available = False
            avail_page.save()
            new_booking = Booking.objects.create(availablity=avail_page, student=stud_booking) 
            new_booking.save()
            return render(request, 'booking-confirmed.html')
    else:
        form = BookingForm()
    return render(request, 'booking_form.html', {'form': form, 'booking_id': booking_idx, \
        'all_availablitys': all_availablitys,})


# GENERIC VIEWS
from django.views import generic
from django.views.generic import DetailView, TemplateView

class BookedView(generic.TemplateView):
    template_name = 'booking-confirmed.html';
## PROFILES VIEW/SEARCH
## Details
@login_required(login_url="/accounts/login/")
def tutor_detail(request, pk):
    tutor = get_object_or_404(Post, pk=pk)
    return render(request, 'tutor_detail.html', {'tutor': tutor})

@login_required(login_url="/accounts/login/")
def student_detail(request, pk):
    tutor = get_object_or_404(Post, pk=pk)
    return render(request, 'student_detail.html', {'student': student})
'''
## Search
@login_required(login_url="/accounts/login/")
def search(request):
    tutor_search = ''
    student_search = ''
    tutors = Tutor.objects.all()
    students = Student.objects.all()

    # search bar
    if 'student_search' in request.GET:
        student_search = request.GET['student_search']
        tutors = tutors.filter(Q(instrument__name__icontains=student_search))
    elif 'tutor_search' in request.GET:
        student_search = request.GET['student_search']
        students = students.filter(Q(instruments__name__icontains=student_search))

    return render(request, 'home/search.html', {'tutors': tutors,'students': students,'student_search': student_search})
'''

# GENERIC VIEWS
from django.views import generic
from django.views.generic import DetailView, TemplateView
#from django.contrib.auth.mixins import LoginRequiredMixin

class AboutView(generic.TemplateView):
    template_name = 'about.html';

class TutorListView(generic.ListView):
    model = Tutor

class StudentListView(generic.ListView):
    model = Student

class TutorDetailView(generic.DetailView):
    model = Tutor

class StudentDetailView(generic.DetailView):
    model = Student