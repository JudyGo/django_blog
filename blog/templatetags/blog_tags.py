from ..models import Post,Category
from django import  template

#实例化
register = template.Library()


#用装饰器把下面的方法装饰 就可以在模板中调用
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]

@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')

@register.simple_tag
def get_categories():
    return Category.objects.all()

