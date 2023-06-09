from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import PacoteDespesa, PacoteReceita, Projeto


@login_required
def painel(request):
    projetos = Projeto.objects.all()
    return render(request, 'painel.html', {'projetos': projetos})


@login_required
def project(request, id_project):
    tipo = request.GET.get('tipo')
    projeto = get_object_or_404(Projeto, pk=id_project)
    pacotes_despesa = PacoteDespesa.objects.filter(projeto=id_project)
    pacotes_receita = PacoteReceita.objects.filter(projeto=id_project)
    context = {
        'tipo': tipo,
        'projeto': projeto,
        'pacotes_despesa': pacotes_despesa,
        'pacotes_receita': pacotes_receita,
    }
    return render(request, 'project.html', context)


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


@login_required
def newpackagedesp(request, id_project):
    if request.method == 'GET':

        return render(request, 'newpackagedesp.html', {'id_project': id_project})
