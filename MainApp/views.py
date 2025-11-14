from django.http import Http404, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render, redirect
from MainApp.forms import SnippetForm
from MainApp.models import Snippet
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)

@login_required
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
            snippet = form.save(commit=False) # Получаем экземпляр класса Snippet
            if request.user.is_authenticated:
                snippet.user = request.user
                snippet.save()
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
                'snippets': Snippet.objects.filter(public=True)
            }
    return render(request, 'pages/view_snippets.html', context)

@login_required
def snippet_delete(request, snippet_id):
    if request.method == "GET" or request.method == "POST":
        snippet = get_object_or_404(Snippet.objects.filter(user=request.user), id=snippet_id)
        snippet.delete()
    return redirect("snippets-list") # URL для списка сниппетов


def snippet_edit(request, snippet_id):
    # pass
    # Создаем форму при запросе GET
    if request.method == "GET":
        snippet = get_object_or_404(Snippet.objects.filter(user=request.user), id=snippet_id)
        form = SnippetForm(instance=snippet)
        context = {
            'pagename': 'Редактирование сниппета',
            'form': form
            }
        return render(request, 'pages/snippet_edit.html', context)
    if request.method == "POST":
        snippet = get_object_or_404(Snippet, id=snippet_id)
        form = request.POST
        snippet.name = form['name']
        snippet.lang = form['lang']
        snippet.code = form['code']
        snippet.public = form.get('public', False)
        snippet.save()
        return redirect("snippets-list") # URL для списка сниппетов


def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        # print("username =", username)
        # print("password =", password)
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            context = {
                "pagename": "PythonBin",
                "errors": ["Wrong username or password."]
            }
            return render(request, "pages/index.html", context)
    return redirect('home')


def logout(request):
    auth.logout(request)
    return redirect(to='home')

@login_required
def my_snippets(request):
  
    context = {'pagename': 'Мои сниппеты',
        'snippets': Snippet.objects.filter(user=request.user)
    }
    return render(request, 'pages/my_snippets.html', context)

