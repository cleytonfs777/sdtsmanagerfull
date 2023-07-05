from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from utils.tratamentos import removereais, trataelementoitem

from .models import (Cronograma, DotacaoOrcamentaria, EquipamentoServico,
                     ObservacaoPendencia, PacoteAquisicao,
                     PacoteAquisicaoEquipamentoServico, PacoteEmpenho, Projeto,
                     Tasks_Cronograma)


@login_required
def painel(request):
    projetos = Projeto.objects.all()
    return render(request, 'painel.html', {'projetos': projetos})


@login_required
def project(request, id_project):
    tipo = request.GET.get('tipo')
    projeto = Projeto.objects.get(id=id_project)
    pacotes_aquisicao = projeto.pacote_aquisicao.all()
    context = {
        'tipo': tipo,
        'projeto': projeto,
        'pacotes_aquisicao': pacotes_aquisicao,
    }
    return render(request, 'project.html', context)


@login_required
def pacoteedit(request, id_pacote):
    if request.method == 'POST':
        ...
    else:
        all_equipamentos = EquipamentoServico.objects.all()
        pacote = PacoteAquisicao.objects.get(id=id_pacote)
        return render(request, 'pacoteedit.html', {'pacote': pacote, 'id_pacote': id_pacote, 'all_equipamentos': all_equipamentos})


@login_required
def deleteequip(request, id_element):
    if request.method == 'POST':
        equipamento_exclude = PacoteAquisicaoEquipamentoServico.objects.get(
            id=id_element)
        try:
            equipamento_exclude.delete()
            messages.add_message(request, messages.SUCCESS,
                                 'Equipamento deletado com sucesso')
            return redirect(reverse('pacoteedit', kwargs={'id_pacote': equipamento_exclude.pacotedespesa.id}))
        except Exception as e:
            messages.add_message(request, messages.ERROR,
                                 f'Erro ao deletar equipamento: {e}')
            return redirect(reverse('pacoteedit', kwargs={'id_pacote': equipamento_exclude.pacotedespesa.id}))
    else:
        return HttpResponse(f"Você não tem autorização para acessar essa pagina: {e}", status=401)


@login_required
def allservpack(request, id_element):
    if request.method == 'POST':
        # Serão recebidos diversos elementos do equipamento. Deve se pegar o id e buscar pelo equipamento. Após isso deve se comparar cada elemento do recebido com o do equipamento no banco de dados. Caso haja alguma diferença, deve se atualizar o equipamento no banco de dados.

        # Receber os valores do formulário
        id_equip, classe, natureza, valor_portal = request.POST.get(
            'modalEquipList', '').split('-')

        entrega_instalacao = request.POST.get('modalequipEntrInst', '')
        destino = request.POST.get('modalequipDest', '')  # Local de destino
        valor_1 = request.POST.get('modalequipValor1', '')  # Valor 1
        valor_2 = request.POST.get('modalequipValor2', '')  # Valor 2
        valor_3 = request.POST.get('modalequipValor3', '')  # Valor 3
        valor_medio = request.POST.get(
            'modalequipValorMedio', '')  # Valor médio

        usar_valueportal = request.POST.get(
            'modalequipValorUnit', '')  # Usar valor do portal
        quantidade = request.POST.get('modalequipQtd', '')  # Quantidade
        data_entrega = request.POST.get(
            'modalequipDataEnt', '')  # Data de entrega
        data_instalacao = request.POST.get(
            'modalequipDataInst', '')  # Data de instalação
        observacoes = request.POST.get('modalequipObs', '')  # Observações

        # Pegar a instancia do equipamento com id igual a id_element
        try:
            equipamento_select = PacoteAquisicaoEquipamentoServico.objects.get(
                id=id_element)
        except:
            return HttpResponse("Erro ao encontrar o equipamento")

        # Comparar os valores recebidos com os valores do equipamento no banco de dados
        if equipamento_select.equipamento.id != id_equip:
            equip_new = EquipamentoServico.objects.get(id=id_equip)
            equipamento_select.equipamento = equip_new

        if equipamento_select.entrega_instalacao != entrega_instalacao:
            equipamento_select.entrega_instalacao = entrega_instalacao

        if equipamento_select.destino != destino:
            equipamento_select.destino = destino

        if equipamento_select.valor_1 != removereais(valor_1):
            equipamento_select.valor_1 = removereais(valor_1)

        if equipamento_select.valor_2 != removereais(valor_2):
            equipamento_select.valor_2 = removereais(valor_2)

        if equipamento_select.valor_3 != removereais(valor_3):
            equipamento_select.valor_3 = removereais(valor_3)

        if equipamento_select.valor_medio != removereais(valor_medio):
            equipamento_select.valor_medio = removereais(valor_medio)

        if equipamento_select.usa_preco_portal != usar_valueportal:
            equipamento_select.usa_preco_portal = True if usar_valueportal == 'on' else False

        if equipamento_select.quantidade != quantidade:
            equipamento_select.quantidade = quantidade

        if equipamento_select.data_entrega != data_entrega:
            equipamento_select.data_entrega = data_entrega

        if equipamento_select.data_instalacao != data_instalacao:
            equipamento_select.data_instalacao = data_instalacao

        if equipamento_select.observacoes != observacoes:
            equipamento_select.observacoes = observacoes

        # Salvar o equipamento_select no banco de dados se der algum erro retorna para a pagina com mensagem de erro
        try:
            equipamento_select.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Equipamento atualizado com sucesso')
            return redirect(reverse('pacoteedit', kwargs={'id_pacote': equipamento_select.pacotedespesa.id}))

        except Exception as e:
            print(e)
            messages.add_message(request, messages.ERROR,
                                 'Erro ao atualizar equipamento')
            return redirect(reverse('pacoteedit', kwargs={'id_pacote': equipamento_select.pacotedespesa.id}))


