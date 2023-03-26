
from django.shortcuts import render, get_object_or_404
from quiz.models import Category, Quiz, Question, Answer
from django.utils.safestring import SafeString # Marking something as a "safe string" means that the producer of the string has already turned characters that should not be interpreted by the HTML engine (e.g. '<') into the appropriate entities.
from src.settings import MEDIA_URL
from django.db.models import Count, Q
from django.views.generic import ListView



def index_view(request):
    categories = Category.objects.all()

    context = {
        'title': 'Main page',
        'categories': categories
    }
    return render(request, 'quiz/index.html', context=context)

def category_view(request, category_slug):
    categories = Category.objects.all()
    category = get_object_or_404(Category, slug=category_slug)
    quizs = Quiz.objects.filter(category=category, is_public=True,)

    context = {
        'title': f'Tests about {category.title}',
        'category': category,
        'quizs': quizs,
        'categories': categories
    }

    return render(request, 'quiz/category.html', context=context)

def quiz_view(request, category_slug, quiz_slug):
    quiz = get_object_or_404(Quiz, slug=quiz_slug, category__slug=category_slug)
    questions = quiz.question_set.all().prefetch_related('answer_set') #Returns a QuerySet that will automatically retrieve, in a single batch, related objects for each of the specified lookups.

    quiz_data = {'questions': []}

    for question in questions:
        _question = question.question

        question_data = {
            'q': _question,
            'a': '',
            'options': []
        }

        for answer in question.answer_set.all():
            if answer.is_correct:
                question_data['a'] = answer.answer
            question_data['options'].append(answer.answer)

        quiz_data['questions'].append(question_data)

    context = {
        'title': quiz.title,
        'quiz_data': SafeString(quiz_data),
    }

    return render(request, 'quiz/quiz.html', context)

class SearchResultView(ListView):
    model = Category
    template_name = 'quiz/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Category.objects.filter(
            Q(title__icontains=query) | Q(slug__icontains=query)
        )
        return object_list