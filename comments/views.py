from django.shortcuts import render,redirect,get_object_or_404
from blog.models import Post
from .forms import CommentForm
from .models import Comment


def post_comment(request,post_pk):
    post = get_object_or_404(Post,pk=post_pk)
    #判断方法是否为“POST“
    if request.method == "POST":
        #实例化表单对象
        form = CommentForm(request.POST)
        #验证是否和数据库相符
        if form.is_valid():
            #保存表单内容到数据库
            comment = form.save(commit=False)
            #和要评论的文章联系起来
            comment.post =post
            comment.save()
            #重定向到blog.post里的详情页 detail.html
            return redirect(post)
        else:
            #获取文章的已有的评论
            comment_list = post.comment_set.all()
            context={
                'post':post,
                'form':form,
                'comment_list':comment_list
            }
            return render(request,'detail.html',locals())
    return redirect(post)