@login_required
def pacoteview(request, id_pacote):
    pacote = PacoteAquisicao.objects.get(id=id_pacote)
    # Colocar na variavel 'equiamentos' todos os equipamentos relacionados ao pacote
    equipamentos = pacote.despesa_equipamento.all()
    # Coloca na variavel 'cronograma' todos os cronogramas relacionados ao pacote
    cronogramas = pacote.cronogramas.all()
    # Colocar na variavel 'obspen' todas as observações e pendencias relacionadas ao pacote
    obspens = pacote.observacoes_pendencias.all()

    return render(request, 'pacoteview.html', {'pacote': pacote, 'equipamentos': equipamentos, 'cronogramas': cronogramas, 'obspens': obspens})


@login_required
def newprojectrecet(request):
    if request.method == 'GET':
        return render(request, 'newprojectrecet.html')
    else:
        inputTitulo = request.POST.get('inputTitulo', '')
        inputResp = request.POST.get('inputResp', '')
        descricao = request.POST.get('descricao', '')
        inputEtiqueta = request.POST.get('inputEtiqueta', '')

        if inputTitulo == '' or inputResp == '' or descricao == '' or inputEtiqueta == '':
            messages.add_message(request, messages.ERROR,
                                 'Todos os campos são obrigatórios')
            return redirect(reverse('newprojectrecet'))
        projeto = Projeto(titulo=inputTitulo, responsavel=inputResp,
                          descricao=descricao, etiqueta=inputEtiqueta)
        projeto.save()
        messages.add_message(request, messages.SUCCESS,
                             'Projeto cadastrado com sucesso')
        return redirect(reverse('painel'))


@login_required
def newpackageaqu(request, id_project):
    # Injeta na pagina o titulo do projeto
    name_projet = Projeto.objects.get(id=id_project)
    equipamentos = EquipamentoServico.objects.all()
    return render(request, 'newpackageaqu.html', {'id_project': id_project, 'equipamentos': equipamentos, 'name_project': name_projet})


