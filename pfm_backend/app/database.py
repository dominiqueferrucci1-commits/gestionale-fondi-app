import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Definizione dell'URL del database.
# Default: SQLite con file "pfm_app.db" nella root del progetto.
# Sovrascrivibile via variabile d'ambiente DATABASE_URL (usata dai test
# per puntare a un database separato).
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./pfm_app.db")

# 2. Creazione dell'Engine.
# L'Engine e' il "motore" che traduce le richieste Python in linguaggio SQL.
# 'check_same_thread' e' necessario solo per SQLite in FastAPI per evitare
# errori asincroni.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Creazione della Fabbrica di Sessioni (SessionLocal).
# Ogni volta che l'utente fa una richiesta (es. salva una spesa),
# apriremo una "Sessione" indipendente, per garantire l'isolamento dei dati (ACID).
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Creazione della Classe Base.
# Tutte le nostre tabelle (Utenti, Transazioni, Categorie) erediteranno da questa base.
Base = declarative_base()


# 5. Dependency (Iniezione delle Dipendenze).
# Questa funzione fornira' la connessione al DB solo quando serve,
# e la chiudera' in sicurezza.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
