import os
import sys
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        # 1. VALIDAÇÃO DE SEGURANÇA (O "JAIL")
        jail_path = os.path.abspath(working_directory)
        target_path_raw = os.path.join(jail_path, file_path)
        target_path = os.path.abspath(target_path_raw)

        if not target_path.startswith(jail_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # 2. VALIDAÇÃO DO ARQUIVO
        if not os.path.exists(target_path):
            return f'Error: File "{file_path}" not found.'
        
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        # 3. EXECUTAR O ARQUIVO PYTHON
        command_list = [sys.executable, target_path] + args
        
        completed_process = subprocess.run(
            command_list,
            cwd=jail_path,
            timeout=30,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )

    except subprocess.TimeoutExpired:
        return "Error: Process timed out after 30 seconds."
    except Exception as e:
        return f"Error: executing Python file: {e}"

    # 4. FORMATAR A SAÍDA
    output = []
    stdout = completed_process.stdout.strip()
    stderr = completed_process.stderr.strip()
    return_code = completed_process.returncode

    if stdout:
        output.append(f"STDOUT:\n{stdout}")
    
    if stderr:
        output.append(f"STDERR:\n{stderr}")
    
    if return_code != 0:
        output.append(f"Process exited with code {return_code}")

    if not output:
        return "No output produced."
    
    return "\n".join(output)

# --- Schema (Declaração da Função para a IA) ---
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file (.py) within the working directory with optional arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the Python file to be executed."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="A list of string arguments to pass to the Python script."
            ),
        },
        required=["file_path"]
    ),

)
