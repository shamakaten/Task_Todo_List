from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .api.serializers import LoginSerializer, RegisterSerializer, TodoElementCreateSerializer

from .models import (
    Todo,
    Company,
    Person
)

import requests
import json


# Create your views here.
class IndexView(TemplateView):
    template_name = 'todo/index.html'

    def get_context_data(self, request, **kwargs):
        context = {}
        try:
            current_person = Person.objects.get(user=request.user)
            help_comp = Company.objects.get(id=request.user.first_name)
            current_todo_list = list(Todo.objects.filter(company=help_comp).all().values())

            context['current_person'] = current_person
            context['person_companies'] = help_comp.company_name
            context['current_todo_list'] = current_todo_list
        except:
            print("false")
        return context


    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request)
        return render(request, self.template_name, context)

class LoginView(TemplateView):
    template_name = 'todo/login.html'

    def get_context_data(self, **kwargs):
        context = {}
        context['serializer'] = LoginSerializer()
        return context

    def get(self, request, *args, **kwargs):
        if self.request.user.is_active:
            return redirect('/')
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args,  **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        company = request.POST.get('companies')
        try:
            user = User.objects.get(username=email)
            current_company = Company.objects.get(id=company)
            pers = Person.objects.get(user=user, company=current_company)
        except:
            return HttpResponseRedirect(reverse('login'))

        user = authenticate(username=email, password=password)

        if user is not None:
            user.first_name = company                   # bad, need doing differently
            user.save()
            login(request, user)

        return HttpResponseRedirect(reverse('index'))


class RegisterView(TemplateView):
    template_name = 'todo/register.html'

    def get_context_data(self, **kwargs):
        context = {}
        context['serializer'] = RegisterSerializer()
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        companies = list(request.POST.get('companies'))

        data = {"email": email, "companies": companies}
        url = "{}://{}/api-v1/register/".format(request.scheme, request.get_host())
        response = requests.post(url, data=data)
        response = response.json()
        if response:
            response['user'] = email
            return render(request, 'todo/register_complete.html', response)

        return render(request, 'todo/register.html', {})



class CompleteView(TemplateView):
    template_name = 'todo/index.html'

    def get(self, request, *args, **kwargs):
        todo = Todo.objects.get(pk=kwargs['todo_id'])
        todo.complete = True
        todo.save()
        return redirect('/')

class DecompleteView(TemplateView):
    template_name = 'todo/index.html'

    def get(self, request, *args, **kwargs):
        todo = Todo.objects.get(pk=kwargs['todo_id'])
        todo.complete = False
        todo.save()
        return redirect('/')


class DeletecompleteView(TemplateView):
    template_name = 'todo/index.html'

    def get(self, request, *args, **kwargs):
        Todo.objects.filter(complete__exact=True).delete()
        return redirect('/')

class DeleteallView(TemplateView):
    template_name = 'todo/index.html'

    def get(self, request, *args, **kwargs):
        Todo.objects.all().delete()
        return redirect('/')


class AddTodoView(TemplateView):
    template_name = 'todo/index.html'

    def get_context_data(self, **kwargs):
        print("get_context_data")
        context = {}
        context['serializer'] = TodoElementCreateSerializer()
        return context

    def get(self, request, *args, **kwargs):
        print("get ")
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):

        text = request.POST.get('text')
        print("text = " + str(text))
        return redirect('/')
