from django import template
from ..models import Task
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.simple_tag
def total_tasks():
    return Task.published.count()

@register.inclusion_tag('todo/includes/latest_tasks.html')
def show_latest_tasks(count=3):
    latest_tasks = Task.published.order_by('-publish')[:count]
    return {'latest_tasks': latest_tasks}

@register.simple_tag
def get_most_commented_tasks(count=3):
    return Task.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))