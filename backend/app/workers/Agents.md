# Pasta `workers`

Tarefas assíncronas (fila/processamento em background). Mantenha a lógica reusável em `services` e apenas orquestre aqui.

Exemplo
```python
# app/workers/tasks.py
def generate_report_task(report_id: int) -> None:
    # chamar services para executar o trabalho pesado
    pass
```
