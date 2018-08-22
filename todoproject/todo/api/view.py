from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated

from rest_framework import viewsets
from .serializers import TodoListSerializer

from ..models import (
    Todo,
    Company,
    Person
)

import string, random


# Create your views here.
class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return Response(data={'status': True, 'password': password, 'email': email})
        else:
            return Response(data={'status': False, 'error': "error email or password"})


class LogoutAPIView(APIView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class RegisterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        companies = list(request.POST.get('companies'))
        text = self.create_profiles(email, companies)
        return Response(data= text)

    def create_profiles(self, email, companies):
        context = {}
        password = ''.join(random.choice(string.ascii_lowercase) for x in range(8))
        try:
            user = User.objects.get(username=email)
        except ObjectDoesNotExist:
            user = User.objects.create_user(username=email, password=password, email=email)

        for company in companies:
            company_obj = Company.objects.get(pk=company)
            try:
                profile = Person.objects.get(user=user)
                if company != profile.company:
                    profile.company.add(company_obj)
                    profile.save()
            except:
                profile = Person.objects.create(user=user, password=password)
                profile.company.add(company_obj)
                profile.save()

            context["password"] = password
            context["company"] = company_obj.company_name
        return context


class TodoListViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TodoListSerializer

    def get_queryset(self):
        current_company = Company.objects.get(pk=self.request.user.first_name) # bad idea
        queryset = Todo.objects.filter(company=current_company).all().values()
        return queryset

