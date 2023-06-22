const refreshitem = document.querySelectorAll(".changeble-item");

refreshitem.forEach((item) => {
  item.addEventListener("change", () => {
    alert("Mudou");
  });
});


document.getElementById('formAddTask').addEventListener('submit', function(e) {
  // Impedir o envio do formulário
  e.preventDefault();

  // Recuperar os dados de todos os campos do formulario
  titulotask = document.querySelector("#titleTask").value;
  desctask = document.querySelector("#descTask").value;
  statustask = document.querySelector("#statusTask").value;
  priortask = document.querySelector("#priorTask").value;
  initplantask = document.querySelector("#initPlanTask").value;
  endplantask = document.querySelector("#endPlanTask").value;
  initrealtask = document.querySelector("#initRealTask").value;
  endrealtask = document.querySelector("#endRealTask").value;
  obstask = document.querySelector("#obsTask").value;

  dataInicial = initrealtask ? initrealtask : initplantask;
  dataFinal = endrealtask ? endrealtask : endplantask;

  // cria uma tr a ser inserida dentro do tbody da tabela de id = listTaskTable
  const tbodytask = document.getElementById("listTaskTable").getElementsByTagName("tbody")[0];
  const rowtask = tbodytask.insertRow();
  rowtask.innerHTML = `
  <td  class="rot-info rot-sm">${titulotask}</td>
  <td  class="rot-info rot-sm ocultar">${desctask}</td>
  <td  class="rot-info rot-sm">${statustask}</td>
  <td  class="rot-info rot-sm">${priortask}</td>
  <td  class="rot-info rot-sm ocultar">${initplantask}</td>
  <td  class="rot-info rot-sm ocultar">${endplantask}</td>
  <td  class="rot-info rot-sm ocultar">${initrealtask}</td>
  <td  class="rot-info rot-sm ocultar">${endrealtask}</td>
  <td  class="rot-info rot-sm">${dataInicial}</td>
  <td  class="rot-info rot-sm">${dataFinal}</td>
  <td  class="rot-info rot-sm">${calcularDiferencaDias(dataInicial, dataFinal)}</td>
  <td  class="rot-info rot-sm ocultar">${obstask}</td>
  <td><button type="button" class="btn btn-danger btn-sm" onclick="removeRow(this)"><i class="ri-delete-bin-6-line"></i></button></td>`;

  // Fecha o modal após o processamento do formulário
  var myModal = bootstrap.Modal.getInstance(document.getElementById('modalAddTask'));
  myModal.hide();

});



window.addEventListener('load', function() {
  document.getElementById('form-etapas').reset();
});


