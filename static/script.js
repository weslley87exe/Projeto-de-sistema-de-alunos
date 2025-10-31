const apiUrl = "http://127.0.0.1:8000";

async function carregarAlunos() {
    const res = await fetch(`${apiUrl}/alunos`);
    const alunos = await res.json();
    const tabela = document.querySelector("#tabela-alunos tbody");
    tabela.innerHTML = "";

    alunos.forEach(aluno => {
        const row = `
            <tr>
                <td contenteditable="true" data-field="nome">${aluno.nome}</td>
                <td contenteditable="true" data-field="idade">${aluno.idade}</td>
                <td contenteditable="true" data-field="nota">${aluno.nota}</td>
                <td>${aluno.matricula}</td>
                <td>
                    <button onclick="atualizarAluno('${aluno.matricula}', this)">💾</button>
                    <button onclick="deletarAluno('${aluno.matricula}')">🗑️</button>
                </td>
            </tr>
        `;
        tabela.innerHTML += row;
    });
}

async function adicionarAluno() {
    const nome = document.getElementById("nome").value;
    const idade = parseInt(document.getElementById("idade").value);
    const nota = parseFloat(document.getElementById("nota").value.replace(",", "."));
    const matricula = document.getElementById("matricula").value;

    const aluno = { nome, idade, nota, matricula };

    await fetch(`${apiUrl}/alunos`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(aluno)
    });

    carregarAlunos();
}

async function atualizarAluno(matricula, botao) {
    const row = botao.closest("tr");
    const nome = row.querySelector('[data-field="nome"]').textContent;
    const idade = parseInt(row.querySelector('[data-field="idade"]').textContent);
    const nota = parseFloat(row.querySelector('[data-field="nota"]').textContent.replace(",", "."));

    await fetch(`${apiUrl}/alunos/${matricula}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nome, idade, nota, matricula })
    });

    carregarAlunos();
}

async function deletarAluno(matricula) {
    await fetch(`${apiUrl}/alunos/${matricula}`, { method: "DELETE" });
    carregarAlunos();
}

window.onload = carregarAlunos;
