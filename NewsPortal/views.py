from .forms import PostForm
from .models import Post
from datetime import datetime
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,TemplateView
from .filters import NewsFilter
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect
class PostsList(LoginRequiredMixin,ListView):

    model = Post

    ordering = 'time_in'

    template_name = 'post_list.html'

    context_object_name = 'posts'

    paginate_by = 2



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['is_not_author'] = not (self.request.user.groups.filter(name = 'authors').exists())
        return context



class PostDetail(DetailView):

    model = Post

    template_name = 'post_detail.html'

    context_object_name = 'post'



class PostSearch(ListView):

    model = Post

    template_name = 'post_search.html'

    context_object_name = 'posts'



    def get_queryset(self):

        queryset = super().get_queryset()

        self.filterset = NewsFilter(self.request.GET,queryset)

        return self.filterset.qs

    def get_context_data(self):

        context = super().get_context_data()

        context['filterset'] = self.filterset

        return context


class PostCreate(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('NewsPoral.add_post')

    def form_valid(self, form):
        post = form.save(commit=False)
        value = super().form_valid(form).url
        MASSIV = value.split('/')
        post.type = MASSIV[1]
        return super().form_valid(form)

class PostUpdate(PermissionRequiredMixin,LoginRequiredMixin,UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('NewsPortal.change_post')


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

class Error(TemplateView):
    template_name = 'flatpages/error.html'


@login_required
def become_an_author(request):
    user = request.user
    author_group = Group.objects.get(name = 'authors')
    if not request.user.groups.filter(name = 'authors').exists():
        author_group.user_set.add(user)
    return redirect('/')

