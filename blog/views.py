from django.shortcuts import render, get_object_or_404
from .models import Post,Category
import markdown
from comments.forms import CommentForm
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger




# 主页面
def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    paginator = Paginator(post_list,10)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except  PageNotAnInteger:
        post_list = paginator.page(1)
    except  EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'index.html', locals())


# 查看文章的详细页面
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    form = CommentForm()
    comment_list= post.comment_set.all()
    context = {
        'post': post,
        'form': form,
        'comment_list': comment_list
    }

    return render(request, 'detail.html', locals())


def archives(req, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(req, 'index.html', locals())


def category(req , pk):
    cate = get_object_or_404(Category,pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(req, 'index.html', locals())

def search(request):
    q=request.GET.get("q")
    error=''
    if not q:
        error='查询不存在'
        return render(request,"index.html",locals())
    post_list = Post.objects.filter(title__icontains=q)
    return render(request,'index.html',locals())
