import os
import google.generativeai as genai
import mysql.connector
from dotenv import load_dotenv
import pandas as pd

# Load environment variables    
load_dotenv()

# Configure Genai Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# MySQL database configuration
db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "chatbot")
}

# Define Your Prompt
prompt = ["""You are an expert in converting English questions into SQL queries.
The SQL database contains tables such as "restaurant", "menu", and "reviews" with the following schema:

restaurant:
- restaurant_id (bigint)
- restaurant_name (text)
- cuisine (text)
- city (text)
- state (text)
- address (text)
- latitude (float)
- longitude (float)
- phone_number (text)
- email (text)
- delivery_available (text)
- seating_capacity (int)
- opening_hours (text)
- has_wifi (text)
- has_outdoor_seating (text)
- payment_methods (text)
- parking_available (text)
- alcohol_served (text)
- reservation_required (text)
- music_type (text)
- health_rating (int)
- has_kids_menu (text)

menu:
- restaurant_id (bigint)
- item_name (text)
- price_usd (float)
- is_vegetarian (bool)
- image_url (text)

reviews:
- restaurant_id (bigint)
- rating (float)
- review_count (int)
- sample_review (text)
- tags (text)

-- ✅ Schema Exploration:
SHOW TABLES;
DESCRIBE restaurant;
SELECT * FROM reviews LIMIT 5;
give me top 5 restaurants having google pay
give me 5 restaurant names in NY
give me reviews of customers top 5
top 5 restaurants in Florida
restaurants having outdoor seating
restaurants having health rate more than 90 with vegetarian menu
last 5 restaurant names with phone number
top 5 romantic restaurant names
last 5 restaurant names with email
give me timings for the Adams-White Kitchen restaurant

-- ✅ Sample Queries:
SELECT * FROM restaurant WHERE city = 'Los Angeles' AND health_rating > 90;
SELECT r.restaurant_name FROM restaurant r JOIN menu m ON r.restaurant_id = m.restaurant_id JOIN reviews v ON r.restaurant_id = v.restaurant_id WHERE m.is_vegetarian = 'TRUE' GROUP BY r.restaurant_name ORDER BY AVG(v.rating) DESC LIMIT 5;
SELECT item_name, price_usd FROM menu WHERE is_vegetarian = 'TRUE' AND price_usd < 10;
SELECT r.restaurant_name, AVG(v.rating) FROM restaurant r JOIN reviews v ON r.restaurant_id = v.restaurant_id GROUP BY r.restaurant_name;
SELECT r.restaurant_name, m.item_name, m.price_usd FROM restaurant r JOIN menu m ON r.restaurant_id = m.restaurant_id;
SELECT r.restaurant_name FROM restaurant r JOIN reviews v ON r.restaurant_id = v.restaurant_id WHERE v.tags LIKE '%romantic%' ORDER BY v.rating DESC LIMIT 5;
SELECT r.restaurant_name FROM restaurant r JOIN menu m ON r.restaurant_id = m.restaurant_id JOIN reviews v ON r.restaurant_id = v.restaurant_id WHERE r.health_rating > 90 AND m.is_vegetarian = 'TRUE' GROUP BY r.restaurant_name ORDER BY AVG(v.rating) DESC LIMIT 3;
SELECT restaurant_name FROM restaurant WHERE state = 'Florida' LIMIT 5;

-- ✅ Data Modification:
INSERT INTO restaurant (...);
UPDATE restaurant SET health_rating = 99 WHERE restaurant_id = ...;
DELETE FROM reviews WHERE restaurant_id = ...;

-- ✅ Boolean Fields Handling:
If a user asks about boolean-type features (like outdoor seating, WiFi, kids menu, alcohol served, vegetarian, etc.), use strings like 'yes', 'no', or 'TRUE' (in quotes) in the WHERE clause. 
For example:
✅ Correct: SELECT * FROM restaurant WHERE has_outdoor_seating = 'yes';
✅ Correct: SELECT * FROM menu WHERE is_vegetarian = 'TRUE';
🚫 Incorrect: SELECT * FROM restaurant WHERE has_outdoor_seating = TRUE;
🚫 Incorrect: SELECT * FROM menu WHERE is_vegetarian = TRUE;

Do not generate any output that is unrelated to the defined restaurant, menu, reviews tables. Only provide SQL queries based on the schemas above.
Always return only the SQL query without triple backticks or the word SQL.
"""]

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content([prompt[0], question])
    return response.text.strip()

def execute_sql_query(sql, db_config):
    try:
        conn = mysql.connector.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"]
        )
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        conn.close()
        return True, "Query executed successfully."
    except Exception as e:
        return False, f"Error executing query: {e}"

def read_sql_query(sql, db_config):
    try:
        conn = mysql.connector.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"]
        )
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        df = pd.DataFrame(rows, columns=columns)
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame(), f"Error: {e}"