@login_required
def createequipserv(request, id_project):
    if request.method == 'POST':
        titleItem = request.POST.get('titleItem', '')
        especItem = request.POST.get('especItem', '')
        rpCode = request.POST.get('rpCode', '')
        itemCode = request.POST.get('itemCode', '')
        elItem = trataelementoitem(
            request.POST.get('elItem', ''))  # Tratamento
        classItem = request.POST.get('classItem', '')
        valPortItem = removereais(request.POST.get('valPortItem', 0))
        categoryItem = request.POST.get('categoryItem', '')
        sitItem = request.POST.get('sitItem', '')

        if titleItem == '' or especItem == '' or elItem == '' or classItem == '' or sitItem == '':
            messages.add_message(request, messages.ERROR,
                                 'Todos os campos são obrigatórios')
            return redirect(reverse('newpackageaqu', kwargs={'id_project': id_project}))

        EquipamentoServico.objects.create(
            titulo=titleItem,
            especificacao=especItem,
            natureza=categoryItem,
            registro_preco=rpCode,
            codigo_item=itemCode,
            elemento_item=elItem,
            classe=classItem,
            valor_portal=valPortItem,
            situacao=sitItem

        )
        messages.add_message(request, messages.SUCCESS,
                             'Equipamento cadastrado com sucesso')
        return redirect(reverse('newpackageaqu', kwargs={'id_project': id_project}))


@login_required
def createfullequip(request, id_pacote):
    if request.method == 'POST':

        # Receber os valores do formulário
        id_equip = request.POST.get('modalEquipFullListHidden', '')
        print(f"id_equip: {id_equip} \n")
        # consumo ou permanente
        classe = request.POST.get('modalequipFullClasseHidden', '')
        local = request.POST.get('modalequipFullLocal', '')
        # material, serviço ou material/serviçomodalequipFullValorMedio
        natureza = request.POST.get('modalequipFullNaturezaHidden', '')
        # Demanda, Licitacao e etc...
        entrega_instalacao = request.POST.get('modalequipFullEntrInst', '')
        destino = request.POST.get(
            'modalequipFullDest', '')  # Local de destino
        valor_1 = request.POST.get('modalequipFullValor1', '')  # Valor 1
        valor_2 = request.POST.get('modalequipFullValor2', '')  # Valor 2
        valor_3 = request.POST.get('modalequipFullValor3', '')  # Valor 3
        valor_medio = request.POST.get(
            'modalequipFullValorMedio', '')  # Valor médio
        valor_portal = request.POST.get(
            'modalequipFullPrecoPortal', '')  # Valor do portal
        usar_valueportal = request.POST.get(
            'modalequipFullValorUnit', '')  # Usar valor do portal
        usar_valueportal = True if usar_valueportal == 'on' else False
        quantidade = request.POST.get('modalequipFullQtd', '')  # Quantidade
        data_entrega = request.POST.get(
            'modalequipFullDataEnt', '')  # Data de entrega
        data_instalacao = request.POST.get(
            'modalequipFullDataInst', '')  # Data de instalação
        observacoes = request.POST.get('modalequipFullObs', '')  # Observações

        # Cria um novo objeto do tipo PacoteAquisicaoEquipamentoServico
        try:
            new_equipamento = PacoteAquisicaoEquipamentoServico.objects.create(
                pacotedespesa=PacoteAquisicao.objects.get(id=id_pacote),
                equipamento=EquipamentoServico.objects.get(id=id_equip),
                entrega_instalacao=entrega_instalacao,
                destino=destino,
                valor_1=removereais(valor_1),
                valor_2=removereais(valor_2),
                valor_3=removereais(valor_3),
                valor_medio=removereais(valor_medio),
                usa_preco_portal=usar_valueportal,
                quantidade=quantidade,
                data_entrega=data_entrega,
                data_instalacao=data_instalacao,
                observacoes=observacoes,
                local=local,
            )
            messages.add_message(request, messages.SUCCESS,
                                 'Equipamento cadastrado com sucesso')
            return redirect(reverse('pacoteedit', kwargs={'id_pacote': id_pacote}))
        except Exception as e:
            messages.add_message(request, messages.ERROR,
                                 f'Erro ao cadastrar equipamento: {e}')
            return redirect(reverse('pacoteedit', kwargs={'id_pacote': id_pacote}))


