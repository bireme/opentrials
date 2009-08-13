# coding: utf-8

from django.shortcuts import render_to_response

def index(request):
    username = request.user.username if request.user.is_authenticated() else None
    return render_to_response('rebrac/index.html', locals())

def user_dump(request):
    uvars = [{'k':k, 'v':v} for k, v in request.user.__dict__.items()]
    return render_to_response('rebrac/user_dump.html', locals())
