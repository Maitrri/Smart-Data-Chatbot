import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv
import os
import importlib.util
import pandas as pd
from datetime import datetime
import io
import speech_recognition as sr
import pydeck as pdk

# --- Load environment and model ---
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(openai_api_key=api_key, temperature=0)

# --- Dynamic module loading ---
def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

nosql_module = load_module("maincpy_cleaned.py", "nosql_module")
sql_module = load_module("sqlrest_cleaned.py", "sql_module")

# --- Keywords for backend detection ---
sql_keywords = {"restaurant", "menu", "reviews"}
nosql_keywords = {"listing", "review", "housing", "apartment"}

# --- Streamlit Page Config ---
st.set_page_config(page_title="Smart Data Chatbot", layout="wide", page_icon="🤖")

# --- Chat History State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar: Mode, Reset, Voice Input, Download ---
with st.sidebar:
    st.title("⚙️ Settings")
    selected_mode = st.radio("Choose Query Mode", ["Auto Detect", 
     "Housing", "Restaurant"])

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    if st.button("📥 Download Chat History"):
        if st.session_state.messages:
            df_chat = pd.DataFrame(st.session_state.messages)
            buffer = io.StringIO()
            df_chat.to_csv(buffer, index=False)
            st.download_button(
                label="Download as CSV",
                data=buffer.getvalue(),
                file_name="chat_history.csv",
                mime="text/csv"
            )
        else:
            st.info("No chat history to download.")

    if st.button("🎙️ Start Voice Input"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("🎤 Listening... Please speak clearly.")
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                st.success("✅ Captured voice input. Processing...")
                voice_query = recognizer.recognize_google(audio)
                st.session_state["voice_input"] = voice_query
                st.rerun()
            except sr.UnknownValueError:
                st.error("😕 Could not understand audio.")
            except sr.RequestError:
                st.error("⚠️ Speech Recognition service error.")
            except Exception as e:
                st.error(f"🎙️ Unexpected error: {e}")

# --- App Header ---
st.title("🤖 Unified Chatbot Interface")
st.markdown("Chat with your **🏡 housing** or **🍽️ restaurant** data in natural language.")

# --- Display Chat History ---
for msg in st.session_state.messages:
    timestamp = msg.get("timestamp", "")
    with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🤖"):
        st.markdown(f"{msg['content']}")
        if timestamp:
            st.caption(f"🕒 {timestamp}")

# --- Query Backend Detector ---
def detect_backend(query: str) -> str:
    if selected_mode == "Restaurant": return "sql"
    if selected_mode == "Housing": return "mongo"

    query_lower = query.lower()
    sql_match = any(word in query_lower for word in sql_keywords)
    nosql_match = any(word in query_lower for word in nosql_keywords)

    if sql_match and not nosql_match: return "sql"
    elif nosql_match and not sql_match: return "mongo"
    elif sql_match and nosql_match:
        classification_prompt = f"""
        The user asked: \"{query}\"

        Decide which database to use to answer this: SQL (for restaurant/menu/reviews) or MongoDB (for housing/listing data/review).
        Reply with just one word: SQL or MongoDB.
        """
        try:
            result = llm.invoke([HumanMessage(content=classification_prompt)]).content.strip().lower()
            return "mongo" if "mongo" in result else "sql"
        except:
            return "unknown"
    else:
        classification_prompt = f"""
        Decide if the following question should be handled using SQL (for relational data) or MongoDB (for NoSQL documents).
        Reply with one word: SQL or MongoDB.

        Question: {query}
        """
        try:
            result = llm.invoke([HumanMessage(content=classification_prompt)]).content.strip().lower()
            return "mongo" if "mongo" in result else "sql"
        except:
            return "unknown"

# --- Chat Input (Text or Voice) ---
query = st.session_state.pop("voice_input", None) or st.chat_input("Ask me anything...")

if query:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.messages.append({"role": "user", "content": query, "timestamp": timestamp})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(query)
        st.caption(f"🕒 {timestamp}")

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🧠 Thinking..."):
            db_type = detect_backend(query)
            try:
                if db_type == "sql":
                    st.markdown("### 🗂️ Detected: SQL")
                    sql_query = sql_module.get_gemini_response(query, sql_module.prompt)
                    with st.expander("🧾 SQL Query"):
                        st.code(sql_query, language="sql")

                    if sql_query.lower().strip().startswith("select"):
                        df = sql_module.read_sql_query(sql_query, sql_module.db_config)
                        df.index += 1
                        with st.expander("📊 SQL Data Results"):
                            st.dataframe(df)

                        if not df.empty:
                            summary_prompt = f"""You are a helpful assistant. \nUser asked: \"{query}\"\nHere are the SQL results:\n{df.head(10).to_markdown(index=False)}\nExplain this in plain English."""
                            final_response = llm.invoke([HumanMessage(content=summary_prompt)]).content
                            st.subheader("🧠 Natural Language Answer")
                            st.write(final_response)
                            st.session_state.messages.append({"role": "assistant", "content": final_response, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                        else:
                            st.warning("⚠️ No data returned from SQL.")
                    else:
                        success, msg = sql_module.execute_sql_query(sql_query, sql_module.db_config)
                        if success:
                            st.success(msg)
                            st.session_state.messages.append({"role": "assistant", "content": msg, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                        else:
                            st.error("❌ SQL Execution Failed:")
                            st.code(msg)

                elif db_type == "mongo":
                    st.markdown("### 🍃 Detected: MongoDB")
                    df = nosql_module.handle_mongo_query(query, show_detailed_results=True)
                    if isinstance(df, pd.DataFrame) and not df.empty:
                        df.index += 1
                        with st.expander("📊 MongoDB Data Results"):
                            st.dataframe(df)

                        if 'latitude' in df.columns and 'longitude' in df.columns:
                            st.subheader("🗺️ Map View of Listings")
                            map_df = df[['latitude', 'longitude']].dropna()
                            st.map(map_df)

                        summary_prompt = f"""You are a helpful assistant. \nUser asked: \"{query}\"\nHere are the MongoDB results:\n{df.head(10).to_markdown(index=False)}\nExplain this in plain English."""
                        final_response = llm.invoke([HumanMessage(content=summary_prompt)]).content
                        st.subheader("🧠 Natural Language Answer")
                        st.write(final_response)
                        st.session_state.messages.append({"role": "assistant", "content": final_response, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                    else:
                        pass
                elif db_type == "mixed":
                    msg = "⚠️ Your question refers to both SQL and MongoDB. Please split it."
                    st.warning(msg)
                    st.session_state.messages.append({"role": "assistant", "content": msg, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                else:
                    msg = "🤖 Couldn't detect backend. Please rephrase."
                    st.warning(msg)
                    st.session_state.messages.append({"role": "assistant", "content": msg, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            except Exception as e:
                st.error(f"Unexpected error: {e}")

# --- Style Tweaks ---
st.markdown("""
    <style>
        .block-container { padding: 2rem  2rem 2rem 2rem; }
        footer {visibility: hidden;}
        .stChatMessage { max-width: 90%; }
    </style>
""", unsafe_allow_html=True)
