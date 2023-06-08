from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import Projeto


@login_required
def painel(request):
    projetos = Projeto.objects.all()
    return render(request, 'painel.html', {'projetos': projetos})


@login_required
def project(request):
    tipo = request.GET.get('tipo')
    return render(request, 'project.html', {'tipo': tipo})


@login_required
def pacoteedit(request):
    return render(request, 'pacoteedit.html')


@login_required
def pacoteview(request):
    return render(request, 'pacoteview.html')


@login_required
def newprojectrecet(request):
    if request.method == 'GET':
        return render(request, 'newprojectrecet.html')
    else:
        inputTitulo = request.POST.get('inputTitulo', '')
        inputResp = request.POST.get('inputResp', '')
        descricao = request.POST.get('descricao', '')
        inputTipo = request.POST.get('inputTipo', '')
        inputEtiqueta = request.POST.get('inputEtiqueta', '')

        if inputTitulo == '' or inputResp == '' or descricao == '' or inputTipo == '' or inputEtiqueta == '':
            messages.add_message(request, messages.ERROR,
                                 'Todos os campos são obrigatórios')
            return redirect(reverse('newprojectrecet'))
        projeto = Projeto(titulo=inputTitulo, tipo=inputTipo,
                          responsavel=inputResp, descricao=descricao, etiqueta=inputEtiqueta)
        projeto.save()
        messages.add_message(request, messages.SUCCESS,
                             'Projeto cadastrado com sucesso')
        return redirect(reverse('painel'))
