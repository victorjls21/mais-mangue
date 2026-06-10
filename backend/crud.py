import os # caminhos de arquivos e pastas
import sqlite3 # trabalhar com banco de dados SQLite
import hashlib  # usada para criar hash de senha
import secrets #  usada para gerar valores aleatórios seguros

# Define o caminho do banco de dados database.db
# Ele será criado na mesma pasta onde este arquivo Python estiver salvo
DB_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")

# Cria uma função para conectar ao banco de dados
def conectar():
    # Abre uma conexão com o banco SQLite
    conn = sqlite3.connect(DB_NAME)
     # Permite acessar os dados pelo nome da coluna, e não apenas por posição
    conn.row_factory = sqlite3.Row
    # Retorna a conexão criada
    return conn

# Cria uma função para criar a tabela de usuários
def create_table():
    # Abre conexão com o banco
    conn = conectar()
    # Executa um comando SQL para criar a tabela usuarios, caso ela ainda não exista
    conn.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario         TEXT NOT NULL UNIQUE,
            nome_completo   TEXT NOT NULL,
            email           TEXT NOT NULL UNIQUE,
            data_nascimento TEXT NOT NULL,
            genero          TEXT NOT NULL,
            senha_hash      TEXT NOT NULL,
            senha_salt      TEXT NOT NULL
        )
    """)
    conn.commit() # Salva as alterações feitas no banco
    conn.close() # Fecha a conexão com o banco

# Cria uma função para transformar a senha em hash
def _embaralhar_senha(senha, salt=None):
    if salt is None: # Verifica se o salt não foi informado
        salt = secrets.token_hex(16)  # Gera um salt aleatório seguro
    codigo = hashlib.pbkdf2_hmac("sha256", senha.encode(), salt.encode(), 260_000)  # Cria o hash da senha usando o algoritmo SHA-256 com PBKDF2
    return codigo.hex(), salt  # Retorna o hash em formato hexadecimal e o salt utilizado

# Cria uma função para cadastrar um novo usuário
def criar_usuario(usuario, nome_completo, email, data_nascimento, genero, senha):
    senha_hash, senha_salt = _embaralhar_senha(senha)  # Gera o hash e o salt da senha informada

    conn = conectar()  # Abre conexão com o banco
    cursor = conn.execute(                                   # Insere os dados do usuário na tabela usuarios
        """INSERT INTO usuarios
           (usuario, nome_completo, email, data_nascimento, genero, senha_hash, senha_salt)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (usuario, nome_completo, email, data_nascimento, genero, senha_hash, senha_salt),
    )
    conn.commit() # Salva o cadastro no banco
    conn.close() # Fecha a conexão
    return cursor.lastrowid # Retorna o ID do usuário recém-criado

# Cria uma função para listar todos os usuários
def listar_usuarios():
    conn = conectar() # Abre conexão com o banco
    linhas = conn.execute(           # Busca os usuários cadastrados, sem mostrar senha_hash e senha_salt
        "SELECT id, usuario, nome_completo, email, data_nascimento, genero FROM usuarios ORDER BY id"
    ).fetchall()
    conn.close()  # Fecha a conexão
    return [dict(linha) for linha in linhas] # Converte cada linha do banco em dicionário e retorna a lista

# Cria uma função para buscar um usuário pelo ID
def buscar_usuario(usuario_id):
    conn = conectar() # Abre conexão com o banco
    linha = conn.execute(               # Busca apenas um usuário com o ID informado
        "SELECT id, usuario, nome_completo, email, data_nascimento, genero FROM usuarios WHERE id = ?",
        (usuario_id,),
    ).fetchone()
    conn.close()  # Fecha a conexão
    return dict(linha) if linha else None # Se encontrou o usuário, retorna como dicionário; caso contrário, retorna None


def buscar_por_login(identificador):
    conn = conectar()
    linha = conn.execute(
        """SELECT id, usuario, nome_completo, email, data_nascimento, genero
           FROM usuarios WHERE usuario = ? OR LOWER(email) = LOWER(?)""",
        (identificador, identificador),
    ).fetchone()
    conn.close()
    return dict(linha) if linha else None


def verificar_senha(usuario_id, senha): # Cria uma função para verificar se a senha digitada está correta
    conn = conectar()
    linha = conn.execute( # Busca o hash e o salt da senha do usuário
        "SELECT senha_hash, senha_salt FROM usuarios WHERE id = ?", (usuario_id,)
    ).fetchone()
    conn.close()

    if linha is None:  # Se o usuário não existir, retorna False
        return False
    codigo, _ = _embaralhar_senha(senha, linha["senha_salt"])     # Gera novamente o hash da senha digitada usando o mesmo salt salvo
    return secrets.compare_digest(codigo, linha["senha_hash"])    # Compara o hash gerado com o hash salvo no banco

