from django.contrib import admin

# Register your models here.
from .models import Project, Review, Tag


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'owner')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('project', 'value')

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Project, ProjectAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Tag, TagAdmin)