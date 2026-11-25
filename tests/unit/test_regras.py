
import pytest

from app import (
    pacientes,
    medicos,
    consultas,
    cadastrar_paciente,
    cadastrar_medico,
    agendar_consulta,
    cancelar_consulta,
    verificar_disponibilidade,
    buscar_consulta
)


# LIMPAR OS DADOS ANTES DE CADA TESTE

@pytest.fixture(autouse=True)
def limpar_dados():
    pacientes.clear()
    medicos.clear()
    consultas.clear()


# FUNÇÕES AUXILIARES PARA OS TESTES

def criar_paciente():
    return cadastrar_paciente("João Silva", "12345678900")


def criar_medico():
    return cadastrar_medico(
        "Carlos Oliveira", "12345", "Cardiologia"
    )


def criar_consulta():
    paciente = criar_paciente()
    medico = criar_medico()

    return agendar_consulta(
        paciente["id"],
        medico["id"],
        "2026-12-01T14:00:00"
    )


# =====================================
# 1. TESTES DE CADASTRAR PACIENTE
# =====================================

def test_cadastrar_paciente_sucesso():
    resultado = cadastrar_paciente("João Silva", "12345678900")

    assert resultado["nome"] == "João Silva"
    assert resultado["cpf"] == "12345678900"


def test_cadastrar_paciente_com_espacos():
    resultado = cadastrar_paciente(" João Silva ", " 123 ")

    assert resultado["nome"] == "João Silva"
    assert resultado["cpf"] == "123"


def test_cadastrar_paciente_sem_nome():
    with pytest.raises(ValueError):
        cadastrar_paciente("", "12345678900")


def test_cadastrar_paciente_sem_cpf():
    with pytest.raises(ValueError):
        cadastrar_paciente("João Silva", "")


def test_cadastrar_paciente_duplicado():
    cadastrar_paciente("João Silva", "12345678900")

    with pytest.raises(ValueError):
        cadastrar_paciente("Maria Silva", "12345678900")


# =====================================
# 2. TESTES DE CADASTRAR MÉDICO
# =====================================

def test_cadastrar_medico_sucesso():
    resultado = criar_medico()

    assert resultado["nome"] == "Carlos Oliveira"
    assert resultado["crm"] == "12345"
    assert resultado["especialidade"] == "Cardiologia"


def test_cadastrar_medico_com_espacos():
    resultado = cadastrar_medico(
        " Carlos ", " 123 ", " Cardiologia "
    )

    assert resultado["nome"] == "Carlos"
    assert resultado["crm"] == "123"
    assert resultado["especialidade"] == "Cardiologia"


def test_cadastrar_medico_sem_nome():
    with pytest.raises(ValueError):
        cadastrar_medico("", "12345", "Cardiologia")


def test_cadastrar_medico_sem_crm():
    with pytest.raises(ValueError):
        cadastrar_medico("Carlos", "", "Cardiologia")


def test_cadastrar_medico_duplicado():
    criar_medico()

    with pytest.raises(ValueError):
        cadastrar_medico(
            "Outro Médico", "12345", "Neurologia"
        )


# =====================================
# 3. TESTES DE VERIFICAR DISPONIBILIDADE
# =====================================

def test_verificar_horario_disponivel():
    medico = criar_medico()

    resultado = verificar_disponibilidade(
        medico["id"], "2026-12-01T14:00:00"
    )

    assert resultado is True


def test_verificar_medico_inexistente():
    with pytest.raises(ValueError):
        verificar_disponibilidade(
            99, "2026-12-01T14:00:00"
        )


def test_verificar_data_invalida():
    medico = criar_medico()

    with pytest.raises(ValueError):
        verificar_disponibilidade(
            medico["id"], "data-invalida"
        )


def test_verificar_horario_ocupado():
    consulta = criar_consulta()

    resultado = verificar_disponibilidade(
        consulta["medico_id"],
        consulta["data_hora"]
    )

    assert resultado is False


def test_verificar_horario_apos_cancelamento():
    consulta = criar_consulta()

    cancelar_consulta(consulta["id"])

    resultado = verificar_disponibilidade(
        consulta["medico_id"],
        consulta["data_hora"]
    )

    assert resultado is True


# =====================================
# 4. TESTES DE AGENDAR CONSULTA
# =====================================

def test_agendar_consulta_sucesso():
    paciente = criar_paciente()
    medico = criar_medico()

    resultado = agendar_consulta(
        paciente["id"],
        medico["id"],
        "2026-12-01T14:00:00"
    )

    assert resultado["status"] == "agendada"
    assert resultado["paciente_id"] == paciente["id"]
    assert resultado["medico_id"] == medico["id"]


def test_agendar_consulta_paciente_inexistente():
    medico = criar_medico()

    with pytest.raises(ValueError):
        agendar_consulta(
            99, medico["id"], "2026-12-01T14:00:00"
        )


def test_agendar_consulta_medico_inexistente():
    paciente = criar_paciente()

    with pytest.raises(ValueError):
        agendar_consulta(
            paciente["id"], 99, "2026-12-01T14:00:00"
        )


def test_agendar_consulta_data_invalida():
    paciente = criar_paciente()
    medico = criar_medico()

    with pytest.raises(ValueError):
        agendar_consulta(
            paciente["id"], medico["id"], "data-invalida"
        )


def test_agendar_consulta_horario_ocupado():
    criar_consulta()

    with pytest.raises(ValueError):
        agendar_consulta(
            1, 1, "2026-12-01T14:00:00"
        )


# =====================================
# 5. TESTES DE CANCELAR CONSULTA
# =====================================

def test_cancelar_consulta_sucesso():
    consulta = criar_consulta()

    resultado = cancelar_consulta(consulta["id"])

    assert resultado["status"] == "cancelada"


def test_cancelar_consulta_inexistente():
    with pytest.raises(ValueError):
        cancelar_consulta(99)


def test_cancelar_consulta_ja_cancelada():
    consulta = criar_consulta()

    cancelar_consulta(consulta["id"])

    with pytest.raises(ValueError):
        cancelar_consulta(consulta["id"])


def test_cancelar_consulta_mantem_identificador():
    consulta = criar_consulta()

    resultado = cancelar_consulta(consulta["id"])

    assert resultado["id"] == consulta["id"]


def test_cancelar_consulta_mantem_paciente():
    consulta = criar_consulta()

    resultado = cancelar_consulta(consulta["id"])

    assert resultado["paciente_id"] == consulta["paciente_id"]


# =====================================
# 6. TESTES DE BUSCAR CONSULTA
# =====================================

def test_buscar_consulta_sucesso():
    consulta = criar_consulta()

    resultado = buscar_consulta(consulta["id"])

    assert resultado["id"] == consulta["id"]


def test_buscar_consulta_inexistente():
    with pytest.raises(ValueError):
        buscar_consulta(99)


def test_buscar_consulta_retorna_paciente():
    consulta = criar_consulta()

    resultado = buscar_consulta(consulta["id"])

    assert resultado["paciente_id"] == 1


def test_buscar_consulta_retorna_medico():
    consulta = criar_consulta()

    resultado = buscar_consulta(consulta["id"])

    assert resultado["medico_id"] == 1


def test_buscar_consulta_cancelada():
    consulta = criar_consulta()

    cancelar_consulta(consulta["id"])

    resultado = buscar_consulta(consulta["id"])

    assert resultado["status"] == "cancelada"
