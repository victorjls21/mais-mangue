# Importa a biblioteca os para trabalhar com caminhos de arquivos
import os

# Importa sqlite3 para usar banco de dados SQLite
import sqlite3


# Define o nome e o caminho do banco de dados
DB_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mangue.db")


# Função para conectar ao banco de dados
def conectar():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# Função para criar as tabelas do sistema
def criar_tabelas():
    conn = conectar()

    # Tabela das denúncias feitas pela população
    conn.execute("""
        CREATE TABLE IF NOT EXISTS denuncias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            localizacao TEXT NOT NULL,
            descricao TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    # Tabela dos projetos ambientais
    conn.execute("""
        CREATE TABLE IF NOT EXISTS projetos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            area TEXT NOT NULL,
            valor REAL NOT NULL,
            status TEXT NOT NULL
        )
    """)

    # Tabela dos investimentos feitos pelas empresas
    conn.execute("""
        CREATE TABLE IF NOT EXISTS investimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa TEXT NOT NULL,
            projeto TEXT NOT NULL,
            valor REAL NOT NULL,
            carbono_compensado REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()



# APP DA POPULAÇÃO


# CREATE: registra uma nova denúncia
def registrar_denuncia(tipo, localizacao, descricao):
    conn = conectar()

    cursor = conn.execute(
        """INSERT INTO denuncias
           (tipo, localizacao, descricao, status)
           VALUES (?, ?, ?, ?)""",
        (tipo, localizacao, descricao, "Em análise"),
    )

    conn.commit()
    conn.close()
    return cursor.lastrowid


# READ: lista todas as denúncias
def listar_denuncias():
    conn = conectar()

    linhas = conn.execute(
        "SELECT id, tipo, localizacao, descricao, status FROM denuncias ORDER BY id"
    ).fetchall()

    conn.close()
    return [dict(linha) for linha in linhas]


# UPDATE: atualiza o status de uma denúncia
def atualizar_status_denuncia(denuncia_id, novo_status):
    conn = conectar()

    cursor = conn.execute(
        "UPDATE denuncias SET status = ? WHERE id = ?",
        (novo_status, denuncia_id),
    )

    conn.commit()
    conn.close()
    return cursor.rowcount > 0


# DELETE: apaga uma denúncia pelo ID
def deletar_denuncia(denuncia_id):
    conn = conectar()

    cursor = conn.execute(
        "DELETE FROM denuncias WHERE id = ?",
        (denuncia_id,),
    )

    conn.commit()
    conn.close()
    return cursor.rowcount > 0


# Função para calcular EcoPontos
def calcular_ecopontos(qtd_denuncias, qtd_participacoes):
    pontos = (qtd_denuncias * 10) + (qtd_participacoes * 30)

    if pontos >= 200:
        ranking = "Ouro"
    elif pontos >= 100:
        ranking = "Prata"
    else:
        ranking = "Bronze"

    return pontos, ranking



# PLATAFORMA DAS EMPRESAS


# CREATE: cria um projeto ambiental
def criar_projeto(nome, area, valor):
    conn = conectar()

    cursor = conn.execute(
        """INSERT INTO projetos
           (nome, area, valor, status)
           VALUES (?, ?, ?, ?)""",
        (nome, area, valor, "Ativo"),
    )

    conn.commit()
    conn.close()
    return cursor.lastrowid


# READ: lista os projetos ambientais
def listar_projetos():
    conn = conectar()

    linhas = conn.execute(
        "SELECT id, nome, area, valor, status FROM projetos ORDER BY id"
    ).fetchall()

    conn.close()
    return [dict(linha) for linha in linhas]


# UPDATE: atualiza os dados de um projeto ambiental
def atualizar_projeto(projeto_id, nome, area, valor, status):
    conn = conectar()

    cursor = conn.execute(
        """UPDATE projetos
           SET nome = ?, area = ?, valor = ?, status = ?
           WHERE id = ?""",
        (nome, area, valor, status, projeto_id),
    )

    conn.commit()
    conn.close()
    return cursor.rowcount > 0


# DELETE: apaga um projeto ambiental pelo ID
def deletar_projeto(projeto_id):
    conn = conectar()

    cursor = conn.execute(
        "DELETE FROM projetos WHERE id = ?",
        (projeto_id,),
    )

    conn.commit()
    conn.close()
    return cursor.rowcount > 0


# Calcula a pegada de carbono estimada da empresa
def calcular_carbono(consumo_energia, km_frota, residuos):
    carbono = (consumo_energia * 0.0005) + (km_frota * 0.0002) + (residuos * 0.8)
    return carbono


# Registra investimento de uma empresa em um projeto
def investir_em_projeto(empresa, projeto, valor):
    carbono_compensado = valor * 0.05

    conn = conectar()

    cursor = conn.execute(
        """INSERT INTO investimentos
           (empresa, projeto, valor, carbono_compensado)
           VALUES (?, ?, ?, ?)""",
        (empresa, projeto, valor, carbono_compensado),
    )

    conn.commit()
    conn.close()

    return cursor.lastrowid, carbono_compensado


