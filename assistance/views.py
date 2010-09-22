# coding: utf-8

from django.shortcuts import render_to_response
from django.template.context import RequestContext

from assistance.models import Question, QuestionTranslation
from assistance.models import Category, CategoryTranslation


def faq(request):
    questions = Question.objects.all().order_by('category', 'order')

    if len(questions) < 1:
        object_list = None
    else:
        object_list = []
        for question in questions:
            q = Question()
            c = Category()
            try:
                trans = question.translations.get(language__iexact=request.LANGUAGE_CODE)
                q.title = trans.title
                q.answer = trans.answer
                q.order = question.order
                q.created = question.created
            except QuestionTranslation.DoesNotExist:
                q = question
            try:
                trans = question.category.translations.get(language__iexact=request.LANGUAGE_CODE)
                c.label = trans.label
            except CategoryTranslation.DoesNotExist:
                c = question.category
            
            q.category = c
            object_list.append(q)

    return render_to_response('assistance/question_list.html', {
                          'object_list': object_list,},
                          context_instance=RequestContext(request))
