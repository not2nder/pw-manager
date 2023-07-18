import os
import re
import datetime as dt
import time

import sqlite3

from rich import print
from rich.table import Table
from rich.console import Console
from rich.panel import Panel

from pick import pick
import keyboard as kb
import pwinput as pw
import webbrowser
import clipboard as cb

console = Console()

def get_latest_date():
    return f"{dt.datetime.now().strftime('%X')[0:5]}, {dt.datetime.now().strftime('%x')}"

class Senha:
    def __init__(self, user: str, serv: str, senha: str):
        self.user = user
        self.serv = serv
        self.senha = senha
        self.data = get_latest_date()
        cur.execute("SELECT * FROM senhas")
        rows = cur.fetchall()
        self.id_senha = 1 if len(rows)==0 else rows[(len(rows)-1)][4]+1

con = sqlite3.connect("passwords.db")
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS senhas (
            user TEXT NOT NULL,
            serv TEXT NOT NULL,
            senha TEXT NOT NULL,
            data_mod TEXT NOT NULL,
            senha_id INTEGER NOT NULL
        )
''')

def count_columns(message:str):
    cur.execute("SELECT *from senhas")
    if len(cur.fetchall()) >0:
        pass
    else:
        os.system('cls')
        print(f"[i]{message}")
        time.sleep(1)
        print("[i]Voltando ao menu...[/i]")
        time.sleep(1)
        menu()

def check_id(id):
    cur.execute("SELECT * FROM senhas")
    rows = (cur.fetchall())
    return [id == rows[i][4] for i in range(len(rows))]

def color(input:str):
    servs = {
    "google":"[blue]G[red]o[yellow]o[blue]g[green]l[red]e",
    "youtube":"[red]You[white]Tube",
    "twitter":"[bright_cyan]Twitter",
    "instagram":"[bright_magenta]Instagram",
    "discord":"[blue]Discord",
    "twitch":"[purple4]Twitch",
    "github":"[purple3]Github",
    "pinterest":"[red1]Pinterest",
    "soundcloud":"[orange_red1]Soundcloud",
    "gmail":"[blue]G[red]m[yellow]a[blue]i[green]l",
    "facebook":"[blue3]Facebook",
    "":"[i]???",
    }
    if input.lower() in servs:
        return f"[bold]{servs[input.lower()]}[/bold]"
    else:
        return f"[bold]{input}[/bold]"

def pass_strength(senha):
    patterns = [r"[a-z]{8,}",r"[A-Z]{2,}",r"\W+",r"\d+"]
    if all([re.findall(item,senha) for item in patterns]):
        return f"[chartreuse3]{senha}"
    elif not(any([re.findall(item,senha) for item in patterns])):
        return f"[red]{senha}[/red]"
    else:
        return f"[orange3]{senha}"

def confirm_options():
    os.system('cls')
    time.sleep(0.3)
    print("[bold]Continuar?[/bold]")
    print("\n[bold][green][S] Sim \n[red][N] Não (Voltar)[/bold]")
    while True:
        if kb.is_pressed("s"):
            kb.press("backspace")
            pass
            break
        elif kb.is_pressed("n"):
            kb.press("backspace")
            menu()
            break
    print()

def mostrar(back_option=True, show_marks=True):
    os.system('cls')
    time.sleep(0.1)
    tabela = Table(title="Senhas")
    tabela.add_column("USUÁRIO|EMAIL",style="bold grey89",justify="center"); tabela.add_column("SERVIÇO|USO",justify="center")
    tabela.add_column("SENHA",justify="center"); tabela.add_column("DATA. MOD",justify="center")
    tabela.add_column("ID",style="cyan3",justify="center")

    rows = cur.execute("SELECT * FROM senhas")
    for row in rows:
        tabela.add_row(row[0],color(str(row[1])),pass_strength(row[2]),row[3],str(row[4]))
    console.print(tabela)

    if (show_marks):
        print("\n[chartreuse3]● - Forte[/chartreuse3] \n[orange3]● - Média \n[red]● - Fraca")

    if (back_option):
        print("\n[bold red][X] Voltar")
        while True:
            if kb.is_pressed("x"):
                kb.press("backspace")
                menu()
                break
    else:
        pass

def atualizar():
    confirm_options()
    while True:
        user = input("Usuário|Email: ")
        if user == "":
            print("[bold red]O CAMPO NÃO PODE FICAR EM BRANCO!\n")
            time.sleep(0.3)
        else:
            serv = input("Serviço|Categoria: ")
            senha = pw.pwinput(prompt="Senha: ",mask='*')
            if senha == "":
                print("[bold red]O CAMPO NÃO PODE FICAR EM BRANCO!\n")
                time.sleep(0.3)
            else:
                senha_confirm = pw.pwinput(prompt="Confirme a Senha Digitada: ",mask='*')
                if not(confirm(senha,senha_confirm)):
                    print("[bold red]Senhas não correspondem[/red][/bold]\n")
                    time.sleep(0.3)
                else:
                    dados_senha = Senha(user,serv,senha)
                    cur.execute('''INSERT INTO senhas (user,senha,serv,data_mod,senha_id)
                        VALUES (?,?,?,?,?)''', (dados_senha.user, dados_senha.senha,
                                                dados_senha.serv,dados_senha.data,
                                                dados_senha.id_senha))
                    con.commit()
                    mostrar(back_option=True)
                    break

def modificar():
    count_columns("Não Há Senhas para Modificar")
    confirm_options()
    mostrar(back_option=False,show_marks=False)
    while True:
        try:
            id = int(input("Digite o ID da senha: "))
            if not(any(check_id(id))):
                print("[bold red]ID INEXISTENTE!\n")
                time.sleep(0.3)
            else:
                idd = int(input("Confirme o ID: "))
                if not(confirm(id,idd)):
                    print("[bold red] IDs NÇAO CORRESPONDEM!\n")
                    time.sleep(0.3)
                else:
                    time.sleep(0.3)
                    print()
                    senha = pw.pwinput(prompt="Digite a Nova Senha: ", mask='*')
                    if senha == "":
                        print("[bold red]O CAMPO NÃO PODE FICAR EM BRANCO!\n")
                        time.sleep(0.3)
                    else:
                        con.execute('''UPDATE senhas SET senha=?, data_mod=? WHERE senha_id=?''',(senha,get_latest_date(),id))
                        con.commit()
                        mostrar(back_option=True)
                        pass
                    break
        except ValueError:
            print("[bold red]O CAMPO NÃO PODE FICAR EM BRANCO!\n")

confirm = lambda x,y: x==y

def deletar():
    count_columns("Não há Senhas para Deletar")
    confirm_options()
    os.system('cls')
    time.sleep(0.1)
    mostrar(back_option=False,show_marks=False)
    print("\n[bold]Obs: Digite [cyan]'sair'[/cyan] para [red]Cancelar[/red]")

    while True:
        id = str(input("Informe o ID da senha: ")).lower()
        if(id != "sair"):
            idd = str(input("Confirme o ID digitado: "))
            if not(confirm(id,idd)):
                print("[bold][red]IDs NÇAO CORRESPONDEM!\n[/red][/bold]\n")
                time.sleep(0.1)
            else:
                cur.execute('''DELETE FROM senhas WHERE senha_id=?''',(id,))
                con.commit()

                time.sleep(0.3)
                print("[bold][green]SENHA DELETADA COM SUCESSO![/green][/bold]")
                print(1.0)
                mostrar()
                break
        else:
            break

def escolha(lista:list, titulo:str,indicador:str):
    option, index = pick(lista,titulo,indicator=indicador)
    return option

def github():
    webbrowser.open("www.github.com/not2nder")
    time.sleep(0.3)
    menu()

def menu():
    title = '''                                              
    █▀█ █ █   █▄█ █▀█ █▀█ █▀█ █▀▀ █▀▀ █▀█
    █▀▀ █▄█   █ █ █▀█ █ █ █▀█ █ █ █▀▀ █▀▄
    ▀   ▀ ▀   ▀ ▀ ▀ ▀ ▀ ▀ ▀ ▀ ▀▀▀ ▀▀▀ ▀ ▀
            GERENCIADOR DE SENHAS 
    '''

    options = ["Mostrar Senhas","Criar Nova","Deletar","Modificar","Sair","Github"]
    op = escolha(options,title,"•")

    commands = {
        "Mostrar Senhas":mostrar,
        "Criar Nova":atualizar,
        "Deletar":deletar,
        "Github":github,
        "Modificar":modificar,
    }

    if op in commands:
        func = commands[op]
        func()
menu()