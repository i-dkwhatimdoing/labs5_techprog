from django.shortcuts import render

# Create your views here.
from .models import Article
from django.http import Http404

def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})

def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404

def create_post(request):
    if not request.user.is_anonymous:
        if request.method == "POST":
            form = {
                'text': request.POST["text"], 'title': request.POST["title"]
            }
            if form["text"] and form["title"]:
                if_article_unique = Article.objects.filter(title=form["title"])
                breakpoint()
                if len(if_article_unique) == 0:
                    article = Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                    return redirect('get_article', article_id=article.id)
                else:
                    form['errors'] = u"Такая статья уже существует"
                    return render(request, 'form.html', {'form': form})
            else:
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'form.html', {'form': form})
        else:
            return render(request, 'form.html', {})
    else:
        raise Http404