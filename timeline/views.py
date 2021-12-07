from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .models import Content, Title

# Create your views here.


def index(request):
    title = Title.objects.all().order_by('-pk')
    return redirect(f'/timelines/{title[0].slug}')
    # content = Content.objects.all()
    # title = Title.objects.all()
    # index = {
    #     # 'content': content,
    #     'title': title
    # }

    # return render(request, 'index.html', index)


def Posts_in_TitleView(request, slug):
    category = get_object_or_404(Title, slug=slug)
    specefic = Content.objects.filter(title=category).order_by('-pk')
    title = Title.objects.all().order_by('-pk')
    context = {
        'cat_name': category,
        'content': specefic,
        'title': title,
    }
    return render(request, 'timeline/timeline.html', context)
