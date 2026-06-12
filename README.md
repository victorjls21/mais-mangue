# 🦀 +Mangue

> Plataforma ambiental de preservação dos **manguezais urbanos do Recife** — Pernambuco, Brasil.
> Conecta cidadãos, voluntários e empresas em torno da recuperação dos manguezais. **ODS 13**.

O projeto é dividido em duas partes que rodam juntas:

| Parte | Tecnologia | Pasta | Porta |
| --- | --- | --- | --- |
| **Frontend** | React + Vite + TypeScript + Tailwind | [`frontend/`](frontend/) | `5173` |
| **Backend** | Python + Flask + SQLite | [`backend/`](backend/) | `5000` |

O Vite faz **proxy** das chamadas `/api/*` para o Flask, então o navegador usa uma
única origem (`localhost:5173`) e o cookie de sessão funciona normalmente.

---

## 📸 Telas

### Landing page
![Landing](docs/screenshots/01-landing.jpg)

### Login e Cadastro (integrados ao backend)
| Entrar | Criar conta |
| --- | --- |
| ![Login](docs/screenshots/02-login.jpg) | ![Cadastro](docs/screenshots/03-cadastro.jpg) |

### Dashboard do usuário (com a Área do Desenvolvedor)
![Dashboard](docs/screenshots/04-dashboard.jpg)

### Gerenciar Usuários — CRUD completo
| Listagem | Edição |
| --- | --- |
| ![Usuários](docs/screenshots/05-usuarios.jpg) | ![Editar](docs/screenshots/06-editar.jpg) |

---

## ✨ Funcionalidades

**Landing page**
- Navbar fixa com efeito blur e estado de sessão (mostra **"Meu Painel"** quando logado).
- Hero em carrossel (autoplay) com chamadas para população e empresas.
- Seção "Você sabia?" sobre a importância dos manguezais.
- **Mapa interativo** (Leaflet) com 11 áreas de manguezal de Pernambuco, polígonos,
  legenda e painel de detalhes.
- Seção "Por que usar o +Mangue" com os produtos App e Plataforma.
- Ondas SVG orgânicas separando as seções e animações sutis.

**Autenticação (conectada ao Flask)**
- Login por **usuário _ou_ e-mail** + senha, com mostrar/ocultar senha.
- Cadastro completo (usuário, nome, e-mail, data de nascimento, gênero, senha).
- Sessão por cookie; ao entrar/cadastrar o usuário vai para o dashboard.

**Dashboard do usuário** (`/dashboard`)
- Saudação personalizada, cards de impacto e ações rápidas.
- **Área do Desenvolvedor** → atalho para o painel de Gerenciar Usuários.

**Gerenciar Usuários** (`/dashboard/usuarios`) — o CRUD
- Estatísticas (total e por gênero), busca, ordenação por coluna e paginação.
- Criar (via cadastro), **editar**, **redefinir senha** e **excluir** usuários.
- Proteção: não é possível excluir o próprio usuário logado.

**Segurança**
- Senhas com hash **PBKDF2-HMAC-SHA256** + salt aleatório por usuário.
- Rotas de dados protegidas por sessão (401 sem login).

---

## 🚀 Como rodar

> Pré-requisitos: **Node.js 18+** e **Python 3.10+**. São necessários **2 terminais**.

### 1. Backend (Flask) — porta 5000

```bash
cd backend
python3 -m venv .venv                 # cria o ambiente virtual
source .venv/bin/activate             # Windows: .venv\Scripts\activate
pip install -r requirements.txt       # instala o Flask
python app.py                         # inicia a API em http://localhost:5000
```

### 2. Frontend (React) — porta 5173

Em **outro terminal**:

```bash
cd frontend
npm install                           # instala as dependências
npm run dev                           # inicia o app em http://localhost:5173
```

### 3. Acesse

Abra **<http://localhost:5173>** no navegador, crie uma conta e explore.
O banco `backend/database.db` é criado automaticamente na primeira execução.

---

## 🔌 API do backend

Todas as rotas retornam JSON. As de dados exigem sessão ativa (cookie).

| Método | Rota | Descrição |
| --- | --- | --- |
| `POST` | `/api/register` | cria usuário e inicia a sessão |
| `POST` | `/api/login` | autentica por usuário **ou** e-mail + senha |
| `POST` | `/api/logout` | encerra a sessão |
| `GET` | `/api/me` | retorna o usuário logado (401 se não houver sessão) |
| `GET` | `/api/users` | lista todos os usuários |
| `PUT` | `/api/users/<id>` | atualiza os dados de um usuário |
| `PUT` | `/api/users/<id>/password` | redefine a senha |
| `DELETE` | `/api/users/<id>` | remove um usuário |

---

## 📂 Estrutura

```
+mangue/
├── backend/                  # API Flask + SQLite
│   ├── app.py                # rotas /api
│   ├── crud.py               # acesso ao banco (CRUD + hash de senha)
│   ├── requirements.txt
│   └── database.db           # gerado automaticamente (ignorado pelo git
│   ├── mangue_funcoes.py     # crud das plataformas (APP e Desktop)
│
├── frontend/                 # App React + Vite
│   ├── index.html
│   ├── vite.config.ts        # plugins + proxy /api -> :5000
│   ├── tsconfig.json
│   ├── package.json
│   └── src/
│       ├── main.tsx          # entrada + BrowserRouter
│       ├── app/
│       │   ├── App.tsx       # rotas
│       │   ├── pages/        # LandingPage, Dashboard, UserManagement
│       │   ├── components/   # Navbar, HeroCarousel, modais, mapa, dashboard/...
│       │   ├── hooks/        # useAuth (proteção de rota)
│       │   └── lib/          # api.ts (cliente Flask), theme.ts (paleta)
│       ├── imports/          # logos
│       └── styles/           # fontes, tailwind, tema
│
├── docs/screenshots/         # imagens do README
├── ATTRIBUTIONS.md
└── README.md
```

---

## 🎨 Design system

| Token | Cor | Uso |
| --- | --- | --- |
| Verde escuro | `#404925` | primária |
| Verde oliva | `#A4AA7F` | apoio |
| Azul | `#6C94B4` | destaque |
| Lima | `#AFB11C` | acento |
| Creme | `#F1F4E0` | superfícies |
| Fundo | `#F8FAF0` | geral |

Tipografia: **Lora** (títulos) + **Work Sans** (corpo).

---

## 🛠️ Scripts úteis (frontend)

```bash
npm run dev        # servidor de desenvolvimento
npm run build      # build de produção (gera dist/)
npm run preview    # serve o build localmente
npm run typecheck  # checagem de tipos TypeScript
```
