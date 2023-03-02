from django.contrib import admin
from django.contrib.admin import register, TabularInline
from quiz.models import Category, Quiz, Question, Answer
from adminsortable2.admin import SortableAdminMixin # This creates a list view with a drag area for each item. By dragging and dropping those items, one can resort the items in the database.


@register(Category)
class CategoryModelAdmin(SortableAdminMixin, admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    # для того чтобы поле slug было уникально решил передать параметр id в prepopulated_fields. 

@register(Quiz)
class QuizModelAdmin(SortableAdminMixin, admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    # для того чтобы поле slug было уникально решил передать параметр id в prepopulated_fields. 

class AnswerTabularInline(TabularInline):
    model = Answer

@register(Question)
class QuestionModelAdmin(admin.ModelAdmin):
    inlines = (AnswerTabularInline,) # to edit the books authored by an author on the author page. 
