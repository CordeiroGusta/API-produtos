from sqlalchemy import text
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from app.database.db_connection import engine

def test_database_connection() -> dict:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "connected": True,
            "message": "Conexão com o banco de dados estabelecida com sucesso!"
        }

    except OperationalError as e:
        return {
            "connected": False,
            "error_type": "OperationalError",
            "details": str(e.orig) if hasattr(e, 'orig') else str(e)
        }
    
    except SQLAlchemyError as e:
        return {
            "connected": False,
            "error_type": "SQLAlchemyError",
            "details": str(e)
        }

    except Exception as e:
        return {
            "connected": False,
            "error_type": "GenericError",
            "details": str(e)
        }