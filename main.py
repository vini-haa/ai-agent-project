import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

# --- Importações das funções e schemas (sem alteração) ---
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# --- Constantes Globais ---
client = genai.Client(api_key=api_key)
model_name = 'gemini-2.0-flash-001'
WORKING_DIR = "./calculator"

# --- Mapa de Funções (sem alteração) ---
available_function_objects = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

# --- Prompt do Sistema (sem alteração) ---
system_prompt = """
You are an expert AI coding agent.

When a user asks you to fix a bug or add a feature, your workflow MUST be:
1.  First, use 'get_files_info' to understand the project structure.
2.  Second, use 'get_file_content' to read the relevant files and understand the existing code.
3.  Based on your analysis, use 'write_file' to apply the necessary code changes.
4.  Finally, use 'run_python_file' to execute the relevant script (like tests or main) to verify your fix.
5.  Do not assume the user's bug report is wrong. Always investigate the code files first.

You can perform the following operations:
- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# --- Ferramentas Disponíveis (sem alteração) ---
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)

# --- Função 'call_function' (sem alteração) ---
def call_function(function_call_part, verbose=False):
    """
    Executa uma chamada de função e retorna um objeto types.Content 
    estruturado com o resultado (ou erro).
    """
    function_name = function_call_part.name
    function_args = function_call_part.args

    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    function_to_call = available_function_objects.get(function_name)

    if function_to_call is None:
        if verbose:
            print(f"Error: Unknown function name: {function_name}")
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    function_args["working_directory"] = WORKING_DIR

    try:
        function_result = function_to_call(**function_args)
        
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    except Exception as e:
        if verbose:
            print(f"Error executing function {function_name}: {e}")
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Error executing function: {str(e)}"},
                )
            ],
        )

# --- NOVA LÓGICA DO AGENTE (LOOP PRINCIPAL) 
def run_agent_loop(user_prompt, is_verbose=False):
    """
    Executa o loop do agente de IA, gerenciando o histórico
    da conversa e as chamadas de função.
    """
    
    # 1. Inicializa o histórico da conversa com o prompt do usuário
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    if is_verbose:
        print(f"User prompt: {user_prompt}")
    
    # 2. Inicia o loop (com limite de 20 iterações)
    try:
        for i in range(20):
            # 3. Chama a IA (passando o histórico COMPLETO)
            response = client.models.generate_content(
                model=model_name,
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt
                ),
            )
            
            # 4. Adiciona a resposta da IA (plano ou texto) ao histórico
            if not response.candidates:
                print("Error: A IA não forneceu resposta.")
                break
            
            model_response_content = response.candidates[0].content
            messages.append(model_response_content)

            # 5. Verifica se a IA respondeu com texto (FIM DO LOOP)
            if not response.function_calls:
                print(f"\nFinal response:\n{response.text}")
                break # Sai do loop com sucesso
            
            # 6. Se a IA quiser chamar funções, execute-as
            
            # Lista para guardar os resultados das ferramentas
            tool_call_results = []
            
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, is_verbose)
                tool_call_results.append(function_call_result)
                
                if is_verbose:
                    try:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                    except (AttributeError, IndexError):
                        print("-> Error: Could not parse function result.")
            
            # 7. Adiciona os resultados das ferramentas ao histórico
            for tool_result in tool_call_results:
                messages.append(tool_result)

        # 8. Se o loop terminar por limite de iterações
        else: 
            print("\nError: Limite máximo de 20 iterações atingido.")

    except Exception as e:
        print(f"\n--- Um Erro Inesperado Ocorreu ---")
        print(f"Error: {e}")
        sys.exit(1)
        
    # Impressão final de tokens (se verbose)
    if is_verbose:
        try:
            prompt_tokens = response.usage_metadata.prompt_token_count
            response_tokens = response.usage_metadata.candidates_token_count
            print(f"\nPrompt tokens (last call): {prompt_tokens}")
            print(f"Response tokens (last call): {response_tokens}")
        except (AttributeError, ValueError):
            print("\nToken usage metadata not available.")

# --- Bloco de Execução Principal 
def main():
    parser = argparse.ArgumentParser(description="Agente de IA Gemini")
    parser.add_argument(
        "prompt",
        type=str,
        help="O prompt a ser enviado para a IA."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Ativa a saída detalhada (tokens, prompt do usuário)"
    )
    args = parser.parse_args()
    
    # Inicia o loop do agente
    run_agent_loop(args.prompt, args.verbose)

if __name__ == "__main__":
    main()
