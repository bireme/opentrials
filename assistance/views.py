# coding: utf-8

from django.shortcuts import render_to_response
from django.template.context import RequestContext

from assistance.models import Question, QuestionTranslation
from assistance.models import Category, CategoryTranslation


def faq(request):
    """
    ATTENTION: This view has a complexity of O(question * N * 2) on database load, because each
    question does 1 or 2 calls to database to get question and category translations.

    It is prepared to get questions including category fields at once SQL call and using cache
    to get translations as far as possible.

    If the questions quantity grow a lot, this logic should be replaced to something that gets
    all translations from database at once.
    """
    questions = Question.objects.select_related('category').order_by('category', 'order')

    if len(questions) < 1:
        object_list = None
    else:
        object_list = []
        for question in questions:
            q = Question()
            c = Category()
            try:
                #trans = question.translations.get(language__iexact=request.LANGUAGE_CODE)
                trans = QuestionTranslation.objects.get_translation_for_object(request.LANGUAGE_CODE, question)
                q.title = trans.title
                q.answer = trans.answer
                q.order = question.order
                q.created = question.created
            except QuestionTranslation.DoesNotExist:
                q = question
            try:
                #trans = question.category.translations.get(language__iexact=request.LANGUAGE_CODE)
                trans = CategoryTranslation.objects.get_translation_for_object(request.LANGUAGE_CODE, question.category)
                c.label = trans.label
            except CategoryTranslation.DoesNotExist:
                c = question.category
            
            q.category = c
            object_list.append(q)

    return render_to_response('assistance/question_list.html', {
                          'object_list': object_list,},
                          context_instance=RequestContext(request))
