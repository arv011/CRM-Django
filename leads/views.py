from django.core.mail import send_mail
from django.shortcuts import render,redirect, reverse
from django.http import HttpResponse
from leads.models import Leads, Agent, User, Category
from leads.mixins import organiserLoginRequiredMixin
from leads.forms import (Leadform, leadmodelforms, CustomUserCreationform, Agentmodelforms, 
AssignAgentmodelforms, leadcategorymodelforms, Categorymodelform, userprofileform)
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
import random
from django.conf import settings

class Signupview(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationform

    def get_success_url(self):
        return reverse("login")

class Firstpageview(generic.TemplateView):
    template_name = 'firstpage.html'


class Homeleadsview(LoginRequiredMixin, generic.ListView):
    template_name = 'home.html'
    context_object_name = 'all_leads'

    def get_queryset(self):
        user = self.request.user

        if user.is_organiser:
            queryset = Leads.objects.filter(organisation = user.userprofile, assigned_agent__isnull = False)
        elif user.is_agent:
            # queryset = Leads.objects.filter(organisation = user.agent.organisation)
            queryset = Leads.objects.filter(assigned_agent__user = user,assigned_agent__isnull = False )
        return queryset

    def get_context_data(self, **kwargs):
        context = super(Homeleadsview, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organiser:
            queryset = Leads.objects.filter(organisation = user.userprofile, assigned_agent__isnull = True)
            context.update({
                'unassigned_leads': queryset
            })
        return context

class AssignAgentView(organiserLoginRequiredMixin, generic.FormView):
    template_name = 'Assign_agent.html'
    form_class = AssignAgentmodelforms

    
    def get_success_url(self):
        return reverse("leads:Home")
    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView,self).get_form_kwargs(**kwargs)
        kwargs.update({
            'request':self.request
        })
        return kwargs

    def form_valid(self,form):
        agent = form.cleaned_data['agent']
        lead = Leads.objects.get(id = self.kwargs['pk'])
        lead.assigned_agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)


class leadview(LoginRequiredMixin, generic.DetailView):
    template_name = 'lead_detail.html'
    context_object_name = 'lead'

    
    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Leads.objects.filter(organisation = user.userprofile)
        elif user.is_agent:
            queryset = Leads.objects.filter(assigned_agent__user = user)
        return queryset



