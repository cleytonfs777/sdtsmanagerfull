function formatToCurrency(element) {
    let input = element.value;
    input = input.replace(/[\D]/g, ""); // Remove tudo que não é número
    input = input.replace(/(\d)(\d{2})$/, "$1,$2"); // Coloca vírgula antes dos últimos 2 dígitos
    input = input.replace(/(?=(\d{3})+(\D))\B/g, "."); // Coloca ponto a cada 3 dígitos
    if(input == '' || input == 0){
        element.value = "";
    }else{
        element.value = `R$ ${input}`;
    }
  }

function calcMedia() {
    let nota1 = parseFloat(document.getElementById("val1Item").value == "" ? 0 : document.getElementById("val1Item").value.replace("R$ ", "").replace(".", "").replace(",", "."));
    let nota2 = parseFloat(document.getElementById("val2Item").value == "" ? 0 : document.getElementById("val2Item").value.replace("R$ ", "").replace(".", "").replace(",", "."));
    let nota3 = parseFloat(document.getElementById("val3Item").value == "" ? 0 : document.getElementById("val3Item").value.replace("R$ ", "").replace(".", "").replace(",", "."));
    let cont = 0;
    
    if (nota1 != 0) {
        cont++;
    }
    if (nota2 != 0) {
        cont++;
    }
    if (nota3 != 0) {
        cont++;
    }
    let media = (nota1 + nota2 + nota3) / cont;
    media = media.toFixed(2);
    //Tratamento para quando o usuário não digitar nada
    media = String(media);
    media = media.replace(/[\D]/g, ""); // Remove tudo que não é número
    media = media.replace(/(\d)(\d{2})$/, "$1,$2"); // Coloca vírgula antes dos últimos 2 dígitos
    media = media.replace(/(?=(\d{3})+(\D))\B/g, "."); // Coloca ponto a cada 3 dígitos

    document.getElementById("valMedItem").value = `R$ ${media}`;
}

