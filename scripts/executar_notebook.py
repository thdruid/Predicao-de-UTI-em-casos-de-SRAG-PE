"""Executa a análise e salva uma cópia local com saídas em results/reports/."""

from pathlib import Path

import nbformat
from nbclient import NotebookClient


RAIZ = Path(__file__).resolve().parents[1]
ENTRADA = RAIZ / "notebooks/modeling/predicao_uti_pediatrica.ipynb"
SAIDA = RAIZ / "results/reports/predicao_uti_pediatrica_executado.ipynb"


def informar_progresso(cell, cell_index, **kwargs):
    if cell.cell_type == "code":
        print(f"Executando célula {cell_index + 1}...", flush=True)


def main():
    notebook = nbformat.read(ENTRADA, as_version=4)
    cliente = NotebookClient(
        notebook,
        timeout=3600,
        kernel_name="python3",
        resources={"metadata": {"path": str(RAIZ)}},
        on_cell_start=informar_progresso,
    )
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    try:
        cliente.execute()
    finally:
        # Preserva também a execução parcial para diagnosticar eventuais erros.
        nbformat.write(notebook, SAIDA)
    print(f"Execução concluída: {SAIDA}", flush=True)


if __name__ == "__main__":
    main()
