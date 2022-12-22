from .models import Article
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import Http404
# Create your views here.

def archive(request):

   return render(request, 'archive.html', {"posts": Article.objects.all()})

def get_article(request, article_id):
    # one article view
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise 
    
def create_post(request):
    if not request.user.is_anonymous:
        # Здесь будет основной код представления
        if request.method == "POST":
        # обработать данные формы, если метод POST
            form = {
                'text': request.POST["text"], 'title': request.POST["title"]
            }
        # в словаре form будет храниться информация, введенная пользователем
            if form["text"] and form["title"]:
        # если поля заполнены без ошибок проверяем уникальна ли статья
                if_article_unique = Article.objects.filter(title=form["title"])
                breakpoint()
                if len(if_article_unique) == 0:
                    article = Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                    return redirect('get_article', article_id=article.id)
                else:
                    form['errors'] = u"Такая статья уже существует"
                    return render(request, 'form.html', {'form': form})
            # перейти на страницу поста
            else:
        # если введенные данные некорректны
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'form.html', {'form': form})
        else:
        # просто вернуть страницу с формой, если метод GET
            return render(request, 'form.html', {})
    else:
        raise Http404
