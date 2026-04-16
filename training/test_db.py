from sqlalchemy import text
from app.database import engine 

def test_connection():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("Conexión OK:", result.scalar())

if __name__== "__main__":
    test_connection()