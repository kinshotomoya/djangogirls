#このファイルでは、rails でいうcontrollerの役割をしている！
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone #timezoneを使うときは、importしてあげる！
from .models import Post #Postモデルを使うのでimpoerする！
from .forms import PostForm


# Create your views here.
def post_list(request):
    posts = Post.objects.filter(created_date__lte=timezone.now()).order_by('published_date') #クエリセット！
    return render(request, 'blog/post_list.html', {'posts': posts}) #post_list.tmlのviewで使えるように値を送っている！！


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render (request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
