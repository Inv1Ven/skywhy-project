import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Task

class LatestTasksFeed(Feed):
    title = 'CS2 Рынок Скинов'
    link = reverse_lazy('todo:task_list')
    description = 'Последние поступления скинов в магазине.'

    def items(self):
        return Task.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.content), 30)

    def item_pubdate(self, item):
        return item.publish