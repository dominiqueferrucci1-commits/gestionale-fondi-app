from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Definizione dell'URL del database.
# Usiamo SQLite. Creerà un file chiamato "pfm_app.db" nella root del progetto.
SQLALCHEMY_DATABASE_URL = "sqlite:///./pfm_app.db"

# 2. Creazione dell'Engine.
# L'Engine è il "motore" che traduce le richieste Python in linguaggio SQL.
# 'check_same_thread' è necessario solo per SQLite in FastAPI per evitare errori asincroni.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Creazione della Fabbrica di Sessioni (SessionLocal).
# Ogni volta che l'utente fa una richiesta (es. salva una spesa),
# apriremo una "Sessione" indipendente, per garantire l'isolamento dei dati (principi ACID).
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Creazione della Classe Base.
# Tutte le nostre tabelle (Utenti, Transazioni, Categorie) erediteranno da questa base.
Base = declarative_base()


# 5. Dependency (Iniezione delle Dipendenze).
# Questa funzione fornirà la connessione al DB solo quando serve, e la chiuderà in sicurezza.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
