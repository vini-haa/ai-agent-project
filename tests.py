#!/usr/bin/env python3
import os
# Importa a NOVA função
from functions.run_python_file import run_python_file

def print_result(header, result):
    """Uma função auxiliar para formatar a saída."""
    print(header)
    # Adiciona indentação se for uma mensagem de erro
    if result.startswith("Erro:"):
        print(f"    {result}")
    else:
        print(result)
    print("\n" + "="*30 + "\n") # Imprime um separador

def main():
    base_dir = "calculator"

    # Verifica se o diretório 'calculator' existe
    if not os.path.isdir(base_dir):
        print(f"Error: O diretório '{base_dir}' não foi encontrado.")
        print("Certifique-se de executar 'tests.py' da raiz do projeto.")
        return

    # --- Executa os 6 testes solicitados ---

    # Teste 1: Executar 'main.py' (sem args)
    print_result(
        f"Result for running '{base_dir}/main.py' (no args):",
        run_python_file(base_dir, "main.py")
    )

    # Teste 2: Executar 'main.py' (com args)
    print_result(
        f"Result for running '{base_dir}/main.py' (with args):",
        run_python_file(base_dir, "main.py", ["3 + 5"])
    )

    # Teste 3: Executar 'tests.py' (o da calculadora)
    print_result(
        f"Result for running '{base_dir}/tests.py':",
        run_python_file(base_dir, "tests.py")
    )

    # Teste 4: Tentar escapar da "jaula" (../main.py)
    print_result(
        f"Result for running '{base_dir}/../main.py':",
        run_python_file(base_dir, "../main.py")
    )
    
    # Teste 5: Tentar executar arquivo inexistente
    print_result(
        f"Result for running '{base_dir}/nonexistent.py':",
        run_python_file(base_dir, "nonexistent.py")
    )

    # Teste 6: Tentar executar arquivo não-Python
    print_result(
        f"Result for running '{base_dir}/lorem.txt':",
        run_python_file(base_dir, "lorem.txt")
    )

if __name__ == "__main__":
    main()