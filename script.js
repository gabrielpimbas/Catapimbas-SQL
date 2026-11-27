// Endereço da API Python (Flask)
const API_URL = "http://localhost:5000/ITENS";

// Ao carregar a página, busca os itens e configura o formulário
document.addEventListener("DOMContentLoaded", () => {
  carregarItens();
  document
    .getElementById("form-cadastro")
    .addEventListener("submit", cadastrarItem);
});

// [R] READ - Requisição GET para listar todos os itens
async function carregarItens() {
  try {
    const resposta = await fetch(API_URL); // GET é o método padrão do fetch
    const ITENS = await resposta.json();

    const tabela = document.getElementById("tabela-itens");
    tabela.innerHTML = ""; // Limpa a tabela antes de redesenhar

    ITENS.forEach((item) => {
      const tr = document.createElement("tr");

      const botaoAcao =
        item.status === "Disponivel"
          ? `<button onclick="devolverItem(${item.id})">Devolver</button>`
          : `<span>Retirado Por: <b>${item.retirado_por}</b></span>`;

      tr.innerHTML = `
                <td>${item.id}</td>
                <td>${item.titulo}</td>
                <td>${item.descricao || "-"}</td>
                <td>${item.local_encontrado}</td>
                <td>${item.data_encontro}</td>
                <td>${item.status}</td>
                <td>
                    ${botaoAcao}
                    <button onclick="deletarItem(${item.id})"
                    style="background:#b91c1c;">Excluir</button>
                </td>
            `;
      tabela.appendChild(tr);
    });
  } catch (error) {
    console.error("Erro ao conectar com a API Python:", error);
  }
}

// [C] CREATE - Requisição POST enviando JSON para cadastrar
async function cadastrarItem(evento) {
  evento.preventDefault(); // Impede o recarregamento da página

  const novoItem = {
    titulo: document.getElementById("titulo").value,
    descricao: document.getElementById("descricao").value,
    local_encontrado: document.getElementById("local_encontrado").value,
    data_encontro: document.getElementById("data_encontro").value,
  };

  const resposta = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(novoItem), // Converte o objeto JS para texto JSON
  });

  if (resposta.ok) {
    document.getElementById("form-cadastro").reset();
    carregarItens(); // Atualiza a lista na tela
  } else {
    const erro = await resposta.json();
    alert("Erro ao cadastrar: " + erro.erro);
  }
}

// [U] UPDATE - Requisição PUT para registrar devolução
async function devolverItem(id) {
  const nomePessoa = prompt("Digite o nome de quem está retirando o item:");
  if (!nomePessoa) return;

  const resposta = await fetch(`${API_URL}/${id}/devolver`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ retirado_por: nomePessoa }),
  });

  if (resposta.ok) {
    carregarItens();
  } else {
    alert("Erro ao registrar devolução.");
  }
}

// [D] DELETE - Requisição DELETE para apagar um registro
async function deletarItem(id) {
  if (!confirm("Tem certeza que deseja excluir este registro?")) return;

  const resposta = await fetch(`${API_URL}/${id}`, {
    method: "DELETE",
  });

  if (resposta.ok) {
    carregarItens();
  } else {
    alert("Erro ao excluir item.");
  }
}
