from django.shortcuts import render


def index(request):

    context = {'title': "Book Recommendations"}

    return render(request, 'index.html', context)


def results(request):
    pass


# todo Require at least two titles.
# todo Have data consistency checks to throw out (or rank weakly) bogus data.
# todo Allow a registration option that will weigh your entries more heavily than other entries
# todo At least initially, don't let users rank their favourties, but rank recommendations.