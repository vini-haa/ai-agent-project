import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    """
    Lista o conteúdo de um diretório de forma segura, permanecendo 
    dentro do 'working_directory' (o "jail").

    Sempre retorna uma string: ou a lista formatada ou uma mensagem de erro.
    """
    try:
        # 1. VALIDAÇÃO DE SEGURANÇA (O "JAIL")
        jail_path = os.path.abspath(working_directory)
        target_path_raw = os.path.join(jail_path, directory)
        target_path = os.path.abspath(target_path_raw)

        if not target_path.startswith(jail_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # 2. VERIFICAR SE É UM DIRETÓRIO
        if not os.path.isdir(target_path):
            return f'Error: "{directory}" is not a directory'

        # 3. CRIAR A STRING DE SAÍDA FORMATADA
        output_lines = []
        for item_name in os.listdir(target_path):
            full_item_path = os.path.join(target_path, item_name)
            try:
                file_size = os.path.getsize(full_item_path)
                is_dir = os.path.isdir(full_item_path)
                output_lines.append(f"- {item_name}: file_size={file_size} bytes, is_dir={is_dir}")
            except OSError as item_e:
                output_lines.append(f"- {item_name}: Error (cannot access: {item_e.strerror})")

        return "\n".join(output_lines)

    except OSError as e:
        return f'Error: Cannot access directory "{directory}". {e.strerror}'
    except Exception as e:
        return f"Error: An unexpected error occurred. {str(e)}"

# --- Schema (Declaração da Função para a IA) ---
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)