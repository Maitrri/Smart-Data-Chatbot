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
```

> **Note:** MongoDB credentials are currently hardcoded in `maincpy_cleaned.py`. Modify them if needed.

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