document.addEventListener('DOMContentLoaded', function() {
  var selectCategoria = document.getElementById('selectCategoria');
  var selectEquip = document.getElementById('selectEquip');


  selectCategoria.addEventListener('change', function(){
    // Limpa as opções existentes
    selectEquip.innerHTML = '';

    // Adiciona a opção "disabled" no início
    var defaultOption = document.createElement('option');
    defaultOption.setAttribute('selected', '');
    defaultOption.setAttribute('disabled', '');
    defaultOption.innerText = 'Escolha o equipamento/serviço';
    selectEquip.appendChild(defaultOption);

    // Adiciona as opções correspondentes ao tipo selecionado
    {% for equipamento in equipamentos %}
      if ('{{equipamento.tipo}}' == selectCategoria.value) {
        var option = document.createElement('option');
        option.value = "{{equipamento.id}}-{{equipamento.classe}}";
        option.innerText = "{{equipamento.titulo}}";
        selectEquip.appendChild(option);
      }
    {% endfor %}
  });

  selectEquip.addEventListener('change', function(){
    var equipamentoIdClasse = this.value.split('-');
    var equipamentoId = equipamentoIdClasse[0];

    {% for equipamento in equipamentos %}
      if ("{{equipamento.id}}" == equipamentoId) {
        document.getElementById('equipamentoValorPortal').innerText = 'Valor: R$ ' + '{{equipamento.valor_portal}}';
        return;
      }
    {% endfor %}
  });
});
document.addEventListener("DOMContentLoaded", function () {
  var etapas = Array.from(
    document.querySelectorAll("#form-etapas .form-etapa")
  );
  var count = etapas.length;
  var current = 0;

  var btnsNext = Array.from(document.querySelectorAll(".btn-next"));
  var btnsPrev = Array.from(document.querySelectorAll(".btn-prev"));

  // Ao carregar a página, verifique se há uma etapa armazenada em sessionStorage
  var savedStep = sessionStorage.getItem('currentStep');
  if (savedStep) {
    // Se houver, use-o como a etapa atual e exiba a etapa correta
    current = parseInt(savedStep, 10);
    etapas.forEach((etapa, index) => {
      if (index === current) {
        etapa.classList.add("ativo");
      } else {
        etapa.classList.remove("ativo");
      }
    });
  }

  btnsNext.forEach((btn) => {
    btn.addEventListener("click", function () {
      if (current < count - 1) {
        etapas[current].classList.remove("ativo");
        current++;
        // Quando o usuário avança, salve a etapa atual em sessionStorage
        sessionStorage.setItem('currentStep', current);
        etapas[current].classList.add("ativo");
      }
    });
  });

  btnsPrev.forEach((btn) => {
    btn.addEventListener("click", function () {
      if (current > 0) {
        etapas[current].classList.remove("ativo");
        current--;
        // Quando o usuário retrocede, salve a etapa atual em sessionStorage
        sessionStorage.setItem('currentStep', current);
        etapas[current].classList.add("ativo");
      }
    });
  });

  // Ajusta display para RP, PG e Terceiros
  const statusSelect = document.querySelector(".form-select");
  const rpSelect = document.getElementById("selectnewrp");
  const pgSelect = document.getElementById("selectPgNew");
  const terceirosElement = document.getElementById("Terceiros");

  // inicia ambos selects ocultos
  rpSelect.style.display = "none";
  pgSelect.style.display = "none";

  statusSelect.addEventListener("change", function () {
    // esconde ambos selects
    rpSelect.style.display = "none";
    pgSelect.style.display = "none";
    terceirosElement.style.display = "block"; // mostra "Terceiros"

    if (this.value === "RP") {
      rpSelect.style.display = "block";
      terceirosElement.style.display = "none"; // oculta "Terceiros"
    } else if (this.value === "PG") {
      pgSelect.style.display = "block";
      terceirosElement.style.display = "none"; // oculta "Terceiros"
    }
  });
});
document
  .getElementById("button-addon1-new")
  .addEventListener("click", function () {
    const inputText = document.getElementById("inputText-new");
    const listContainer = document.getElementById("listContainer-new");

    // Verifica se o texto já existe na lista
    if (!listContainer.innerHTML.includes(inputText.value)) {
      // Cria um novo item da lista
      const newItem = document.createElement("div");
      newItem.classList.add(
        "d-flex",
        "flex-row",
        "justify-content-between",
        "w-100",
        "align-items-center",
        "mb-1"
      );
      newItem.innerHTML = `<p class="labelsei">${inputText.value}</p> <button class="btn btn-danger btn-sm me-2" onclick="removeItem(event)">X</button>`;

      // Adiciona o novo item à lista
      listContainer.appendChild(newItem);
    }

    // Limpa o campo de entrada
    inputText.value = "";
  });

function removeItem(event) {
  const item = event.target.parentNode;
  item.parentNode.removeChild(item);
}
// Função que será chamada sempre que um elemento for adicionado ou removido de "maincontent"
// Seleciona o nó que será observado
const targetNode = document.getElementById("listContainer-new");

// Cria uma instância de observer
const observer = new MutationObserver((mutationsList, observer) => {
  // Itera sobre todas as mutações que acabaram de ocorrer
  for (let mutation of mutationsList) {
    // Se o `mutation.type` for `childList`, adiciona o conteúdo do elemento p ao input hidden
    if (mutation.type === "childList") {
      let textValues = "";
      let childDivs = targetNode.children;
      for (let i = 0; i < childDivs.length; i++) {
        // Acessa o conteúdo do elemento p dentro da div
        let pContent =
          childDivs[i].getElementsByTagName("p")[0].textContent;
        textValues += pContent + ";";
      }

      // Remove o último ';'
      textValues = textValues.slice(0, -1);

      // Armazena os valores no input hidden
      document.getElementById("hiddensei").value = textValues;
    }
  }
});

// Configuração do observer: quais mutações serão observadas
const config = { attributes: false, childList: true, subtree: false };
// Inicia a observação do nó configurado
observer.observe(targetNode, config);


