import pytest
from datetime import date, timedelta

from src.regras import (
    alunos,
    planos,
    matriculas,
    cadastrar_aluno,
    cadastrar_plano,
    matricular_aluno,
    cancelar_matricula,
    verificar_validade_plano,
    buscar_matricula
)


@pytest.fixture(autouse=True)
def limpar_dados():
    alunos.clear()
    planos.clear()
    matriculas.clear()


def criar_matricula_teste():
    aluno = cadastrar_aluno("Joao", "12345678900")
    plano = cadastrar_plano("Mensal", 100, 30)

    return matricular_aluno(aluno["id"], plano["id"])


# ==========================================
# 1. TESTES DE CADASTRO DE ALUNO
# ==========================================

def test_cadastrar_aluno_sucesso():
    # Arrange
    nome = "Joao"
    cpf = "12345678900"

    # Act
    resultado = cadastrar_aluno(nome, cpf)

    # Assert
    assert resultado["nome"] == nome
    assert resultado["cpf"] == cpf
    assert resultado["id"] == 1


@pytest.mark.parametrize("nome, cpf", [
    ("", "12345678900"),
    ("Joao", ""),
    ("   ", "12345678900")
])
def test_cadastrar_aluno_dados_invalidos(nome, cpf):
    with pytest.raises(ValueError):
        cadastrar_aluno(nome, cpf)


def test_cadastrar_aluno_cpf_duplicado():
    cadastrar_aluno("Joao", "12345678900")

    with pytest.raises(ValueError):
        cadastrar_aluno("Maria", "12345678900")


def test_cadastrar_aluno_remover_espacos():
    resultado = cadastrar_aluno("  Joao  ", "12345678900")

    assert resultado["nome"] == "Joao"


# ==========================================
# 2. TESTES DE CADASTRO DE PLANO
# ==========================================

def test_cadastrar_plano_sucesso():
    # Arrange
    nome = "Mensal"
    valor = 100
    duracao = 30

    # Act
    resultado = cadastrar_plano(nome, valor, duracao)

    # Assert
    assert resultado["nome"] == nome
    assert resultado["valor"] == valor
    assert resultado["duracao"] == duracao


@pytest.mark.parametrize("valor", [-100, 0])
def test_cadastrar_plano_valor_invalido(valor):
    with pytest.raises(ValueError):
        cadastrar_plano("Mensal", valor, 30)


@pytest.mark.parametrize("duracao", [-1, 0])
def test_cadastrar_plano_duracao_invalida(duracao):
    with pytest.raises(ValueError):
        cadastrar_plano("Mensal", 100, duracao)


def test_cadastrar_plano_nome_vazio():
    with pytest.raises(ValueError):
        cadastrar_plano("", 100, 30)


def test_cadastrar_plano_valor_limite():
    resultado = cadastrar_plano("Diario", 0.01, 1)

    assert resultado["valor"] == 0.01
    assert resultado["duracao"] == 1


# ==========================================
# 3. TESTES DE MATRICULA
# ==========================================

def test_matricular_aluno_sucesso():
    # Arrange
    aluno = cadastrar_aluno("Joao", "12345678900")
    plano = cadastrar_plano("Mensal", 100, 30)

    # Act
    resultado = matricular_aluno(aluno["id"], plano["id"])

    # Assert
    assert resultado["aluno_id"] == aluno["id"]
    assert resultado["plano_id"] == plano["id"]
    assert resultado["ativa"] is True


def test_matricular_aluno_inexistente():
    plano = cadastrar_plano("Mensal", 100, 30)

    with pytest.raises(ValueError):
        matricular_aluno(999, plano["id"])


def test_matricular_plano_inexistente():
    aluno = cadastrar_aluno("Joao", "12345678900")

    with pytest.raises(ValueError):
        matricular_aluno(aluno["id"], 999)


def test_matricula_duplicada():
    matricula = criar_matricula_teste()

    with pytest.raises(ValueError):
        matricular_aluno(
            matricula["aluno_id"],
            matricula["plano_id"]
        )


def test_matricular_apos_cancelamento():
    matricula = criar_matricula_teste()

    cancelar_matricula(matricula["id"])

    nova = matricular_aluno(
        matricula["aluno_id"],
        matricula["plano_id"]
    )

    assert nova["ativa"] is True
    assert nova["id"] != matricula["id"]


def test_data_vencimento_matricula():
    matricula = criar_matricula_teste()

    esperado = date.today() + timedelta(days=30)

    assert matricula["vencimento"] == esperado.isoformat()


# ==========================================
# 4. TESTES DE CANCELAMENTO
# ==========================================

def test_cancelar_matricula_sucesso():
    # Arrange
    matricula = criar_matricula_teste()

    # Act
    resultado = cancelar_matricula(matricula["id"])

    # Assert
    assert resultado["ativa"] is False


@pytest.mark.parametrize("matricula_id", [0, -1, 999])
def test_cancelar_matricula_inexistente(matricula_id):
    with pytest.raises(ValueError):
        cancelar_matricula(matricula_id)


def test_cancelar_matricula_duas_vezes():
    matricula = criar_matricula_teste()

    cancelar_matricula(matricula["id"])

    with pytest.raises(ValueError):
        cancelar_matricula(matricula["id"])


# ==========================================
# 5. TESTES DE VALIDADE DO PLANO
# ==========================================

def test_plano_valido():
    matricula = criar_matricula_teste()

    resultado = verificar_validade_plano(matricula["id"])

    assert resultado is True


def test_plano_cancelado():
    matricula = criar_matricula_teste()

    cancelar_matricula(matricula["id"])

    assert verificar_validade_plano(matricula["id"]) is False


@pytest.mark.parametrize("dias, esperado", [
    (-1, False),
    (0, False),
    (1, True)
])
def test_validade_fronteira(dias, esperado):
    # Arrange
    matricula = criar_matricula_teste()

    matricula["vencimento"] = (
        date.today() + timedelta(days=dias)
    ).isoformat()

    # Act
    resultado = verificar_validade_plano(matricula["id"])

    # Assert
    assert resultado is esperado


def test_verificar_matricula_inexistente():
    with pytest.raises(ValueError):
        verificar_validade_plano(999)


# ==========================================
# 6. TESTES DE BUSCA DE MATRICULA
# ==========================================

def test_buscar_matricula_sucesso():
    # Arrange
    matricula = criar_matricula_teste()

    # Act
    resultado = buscar_matricula(matricula["id"])

    # Assert
    assert resultado == matricula


@pytest.mark.parametrize("matricula_id", [0, -1, 999])
def test_buscar_matricula_inexistente(matricula_id):
    with pytest.raises(ValueError):
        buscar_matricula(matricula_id)


def test_buscar_matricula_cancelada():
    matricula = criar_matricula_teste()

    cancelar_matricula(matricula["id"])

    resultado = buscar_matricula(matricula["id"])

    assert resultado["ativa"] is False