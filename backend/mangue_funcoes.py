import os
import sqlite3

DB_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mangue.db")


def conectar():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def criar_tabelas():
    conn = conectar()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS denuncias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            localizacao TEXT NOT NULL,
            descricao TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS projetos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            area TEXT NOT NULL,
            valor REAL NOT NULL,
            status TEXT NOT NULL
        )
    """)

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


# =========================
# FUNÇÕES DO APP - POPULAÇÃO
# =========================

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


def listar_denuncias():
    conn = conectar()
    linhas = conn.execute(
        "SELECT id, tipo, localizacao, descricao, status FROM denuncias ORDER BY id"
    ).fetchall()
    conn.close()
    return [dict(linha) for linha in linhas]


def atualizar_status_denuncia(denuncia_id, novo_status):
    conn = conectar()
    cursor = conn.execute(
        "UPDATE denuncias SET status = ? WHERE id = ?",
        (novo_status, denuncia_id),
    )
    conn.commit()
    conn.close()
    return cursor.rowcount > 0


def calcular_ecopontos(qtd_denuncias, qtd_participacoes):
    pontos = (qtd_denuncias * 10) + (qtd_participacoes * 30)

    if pontos >= 200:
        ranking = "Ouro"
    elif pontos >= 100:
        ranking = "Prata"
    else:
        ranking = "Bronze"

    return pontos, ranking


# =========================
# FUNÇÕES DA PLATAFORMA - EMPRESAS
# =========================

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


def listar_projetos():
    conn = conectar()
    linhas = conn.execute(
        "SELECT id, nome, area, valor, status FROM projetos ORDER BY id"
    ).fetchall()
    conn.close()
    return [dict(linha) for linha in linhas]


def calcular_carbono(consumo_energia, km_frota, residuos):
    carbono = (consumo_energia * 0.0005) + (km_frota * 0.0002) + (residuos * 0.8)
    return carbono


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


def listar_investimentos():
    conn = conectar()
    linhas = conn.execute(
        "SELECT id, empresa, projeto, valor, carbono_compensado FROM investimentos ORDER BY id"
    ).fetchall()
    conn.close()
    return [dict(linha) for linha in linhas]


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


# =========================
# EXIBIÇÃO
# =========================

def exibir_lista(lista):
    if not lista:
        print("Nenhum registro encontrado.")
        return

    for item in lista:
        print(item)


# =========================
# MENU DO APP
# =========================

def menu_app():
    while True:
        print("\n===== APP POPULAÇÃO =====")
        print("1 - Registrar denúncia")
        print("2 - Listar denúncias")
        print("3 - Ver EcoPontos")
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
            qtd_denuncias = len(listar_denuncias())
            qtd_participacoes = int(input("Quantidade de ações ambientais que participou: "))
            pontos, ranking = calcular_ecopontos(qtd_denuncias, qtd_participacoes)
            print(f"Você possui {pontos} EcoPontos. Ranking: {ranking}")

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")


# =========================
# MENU DA PLATAFORMA
# =========================

def menu_plataforma():
    while True:
        print("\n===== PLATAFORMA EMPRESAS =====")
        print("1 - Criar projeto ambiental")
        print("2 - Listar projetos")
        print("3 - Calcular carbono")
        print("4 - Investir em projeto")
        print("5 - Gerar relatório ESG")
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
            energia = float(input("Consumo de energia (kWh): "))
            km = float(input("Km rodados pela frota: "))
            residuos = float(input("Resíduos gerados (toneladas): "))
            carbono = calcular_carbono(energia, km, residuos)
            print(f"Pegada de carbono estimada: {carbono:.2f} tCO2e")

        elif opcao == "4":
            empresa = input("Nome da empresa: ")
            projeto = input("Nome do projeto apoiado: ")
            valor = float(input("Valor do investimento: "))
            investimento_id, carbono = investir_em_projeto(empresa, projeto, valor)
            print(f"Investimento registrado com id {investimento_id}.")
            print(f"Carbono compensado estimado: {carbono:.2f} tCO2e")

        elif opcao == "5":
            gerar_relatorio_esg()

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")


# =========================
# MENU PRINCIPAL
# =========================

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


if __name__ == "__main__":
    menu_principal()