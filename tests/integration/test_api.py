
import pytest
from fastapi.testclient import TestClient

from app import app, pacientes, medicos, consultas

client = TestClient(app)


# LIMPAR OS DADOS ANTES DE CADA TESTE

@pytest.fixture(autouse=True)
def limpar_dados():
    pacientes.clear()
    medicos.clear()
    consultas.clear()


# =====================================
# 1. TESTES DA ROTA POST /pacientes
# =====================================

def test_criar_paciente_com_sucesso():
    resposta = client.post(
        "/pacientes",
        json={
            "nome": "João Silva",
            "cpf": "12345678900"
        }
    )

    assert resposta.status_code == 201
    assert resposta.json()["nome"] == "João Silva"


def test_criar_paciente_com_dados_invalidos():
    resposta = client.post(
        "/pacientes",
        json={
            "nome": "",
            "cpf": "12345678900"
        }
    )

    assert resposta.status_code == 400
    assert resposta.json()["detail"] == "Nome e CPF são obrigatórios."


# =====================================
# 2. TESTES DA ROTA POST /consultas
# =====================================

def test_criar_consulta_com_sucesso():
    # Cadastrar paciente
    paciente = client.post(
        "/pacientes",
        json={
            "nome": "Maria Silva",
            "cpf": "98765432100"
        }
    )

    # Cadastrar médico
    medico = client.post(
        "/medicos",
        json={
            "nome": "Carlos Oliveira",
            "crm": "12345",
            "especialidade": "Cardiologia"
        }
    )

    resposta = client.post(
        "/consultas",
        json={
            "paciente_id": paciente.json()["id"],
            "medico_id": medico.json()["id"],
            "data_hora": "2026-12-01T14:00:00"
        }
    )

    assert resposta.status_code == 201
    assert resposta.json()["status"] == "agendada"


def test_criar_consulta_com_paciente_inexistente():
    # Cadastrar médico
    medico = client.post(
        "/medicos",
        json={
            "nome": "Carlos Oliveira",
            "crm": "12345",
            "especialidade": "Cardiologia"
        }
    )

    resposta = client.post(
        "/consultas",
        json={
            "paciente_id": 99,
            "medico_id": medico.json()["id"],
            "data_hora": "2026-12-01T14:00:00"
        }
    )

    assert resposta.status_code == 400
    assert resposta.json()["detail"] == "Paciente não encontrado."


# =====================================
# 3. TESTES DA ROTA GET /consultas/{id}
# =====================================

def test_buscar_consulta_com_sucesso():
    # Cadastrar paciente
    paciente = client.post(
        "/pacientes",
        json={
            "nome": "Pedro Santos",
            "cpf": "11122233344"
        }
    )

    # Cadastrar médico
    medico = client.post(
        "/medicos",
        json={
            "nome": "Ana Souza",
            "crm": "54321",
            "especialidade": "Dermatologia"
        }
    )

    # Agendar consulta
    consulta = client.post(
        "/consultas",
        json={
            "paciente_id": paciente.json()["id"],
            "medico_id": medico.json()["id"],
            "data_hora": "2026-12-02T10:00:00"
        }
    )

    consulta_id = consulta.json()["id"]

    resposta = client.get(f"/consultas/{consulta_id}")

    assert resposta.status_code == 200
    assert resposta.json()["id"] == consulta_id


def test_buscar_consulta_inexistente():
    resposta = client.get("/consultas/99")

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Consulta não encontrada."
