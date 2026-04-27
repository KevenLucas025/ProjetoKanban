function fecharNovoCard(){
    document.getElementById("modalNovoCard").style.display = "none";
}

function salvarNovoCard(){

    const nome = document.getElementById("nomeNovoCard").value.trim();

    if(nome === ""){
        return;
    }

    const csrf =
        document.querySelector("[name=csrfmiddlewaretoken]").value;

    fetch("/card/criar/", {
        method:"POST",
        headers:{
            "Content-Type":"application/json",
            "X-CSRFToken": csrf
        },
        body: JSON.stringify({
            titulo: nome,
            coluna: colunaSelecionada.dataset.coluna
        })
    })
    .then(res => res.json())
    .then(data => {

        const novo = document.createElement("div");

        novo.className = "card-task";
        novo.setAttribute("data-id", data.id);

        novo.innerHTML = `
            <div class="topo-card">

                <span class="titulo-card">${data.titulo}</span>

                <button class="btn-menu-card"
                    onclick="toggleMenuCard(this)">
                    ⋮
                </button>

                <div class="menu-card">

                    <a href="javascript:void(0)"
                       onclick="renomearCard(this)">
                       ✏️ Renomear
                    </a>

                    <a href="javascript:void(0)"
                       onclick="excluirCard(this)">
                       🗑️ Excluir
                    </a>

                </div>

            </div>
        `;

        colunaSelecionada.appendChild(novo);

        atualizarContador(colunaSelecionada.dataset.coluna, 1);

        fecharNovoCard();
    });

}


let cardParaExcluir = null;

function excluirCard(link){

    const card = link.closest(".card-task");
    const menu = link.closest(".menu-card");

    //fecha o menu aberto
    menu.style.display = "none";
    card.classList.remove("menu-open");

    // guardar o card selecionado
    cardParaExcluir = card;

    // abre modal
    document.getElementById("modalExcluirCard").style.display = "flex";
}

function fecharExcluirCard(){
    document.getElementById("modalExcluirCard").style.display = "none";
    cardParaExcluir = null;
}

function confirmarExcluirCard(){

    if(!cardParaExcluir) return;

    const cardId = cardParaExcluir.getAttribute("data-id");

    const csrf = document.querySelector("[name=csrfmiddlewaretoken]").value;

    fetch(`/card/excluir/${cardId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrf
        }
    })
    .then(res => res.json())
    .then(data => {

        if(data.status === "ok"){

            const coluna = cardParaExcluir.closest(".coluna");

            cardParaExcluir.remove();

            atualizarContador(coluna.dataset.coluna, -1);

            fecharExcluirCard();
        }

    });

}

let tituloEditando = null;

function renomearCard(link){

    const card = link.closest(".card-task");

    link.closest(".menu-card").style.display = "none";

    card.classList.remove("menu-open");

    tituloEditando = card.querySelector(".titulo-card");

    document.getElementById("inputRenomearCard").value =
        tituloEditando.innerText;

    document.getElementById("modalRenomearCard").style.display = "flex";
}
function fecharRenomearCard(){
    document.getElementById("modalRenomearCard").style.display = "none";
}

function salvarRenomearCard(){

    const novoNome = document.getElementById("inputRenomearCard").value.trim();

    if(novoNome === ""){
        return;
    }

    const cardId = tituloEditando.closest(".card-task").getAttribute("data-id");

    const csrf = document.querySelector("[name=csrfmiddlewaretoken]").value;

    fetch(`/card/renomear/${cardId}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf
        },
        body: JSON.stringify({
            titulo: novoNome
        })
    })
    .then(res => res.json())
    .then(data => {

        if(data.status === "ok"){
            tituloEditando.innerText = novoNome;
            fecharRenomearCard();
        }

    });

}
document.addEventListener("click", function (e) {

    // =========================
    // FECHAR MENU DA COLUNA
    // =========================
    const menusLista = document.querySelectorAll(".menu-lista");

    menusLista.forEach(menu => {

        const botao = menu.previousElementSibling; // ⋮ da coluna

        const clicouDentro = menu.contains(e.target) || botao.contains(e.target);

        if (!clicouDentro) {
            menu.style.display = "none";
        }

    });


    // =========================
    // FECHAR MENU DO CARD
    // =========================
    const menusCard = document.querySelectorAll(".menu-card");

    menusCard.forEach(menu => {

        const botao = menu.previousElementSibling; // ⋮ do card

        const clicouDentro = menu.contains(e.target) || botao.contains(e.target);

        if (!clicouDentro) {
            menu.style.display = "none";
        }

    });

});

function atualizarContador(colunaCodigo, delta) {

    const coluna = document.querySelector(`[data-coluna="${colunaCodigo}"]`);

    if (!coluna) return;

    const span = coluna.querySelector("h2 span");

    if (!span) return;

    let valorAtual = parseInt(span.innerText || "0");

    span.innerText = valorAtual + delta;
}

let colunaSelecionada = null;

function adicionarCard(link){

    colunaSelecionada = link.closest(".coluna");

    document.getElementById("modalNovoCard").style.display = "flex";

    document.getElementById("nomeNovoCard").value = "";

    link.closest(".menu-lista").style.display = "none";
}

let listaSelecionada = null;

function excluirLista(link){

    listaSelecionada = link.closest(".coluna");


    // fecha menu
    link.closest(".menu-lista").style.display = "none";

    document.getElementById("modalExcluirLista").style.display = "flex";
}

function fecharExcluirLista(){
    document.getElementById("modalExcluirLista").style.display = "none";
    listaSelecionada = null;
}


