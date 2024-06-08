from django import template
from django.shortcuts import get_object_or_404
from services.redis_services import r
from django.db.models import Count
from django.core.cache import cache

from ..models import Post, Category, Tag


register = template.Library()


@register.inclusion_tag('post/post/list_categories.html')
def show_categories():
    cats_lst = cache.get('cats')
    if not cats_lst:
        cats_lst = Category.objects.annotate(total=Count("posts")).filter(total__gt=0)
        cache.set('cats', cats_lst, 60)
    return {'cats': cats_lst}


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.simple_tag
def get_most_commented_posts(count=3):
    most_commented_posts = cache.get('most_commented_posts')
    if not most_commented_posts:
        most_commented_posts = Post.published.annotate(total_comments=Count('comments'))\
                         .order_by('-total_comments')[:count]
        cache.set('most_commented_posts', most_commented_posts, 60)
    return most_commented_posts


@register.simple_tag
def get_total_views(pk):
    total_views = int(r.get(f'post:{pk}:views')) if r.get(f'post:{pk}:views') else 0
    return total_views


@register.simple_tag
def get_category_name(pk):
    cat = get_object_or_404(Category, pk=pk)
    return cat.cat_title


@register.inclusion_tag('post/post/includes/tags_list.html')
def show_all_tags():
    tag_lst = cache.get('tag_lst')
    if not tag_lst:
        tag_lst = Tag.objects.all().only('slug', 'name')
        cache.set('tag_lst', tag_lst, 60)
    return {'tags': tag_lst}
