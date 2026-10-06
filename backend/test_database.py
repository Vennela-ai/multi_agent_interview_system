from database import engine

try:
    with engine.connect() as connection:
        print("✅ PostgreSQL connection successful!")
        print("✅ Connected to multi_agent_db")

except Exception as e:
    print("❌ PostgreSQL connection failed!")
    print(e)