import json
import psycopg2
from psycopg2.extras import Json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection configuration
DB_CONFIG = {
    'host': 'awseb-e-emr25gqgfk-stack-awsebrdsdatabase-z5dannxd2soi.crkkaaui2n2g.us-east-1.rds.amazonaws.com',
    'database': os.getenv('DB_NAME', 'ebdb'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'port': '5432'
}

def connect_to_db():
    """Establish database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def create_table(conn):
    """Create table if it doesn't exist"""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS events (
        id SERIAL PRIMARY KEY,
        title TEXT,
        description TEXT,
        event_date TIMESTAMP,
        url TEXT,
        data JSONB,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    try:
        with conn.cursor() as cur:
            cur.execute(create_table_query)
            conn.commit()
    except Exception as e:
        print(f"Error creating table: {e}")
        conn.rollback()

def insert_data(conn, data):
    """Insert JSON data into database"""
    insert_query = """
    INSERT INTO events (title, description, event_date, url, data)
    VALUES (%(title)s, %(description)s, %(event_date)s, %(url)s, %(data)s)
    """
    try:
        with conn.cursor() as cur:
            for item in data:
                # Prepare the record
                record = {
                    'title': item.get('title'),
                    'description': item.get('description'),
                    'event_date': item.get('date'),
                    'url': item.get('url'),
                    'data': Json(item)  # Store complete JSON as JSONB
                }
                cur.execute(insert_query, record)
            conn.commit()
            print("Data inserted successfully")
    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()

def main():
    # Read JSON file
    try:
        with open('events_data.json', 'r') as file:
            data = json.load(file)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return

    # Connect to database
    conn = connect_to_db()
    if not conn:
        return

    try:
        # Create table
        create_table(conn)
        
        # Insert data
        insert_data(conn, data)
    finally:
        conn.close()

if __name__ == "__main__":
    main()