function insereRowTable(){

  // Pega o value e o texto do select com id selectEquip
  const selectEquip = document.querySelector("#selectEquip");
  const inputQtd = document.getElementById("inputQtnew").value;
  console.log(inputQtd)
  if (selectEquip.value == "Escolha o equipamento/serviço") {
    alert("A opção SELECIONAR não pode ficar vazia");
    return;
  }else if (inputQtd == undefined || inputQtd == "") {
    alert("A opção QUANTIDADE não pode ficar vazia");
    return;
  }
  // Fazer split no value pela caractere '-' e salvar em id e classe
  const id = selectEquip.value.split("-")[0] ==  "Escolha o equipamento" ? "" : selectEquip.value.split("-")[0];
  const classe = selectEquip.value.split("-")[1] == undefined ? "" : selectEquip.value.split("-")[1];
  const text = selectEquip.options[selectEquip.selectedIndex].text;
  // Pega o texto do option selecionado
  // Pega a categoria
  const selectCategoria = document.querySelector("#selectCategoria").value;
  // Pega LOCAL, DESTINO e QUANTIDADE
  const inputLoc = document.getElementById("inputLocnew").value;
  const inputDest = document.getElementById("inputDestnew").value;

  // Pega VALORES
  const val1Item = document.getElementById("val1Item").value;
  const val2Item = document.getElementById("val2Item").value
  const val3Item = document.getElementById("val3Item").value
  const valMedItem = document.getElementById("valMedItem").value
  const bolPortItem = document.querySelector("#flexSwitchCheckDefault").value == 'on' ? true : false
  const ValPortITem = document.querySelector("#equipamentoValorPortal").textContent
  valPortItem = ValPortITem.replace('Valor:', '')
  console.log(`Valor Portal: ${valPortItem}`)
  const puroValItem = valPortItem.replace('R$ ', '').replace('.', '').replace(',', '.')
  const valtotal = `R$ ${puroValItem * inputQtd}`
  // Pega STATUS e CONTRATO
  const statusItem = document.getElementById("statusItem").value
  // Pega DATAS
  const dateEntEquip = document.getElementById("dateEntEquip").value
  const dateInsEquip = document.getElementById("dateInsEquip").value
  // Pega OBSERVAÇÕES
  const obsItem = document.getElementById("obsItem").value
  // Pega o tbody da tabela de id = main-table, cria uma row, insere cada um dos valores acima em sua respectiva coluna, insere dentro do tbody e limpa todos os campos
  const tbody = document.getElementById("main-table").getElementsByTagName("tbody")[0];
  const row = tbody.insertRow();
  row.innerHTML = `
  <td  class="rot-info rot-sm">${text}</td>
  <td  class="rot-info rot-sm ocultar">${id}</td>
  <td  class="rot-info rot-sm">${classe}</td>
  <td  class="rot-info rot-sm">${selectCategoria}</td>
  <td  class="rot-info rot-sm">${statusItem}</td>
  <td  class="rot-info rot-sm ocultar">${val1Item}</td>
  <td  class="rot-info rot-sm ocultar">${val2Item}</td>
  <td  class="rot-info rot-sm ocultar">${val3Item}</td>
  <td  class="rot-info rot-sm ocultar">${valMedItem}</td>
  <td  class="rot-info rot-sm ocultar">${bolPortItem}</td>
  <td  class="rot-info rot-sm">${valPortItem}</td>
  <td  class="rot-info rot-sm">${inputQtd}</td>
  <td  class="rot-info rot-sm">${valtotal}</td>
  <td  class="rot-info rot-sm ocultar">${inputLoc}</td>
  <td  class="rot-info rot-sm ocultar">${dateEntEquip}</td>
  <td  class="rot-info rot-sm ocultar">${dateInsEquip}</td>
  <td  class="rot-info rot-sm ocultar">${obsItem}</td>
  <td  class="rot-info rot-sm">${inputDest}</td>
  <td><button type="button" class="btn btn-danger btn-sm" onclick="removeRow(this)"><i class="ri-delete-bin-6-line"></i></button></td>`;

  setEquipSession();
}
function removeRow(btn){
  var row = btn.parentNode.parentNode;
  row.parentNode.removeChild(row);
}
function calcularDiferencaDias(dataInicial, dataFinal) {
  // Criar objetos Date a partir das strings de data

  if (dataInicial == "" || dataFinal == "") {
    return 0;
  }
  var dateInicial = new Date(dataInicial);
  var dateFinal = new Date(dataFinal);

  // Calcular a diferença em milissegundos
  var diferenca = dateFinal.getTime() - dateInicial.getTime();

  // Converter a diferença de milissegundos para dias
  var dias = diferenca / (1000 * 3600 * 24);

  // Retornar a diferença de dias
  return Math.round(dias);
}
function insereObsPen(){
  // Primeiramente pega os valores dos campos DESCRIÇÃO, CATEGORIA e DATA
  const descObsPen = document.getElementById("descObsPen").value
  const selectCategoriaObsPen = document.getElementById("selectCategoriaObsPen").value
  const dateObsPen = document.querySelector("#dateObsPen").value
  
  console.log(`Descrição: ${descObsPen}`)
  console.log(`Categoria: ${selectCategoriaObsPen}`)
  console.log(`Data: ${dateObsPen}`)

  //Seleciona a tabela de id=listObsPenTable e o tbody dela, e então insere a row com os dados
  const tbodyObsPen = document.getElementById("listObsPenTable").getElementsByTagName("tbody")[0];
  const rowObsPen = tbodyObsPen.insertRow();
  rowObsPen.innerHTML = `
  <td  class="rot-info rot-sm">${descObsPen}</td>
  <td  class="rot-info rot-sm">${selectCategoriaObsPen}</td>
  <td  class="rot-info rot-sm">${dateObsPen}</td>
  <td><button type="button" class="btn btn-danger btn-sm" onclick="removeRow(this)"><i class="ri-delete-bin-6-line"></i></button></td>`;

// Limpa os campos

document.getElementById("descObsPen").value = ""
document.getElementById("selectCategoriaObsPen").value = ""
document.getElementById("dateObsPen").value = ""

}

