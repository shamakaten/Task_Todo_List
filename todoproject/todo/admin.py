from django.contrib import admin

# Register your models here.
from . import models

class PersonListAdmin(admin.ModelAdmin):
	list_display = ("user","password", "get_company")

class TodoListAdmin(admin.ModelAdmin):
	list_display = ("text",  "complete", "company")

class CompanyAdmin(admin.ModelAdmin):
	list_display = ("company_name",)



admin.site.register(models.Todo, TodoListAdmin)
admin.site.register(models.Person, PersonListAdmin)
admin.site.register(models.Company, CompanyAdmin)
