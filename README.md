# 🤖 Smart Data Chatbot

An AI-powered chatbot built with **Streamlit** that understands natural language queries and intelligently routes them to **MongoDB** (for housing data) or **MySQL** (for restaurant data). It supports voice input, map visualization, and generates smart summaries using OpenAI and Gemini.

---

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
- `OPENAI_API_KEY`: for LangChain + OpenAI LLM
- `GOOGLE_API_KEY`: for Gemini SQL query generation

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

### 🔧 Setup MongoDB Atlas

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) and **create a new account** (if you don't have one).
2. Once logged in, **create a new project** and give it a name.
3. Inside the project, **build a new cluster**. Choose the **free shared cluster**.
4. After the cluster is created, go to **Database Access** and **add a new database user**:
   - Set a **username** and **password**
   - Keep these credentials ready to add in the `.env` file

### 🔌 Connect with MongoDB Compass

5. Click on **Connect**, then choose **MongoDB Compass** as the connection method.
6. Select **"I have MongoDB Compass installed"**
7. Copy the **connection string**, which will look like:
     mongodb+srv://<username>:<password>@cluster0.hfendqx.mongodb.net/

### 🧭 Setup MongoDB Compass

8. If you don’t have Compass, download it from [here](https://www.mongodb.com/try/download/compass)
9. Open Compass and **paste the connection string** in the **URI** field
10. **Click Connect**

### 🗃️ Create Database & Collections

11. Inside Compass:
 - Create a new **Database** called `house`
 - Inside `house`, create a **Collection** called `listing`
 - Import your **housing CSV data** into this collection

12. Create two additional collections in the `house` database:
 - `review`
 - `host`
 - Import the respective CSV data into each collection

### ✅ Final Verification

13. Go back to MongoDB Atlas and check the **Clusters > Collections** tab to verify your data is uploaded correctly.


> Your MongoDB setup is now complete and ready to be used with Smart Data Chatbot!
---
# 🧠 Natural Language to SQL Query Converter

This project allows users to interact with an SQL database using *natural language* via a user-friendly *Streamlit chatbot interface*. Users can enter prompts like:

> "Show all the tables in the database"  
> "List all vegetarian menu items under $10"  
> "Add a new restaurant to the database"

The system will then:
- Generate the corresponding *SQL query*
- Execute it on the database
- Display both the query and the output in the interface

---

## 💡 Features

The chatbot supports the following functionalities:

1. *📊 Data Exploration* – Retrieve data using filters, joins, and conditions  
2. *📚 Schema Interaction* – Show tables, describe structures, inspect fields  
3. *✏️ Data Manipulation* – Insert, update, and delete records

---

## 🗂️ Dataset Structure

Make sure the following tables are uploaded to your *SQL Server* under a *single schema named chatbot*:

### restaurant
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

### menu
- restaurant_id (bigint)  
- item_name (text)  
- price_usd (float)  
- is_vegetarian (bool)  
- image_url (text)

### reviews
- restaurant_id (bigint)  
- rating (float)  
- review_count (int)  
- sample_review (text)  
- tags (text)

---

## 🧪 Example Natural Language Queries

```sql
-- ✅ Schema Exploration:
"Show all tables"
"Describe the restaurant table"
"Display first 5 reviews"

-- ✅ Data Showing:
"List all restaurants in Los Angeles with health rating over 90"
"Show vegetarian items under $10"
"Get average rating for each restaurant"

-- ✅ Data Manipulation:
"Add a new restaurant"
"Update the health rating of a restaurant"
"Delete a review for a specific restaurant"
⚙️ Setup Instructions
Follow these steps to get the project running locally:

* Clone the repository

bash
git clone https://github.com/your-username/nl-to-sql-chatbot.git
cd nl-to-sql-chatbot
* Create a Python virtual environment

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
* Install all dependencies using the provided requirements.txt

pip install -r requirements.txt
* Create a .env file in the root directory and add your Google API key

ini
GOOGLE_API_KEY=your_google_api_key_here
* Ensure your SQL database is accessible and contains the required schema chatbot with the tables restaurant, menu, and reviews

* Run the Streamlit application


streamlit run app.py
📦 Dependencies
This project uses the following libraries:

google-generativeai – For natural language to SQL translation

mysql-connector-python – SQL database connection

python-dotenv – For managing API keys and secrets

streamlit – To build the user interface

All dependencies are listed in the requirements.txt file for easy installation.

⚠️ Important Notes
* The dataset must be uploaded to your SQL server under a schema named chatbot
* The table names must match exactly: restaurant, menu, and reviews
* Always use a Python virtual environment to manage dependencies:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

---
## 🚀 How to Run

1. Ensure MySQL and MongoDB (Atlas) are populated with the proper schemas and collections.
2. Launch the app:
```bash
streamlit run apptry.py
```

---

## 💡 Features

- Auto-detect SQL vs NoSQL backend
- Natural language to query conversion via LLMs
- Voice input and map-based visualization
- Download chat history as CSV
- Plain English response summaries

---

## 📘 Description

Smart Data Chatbot is an intelligent, multimodal chatbot built using Streamlit, designed to process natural language queries and route them to the correct backend: MongoDB for housing data or MySQL (SQL) for restaurant data. It combines OpenAI’s GPT model (via LangChain) and Google Gemini to translate user questions into executable queries, automatically detect the relevant domain, and display results in both tabular and natural language format. The app also supports voice input, interactive maps, and CSV downloads for an enriched user experience.

This chatbot is ideal for scenarios where users need to search or modify data without writing complex queries — e.g., students looking for off-campus housing or customers searching for restaurants by cuisine, health ratings, or reviews.
