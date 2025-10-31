import sqlite3
from schemas import Aluno, AlunoCreate, AlunoUpdate

# crud.py (trecho)
DB_PATH = "meubanco.db"

def criar_tabela():
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER NOT NULL,
            nota TEXT NOT NULL,
            matricula TEXT UNIQUE NOT NULL
        )
    """)
    conn.commit()
    conn.close()

criar_tabela()

# listar_alunos (já com str(row[3]))
def listar_alunos(nome: str = None, matricula: str = None):
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = "SELECT id, nome, idade, nota, matricula FROM alunos WHERE 1=1"
    params = []
    if nome:
        query += " AND nome LIKE ?"
        params.append(f"%{nome}%")
    if matricula:
        query += " AND matricula LIKE ?"
        params.append(f"%{matricula}%")
    cursor.execute(query, params)
    rows = cursor.fetchall()
    alunos = [
        {
            "id": row[0],
            "nome": row[1],
            "idade": row[2],
            "nota": str(row[3]),
            "matricula": row[4]
        }
        for row in rows
    ]
    conn.close()
    return alunos


# Funções CRUD
def adicionar_aluno(aluno: AlunoCreate):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO alunos (nome, idade, nota, matricula) VALUES (?, ?, ?, ?)",
            (aluno.nome, aluno.idade, aluno.nota, aluno.matricula)
        )
        conn.commit()
        aluno_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        conn.close()
        return None
    conn.close()
    return aluno_id


def buscar_aluno_por_matricula(matricula: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, idade, nota, matricula FROM alunos WHERE matricula = ?", (matricula,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Aluno(id=row[0], nome=row[1], idade=row[2], nota=row[3], matricula=row[4])
    return None

def atualizar_aluno(matricula: str, aluno: AlunoUpdate):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE alunos SET nome = ?, idade = ?, nota = ?, matricula = ? WHERE matricula = ?
    """, (aluno.nome, aluno.idade, aluno.nota, aluno.matricula, matricula))
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    return updated > 0

def remover_aluno(matricula: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alunos WHERE matricula = ?", (matricula,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    return deleted > 0
