def next_url(request):
    return {'next': request.GET.get('next')}