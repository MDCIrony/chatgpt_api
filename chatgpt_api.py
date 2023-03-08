import openai  # pip install openai
import typer  # pip install "typer[all]"
import os
import sys
import argparse
from rich import print  # pip install rich
from rich.table import Table
from dotenv import load_dotenv  # pip install python-dotenv

load_dotenv()

#Taking the API key from the .env file
API_KEY = os.getenv("API_KEY")

#Taking the user parameters in the initial call

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--content", help="Content to be sent to the API", type=str)
args = parser.parse_args()

"""
Webs de interés:
- Módulo OpenAI: https://github.com/openai/openai-python
- Documentación API ChatGPT: https://platform.openai.com/docs/api-reference/chat
- Typer: https://typer.tiangolo.com
- Rich: https://rich.readthedocs.io/en/stable/
"""

def regular(content_parameter: str) -> None:
    openai.api_key = API_KEY

    context = {"role": "system",
               "content": "Eres un asistente muy útil."}
    messages = [context]

    content = content_parameter

    messages.append({"role": "user", "content": content})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages)
    
    response_content = response.choices[0].message.content

    print(response_content)

def main():
    
    openai.api_key = API_KEY

    print("💬 [bold green]ChatGPT API en Python[/bold green]")

    table = Table("Comando", "Descripción")
    table.add_row("exit", "Salir de la aplicación")
    table.add_row("new", "Crear una nueva conversación")

    print(table)

    # Contexto del asistente
    context = {"role": "system",
               "content": "Eres un asistente muy útil."}
    messages = [context]

    while True:

        content = __prompt()

        if content == "new":
            print("🆕 Nueva conversación creada")
            messages = [context]
            content = __prompt()

        messages.append({"role": "user", "content": content})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages)

        response_content = response.choices[0].message.content

        messages.append({"role": "assistant", "content": response_content})

        print(f"[bold green]> [/bold green] [green]{response_content}[/green]")


def __prompt() -> str:
    prompt = typer.prompt("\n¿Sobre qué quieres hablar? ")

    if prompt == "exit":
        exit = typer.confirm("✋ ¿Estás seguro?")
        if exit:
            print("👋 ¡Hasta luego!")
            raise typer.Abort()

        return __prompt()

    return prompt


if __name__ == "__main__":
    if args.content:
        regular(args.__contains__("content"))
    typer.run(main)
    