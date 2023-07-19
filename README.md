## `🔐` PW Manager

### Gerenciador de senhas

## `💻` Requisitos
1. Python Instalado
- [Windows](https://www.python.org/downloads/)
     - Choco: `choco install python`
   - [Mac](https://www.python.org/downloads/)
     - Brew: `brew install python3` and `brew install pip3`
   - [Ubuntu Guide](https://linuxize.com/post/how-to-install-python-3-9-on-ubuntu-20-04/)

### `⚙` Instalação
1. Execute o arquivo `setup.py` **apenas na PRIMEIRA instalação**
2. Execute o arquivo `main.py`

### `❓` Como usar?

- Todas as senhas são mostradas em uma tabela. As quais ficam salvas no arquivo `passwords.db`.
- organização dos dados na tabela:

  | COLUNA        | CONTEÚDO                                       |
  |---------------|------------------------------------------------|
  | USUÁRIO/EMAIL | usuário ou email da senha guardada             |
  | SERVIÇO/USO   | aplicaivo ou sistema onde a senha é usada      |
  | SENHA         | senha armazenada                               |
  | DATA. MOD     | data de criação ou última modificação da senha |
  | ID            | Identificador na senha no banco de dados       |

- Para Salvar uma nova senha, basta descer as opções do menu e selecionar `Criar Nova`
    - Preencha os dados pedidos e confirme digitando a senha **duas vezes** e a senha ficará salva.
- Para deletar uma senha, basta selecionar no menu a opção `Deletar`
    - Digite o `ID` da senha que deseja deletar e confirme.
    - `⚠️` Você também pode digitar `'sair'` caso queira cancelar a operação
- Para modificar uma senha, desca as opções do menu até `Modificar`
- Cada Serviço de senha possui sua própria cor na tabela
- Cada senha aparece com uma cor diferente dependendo do quão forte ela é (essa função não está 100% finalizada)



### Mostrando a aplicação
Menu Inicial

![](img/menu.png)

Tabela de senhas

![](img/table.png)

### Classificação de senhas:

| CLASSIFICAÇÃO | DESCRIÇÃO                                                                                                                            |
|---------------|--------------------------------------------------------------------------------------------------------------------------------------|
| **Forte**     | possuí 1 ou mais caracteres minúsculos, 2  maiúsculos, 2 ou mais números, um ou mais caracteres especiais e tem mais de 8 caracteres |
| **Média**     | atende a ao menos 4 das exigências acima                                                                                             |
| **Fraca**     | atende a menos que 4 das exigências citadas                                                                                          |


### `⚙️` Futuras atualizações
1. Gerador de senha
2. Função de copiar senha pelo id
