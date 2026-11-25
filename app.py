
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Clínica Médica & Agendamentos")

# Armazenamento temporário em memória
pacientes = {}
medicos = {}
consultas = {}


# MODELOS DA API

class PacienteEntrada(BaseModel):
    nome: str
    cpf: str


class MedicoEntrada(BaseModel):
    nome: str
    crm: str
    especialidade: str


class ConsultaEntrada(BaseModel):
    paciente_id: int
    medico_id: int
    data_hora: str


# 1. CADASTRAR PACIENTE

def cadastrar_paciente(nome, cpf):
    nome = nome.strip()
    cpf = cpf.strip()

    if not nome or not cpf:
        raise ValueError("Nome e CPF são obrigatórios.")

    if any(p["cpf"] == cpf for p in pacientes.values()):
        raise ValueError("Paciente já cadastrado.")

    paciente_id = len(pacientes) + 1

    paciente = {
        "id": paciente_id,
        "nome": nome,
        "cpf": cpf
    }

    pacientes[paciente_id] = paciente
    return paciente


# 2. CADASTRAR MÉDICO

def cadastrar_medico(nome, crm, especialidade):
    nome = nome.strip()
    crm = crm.strip()
    especialidade = especialidade.strip()

    if not nome or not crm or not especialidade:
        raise ValueError("Todos os campos são obrigatórios.")

    if any(m["crm"] == crm for m in medicos.values()):
        raise ValueError("Médico já cadastrado.")

    medico_id = len(medicos) + 1

    medico = {
        "id": medico_id,
        "nome": nome,
        "crm": crm,
        "especialidade": especialidade
    }

    medicos[medico_id] = medico
    return medico


# 3. VERIFICAR DISPONIBILIDADE

def verificar_disponibilidade(medico_id, data_hora):
    if medico_id not in medicos:
        raise ValueError("Médico não encontrado.")

    try:
        horario = datetime.fromisoformat(data_hora)
    except ValueError:
        raise ValueError("Data ou horário inválido.")

    for consulta in consultas.values():
        if (
            consulta["medico_id"] == medico_id
            and consulta["data_hora"] == data_hora
            and consulta["status"] == "agendada"
        ):
            return False

    return True


# 4. AGENDAR CONSULTA

def agendar_consulta(paciente_id, medico_id, data_hora):
    if paciente_id not in pacientes:
        raise ValueError("Paciente não encontrado.")

    if medico_id not in medicos:
        raise ValueError("Médico não encontrado.")

    try:
        datetime.fromisoformat(data_hora)
    except ValueError:
        raise ValueError("Data ou horário inválido.")

    if not verificar_disponibilidade(medico_id, data_hora):
        raise ValueError("Horário indisponível.")

    consulta_id = len(consultas) + 1

    consulta = {
        "id": consulta_id,
        "paciente_id": paciente_id,
        "medico_id": medico_id,
        "data_hora": data_hora,
        "status": "agendada"
    }

    consultas[consulta_id] = consulta
    return consulta


# 5. CANCELAR CONSULTA

def cancelar_consulta(consulta_id):
    if consulta_id not in consultas:
        raise ValueError("Consulta não encontrada.")

    consulta = consultas[consulta_id]

    if consulta["status"] == "cancelada":
        raise ValueError("Consulta já foi cancelada.")

    consulta["status"] = "cancelada"
    return consulta


# 6. BUSCAR CONSULTA

def buscar_consulta(consulta_id):
    if consulta_id not in consultas:
        raise ValueError("Consulta não encontrada.")

    return consultas[consulta_id]


# ROTAS DA API

@app.post("/pacientes", status_code=201)
def api_cadastrar_paciente(dados: PacienteEntrada):
    try:
        return cadastrar_paciente(dados.nome, dados.cpf)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@app.post("/medicos", status_code=201)
def api_cadastrar_medico(dados: MedicoEntrada):
    try:
        return cadastrar_medico(
            dados.nome, dados.crm, dados.especialidade
        )
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@app.post("/consultas", status_code=201)
def api_agendar_consulta(dados: ConsultaEntrada):
    try:
        return agendar_consulta(
            dados.paciente_id,
            dados.medico_id,
            dados.data_hora
        )
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@app.get("/consultas/{consulta_id}")
def api_buscar_consulta(consulta_id: int):
    try:
        return buscar_consulta(consulta_id)
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))


@app.delete("/consultas/{consulta_id}")
def api_cancelar_consulta(consulta_id: int):
    try:
        return cancelar_consulta(consulta_id)
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))
