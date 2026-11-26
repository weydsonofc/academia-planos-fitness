# Academia & Planos Fitness

## Sobre o projeto

O projeto Academia & Planos Fitness é uma API REST desenvolvida em Python com FastAPI, destinada ao gerenciamento de alunos, planos e matrículas de uma academia.

O objetivo é aplicar conceitos de qualidade de software, testes automatizados e Integração Contínua (CI), garantindo maior confiabilidade às funcionalidades da aplicação.

## Equipe

- Guilherme
- Wesley
- Atos
- Weydson
- Davi

## Tecnologias utilizadas

- Python
- FastAPI
- Uvicorn
- Pytest
- Pytest-cov
- HTTPX
- FastAPI TestClient
- Git e GitHub
- GitHub Actions

## Regras de negócio

| Função | Descrição |
|---|---|
| cadastrar_aluno() | Realiza o cadastro de alunos e impede CPFs duplicados. |
| cadastrar_plano() | Cadastra planos com valor e duração válidos. |
| matricular_aluno() | Vincula um aluno a um plano e impede matrículas válidas duplicadas. |
| cancelar_matricula() | Cancela uma matrícula existente. |
| verificar_validade_plano() | Verifica se a matrícula está ativa e dentro do prazo de validade. |
| buscar_matricula() | Consulta os dados de uma matrícula existente. |

## Rotas da API

| Método | Rota | Descrição |
|---|---|---|
| GET | /health | Verifica o funcionamento da API. |
| POST | /alunos | Cadastra um aluno. |
| POST | /planos | Cadastra um plano. |
| POST | /matriculas | Realiza uma matrícula. |
| GET | /matriculas/{id} | Consulta uma matrícula. |
| DELETE | /matriculas/{id} | Cancela uma matrícula. |
| GET | /matriculas/{id}/validade | Verifica a validade da matrícula. |

## Estrutura do projeto

- src/
  - app.py
  - regras.py
  - __init__.py
- tests/
  - unit/
    - test_regras.py
  - integration/
    - test_api.py
- .github/
  - workflows/
    - ci.yml
- requirements.txt
- pytest.ini
- .gitignore
- README.md

## Instalação das dependências

`pip install -r requirements.txt`

## Executar a aplicação

`python -m uvicorn src.app:app --reload`

Documentação interativa da API:

http://127.0.0.1:8000/docs

## Testes automatizados

O projeto possui duas suítes de testes automatizados:

- 35 testes unitários.
- 16 testes de integração.
- 51 casos de teste no total.

As técnicas utilizadas incluem:

- Padrão AAA (Arrange, Act, Assert).
- Classes de equivalência.
- Análise de valor limite.
- Parametrização com pytest.mark.parametrize.
- Validação de exceções com pytest.raises.
- Fixtures para isolamento dos testes.
- TestClient para testes de API.

### Executar testes unitários

`python -m pytest tests/unit -v`

### Executar testes de integração

`python -m pytest tests/integration -v`

### Executar todos os testes

`python -m pytest tests/ -v`

## Cobertura de código

A cobertura é medida utilizando o pytest-cov, com uma meta mínima de 80%.

Resultado da medição local das duas suítes: 100% de cobertura.

Para gerar o relatório, execute:

`python -m pytest --cov=src --cov-report=html --cov-report=term-missing --cov-fail-under=80`

O relatório HTML estará disponível em htmlcov/index.html.

## Integração Contínua (CI)

A pipeline foi desenvolvida utilizando GitHub Actions e é executada automaticamente nos eventos push e pull_request.

Ela possui dois jobs encadeados:

1. unit-tests: executa os testes unitários.
2. integration-tests: executa os testes de integração e gera o relatório de cobertura.

A estratégia Fail Fast impede a execução do segundo job caso os testes unitários falhem.

O relatório HTML de cobertura é disponibilizado como artefato com o nome coverage-report.