@login_required
def createequipserv_edit(request, id_pacote):
    if request.method == 'POST':
        titleItem = request.POST.get('titleItem', '')
        especItem = request.POST.get('especItem', '')
        rpCode = request.POST.get('rpCode', '')
        itemCode = request.POST.get('itemCode', '')
        elItem = trataelementoitem(
            request.POST.get('elItem', ''))  # Tratamento
        classItem = request.POST.get('classItem', '')
        valPortItem = removereais(request.POST.get('valPortItem', 0))
        categoryItem = request.POST.get('categoryItem', '')
        sitItem = request.POST.get('sitItem', '')

        if titleItem == '' or especItem == '' or elItem == '' or classItem == '' or sitItem == '':
            messages.add_message(request, messages.ERROR,
                                 'Todos os campos são obrigatórios')
            return redirect(reverse('pacoteedit', kwargs={'id_pacote': id_pacote}))

        EquipamentoServico.objects.create(
            titulo=titleItem,
            especificacao=especItem,
            natureza=categoryItem,
            registro_preco=rpCode,
            codigo_item=itemCode,
            elemento_item=elItem,
            classe=classItem,
            valor_portal=valPortItem,
            situacao=sitItem

        )
        messages.add_message(request, messages.SUCCESS,
                             'Equipamento cadastrado com sucesso')
        return redirect(reverse('pacoteedit', kwargs={'id_pacote': id_pacote}))


