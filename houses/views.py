from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import House
from .utils import scrape_funda
from .forms import FundaLoginForm
from hendrix.experience import crosstown_traffic


def status(request, channel_name=None):

    """
        if we have a chat_channel_name kwarg,
        have the response include that channel name
        so the javascript knows to subscribe to that
        channel...
    """

    if not channel_name:
        channel_name = 'homepage'

    context = {
        'address': channel_name,
        'history': [],
    }

    if House.objects.filter(channel=channel_name).exists():
        context['history'] = House.objects.filter(
            channel=channel_name)

    return render(request, 'status.html', context)


def funda_login(request):

    if request.method == 'POST':
        form = FundaLoginForm(request.POST)

        if form.is_valid():
            funda_user = form.cleaned_data['funda_username']
            funda_pass = form.cleaned_data['funda_password']
            House.objects.all().delete()
            @crosstown_traffic()
            def scrape_funda_later():
                scrape_funda(funda_user, funda_pass)

            return HttpResponseRedirect('/status/')
    else:
        form = FundaLoginForm()
    return render(request, 'fundalogin.html', {'form': form})
