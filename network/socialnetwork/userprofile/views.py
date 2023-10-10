from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.utils import timezone
from typing import Any, Dict
from django.contrib import messages
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Q
from . import models
from . import forms
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
@login_required
def my_profile_view(request):

    profile = models.Profile.objects.get(user = request.user)
    
    confirm = False
    context = {}
    if request.method == "POST":
         form = forms.ProfileModelForm(request.POST or None, request.FILES, instance=profile)
         if form.is_valid():
                         form.save()
                         confirm=True
    else:
        form = forms.ProfileModelForm(instance=profile)
         
    return render(request, 'userprofile/myprofile.html', {
        'profile':profile,
        'form' : form,
        'confirm': confirm
		     })

    
@login_required    
def invites_received_view(request):
    profile = models.Profile.objects.get(user = request.user)
    qs = models.Relationship.objects.invatations_received(profile)
    results = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(results)==0:
        is_empty=True
    context = {
        'qs':results,
        'is_empty':is_empty 
		}
    return render(request, 'userprofile/my_invates.html', context)
@login_required
def accept_invatation(request):
    if request.method=="POST":
        pk = request.POST.get('profile_pk')
        sender = models.Profile.objects.get(pk=pk)
        receiver = models.Profile.objects.get(user=request.user)
        rel = get_object_or_404(models.Relationship, sender = sender, receiver=receiver)
        if rel.status == "send":
            rel.status = 'accepted'
            rel.save()
    return redirect('userprofile:my-invites-view')
@login_required        
def reject_invatation(request):
    if request.method=="POST":
        pk = request.POST.get('profile_pk')
        sender = models.Profile.objects.get(pk=pk)
        receiver = models.Profile.objects.get(user=request.user)
        rel = get_object_or_404(models.Relationship, sender = sender, receiver=receiver)
        rel.delete()
    return redirect('userprofile:my-invites-view')   
@login_required
def invite_profile_list_view(request):
    user = request.user
    qs = models.Profile.objects.get_all_profiles_to_invite(user)
    profile = models.Profile.objects.get(user=user)
    rel_r = models.Relationship.objects.filter(sender=profile)
    rel_s = models.Relationship.objects.filter(receiver=profile)
    rel_sender = []
    for item in rel_s:
            rel_sender.append(item.sender.user)
    rel_receiver = []
    for item in rel_r:
            rel_receiver.append(item.receiver.user)
    context = {
        'qs':qs,
        'rel_receiver':rel_receiver,
        'rel_sender':rel_sender
		}
    return render(request, 'userprofile/to_invite_list.html', context)
@login_required
def profile_list_view(request):
    user = request.user
    profile = models.Profile.objects.get(user=user)
    qs = models.Profile.objects.get_all_profiles(user)
    rel_r = models.Relationship.objects.filter(sender=profile)
    rel_s = models.Relationship.objects.filter(receiver=profile)
    rel_sender = []
    for item in rel_s:
            rel_sender.append(item.sender.user)
    rel_receiver = []
    for item in rel_r:
            rel_receiver.append(item.receiver.user)
    context = {
        'qs':qs,
        'rel_receiver':rel_receiver,
        'rel_sender':rel_sender
		}
    return render(request, 'userprofile/profile_list.html', context)
class ProfileDetailView(LoginRequiredMixin,DetailView):
    model = models.Profile
    template_name = 'userprofile/detail.html'
    def get_object(self, slug=None):
        slug = self.kwargs.get('slug')
        profile = models.Profile.objects.get(slug = slug)
        return profile
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = models.Profile.objects.get(user=user)
        context['profile'] = profile
        rel_r = models.Relationship.objects.filter(sender=profile)
        rel_s = models.Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['posts'] = self.get_object().get_all_authors_posts()
        context['len_posts'] = True if len(self.get_object().get_all_authors_posts())>0 else False
        return context


class ProfileListView(LoginRequiredMixin,ListView):
    model = models.Profile
    template_name = 'userprofile/profile_list.html'
    #context_object_name = 'qs'
    def get_queryset(self):
       qs = models.Profile.objects.get_all_profiles(self.request.user) 
       return qs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = models.Profile.objects.get(user=user)
        context['profile'] = profile
        rel_r = models.Relationship.objects.filter(sender=profile)
        rel_s = models.Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset())==0:
            context['is_empty'] = True
        return context
@login_required
def send_invatations(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = models.Profile.objects.get(user=user)
        receiver = models.Profile.objects.get(pk=pk)
        rel = models.Relationship.objects.create(sender=sender, receiver=receiver, status='send')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('userprofile:my-profile-view')
@login_required
def remove_from_friends(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = models.Profile.objects.get(user=user)
        receiver = models.Profile.objects.get(pk=pk)
        rel = models.Relationship.objects.get((Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender)))
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('userprofile:my-profile-view')

