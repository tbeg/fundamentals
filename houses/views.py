from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import House
from .utils import scrape_funda
from .forms import FundaLoginForm
from hendrix.experience import crosstown_traffic


def status(request):

    total = House.objects.count()
    houses = House.objects.all()

    paginator = Paginator(houses, 4) # Show 25 contacts per page
    page = request.GET.get('page')

    try:
        houses_pag = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        houses_pag = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        houses_pag = paginator.page(paginator.num_pages)

    context = {
        'total': total,
        'houses': houses,
        'houses_pag': houses_pag
    }

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