// Função que gera a string representando o conteúdo da tabela
function generateTableString(idTable) {
var table = document.getElementById(idTable);
var rows = Array.from(table.rows).slice(1); // Ignora a primeira linha (cabeçalho)
var result = rows.map((row) => {
  return Array.from(row.cells).map(cell => cell.textContent).join('|');
});
return result.join(';');
}


// Supondo que 'myForm' é o id do seu formulário
var formain = document.getElementById('form-etapas');

formain.addEventListener('submit', function(e) {
var confirmSubmit = window.confirm('Você tem certeza de que deseja enviar este formulário?');
if (confirmSubmit) {
  e.preventDefault();
  // Andamento
  const status = document.getElementById("selectStatusNew").value
  const selectnewrp = document.getElementById("selectnewrp").value
  const selectpgnew = document.getElementById("selectPgNew").value
  const etiqueta = document.getElementById("selectEtiquetaNew").value
  const natureza = document.getElementById("selectNaturezaNew").value
  // Documentos
  const contrato = document.getElementById("inputContratoNew").value
  const dataInitCont = document.getElementById("dateInitialInput").value
  const dataFinalCont = document.getElementById("dateFinalInput").value
  const listSei = document.getElementById("hiddensei").value
  // Equipamentos/Servicos
  const equipservice = generateTableString('main-table')
  document.getElementById('hiddenequipser').value = equipservice
  // Cronograma
  const titulocronograma = document.getElementById("inputTitleCron").value
  const descCronograma = document.getElementById("desCron").value
  const obsCronograma = document.getElementById("obsCron").value
  const taksCronograma = generateTableString('listTaskTable')
  document.getElementById('hiddentasks').value = taksCronograma
  // Observações/Pendencias
  const obsPendencias = generateTableString('listObsPenTable')
  document.getElementById('hiddenobspend').value = obsPendencias

  // Faz um print de todos os valores
  console.log(`Status: ${status}`)
  console.log(`RP: ${selectnewrp}`)
  console.log(`PG: ${selectpgnew}`)
  console.log(`Etiqueta: ${etiqueta}`)
  console.log(`Natureza: ${natureza}`)
  console.log(`Contrato: ${contrato}`)
  console.log(`Data Inicial Contrato: ${dataInitCont}`)
  console.log(`Data Final Contrato: ${dataFinalCont}`)
  console.log(`SEI: ${listSei}`)
  console.log(`Equipamentos/Serviços: ${equipservice}`)
  console.log(`Título Cronograma: ${titulocronograma}`)
  console.log(`Descrição Cronograma: ${descCronograma}`)
  console.log(`Observações Cronograma: ${obsCronograma}`)
  console.log(`Tarefas Cronograma: ${taksCronograma}`)
  console.log(`Observações/Pendências: ${obsPendencias}`)
  // Faz o submit do formulário

  formain.submit();

}else{
  e.preventDefault();
}
});
function setEquipSession(){
const mytablequip = document.querySelector("#main-table>tbody");
// Pegar o conteudo de tbody e gravar em uma variável de sessão
console.log(mytablequip.innerHTML)
sessionStorage.setItem('equipamentos', mytablequip.innerHTML);
}