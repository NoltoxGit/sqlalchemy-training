from database import Base, engine, SessionLocal
from models import Liste_Telephones


def create_database() -> None:
    Base.metadata.create_all(bind=engine)


def add_phone() -> None:
    session = SessionLocal()

    try:
        phone = Liste_Telephones(
            marque="Samsung",
            modele="Galaxy S24",
            espace_stockage=256,
            memoire_ram=8,
            prix=899,
        );
        phone = Liste_Telephones(
            marque="Samsung",
            modele="Galaxy A35",
            espace_stockage=128,
            memoire_ram=6,
            prix=238,
        )

        session.add(phone)
        session.commit()
        session.refresh(phone)

        print(f"Téléphone ajouté avec l'id : {phone.id}")

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


def list_phones() -> None:
    session = SessionLocal()

    try:
        phones = session.query(Liste_Telephones).all()

        for phone in phones:
            print(
                f"{phone.id} - {phone.marque} {phone.modele} "
                f"({phone.espace_stockage} Go, {phone.memoire_ram} Go RAM) - {phone.prix} €"
            )

    finally:
        session.close()


if __name__ == "__main__":
    create_database()
    add_phone()
    list_phones()