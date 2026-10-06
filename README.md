# Gestionale Fondi — PFM (Personal Finance Management)

Applicazione full-stack per la **gestione di spese, entrate e strategie di accumulo di risparmio**.
Il progetto risolve un problema concreto: tenere traccia delle proprie finanze personali in modo strutturato (categorie, transazioni, riepilogo mensili) e ricevere un **consiglio automatico su come destinare il risparmio** del mese, in base alla strategia selezionata.

## Stack tecnologico

| Livello | Tecnologie |
|---|---|
| **Backend** | Python 3.11, FastAPI, SQLAlchemy 2.0, SQLite, Pydantic v2 |
| **Sicurezza** | JWT (access + refresh token), bcrypt, OAuth2 password flow |
| **Frontend** | Expo SDK 57, React Native 0.86, React 19, TypeScript |
| **Comunicazione** | REST API + axios |
| **Tooling** | Uvicorn (dev server), Expo CLI |

## Struttura del repository

```
gestionale-fondi-app/
├── pfm_backend/            # API REST FastAPI
│   ├── app/
│   │   ├── api/            # auth, categories, transactions, analytics, strategies
│   │   ├── core/           # config, sicurezza (JWT)
│   │   ├── services/       # motore di calcolo delle strategie
│   │   ├── models.py       # modelli SQLAlchemy (User, Category, Transaction)
│   │   ├── schemas.py      # schema Pydantic (validazione request/response)
│   │   ├── database.py     # connessione SQLite
│   │   └── main.py         # istanziazione FastAPI e router
│   ├── requirements.txt
│   └── .env.example        # template delle variabili d'ambiente
└── pfm_frontend/           # App mobile Expo / React Native
    ├── App.tsx             # punto di ingresso dell'app
    ├── app.json            # configurazione Expo
    └── package.json
```

## Funzionalità

- **Autenticazione**: registrazione, login, refresh token, profilo utente (`/auth`)
- **Categorie**: CRUD completa per organizzare entrate e spese (`/categories`)
- **Transazioni**: inserimento, modifica, eliminazione e storico delle operazioni (`/transactions`)
- **Analytics**: riepilogo mensile e suddivisione per categoria (`/analytics`)
- **Strategie di accumulo**: raccomandazione automatica per il risparmio (`/strategies`)

### Endpoint principali

| Metodo | Endpoint | Descrizione |
|---|---|---|
| POST | `/auth/register` | Registrazione nuovo utente |
| POST | `/auth/login` | Login (restituisce token JWT) |
| POST | `/auth/refresh` | Rinnovo del token di accesso |
| GET | `/auth/me` | Profilo utente corrente |
| GET/POST | `/categories` | Lista / creazione categorie |
| PUT/DELETE | `/categories/{id}` | Modifica / eliminazione categoria |
| GET/POST | `/transactions` | Lista / creazione transazioni |
| PUT/DELETE | `/transactions/{id}` | Modifica / eliminazione transazione |
| GET | `/analytics/monthly` | Riepilogo del mese corrente |
| GET | `/analytics/by-category` | Spese raggruppate per categoria |
| GET | `/strategies/recommendation` | Raccomandazione strategia di accumulo |

## Anteprima dell'interfaccia

> Aggiungi qui 2-3 screenshot dell'app in funzione (oppure una GIF):
>
> `![Dashboard](docs/screenshot-dashboard.png)`
> `![Dettaglio transazioni](docs/screenshot-transazioni.png)`

## Come eseguire il progetto in locale

### Prerequisiti

- Python 3.11+
- Node.js 18+ (con npm)
- Git

### 1. Backend

```bash
cd pfm_backend

# Ambiente virtuale
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

# Dipendenze
pip install -r requirements.txt

# Variabili d'ambiente
copy .env.example .env         # Windows (cp .env.example .env su macOS/Linux)
# Apri .env e inserisci una SECRET_KEY casuale

# Avvio del server (http://127.0.0.1:8000)
uvicorn app.main:app --reload
```

Documentazione interattiva dell'API: <http://127.0.0.1:8000/docs>

### 2. Frontend

```bash
cd pfm_frontend

# Dipendenze
npm install

# Avvio del dev server Expo
npm start
```

Da lì puoi scansionare il QR code con **Expo Go** (Android/iOS) oppure premere `w` per la versione web.

## Variabili d'ambiente

| Variabile | Descrizione | Default |
|---|---|---|
| `SECRET_KEY` | Chiave segreta per firmare i JWT | `dev-secret-...` (solo dev) |
| `ALGORITHM` | Algoritmo di firma | `HS256` |
| `ACCESS_TOKEN_MINUTES` | Durata access token | `30` |
| `REFRESH_TOKEN_DAYS` | Durata refresh token | `7` |

> ⚠️ Il file `.env` **non viene committato** ed è presente nella `.gitignore`: ogni sviluppatore ne crea uno proprio a partire da `.env.example`.

## Licenza

Il frontend è basato sul template Expo (MIT). Tutti i diritti sul codice applicativo del progetto sono riservati all'autore.
