from django.db.models import Count
from taggit.models import Tag
from .forms import EmailTaskForm, CommentForm
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Task
from .forms import EmailTaskForm


class TaskListView(ListView):
    context_object_name = 'tasks'
    paginate_by = 9
    template_name = 'todo/task_list.html'

    # метод получения списка скинов
    def get_queryset(self):
        queryset = Task.published.all()
        tag_slug = self.kwargs.get('tag_slug')
        self.tag = None
        
        if tag_slug:
            self.tag = get_object_or_404(Tag, name__iexact=tag_slug)
            queryset = queryset.filter(tags__in=[self.tag])
        return queryset

    # тег в контекст шаблона, чтобы вывести его название
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context



def task_detail(request, year, month, day, slug):
    task = get_object_or_404(
        Task.published,
        slug=slug,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )

    comments = task.comments.filter(active=True)
    new_comment = None
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.task = task
            new_comment.save()
            comment_form = CommentForm()

    # Вот этот блок отвечает за поиск похожих скинов по тегам!
    task_tags_ids = task.tags.values_list('id', flat=True)
    similar_tasks = Task.published.filter(tags__in=task_tags_ids) \
                                  .exclude(id=task.id) \
                                  .annotate(same_tags=Count('tags')) \
                                  .order_by('-same_tags', '-publish')[:4]

    return render(request, 'todo/task_detail.html', {
        'task': task,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'similar_tasks': similar_tasks,
    })



def buy_skin(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if not task.is_sold:
        task.is_sold = True
        task.save()
        messages.success(request, f'Вы успешно купили {task.title}!')
    else:
        messages.warning(request, 'Этот скин уже продан.')
    
    return redirect('todo:task_list')

    #http://127.0.0.1:8000/todo/
def task_share(request, task_id):
    task = get_object_or_404(Task, id=task_id, status=Task.Status.PUBLISHED)
    sent = False  
    
    if request.method == 'POST':
        form = EmailTaskForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            
            task_url = request.build_absolute_uri(task.get_absolute_url())
            
            subject = f"{cd['name']} рекомендует вам скин: {task.title}"
            message = (
                f"Привет!\n\n"
                f"Посмотри на этот скин: {task_url}\n\n"
                f"Комментарий от {cd['name']}: {cd['comments']}\n"
            )
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [cd['to']], 
            )
            
            sent = True
            messages.success(request, f'Скин "{task.title}" успешно отправлен на {cd["to"]}!')
    else:
        form = EmailTaskForm()

    return render(request, 'todo/task_share.html', {'task': task, 'form': form, 'sent': sent})

   









