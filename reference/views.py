from django.shortcuts import render, get_object_or_404
from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)
from django.db.models import Count
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, FormView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.text import slugify
from .models import Reference


class ReferenceListView(LoginRequiredMixin, ListView):
    queryset = Reference.objects.all() 
    context_object_name = 'references' 
    paginate_by = 2
    template_name = 'reference/list.html'
    
    def get_queryset(self):
        qs = super().get_queryset()
        tag_slug = self.kwargs.get('tag_slug')

        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            qs = qs.filter(tags__in=[tag])
            self.tag = tag
        else:
            self.tag = None

        return qs

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)

        return context

class ReferenceCreateView(LoginRequiredMixin, CreateView):
    model = Reference
    fields = ['title', 'description', 'link']
    template_name = 'reference/reference_form.html'
    success_url = reverse_lazy('reference:reference_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title, allow_unicode=True)

        return super().form_valid(form)

class ReferenceUpdateView(LoginRequiredMixin, UpdateView):
    model = Reference
    fields = ['title', 'description', 'link']
    template_name = 'reference/reference_form.html'
    success_url = reverse_lazy('reference:reference_list')
    query_pk_and_slug = True

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author = self.request.user)

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title, allow_unicode=True)
        return super().form_valid(form)

class ReferenceDeleteView(LoginRequiredMixin, DeleteView):
    model = Reference
    template_name = 'reference/reference_confirm_delete.html'
    success_url = reverse_lazy('reference:reference_list')
    query_pk_and_slug = True

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author = self.request.user)