@login_required
def createpackage(request, id_project):
    if request.method == 'POST':
        try:
            # Caso de algum erro ele reverte todas as operações
            with transaction.atomic():
                # recupera o titulo
                titulo = request.POST.get('inputTitlePacote', '')
                # status representa a 'fase' o model
                status = request.POST.get('selectStatusNew', '')
                # fase representa o 'esp_fase' do model
                if status == 'RP':
                    fase = request.POST.get('selectnewrp', '')
                elif status == 'PG':
                    fase = request.POST.get('selectnewpg', '')
                else:
                    fase = 'terceiros'
                etiqueta = request.POST.get('selectEtiquetaNew', '')
                natureza = request.POST.get('selectNaturezaNew', '')
                contrato = request.POST.get('inputContratoNew', '')
                datainit = request.POST.get('dateInitialInput', '')
                dataend = request.POST.get('dateFinalInput', '')
                sei = request.POST.get('hiddensei', '')

                # Tratamento de valores e salvar no banco de dados
                # 1 - Criar um pacote de despesas
                pacote_despesa = PacoteAquisicao(
                    projeto_id=id_project,
                    titulo=titulo,
                    status=status,
                    fase=fase,
                    etiqueta=etiqueta,
                    natureza=natureza,
                    contrato=contrato,
                    contratoinit=datainit,
                    contratoend=dataend,
                    doc_ref=sei
                )
                pacote_despesa.save()
                # 2 - Criar equipamentos vinculados a esse pacote de despesas
                # realizar tratamento de equipamento ou serviço
                equipservice = request.POST.get('hiddenequipser', '')
                elem_equipeservice = equipservice.split(';')
                # Retornar o id do pacote de despesa
                for item in elem_equipeservice:
                    if not item:
                        continue
                    each_item = item.split('|')
                    id_equip = each_item[1]
                    status_equip = each_item[4]
                    price1_equip = each_item[5]
                    price2_equip = each_item[6]
                    price3_equip = each_item[7]
                    pricemedia_equip = each_item[8]
                    usar_valueportal = each_item[9].title()
                    qtd_equip = each_item[11]
                    local_equip = each_item[13]
                    dataentrega_equip = each_item[14]
                    datainst_equip = each_item[15]
                    obs_equip = each_item[16]
                    destino_equip = each_item[17]
                    print(f"id_equip: {id_equip} \n")
                    print(f"status_equip: {status_equip} \n")
                    print(f"price1_equip: {price1_equip} \n")
                    print(f"price2_equip: {price2_equip} \n")
                    print(f"price3_equip: {price3_equip} \n")
                    print(f"pricemedia_equip: {pricemedia_equip} \n")
                    print(f"usar_valueportal: {usar_valueportal} \n")
                    print(f"qtd_equip: {qtd_equip} \n")
                    print(f"local_equip: {local_equip} \n")
                    print(f"dataentrega_equip: {dataentrega_equip} \n")
                    print(f"datainst_equip: {datainst_equip} \n")
                    print(f"obs_equip: {obs_equip} \n")
                    print(f"destino_equip: {destino_equip} \n")
                    # Pegar as instancias das foreing keys
                    pacote_despesa = PacoteAquisicao.objects.get(
                        id=pacote_despesa.id)
                    equipamento_desp = EquipamentoServico.objects.get(
                        id=id_equip
                    )
                    # Realizar o cadastro de cada equipamento
                    pacote_desp_equip_serv = PacoteAquisicaoEquipamentoServico(
                        pacotedespesa=pacote_despesa,
                        equipamento=equipamento_desp,
                        entrega_instalacao=status_equip,
                        valor_1=removereais(price1_equip),
                        valor_2=removereais(price2_equip),
                        valor_3=removereais(price3_equip),
                        valor_medio=removereais(pricemedia_equip),
                        usa_preco_portal=usar_valueportal,
                        quantidade=qtd_equip,
                        local=local_equip,
                        data_entrega=dataentrega_equip,
                        data_instalacao=datainst_equip,
                        observacoes=obs_equip,
                        destino=destino_equip
                    )
                    pacote_desp_equip_serv.save()

                # 3 - Criar cronograma vinculado a esse pacote de despesas
                titlecron = request.POST.get('inputTitleCron', '')
                descron = request.POST.get('desCron', '')
                obscron = request.POST.get('obsCron', '')
                cronograma = Cronograma(
                    pacote_despesa=pacote_despesa,
                    titulo=titlecron,
                    descricao=descron,
                    observacoes=obscron
                )
                cronograma.save()
                # tratar para criar tasks
                cronograma_receiv = request.POST.get('hiddentasks', '')
                cronograma_tasks = cronograma_receiv.split(';')
                for task in cronograma_tasks:
                    if not task:
                        continue
                    each_task = task.split('|')
                    title_task = each_task[0]
                    desc_task = each_task[1]
                    status_task = each_task[2]
                    prioridade_task = each_task[3]
                    dataini_task = each_task[4]
                    dataend_task = each_task[5]
                    datarini_task = each_task[8]
                    datarend_task = each_task[9]
                    obs_task = each_task[11]
                    print(f"each_task: {each_task} \n")
                    print(f"title_task: {title_task} \n")
                    print(f"desc_task: {desc_task} \n")
                    print(f"status_task: {status_task} \n")
                    print(f"prioridade_task: {prioridade_task} \n")
                    print(f"dataini_task: {dataini_task} \n")
                    print(f"dataend_task: {dataend_task} \n")
                    print(f"datarini_task: {datarini_task} \n")
                    print(f"datarend_task: {datarend_task} \n")
                    print(f"obs_task: {obs_task} \n")
                    # Realizar o cadastro de cada task
                    task_cronograma = Tasks_Cronograma(
                        cronograma=cronograma,
                        titulo=title_task,
                        descricao=desc_task,
                        status=status_task,
                        prioridade=prioridade_task,
                        data_inicio_planejada=dataini_task,
                        data_fim_planejada=dataend_task,
                        data_inicio_real=datarini_task,
                        data_fim_real=datarend_task,
                        observacoes=obs_task
                    )
                    task_cronograma.save()

                # 4 - Criar observaçoes e pendencias vinculadas a esse pacote de despesas
                obserpendencia = request.POST.get('hiddenobspend', '')
                obspendencia = obserpendencia.split(';')
                for obs in obspendencia:
                    if not obs:
                        continue
                    each_obs = obs.split('|')
                    obspendencia = each_obs[0]
                    statuspendencia = each_obs[1]
                    datapendencia = each_obs[2]
                    print(f"each_obs: {each_obs} \n")
                    print(f"obspendencia: {obspendencia} \n")
                    print(f"statuspendencia: {statuspendencia} \n")
                    print(f"datapendencia: {datapendencia} \n")
                    # Realizar o cadastro de cada pendencia
                    obs_pendencia = ObservacaoPendencia(
                        pacote_despesa=pacote_despesa,
                        decricao=obspendencia,
                        categoria=statuspendencia,
                        data_obs_pend=datapendencia,
                        class_obs_pend='aconcluir'
                    )
                    obs_pendencia.save()

                messages.add_message(request, messages.SUCCESS,
                                     'Criação de pacote de despesa realizada com sucesso')
                return redirect(reverse('painel'))

        except Exception as e:
            print(e)
            messages.add_message(request, messages.ERROR,
                                 'Erro ao criar pacote de despesa')
            return redirect(reverse('painel'))

    else:
        return HttpResponse(f"Você não tem autorização para acessar essa pagina: {e}", status=401)
