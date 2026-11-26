from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.regras import (
    cadastrar_aluno,
    cadastrar_plano,
    matricular_aluno,
    cancelar_matricula,
    verificar_validade_plano,
    buscar_matricula
)

app = FastAPI(title="Academia & Planos Fitness")


class AlunoEntrada(BaseModel):
    nome: str
    cpf: str


class PlanoEntrada(BaseModel):
    nome: str
    valor: float
    duracao: int


class MatriculaEntrada(BaseModel):
    aluno_id: int
    plano_id: int


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/alunos", status_code=201)
def criar_aluno(dados: AlunoEntrada):
    try:
        return cadastrar_aluno(dados.nome, dados.cpf)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@app.post("/planos", status_code=201)
def criar_plano(dados: PlanoEntrada):
    try:
        return cadastrar_plano(
            dados.nome,
            dados.valor,
            dados.duracao
        )
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@app.post("/matriculas", status_code=201)
def criar_matricula(dados: MatriculaEntrada):
    try:
        return matricular_aluno(
            dados.aluno_id,
            dados.plano_id
        )
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@app.get("/matriculas/{matricula_id}")
def consultar_matricula(matricula_id: int):
    try:
        return buscar_matricula(matricula_id)
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))


@app.delete("/matriculas/{matricula_id}")
def excluir_matricula(matricula_id: int):
    try:
        buscar_matricula(matricula_id)
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))

    try:
        return cancelar_matricula(matricula_id)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@app.get("/matriculas/{matricula_id}/validade")
def consultar_validade(matricula_id: int):
    try:
        return {
            "matricula_id": matricula_id,
            "valida": verificar_validade_plano(matricula_id)
        }
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))