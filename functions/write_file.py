import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        # 1. VALIDAÇÃO DE SEGURANÇA (O "JAIL")
        jail_path = os.path.abspath(working_directory)
        target_path_raw = os.path.join(jail_path, file_path)
        target_path = os.path.abspath(target_path_raw)

        if not target_path.startswith(jail_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # 2. CRIAR DIRETÓRIOS PAIS
        target_dir = os.path.dirname(target_path)
        os.makedirs(target_dir, exist_ok=True) 

        # 3. ESCREVER O ARQUIVO
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # 4. RETORNAR SUCESSO
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except (IOError, OSError) as e:
        error_msg = getattr(e, 'strerror', str(e))
        return f"Error: Could not write to file: {error_msg}"
    except Exception as e:
        return f"Error: An unexpected error occurred. {str(e)}"

# --- Schema (Declaração da Função para a IA) ---
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites content to a specified file in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file to be written."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file."
            ),
        },
        required=["file_path", "content"]
    ),

)