class createleadview(organiserLoginRequiredMixin, generic.CreateView):
    template_name = 'create_lead.html'
    form_class = leadmodelforms
    
    def get_success_url(self):
        return reverse("leads:Home")
    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        
        form.save()
        user = self.request.user
        send_mail(
            subject="lead is successfully created",
            message="go to leads and see all the leads ",
            from_email= settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super(createleadview, self).form_valid(form)


class updateleadview(organiserLoginRequiredMixin, generic.UpdateView):
    template_name = "update_lead.html"
    form_class = leadmodelforms
    context_object_name = 'lead'
    
    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Leads.objects.filter(organisation = user.userprofile)
        return queryset

    def get_success_url(self):
        return reverse("leads:Home")
    
class deleteleadview(organiserLoginRequiredMixin, generic.DeleteView):
    template_name = 'delete_lead.html'
    

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Leads.objects.filter(organisation = user.userprofile)
        
        return queryset

    def get_success_url(self):
        return reverse("leads:Home")


class updateleadcategoryview(LoginRequiredMixin,generic.UpdateView):
    template_name = 'updateleadcategory.html'
    form_class = leadcategorymodelforms
    context_object_name = 'lead'

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Leads.objects.filter(organisation = user.userprofile)
        elif user.is_agent:
            queryset = Leads.objects.filter(assigned_agent__user = user)
        return queryset

    def get_success_url(self):
        return reverse("leads:details",kwargs={'pk': self.get_object().id})

#########################################CATEGORY######################################

class HomeCategoryView(LoginRequiredMixin,generic.ListView):
    template_name = 'category_list.html'
    context_object_name = 'Categories'


    def get_queryset(self):
        user = self.request.user
        
        if user.is_organiser:
            queryset = Category.objects.filter(organisation = user.userprofile)
        elif user.is_agent:
            queryset = Category.objects.filter(organisation = user.agent.organisation)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(HomeCategoryView, self).get_context_data(**kwargs)
        user = self.request.user
        list_categories = []
        cate_list = context['object_list'].values()
        if user.is_organiser:
            queryset = Leads.objects.filter(organisation = user.userprofile)
        else:
            queryset = Leads.objects.filter(organisation = user.agent.organisation)

        

        for cat in cate_list:
            cat['Number'] = queryset.filter(category = cat['id']).count()
            x = {'id': cat['id'], 
                'name': cat['Name'],
                'number': cat['Number']}
            list_categories.append(x)


        context.update({
            'unassigned_lead_count': queryset.filter(category__isnull = True).count(),
            'Category_count' : list_categories
            })
        return context

class Categorydetailview(LoginRequiredMixin, generic.DetailView):
    template_name = 'category-detail.html'
    context_object_name = 'category'

    def get_context_data(self,**kwargs):
        context = super(Categorydetailview, self).get_context_data(**kwargs)
        qs = Leads.objects.filter(category=self.get_object())

        context.update({
            'leads': qs
        })
        return context
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_organiser:
            queryset = Category.objects.filter(organisation = user.userprofile)
        elif user.is_agent:
            queryset = Category.objects.filter(organisation = user.agent.organisation)
        return queryset   



class createcategoryview(organiserLoginRequiredMixin, generic.CreateView):
    template_name = 'create_category.html'
    form_class = Categorymodelform
    
    def get_success_url(self):
        return reverse("leads:Home-category")
    def form_valid(self, form):
        Category = form.save(commit=False)
        Category.organisation = self.request.user.userprofile
        form.save()
        
        return super(createcategoryview, self).form_valid(form)



class Categoryupdateview(organiserLoginRequiredMixin, generic.UpdateView):
    template_name = "update_category.html"
    form_class = Categorymodelform
    context_object_name = 'category'
    
    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Category.objects.filter(organisation = user.userprofile)
        return queryset

    def get_success_url(self):
        return reverse("leads:Home-category")


class Categorydeleteview(organiserLoginRequiredMixin, generic.DeleteView):
    template_name = 'delete_category.html'
    
    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Category.objects.filter(organisation = user.userprofile)
        
        return queryset

    def get_success_url(self):
        return reverse("leads:Home-category")

######################################AGENTS######################################
class Homeagentsview(organiserLoginRequiredMixin, generic.ListView):
    template_name = 'home_agent.html'
    context_object_name = 'agents'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        queryset = Agent.objects.filter(organisation=organisation)
        return queryset

class CreateAgentView(organiserLoginRequiredMixin, generic.CreateView):
    template_name = 'create_agent.html'
    form_class = Agentmodelforms
    
    def get_success_url(self):
        return reverse("leads:agent-list")
    def form_valid(self, form):
        user = form.save(commit = False)
        user.is_agent = True
        user.is_organiser = False
        user.set_password(f'{random.randint(0,10000)}')
        user.save()
        Agent.objects.create(user=user, organisation= self.request.user.userprofile)
        send_mail(
            subject='you are invited to an agent',
            message = f'you are added as agent in CRM SYSTEM hosted by Arv and your username id "{user.username}" to set your password go to login and then forgot password fill your email-id we will send you email shortly website Link: crm-by-arv.herokuapp.com',
            from_email= settings.EMAIL_HOST_USER,
            recipient_list = [user.email]
        )
        return super(CreateAgentView, self).form_valid(form)

class agentdetailview(organiserLoginRequiredMixin, generic.DetailView):
    template_name = 'agent_detail.html'
    context_object_name = 'agent'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        queryset = Agent.objects.filter(organisation=organisation)
        return queryset


class DeleteAgentview(organiserLoginRequiredMixin, generic.DeleteView):
    template_name = 'delete_agent.html'
    
    def get_success_url(self):
        return reverse("leads:agent-list")
    
    def get_queryset(self):
        organisation = self.request.user.userprofile
        queryset = Agent.objects.filter(organisation=organisation)
        return queryset

class UpdateAgentview(organiserLoginRequiredMixin, generic.UpdateView):
    template_name = 'update_agent.html'
    form_class = Agentmodelforms
    context_object_name = 'agent'

    
    def get_success_url(self):
        return reverse("leads:agent-list")
    

    def get_queryset(self):
        queryset = Agent.objects.filter(organisation=self.request.user.userprofile)
        return queryset



class userprofileview(LoginRequiredMixin, generic.DetailView):
    template_name = 'userprofile.html'
    
    def get_object(self):
        return self.request.user

class Updateuserprofileview(LoginRequiredMixin, generic.UpdateView):
    template_name = 'updateprofile.html'
    form_class = userprofileform
    context_object_name = 'profile'

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.filter(id = user.id)
        return queryset

    def get_success_url(self):
        return reverse('leads:userprofile',kwargs={'pk': self.get_object().id})