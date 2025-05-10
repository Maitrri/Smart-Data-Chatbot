# 🤖 Smart Data Chatbot

An AI-powered chatbot built with **Streamlit** that understands natural language queries and intelligently routes them to **MongoDB** (for housing data) or **MySQL** (for restaurant data). It supports voice input, map visualization, and generates smart summaries using OpenAI and Gemini.

---

## 📘 Description

Smart Data Chatbot is an intelligent, multimodal chatbot built using Streamlit, designed to process natural language queries and route them to the correct backend: MongoDB for housing data or MySQL (SQL) for restaurant data. It combines OpenAI’s GPT model (via LangChain) and Google Gemini to translate user questions into executable queries, automatically detect the relevant domain, and display results in both tabular and natural language format. The app also supports voice input, interactive maps, and CSV downloads for an enriched user experience.

This chatbot is ideal for scenarios where users need to search or modify data without writing complex queries — e.g., students looking for off-campus housing or customers searching for restaurants by cuisine, health ratings, or reviews.

## 🧩 Project Structure

```
.
├── apptry.py                # Main Streamlit app
├── maincpy_cleaned.py       # MongoDB handler
├── sqlrest_cleaned.py       # SQL (MySQL + Gemini) handler
├── .env                     # Your environment variables (create manually)
├── sample.txt               # Sample prompts for MongoDB (optional)
```

---

## ⚙️ Prerequisites

### 🔑 API Keys

* `OPENAI_API_KEY`: for LangChain + OpenAI LLM
* `GOOGLE_API_KEY`: for Gemini SQL query generation

### 📦 Python Libraries

Install with:

```bash
pip install streamlit langchain openai python-dotenv pymongo mysql-connector-python google-generativeai pandas pydeck speechrecognition
```

---

## 🛠️ Setup

Create a `.env` file in the root directory:

```dotenv
OPENAI_API_KEY=your_openai_key_here
GOOGLE_API_KEY=your_google_api_key_here
DB_HOST=your_mysql_host
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_NAME=chatbot

username = "your_Mongodb_cluster_user-name_here"
pwd = "your_Mongodb_cluster_pass-word_here"
db = client["house"]
listing_collection = db["listing"]
review_collection = db["review"]
host_collection = db["host"]
```

> **Note:** MongoDB credentials are currently hardcoded in `maincpy_cleaned.py`. Modify them if needed.

---

## 🍃 MongoDB Integration Steps

Follow these steps to integrate MongoDB Atlas with your Smart Data Chatbot:

### 🪴 Create MongoDB Account & Cluster

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) and **create a new account** (if you don't have one).
2. Once logged in, **create a new project** and give it a name.
3. Inside the project, **build a new cluster**. Choose the **free shared cluster**.
4. After the cluster is created, go to **Database Access** and **add a new database user**:

   * Set a **username** and **password**
   * Keep these credentials ready to add in the `.env` file

### 🔌 Connect with MongoDB Compass

5. Click on **Connect**, then choose **MongoDB Compass** as the connection method.
6. Select **"I have MongoDB Compass installed"**
7. Copy the **connection string**, which will look like:
   mongodb+srv://<username>:<password>@cluster0.hfendqx.mongodb.net/

### 🧭 Load Data in Compass

8. If you don’t have Compass, download it from [here](https://www.mongodb.com/try/download/compass)
9. Open Compass and **paste the connection string** in the **URI** field
10. **Click Connect**

### 🗃️ Create Database & Collections

11. Inside Compass:

* Create a new **Database** called `house`
* Inside `house`, create a **Collection** called `listing`
* Import your **housing CSV data** into this collection

12. Create two additional collections in the `house` database:

* `review`
* `host`
* Import the respective CSV data into each collection

### ✅ Final Check

13. Go back to MongoDB Atlas and check the **Clusters > Collections** tab to verify your data is uploaded correctly.

> 🌟 Your MongoDB setup is now complete and ready to be used with Smart Data Chatbot!

---

## 🧠 MySQL Chatbot Module

This module empowers users to interact with a MySQL database using natural language through a friendly Streamlit chatbot interface. Users can input prompts such as:

> "List all restaurants in Los Angeles with health rating over 90"
> "Show vegetarian menu items under \$10"
> "Add a new restaurant to the database"

The system processes these queries by:

* Generating the appropriate SQL query
* Executing it on the MySQL backend
* Displaying both the query and its results in the app

---

## 🐬 MySQL Integration Steps

Follow these steps to integrate your MySQL database with the Smart Data Chatbot:

### 🗄️ Setup MySQL Database

1. Install MySQL locally or use a remote MySQL server.
2. Create a new **database** named `chatbot`.
3. Inside the `chatbot` schema, create the following tables:

   * `restaurant`
   * `menu`
   * `reviews`

> You can use MySQL Workbench or command-line tools to execute SQL `CREATE TABLE` scripts for setting this up.

### 📑 Example Table Structure

Use the following structure for each table:

#### `restaurant`

```sql
CREATE TABLE restaurant (
  restaurant_id BIGINT PRIMARY KEY,
  restaurant_name TEXT,
  cuisine TEXT,
  city TEXT,
  state TEXT,
  address TEXT,
  latitude FLOAT,
  longitude FLOAT,
  phone_number TEXT,
  email TEXT,
  delivery_available TEXT,
  seating_capacity INT,
  opening_hours TEXT,
  has_wifi TEXT,
  has_outdoor_seating TEXT,
  payment_methods TEXT,
  parking_available TEXT,
  alcohol_served TEXT,
  reservation_required TEXT,
  music_type TEXT,
  health_rating INT,
  has_kids_menu TEXT
);
```

#### `menu`

```sql
CREATE TABLE menu (
  restaurant_id BIGINT,
  item_name TEXT,
  price_usd FLOAT,
  is_vegetarian BOOLEAN,
  image_url TEXT
);
```

#### `reviews`

```sql
CREATE TABLE reviews (
  restaurant_id BIGINT,
  rating FLOAT,
  review_count INT,
  sample_review TEXT,
  tags TEXT
);
```

### 🔐 Connect SQL in the `.env` file

Add your SQL credentials in the `.env` file like this:

```dotenv
DB_HOST=your_mysql_host
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_NAME=chatbot
```

> Ensure your MySQL server allows connections from your app’s IP or localhost.

### 📥 Import Data

4. Upload data into the above tables using either:

   * MySQL Workbench import wizard
   * CSV `LOAD DATA INFILE` commands
   * Python scripts using `mysql-connector-python`

Example for loading CSV:

```sql
LOAD DATA INFILE '/path/to/restaurant.csv'
INTO TABLE restaurant
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
```

### 🔍 Final Verification

5. Run a few SELECT queries to verify that data is present:

```sql
SELECT * FROM restaurant LIMIT 5;
SELECT * FROM menu LIMIT 5;
```

> 🚀 Your MySQL setup is now complete and ready to be used with Smart Data Chatbot!

---

## 🚀 How to Run

1. Ensure MySQL and MongoDB (Atlas) are populated with the proper schemas and collections.
2. Launch the app:

```bash
streamlit run apptry.py
```

---

## 💡 Features

* Auto-detect SQL vs NoSQL backend
* Natural language to query conversion via LLMs
* Voice input and map-based visualization
* Download chat history as CSV
* Plain English response summaries

---
