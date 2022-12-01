from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Meetup, Participant
from .forms import RegistrationForm


def index(request):
    meetups = Meetup.objects.all()
    # meetups = [
    #     {'title': 'A First Meetup', 'location': 'NY', 'slug': 'a-first-meetup'},
    #     {'title': 'A Second Meetup', 'location': 'Paris', 'slug': 'a-second-meetup'}
    # ]
    return render(request, 'meetups/index.html', {
        # 'show_meetups': True,
        'meetups': meetups
    })


def meetup_details(request, meetup_slug):
    try:
        selected_meetup = Meetup.objects.get(slug=meetup_slug)

        if request.method == 'GET':
            registration_form = RegistrationForm()
    # selected_meetup = {
    #     'title': 'A First Meetup',
    #     'description': 'This is it.'
    # }

        else:
            registration_form = RegistrationForm(request.POST)
            if registration_form.is_valid():
                user_email = registration_form.cleaned_data['email']
                participant, _ = Participant.objects.get_or_create(email=user_email)
                selected_meetup.participants.add(participant)
                return redirect('confirm-registration', meetup_slug=meetup_slug)

        return render(request, 'meetups/meetup-details.html', {
            'meetup_found': True,
            'meetup': selected_meetup,
            'form': registration_form
            # 'meetup_title': selected_meetup.title,
            # 'meetup_description': selected_meetup.description
        })
    except Exception as exc:
        return render(request, 'meetups/meetup-details.html', {
            'meetup_found': False
        })


def confirm_registration(request, meetup_slug):
    meetup = Meetup.objects.get(slug=meetup_slug)
    return render(request, 'meetups/registration-success.html', {
        'organizer_email': meetup.organizer_email
    })