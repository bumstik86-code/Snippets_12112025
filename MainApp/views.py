from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.models import Snippet

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    context = {'pagename': 'Добавление нового сниппета'}
    return render(request, 'pages/add_snippet.html', context)

def snippet_detail(request, snippet_id):
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except Snippet.DoesNotExist:
        raise Http404(f"Snippet with Id={snippet_id} does not exist.")
    else:
        context={
            'pagename': 'Cниппет',
            'snippet': snippet
        }
        return render(request, "pages/snippet_detail.html", context=context)



def snippets_page(request):
    context = {'pagename': 'Просмотр сниппетов',
                'snippets': Snippet.objects.all()
            }
    return render(request, 'pages/view_snippets.html', context)
