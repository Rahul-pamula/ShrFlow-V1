import os
import sys
import psycopg2
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def apply_migrations():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("❌ Error: DATABASE_URL not set in .env")
        return

    migrations_dir = Path(__file__).resolve().parents[1] / "migrations"
    sql_files = sorted([f for f in migrations_dir.glob("*.sql")])

    if not sql_files:
        print("⚠️ No migration files found.")
        return

    print(f"🚀 Found {len(sql_files)} migrations. Connecting to database...")
    
    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cur = conn.cursor()

        # 1. Apply schema.sql first if it exists in scripts/
        schema_file = Path(__file__).resolve().parents[1] / "scripts" / "schema.sql"
        if schema_file.exists():
            print(f"📄 Applying base schema: {schema_file.name}...")
            with open(schema_file, "r") as f:
                cur.execute(f.read())
            print("✅ Base schema applied.")

        # 2. Apply all migrations in order
        for sql_file in sql_files:
            print(f"📜 Applying {sql_file.name}...")
            with open(sql_file, "r") as f:
                sql = f.read()
                try:
                    cur.execute(sql)
                    print(f"  ✅ Success")
                except Exception as e:
                    print(f"  ❌ Error: {e}")
                    # Continue if it's already applied (standard in some systems)
                    pass

        print("\n🎉 All migrations processed!")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    apply_migrations()
