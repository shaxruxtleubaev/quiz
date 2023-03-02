from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Category(models.Model):
    title = models.CharField('Title', max_length=200)
    slug = models.SlugField('URL', unique=True)
    description = models.TextField('Description', blank=True)
    npp = models.PositiveSmallIntegerField('Sort', default=0)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        db_table = 'categories'
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ('npp', )

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

class Quiz(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Author')
    title = models.CharField('Title', max_length=200)
    slug = models.SlugField('URL', unique=False)
    description = models.TextField('Description', blank=True)
    is_public = models.BooleanField('Show on the main page', default=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Category')
    created = models.DateTimeField('Created', auto_now_add=True)
    modified = models.DateTimeField('Modified', auto_now_add=True)
    npp = models.PositiveSmallIntegerField('Sort', default=0)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        db_table = 'quiz'
        verbose_name = 'test'
        verbose_name_plural = 'tests'
        unique_together = ('slug', 'category')
        ordering = ('npp', )

    def get_absolute_url(self):
        return reverse('quiz', kwargs={'quiz_slug': self.slug, 'category_slug': self.category.slug,})

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name='Test')
    question = models.CharField('Question', max_length=200)
    full_text = models.TextField('Description of question', blank=True)
    # image = models.ImageField('Image', blank=True)

    def __str__(self):
        return f'{self.question}'

    class Meta:
        db_table = 'questions'
        verbose_name= 'question'
        verbose_name_plural = 'questions'

class Answer(models.Model):
    answer = models.CharField('Answer', max_length=200)
    is_correct = models.BooleanField('Right answer', default=False)
    comment = models.CharField('Comment to the answer', max_length=250, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Question')

    def __str__(self):
        return f'{self.answer}'

    class Meta:
        verbose_name = 'answer'
        verbose_name_plural = 'answers'