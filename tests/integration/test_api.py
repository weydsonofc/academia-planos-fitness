import pytest
from fastapi.testclient import TestClient

from src.app import app
from src.regras import alunos, planos, matriculas

client = TestClient(app)


@pytest.fixture(autouse=True)
def limpar_dados():
    alunos.clear()
    planos.clear()
    matriculas.clear()


def criar_matricula_teste():
    aluno = client.post("/alunos", json={
        "nome": "Joao",
        "cpf": "12345678900"
    }).json()

    plano = client.post("/planos", json={
        "nome": "Mensal",
        "valor": 100,
        "duracao": 30
    }).json()

    resposta = client.post("/matriculas", json={
        "aluno_id": aluno["id"],
        "plano_id": plano["id"]
    })

    assert resposta.status_code == 201

    return resposta.json()


# ==========================================
# 1. TESTE DA ROTA HEALTH
# ==========================================

def test_health():
    resposta = client.get("/health")

    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok"}


# ==========================================
# 2. TESTES DA ROTA POST /alunos
# ==========================================

def test_criar_aluno_sucesso():
    # Arrange
    dados = {
        "nome": "Joao",
        "cpf": "12345678900"
    }

    # Act
    resposta = client.post("/alunos", json=dados)

    # Assert
    assert resposta.status_code == 201
    assert resposta.json()["nome"] == "Joao"
    assert resposta.json()["cpf"] == "12345678900"


def test_criar_aluno_invalido():
    resposta = client.post("/alunos", json={
        "nome": "",
        "cpf": "12345678900"
    })

    assert resposta.status_code == 400
    assert resposta.json()["detail"] == (
        "Nome e CPF são obrigatórios"
    )


def test_criar_aluno_duplicado():
    dados = {
        "nome": "Joao",
        "cpf": "12345678900"
    }

    client.post("/alunos", json=dados)

    resposta = client.post("/alunos", json=dados)

    assert resposta.status_code == 400
    assert resposta.json()["detail"] == "CPF já cadastrado"


# ==========================================
# 3. TESTES DA ROTA POST /planos
# ==========================================

def test_criar_plano_sucesso():
    resposta = client.post("/planos", json={
        "nome": "Mensal",
        "valor": 100,
        "duracao": 30
    })

    assert resposta.status_code == 201
    assert resposta.json()["nome"] == "Mensal"
    assert resposta.json()["valor"] == 100
    assert resposta.json()["duracao"] == 30


def test_criar_plano_invalido():
    resposta = client.post("/planos", json={
        "nome": "Mensal",
        "valor": 0,
        "duracao": 30
    })

    assert resposta.status_code == 400
    assert resposta.json()["detail"] == (
        "Valor deve ser maior que zero"
    )


# ==========================================
# 4. TESTES DA ROTA POST /matriculas
# ==========================================

def test_criar_matricula_sucesso():
    matricula = criar_matricula_teste()

    assert matricula["id"] == 1
    assert matricula["aluno_id"] == 1
    assert matricula["plano_id"] == 1
    assert matricula["ativa"] is True


def test_criar_matricula_invalida():
    resposta = client.post("/matriculas", json={
        "aluno_id": 999,
        "plano_id": 999
    })

    assert resposta.status_code == 400
    assert resposta.json()["detail"] == (
        "Aluno não encontrado"
    )


# ==========================================
# 5. TESTES DA ROTA GET /matriculas/{id}
# ==========================================

def test_consultar_matricula_sucesso():
    matricula = criar_matricula_teste()

    resposta = client.get(
        f"/matriculas/{matricula['id']}"
    )

    assert resposta.status_code == 200
    assert resposta.json() == matricula


def test_consultar_matricula_inexistente():
    resposta = client.get("/matriculas/999")

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == (
        "Matrícula não encontrada"
    )


# ==========================================
# 6. TESTES DA ROTA DELETE /matriculas/{id}
# ==========================================

def test_cancelar_matricula_sucesso():
    matricula = criar_matricula_teste()

    resposta = client.delete(
        f"/matriculas/{matricula['id']}"
    )

    assert resposta.status_code == 200
    assert resposta.json()["ativa"] is False


def test_cancelar_matricula_inexistente():
    resposta = client.delete("/matriculas/999")

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == (
        "Matrícula não encontrada"
    )


def test_cancelar_matricula_duas_vezes():
    matricula = criar_matricula_teste()

    rota = f"/matriculas/{matricula['id']}"

    client.delete(rota)

    resposta = client.delete(rota)

    assert resposta.status_code == 400
    assert resposta.json()["detail"] == (
        "Matrícula já cancelada"
    )


# ==========================================
# 7. TESTES DA ROTA GET /matriculas/{id}/validade
# ==========================================

def test_consultar_validade_sucesso():
    matricula = criar_matricula_teste()

    resposta = client.get(
        f"/matriculas/{matricula['id']}/validade"
    )

    assert resposta.status_code == 200
    assert resposta.json()["valida"] is True


def test_consultar_validade_inexistente():
    resposta = client.get("/matriculas/999/validade")

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == (
        "Matrícula não encontrada"
    )


def test_consultar_validade_cancelada():
    matricula = criar_matricula_teste()

    client.delete(
        f"/matriculas/{matricula['id']}"
    )

    resposta = client.get(
        f"/matriculas/{matricula['id']}/validade"
    )

    assert resposta.status_code == 200
    assert resposta.json()["valida"] is False