"""Script simple pour initialiser la base et insérer des données de démonstration.

Usage: python scripts/seed_db.py
"""
from pathlib import Path
import sys
from datetime import datetime, timedelta

# Ajouter automatiquement la racine du projet au PYTHONPATH afin que
# `from app...` fonctionne quand on exécute le script directement.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.database import engine, Base, SessionLocal
from app.models import User, Zone, Source, Indicator
from app.core.security import get_password_hash


def seed():
    print("Création des tables si nécessaire...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # Utilisateurs
    if not db.query(User).filter(User.email == "admin@example.com").first():
        admin = User(
            email="admin@example.com",
            hashed_password=get_password_hash("adminpass"),
            is_active=True,
            is_superuser=True,
            role="admin",
        )
        db.add(admin)
        print("-> admin ajouté: admin@example.com / adminpass")

    if not db.query(User).filter(User.email == "user@example.com").first():
        user = User(
            email="user@example.com",
            hashed_password=get_password_hash("userpass"),
            is_active=True,
            is_superuser=False,
            role="user",
        )
        db.add(user)
        print("-> utilisateur ajouté: user@example.com / userpass")

    db.commit()

    # Zones
    if not db.query(Zone).filter(Zone.name == "Ville A").first():
        z1 = Zone(name="Ville A", postal_code="75000")
        z2 = Zone(name="Ville B", postal_code="13000")
        db.add_all([z1, z2])
        db.commit()
        print("-> zones ajoutées")
    else:
        z1 = db.query(Zone).filter(Zone.name == "Ville A").first()
        z2 = db.query(Zone).filter(Zone.name == "Ville B").first()

    # Sources
    if not db.query(Source).filter(Source.name == "OpenAQ").first():
        s1 = Source(name="OpenAQ", url="https://api.openaq.org", description="Données qualité de l'air (exemple)")
        s2 = Source(name="Open-Meteo", url="https://open-meteo.com", description="Données météorologiques (exemple)")
        db.add_all([s1, s2])
        db.commit()
        print("-> sources ajoutées")
    else:
        s1 = db.query(Source).filter(Source.name == "OpenAQ").first()
        s2 = db.query(Source).filter(Source.name == "Open-Meteo").first()

    # Indicators
    now = datetime.utcnow()
    # create some time series points for zone A
    existing = db.query(Indicator).first()
    if not existing:
        points = []
        for i in range(6):
            points.append(
                Indicator(
                    source_id=s1.id if s1 else None,
                    type="pm25",
                    value=12.0 + i * 1.5,
                    unit="µg/m3",
                    timestamp=now - timedelta(hours=i * 6),
                    zone_id=z1.id if z1 else None,
                    metadata_json="{}",
                )
            )
        # create a couple for zone B
        points.append(
            Indicator(
                source_id=s2.id if s2 else None,
                type="temperature",
                value=18.5,
                unit="°C",
                timestamp=now,
                zone_id=z2.id if z2 else None,
                metadata_json="{}",
            )
        )
        db.add_all(points)
        db.commit()
        print("-> indicateurs ajoutés")

    db.close()
    print("Seed terminé.")


if __name__ == "__main__":
    seed()