function confirmarExcluirLista(){

    if(!listaSelecionada) return;

    const colunaCodigo = listaSelecionada.dataset.coluna;

    const csrf = document.querySelector("[name=csrfmiddlewaretoken]").value;

   fetch(`/lista/excluir/${colunaCodigo}/`,{
    method: "POST",
    headers: {
        "X-CSRFToken": csrf
    }
   })
   .then(res => res.json())
   .then(data => {
        if (data.status === "ok"){
            const cards = listaSelecionada.querySelectorAll(".card-task");

            cards.forEach(card => card.remove());

            listaSelecionada.querySelector("h2 span").innerText = "0";

            fecharExcluirLista();
        }
   });
}

function filtrarCards(){
    const de = document.getElementById("dataDe").value;
    const ate = document.getElementById("dataAte").value;

    window.location.href = `?de=${de}&ate=${ate}`;
}
function mostrarAlerta(msg){

    const toast = document.getElementById("toastAlerta");

    toast.innerText = "⚠️ " + msg;

    // reset animação
    toast.classList.remove("show");
    toast.classList.remove("hide");

    setTimeout(() => {
        toast.classList.add("show");
    }, 10);

    setTimeout(() => {
        toast.classList.add("hide");

        setTimeout(() => {
            toast.classList.remove("show");
            toast.classList.remove("hide");
        }, 300);
    }, 2500);
}

document.getElementById("formFiltroData").addEventListener("submit", function(e){

    const de = document.getElementById("dataDe").value;
    const ate = document.getElementById("dataAte").value;

    if(de === "" && ate === ""){
        e.preventDefault();
        mostrarAlerta("Preencha as datas para filtrar.");
        return;
    }

    if(de !== "" && ate === ""){
        e.preventDefault();
        mostrarAlerta("Preencha a data Até.");
        return;
    }

    if(de === "" && ate !== ""){
        e.preventDefault();
        mostrarAlerta("Preencha a data De.");
        return;
    }

});

function abrirNovoCardGlobal(){
    // Fecha menu lateral
    const menuLateral = document.getElementById('menuLateral');
    const bsOffcanvas = bootstrap.Offcanvas.getInstance(menuLateral);
    if (bsOffcanvas) {
        bsOffcanvas.hide();
    }

    // Abre modal
    document.getElementById("modalNovoCardGlobal").style.display = "flex";

    // Input
    const input = document.getElementById("tituloCardsGlobal");
    input.value = "";

    // Reset checkboxes
    const checkAll = document.getElementById("checkAllColunas");
    const checkboxes = document.querySelectorAll(".checkbox-colunas input[type='checkbox']:not(#checkAllColunas)");

    checkboxes.forEach(cb => cb.checked = false);

    if (checkAll) {
        checkAll.checked = false;
        checkAll.indeterminate = false;
    }

    setTimeout(() => input.focus(), 100);
}

function salvarCardsGlobal(){

    const nome = document.getElementById("tituloCardsGlobal").value.trim();

    if(nome === ""){
        mostrarAlerta("Digite um título");
        return;
    }

    const checkboxes = document.querySelectorAll(".checkbox-colunas input:checked");
    const colunas = Array.from(checkboxes)
        .filter(cb => cb.id !== "checkAllColunas")
        .map(cb => cb.value);

    if(colunas.length === 0){
        mostrarAlerta("Selecione pelo menos uma coluna");
        return;
    }

    const csrf = document.querySelector("[name=csrfmiddlewaretoken]")?.value;

    fetch("/card/criar-global/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf
        },
        body: JSON.stringify({
            titulo: nome,
            colunas: colunas
        })
    })
    .then(res => {
        if (!res.ok) throw new Error("Erro no fetch");
        return res.json();
    })
    .then(data => {

    colunas.forEach(colunaCodigo => {

        const coluna = document.querySelector(`[data-coluna="${colunaCodigo}"]`);
        if(!coluna) return;

        const cardInfo = data.cards[colunaCodigo];

        const novo = document.createElement("div");
        novo.className = "card-task";

        novo.setAttribute("data-id", cardInfo.id);

        novo.innerHTML = `
            <div class="topo-card">

                <div style="flex:1">
                    <span class="titulo-card">${data.titulo}</span>

                    <small class="data-card">
                        📅 ${cardInfo.data}
                    </small>
                </div>

                <button class="btn-menu-card" onclick="toggleMenuCard(this)">
                    ⋮
                </button>

                <div class="menu-card">
                    <a href="javascript:void(0)" onclick="renomearCard(this)">✏️ Renomear</a>
                    <a href="javascript:void(0)" onclick="excluirCard(this)">🗑️ Excluir</a>
                </div>

            </div>
        `;

        coluna.appendChild(novo);
        atualizarContador(colunaCodigo, 1);
    });

    fecharCardsGlobal();
});
}

function fecharCardsGlobal(){
    document.getElementById("modalNovoCardGlobal").style.display = "none";
}
const checkAll = document.getElementById("checkAllColunas");

if (checkAll) {
    const checkboxes = document.querySelectorAll(".checkbox-colunas input[type='checkbox']:not(#checkAllColunas)");

    checkAll.addEventListener("change", function () {
        checkboxes.forEach(cb => cb.checked = checkAll.checked);
    });

    checkboxes.forEach(cb => {
        cb.addEventListener("change", () => {
            const allChecked = [...checkboxes].every(c => c.checked);
            const noneChecked = [...checkboxes].every(c => !c.checked);

            if (allChecked) {
                checkAll.checked = true;
                checkAll.indeterminate = false;
            } else if (noneChecked) {
                checkAll.checked = false;
                checkAll.indeterminate = false;
            } else {
                checkAll.indeterminate = true;
            }
        });
    });
}