import os
import config # Importa o config.py
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        # 1. VALIDAÇÃO DE SEGURANÇA (O "JAIL")
        jail_path = os.path.abspath(working_directory)
        target_path_raw = os.path.join(jail_path, file_path)
        target_path = os.path.abspath(target_path_raw)

        if not target_path.startswith(jail_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # 2. VERIFICAR SE É UM ARQUIVO
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # 3. LER O ARQUIVO E TRUNCAR
        try:
            with open(target_path, 'r', encoding='utf-8') as f:
                content = f.read(config.FILE_CONTENT_MAX_CHARS + 1)
            
            if len(content) > config.FILE_CONTENT_MAX_CHARS:
                truncated_content = content[:config.FILE_CONTENT_MAX_CHARS]
                trunc_msg = f'[...File "{file_path}" truncated at {config.FILE_CONTENT_MAX_CHARS} characters]'
                return truncated_content + trunc_msg
            else:
                return content
        except (IOError, UnicodeDecodeError) as read_e:
            return f"Error: Could not read file: {read_e}"

    except Exception as e:
        return f"Error: An unexpected error occurred. {str(e)}"

# --- Schema (Declaração da Função para a IA) ---
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the content of a specified file from the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file to be read."
            ),
        },
        required=["file_path"]
    ),

)
