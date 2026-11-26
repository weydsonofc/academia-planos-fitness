from datetime import date, timedelta

alunos = {}
planos = {}
matriculas = {}


def cadastrar_aluno(nome, cpf):
    if not nome.strip() or not cpf.strip():
        raise ValueError("Nome e CPF são obrigatórios")

    for aluno in alunos.values():
        if aluno["cpf"] == cpf.strip():
            raise ValueError("CPF já cadastrado")

    aluno_id = len(alunos) + 1

    aluno = {
        "id": aluno_id,
        "nome": nome.strip(),
        "cpf": cpf.strip()
    }

    alunos[aluno_id] = aluno
    return aluno


def cadastrar_plano(nome, valor, duracao):
    if not nome.strip():
        raise ValueError("Nome do plano é obrigatório")

    if valor <= 0:
        raise ValueError("Valor deve ser maior que zero")

    if duracao <= 0:
        raise ValueError("Duração deve ser maior que zero")

    plano_id = len(planos) + 1

    plano = {
        "id": plano_id,
        "nome": nome.strip(),
        "valor": valor,
        "duracao": duracao
    }

    planos[plano_id] = plano
    return plano


def matricular_aluno(aluno_id, plano_id):
    if aluno_id not in alunos:
        raise ValueError("Aluno não encontrado")

    if plano_id not in planos:
        raise ValueError("Plano não encontrado")

    for matricula in matriculas.values():
        if (
            matricula["aluno_id"] == aluno_id
            and verificar_validade_plano(matricula["id"])
        ):
            raise ValueError("Aluno já possui matrícula ativa")

    matricula_id = len(matriculas) + 1

    inicio = date.today()
    vencimento = inicio + timedelta(
        days=planos[plano_id]["duracao"]
    )

    matricula = {
        "id": matricula_id,
        "aluno_id": aluno_id,
        "plano_id": plano_id,
        "inicio": inicio.isoformat(),
        "vencimento": vencimento.isoformat(),
        "ativa": True
    }

    matriculas[matricula_id] = matricula
    return matricula


def cancelar_matricula(matricula_id):
    if matricula_id not in matriculas:
        raise ValueError("Matrícula não encontrada")

    if not matriculas[matricula_id]["ativa"]:
        raise ValueError("Matrícula já cancelada")

    matriculas[matricula_id]["ativa"] = False

    return matriculas[matricula_id]


def verificar_validade_plano(matricula_id):
    if matricula_id not in matriculas:
        raise ValueError("Matrícula não encontrada")

    matricula = matriculas[matricula_id]

    vencimento = date.fromisoformat(
        matricula["vencimento"]
    )

    return matricula["ativa"] and date.today() < vencimento


def buscar_matricula(matricula_id):
    if matricula_id not in matriculas:
        raise ValueError("Matrícula não encontrada")

    return matriculas[matricula_id]