# Lista os investimentos cadastrados
def listar_investimentos():
    conn = conectar()

    linhas = conn.execute(
        "SELECT id, empresa, projeto, valor, carbono_compensado FROM investimentos ORDER BY id"
    ).fetchall()

    conn.close()
    return [dict(linha) for linha in linhas]


# Gera um relatório ESG simples no terminal
def gerar_relatorio_esg():
    denuncias = listar_denuncias()
    projetos = listar_projetos()
    investimentos = listar_investimentos()

    total_investido = sum(i["valor"] for i in investimentos)
    total_carbono = sum(i["carbono_compensado"] for i in investimentos)

    print("\n===== RELATÓRIO ESG +MANGUE =====")
    print(f"Denúncias registradas: {len(denuncias)}")
    print(f"Projetos ativos: {len(projetos)}")
    print(f"Total investido: R$ {total_investido:.2f}")
    print(f"Carbono compensado estimado: {total_carbono:.2f} tCO2e")
    print("Certificação: Selo ODS 13")
    print("=================================\n")


# Função para exibir listas no terminal
def exibir_lista(lista):
    if not lista:
        print("Nenhum registro encontrado.")
        return

    for item in lista:
        print(item)



# MENU DO APP


def menu_app():
    while True:
        print("\n===== APP POPULAÇÃO =====")
        print("1 - Registrar denúncia")
        print("2 - Listar denúncias")
        print("3 - Atualizar status da denúncia")
        print("4 - Apagar denúncia")
        print("5 - Ver EcoPontos")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            tipo = input("Tipo do problema: ")
            localizacao = input("Localização: ")
            descricao = input("Descrição: ")

            novo_id = registrar_denuncia(tipo, localizacao, descricao)
            print(f"Denúncia registrada com id {novo_id}.")

        elif opcao == "2":
            exibir_lista(listar_denuncias())

        elif opcao == "3":
            denuncia_id = int(input("ID da denúncia: "))
            novo_status = input("Novo status: ")

            if atualizar_status_denuncia(denuncia_id, novo_status):
                print("Status atualizado.")
            else:
                print("Denúncia não encontrada.")

        elif opcao == "4":
            denuncia_id = int(input("ID da denúncia: "))

            if deletar_denuncia(denuncia_id):
                print("Denúncia apagada com sucesso.")
            else:
                print("Denúncia não encontrada.")

        elif opcao == "5":
            qtd_denuncias = len(listar_denuncias())
            qtd_participacoes = int(input("Quantidade de ações ambientais que participou: "))

            pontos, ranking = calcular_ecopontos(qtd_denuncias, qtd_participacoes)
            print(f"Você possui {pontos} EcoPontos. Ranking: {ranking}")

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")



# MENU DA PLATAFORMA


def menu_plataforma():
    while True:
        print("\n===== PLATAFORMA EMPRESAS =====")
        print("1 - Criar projeto ambiental")
        print("2 - Listar projetos")
        print("3 - Atualizar projeto")
        print("4 - Apagar projeto")
        print("5 - Calcular carbono")
        print("6 - Investir em projeto")
        print("7 - Gerar relatório ESG")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome do projeto: ")
            area = input("Área/local do projeto: ")
            valor = float(input("Valor necessário: "))

            novo_id = criar_projeto(nome, area, valor)
            print(f"Projeto criado com id {novo_id}.")

        elif opcao == "2":
            exibir_lista(listar_projetos())

        elif opcao == "3":
            projeto_id = int(input("ID do projeto: "))
            nome = input("Novo nome: ")
            area = input("Nova área/local: ")
            valor = float(input("Novo valor: "))
            status = input("Novo status: ")

            if atualizar_projeto(projeto_id, nome, area, valor, status):
                print("Projeto atualizado.")
            else:
                print("Projeto não encontrado.")

        elif opcao == "4":
            projeto_id = int(input("ID do projeto: "))

            if deletar_projeto(projeto_id):
                print("Projeto apagado com sucesso.")
            else:
                print("Projeto não encontrado.")

        elif opcao == "5":
            energia = float(input("Consumo de energia (kWh): "))
            km = float(input("Km rodados pela frota: "))
            residuos = float(input("Resíduos gerados (toneladas): "))

            carbono = calcular_carbono(energia, km, residuos)
            print(f"Pegada de carbono estimada: {carbono:.2f} tCO2e")

        elif opcao == "6":
            empresa = input("Nome da empresa: ")
            projeto = input("Nome do projeto apoiado: ")
            valor = float(input("Valor do investimento: "))

            investimento_id, carbono = investir_em_projeto(empresa, projeto, valor)

            print(f"Investimento registrado com id {investimento_id}.")
            print(f"Carbono compensado estimado: {carbono:.2f} tCO2e")

        elif opcao == "7":
            gerar_relatorio_esg()

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")



# MENU PRINCIPAL


def menu_principal():
    criar_tabelas()

    while True:
        print("\n===== +MANGUE =====")
        print("1 - App da população")
        print("2 - Plataforma das empresas")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_app()

        elif opcao == "2":
            menu_plataforma()

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")


# Inicia o programa
if __name__ == "__main__":
    menu_principal()