# Cria uma função para atualizar os dados cadastrais do usuário
def atualizar_usuario(usuario_id, usuario, nome_completo, email, data_nascimento, genero):
    conn = conectar()
    cursor = conn.execute(  # Atualiza os dados do usuário com base no ID
        """UPDATE usuarios
           SET usuario = ?, nome_completo = ?, email = ?, data_nascimento = ?, genero = ?
           WHERE id = ?""",
        (usuario, nome_completo, email, data_nascimento, genero, usuario_id),
    )
    conn.commit() # Salva a atualização no banco
    conn.close()
    return cursor.rowcount > 0 # Retorna True se algum usuário foi atualizado


def atualizar_senha(usuario_id, senha_nova): # Cria uma função para atualizar apenas a senha do usuário
    senha_hash, senha_salt = _embaralhar_senha(senha_nova) # Gera novo hash e novo salt para a senha nova

    conn = conectar()
    cursor = conn.execute(        # Atualiza a senha_hash e senha_salt do usuário
        "UPDATE usuarios SET senha_hash = ?, senha_salt = ? WHERE id = ?",
        (senha_hash, senha_salt, usuario_id),
    )
    conn.commit()
    conn.close()
    return cursor.rowcount > 0 # Retorna True se a senha foi atualizada

# Cria uma função para deletar um usuário
def deletar_usuario(usuario_id):
    conn = conectar()
    cursor = conn.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))  # Deleta o usuário pelo ID
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

# Cria uma função para exibir os usuários no terminal
def exibir_usuarios(usuarios):
    if not usuarios:   # Se a lista estiver vazia, mostra mensagem
        print("Nenhum usuário encontrado.")
        return
    print("\nID  | Usuário        | Nome completo")  # Cabeçalho da tabela exibida no terminal
    print("-" * 50) # Linha separadora
    for u in usuarios: # Percorre cada usuário da lista
        print(f"{u['id']:<3} | {u['usuario']:<14} | {u['nome_completo']}") # Mostra ID, usuário e nome completo formatados
    print()  # Pula uma linha no final

# Cria o menu principal do sistema
def menu():
    create_table() # Garante que a tabela exista antes de iniciar o sistema
    while True: # Cria um loop infinito para manter o menu funcionando
        print("\n===== CRUD de Usuários =====") # Exibe as opções do CRUD
        print("1 - Listar usuários")
        print("2 - Criar usuário")
        print("3 - Atualizar usuário")
        print("4 - Apagar usuário")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ").strip()  # Lê a opção digitada pelo usuário

        if opcao == "1": # Se a opção for 1, lista os usuários
            exibir_usuarios(listar_usuarios())

        elif opcao == "2": # Se a opção for 2, cria um novo usuário
            usuario = input("Usuário: ")
            nome = input("Nome completo: ")
            email = input("E-mail: ")
            nascimento = input("Data de nascimento: ")
            genero = input("Gênero: ")
            senha = input("Senha: ")
            novo_id = criar_usuario(usuario, nome, email, nascimento, genero, senha)  # Chama a função de criação de usuário
            print(f"Usuário criado com id {novo_id}.") # Mostra o ID do novo usuário

        elif opcao == "3":  # Se a opção for 3, atualiza um usuário existente
            uid = int(input("ID do usuário: "))
            usuario = input("Novo usuário: ")
            nome = input("Novo nome completo: ")
            email = input("Novo e-mail: ")
            nascimento = input("Nova data de nascimento: ")
            genero = input("Novo gênero: ")
            if atualizar_usuario(uid, usuario, nome, email, nascimento, genero):   # Chama a função de atualização
                print("Usuário atualizado.")
            else:
                print("Usuário não encontrado.")

        elif opcao == "4":  # Se a opção for 4, apaga um usuário
            uid = int(input("ID do usuário: "))
            if deletar_usuario(uid):
                print("Usuário apagado.")
            else:
                print("Usuário não encontrado.")

        elif opcao == "0": # Se a opção for 0, encerra o programa
            print("Saindo...")
            break

        else: # Se digitar algo diferente das opções válidas
            print("Opção inválida.")


if __name__ == "__main__": # Verifica se este arquivo está sendo executado diretamente
    menu()     # Chama a função menu para iniciar o programa

