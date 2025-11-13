from django.http import Http404, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render, redirect
from MainApp.forms import SnippetForm
from MainApp.models import Snippet

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    # Создаем пустую форму при запросе GET
    if request.method == "GET":
        form = SnippetForm()
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form
            }
        return render(request, 'pages/add_snippet.html', context)
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
            # GET /snippets/list
            return redirect("snippets-list") # URL для списка сниппетов
        return render(request, 'pages/add_snippet.html', context={"form": form})


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


def snippet_delete(request, snippet_id):
    if request.method == "GET" or request.method == "POST":
        snippet = get_object_or_404(Snippet, id=snippet_id)
        snippet.delete()

    return redirect("snippets-list") # URL для списка сниппетов


def snippet_edit(request, snippet_id):
    pass
    # Создаем пустую форму при запросе GET
    # if request.method == "GET":
    #     form = SnippetForm()
    #     context = {
    #         'pagename': 'Редактирование сниппета',
    #         'form': form
    #         }
    #     return render(request, 'pages/snippet_edit.html', context)
    # if request.method == "POST":
    #     form = SnippetForm(request.POST)
    #     snippet = get_object_or_404(Snippet, id=snippet_id)
    #     if form.is_valid():
    #         if snippet.name != form.name:

            
    #         return redirect("snippets-list") # URL для списка сниппетов
    #     return render(request, 'pages/snippet_edit.html', context={"form": form})