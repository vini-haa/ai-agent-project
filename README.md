# Agente de IA com Gemini

Este projeto é um agente de IA de linha de comando (CLI) construído em Python, capaz de interagir com uma base de código local para analisar, modificar e executar arquivos. Ele foi desenvolvido como parte do currículo do [Boot.dev](https://boot.dev/).

O agente utiliza a API Gemini do Google para tomar decisões e um conjunto de "ferramentas" (funções Python) para interagir com o sistema de arquivos. O objetivo final é fornecer um prompt em linguagem natural (como "corrija este bug") e o agente iterativamente usará suas ferramentas até que a tarefa seja concluída.

## 🎯 Funcionalidades Principais

* **Loop de Agente:** Opera em um ciclo de feedback contínuo (Prompt do Usuário -> Decisão da IA -> Chamada de Ferramenta -> Resultado da Ferramenta -> Decisão da IA -> ... -> Resposta Final).
* **"Jaula" de Segurança:** Todas as operações de arquivo são restritas a um diretório de trabalho (`./calculator`) para prevenir que o agente acesse ou modifique arquivos do sistema fora do escopo do projeto.
* **Conjunto de Ferramentas (Toolbelt):** A IA pode escolher e executar quatro funções principais:
    1. `get_files_info`: Listar arquivos e diretórios.
    2. `get_file_content`: Ler o conteúdo de arquivos (com limite de 10.000 caracteres).
    3. `write_file`: Escrever ou sobrescrever arquivos.
    4. `run_python_file`: Executar scripts Python (`.py`) dentro da "jaula".
* **Modo Detalhado (`--verbose`):** Permite ao usuário assistir ao "processo de pensamento" do agente em tempo real, vendo cada chamada de função e seu resultado.

## 🛠️ Tecnologias Utilizadas

* **Python 3.10+**
* **Google Gemini (API):** Modelo `gemini-2.0-flash-001` como o "cérebro" do agente.
* **`google-generativeai`:** Biblioteca cliente oficial do Google.
* **`uv`:** Gerenciador de pacotes e ambiente virtual.
* **`python-dotenv`:** Para gerenciamento seguro de chaves de API.

## 🚀 Configuração e Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/vini-haa/ai-agent-project.git
   cd ai-agent-project
   ```

2. **Crie e ative o ambiente virtual:**
   ```bash
   uv venv
   source .venv/bin/activate
   ```

3. **Instale as dependências:**
   (Se você seguiu o projeto, o `uv` pode já ter o `pyproject.toml` configurado. Caso contrário, adicione as dependências manualmente.)
   ```bash
   uv add google-generativeai python-dotenv
   ```

4. **Crie seu arquivo `.env`:**
   Você precisa de uma chave de API do Google Gemini.
   ```bash
   echo "GEMINI_API_KEY=SUA_CHAVE_API_AQUI" > .env
   ```
   (Substitua `SUA_CHAVE_API_AQUI` pela sua chave real.)

## 🤖 Como Usar

O agente é executado diretamente pelo `main.py`, recebendo um prompt como argumento.

### Exemplo 1: Fazer uma pergunta (Inspeção)

Este comando pede ao agente para analisar o código e explicar uma funcionalidade.

```bash
uv run python main.py "como a calculadora renderiza os resultados?"
```

### Exemplo 2: Corrigir um bug (Ação)

Este comando dá ao agente uma tarefa complexa: encontrar um bug, analisar o código, escrever uma correção e verificar seu trabalho.

```bash
uv run python main.py "corrija o bug: 3 + 7 * 2 não deveria ser 20" --verbose
```

O flag `--verbose` é altamente recomendado para que você possa ver o agente trabalhar:

```
User prompt: corrija o bug: 3 + 7 * 2 não deveria ser 20
 - Calling function: get_files_info
 - Calling function: get_file_content
 - Calling function: write_file
 - Calling function: run_python_file
...
Final response:
All tests passed! The issue with operator precedence has been resolved.
```

## 🚨 AVISO DE SEGURANÇA 🚨

Este é um projeto de aprendizado e **NÃO É SEGURO** para uso em produção ou em sistemas reais.

O agente tem a capacidade de executar código arbitrário (`run_python_file`) e sobrescrever arquivos (`write_file`) dentro do seu diretório de trabalho. Embora tenhamos criado uma "jaula" de segurança, ela é rudimentar.

**Execute este projeto apenas em um ambiente controlado e isolado.**
