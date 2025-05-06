 
import streamlit as st
from pymongo import MongoClient
import urllib, io, json
from dotenv import load_dotenv
import os
import pandas as pd


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
from langchain_community.chat_models import ChatOpenAI
#from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

llm = ChatOpenAI(openai_api_key=api_key, temperature=0)

username = "maitrric"
pwd = "RU6JNDEzJspDWzL3"
connection_string = f"mongodb+srv://{username}:{pwd}@cluster0.mlpkdqu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(connection_string)

db = client["house"]
listing_collection = db["listing"]
review_collection = db["review"]
host_collection = db["host"]

def handle_mongo_query(input_query: str, show_detailed_results: bool = False):
    st.sidebar.title("Settings")
    show_detailed_results = st.sidebar.checkbox("Show Detailed Results", value=show_detailed_results,
                                                help="Toggle to show/hide detailed JSON results and images")

    results_list = []
    #st.markdown("🍃 MongoDB Detected")
    # Display map if latitude and longitude exist
    def display_map(results_list):
        coords = []
        for doc in results_list:
            if isinstance(doc, dict) and "latitude" in doc and "longitude" in doc:
                try:
                    coords.append({"lat": float(doc["latitude"]), "lon": float(doc["longitude"])})
                except:
                    continue
        if coords:
            st.subheader("🗺️ Location Map")
            st.map(pd.DataFrame(coords))

    display_map(results_list)

    def display_results_with_images(results_list):
        if not show_detailed_results:
            return

        for result in results_list:
            if isinstance(result, dict) and "_id" in result and not isinstance(result["_id"], str):
                result["_id"] = str(result["_id"])

        if not results_list:
            #st.info("No results found.")
            return

        count = min(len(results_list), 5)
        with st.expander("📊 MongoDB Data Results"):
            st.write(f"Showing {count} of {len(results_list)} results:")

            for i, result in enumerate(results_list[:count]):
                with st.container():
                    if isinstance(result, dict) and "picture_url" in result and result["picture_url"]:
                        col1, col2 = st.columns([1, 2])
                        try:
                            col1.image(result["picture_url"], use_container_width=True)
                        except Exception as e:
                            col1.error("Could not load image")
                            col1.write(f"URL: {result['picture_url']}")
                        display_data = result.copy()
                        if "picture_url" in display_data:
                            del display_data["picture_url"]
                        col2.json(display_data)
                    else:
                        st.json(result)
                    st.divider()

            if len(results_list) > 5:
                st.info(f"...and {len(results_list) - 5} more (not shown)")

    # Generate MongoDB query using LLM
    try:
        with io.open("sample.txt", "r", encoding="utf-8") as f1:
            sample = f1.read()
    except Exception as e:
        sample = "Sample questions unavailable"

    prompt = f"""
    You are a very intelligent AI assistant who is expert in identifying relevant questions
    from users and converting them into NoSQL MongoDB queries.
    Note: You have to just return the query as JSON, nothing else. Don't return any additional text.

    THREE DIFFERENT QUERY FORMATS:

    1. FOR READ-ONLY OPERATIONS (when user wants to find, list, count, or get information):
    - Return a MongoDB aggregation pipeline as a JSON ARRAY like this:
    [
        {{ "$match": {{ ... }} }},
        {{ "$project": {{ ... }} }}
    ]

    2. FOR DATA MODIFICATION OPERATIONS (when user wants to insert, update, or delete):
    - Return a JSON OBJECT with "operation" field like this:
    {{
        "operation": "insertOne" or "updateOne" or "deleteMany" etc.,
        "filter": {{ ... }},  // For update/delete operations
        "update": {{ ... }},  // For update operations
        "document": {{ ... }} // For insert operations
    }}

    3. FOR LOOKUP OPERATIONS (when user wants to join data across collections):
    - Return a MongoDB aggregation pipeline as a JSON ARRAY with $lookup stage:
    [
        {{ "$match": {{ ... }} }},
        {{ "$lookup": {{ 
            "from": "collection_name", 
            "localField": "field_name", 
            "foreignField": "field_name", 
            "as": "joined_data" 
        }} }},
        {{ "$project": {{ ... }} }}
    ]

    IMPORTANT: If the user specifically asks for images, include "picture_url" in the projection.

    Please use the below schema to write the MongoDB queries:

    schema:
    The MongoDB database contains three collections: listing, review, and host.

    1. LISTING COLLECTION:
    The listing collection contains housing listings for rent or sale with the following fields:
    - **_id**: Unique identifier for the listing (ObjectId).
    - **id**: Numeric identifier for the listing (Primary Key).
    - **category**: Category of the listing (e.g., "housing/rent/apartment").
    - **title**: Title of the listing.
    - **body**: Full description of the listing.
    - **amenities**: Available amenities in the property.
    - **bathrooms**: Number of bathrooms.
    - **bedrooms**: Number of bedrooms.
    - **currency**: Currency used for pricing (e.g., "USD").
    - **picture_url**: URL to the picture of the listing.
    - **fee**: Whether there's a fee (e.g., "No", "Yes").
    - **has_photo**: Photo availability (e.g., "Thumbnail").
    - **pets_allowed**: Pets that are allowed (e.g., "Cats,Dogs").
    - **price**: Price value (numeric).
    - **price_display**: Formatted price string (e.g., "$2,395").
    - **price_type**: Type of pricing (e.g., "Monthly").
    - **square_feet**: Size of the property in square feet.
    - **host_id**: Unique identifier for the host (Foreign Key to host collection).
    - **address**: Street address of the property.
    - **cityname**: City where the property is located.
    - **state**: State where the property is located.
    - **latitude**: Geographical latitude.
    - **longitude**: Geographical longitude.
    - **source**: Source of the listing (e.g., "RentLingo").
    - **time**: Timestamp of when the listing was created/updated.
    - **description**: Detailed description of the property.
    - **neighborhood_overview**: Overview of the neighborhood.

    2. REVIEW COLLECTION:
    The review collection contains reviews related to listings with the following fields:
    - **_id**: Unique identifier for the review (ObjectId).
    - **id**: Numeric identifier linking to listing (Foreign Key to listing.id).
    - **number_of_reviews**: Total number of reviews for the listing.
    - **last_review**: Date of the last review.
    - **first_review**: Date of the first review.
    - **review_scores**: Score of the reviews.

    3. HOST COLLECTION:
    The host collection contains information about hosts/landlords with the following fields:
    - **_id**: Unique identifier for the host record (ObjectId).
    - **host_name**: Name of the host.
    - **host_since**: Date since when the host is active.
    - **host_response_time**: Response time of the host.
    - **host_id**: Unique identifier for the host (Primary Key, linked from listing.host_id).
    - **host_about**: Information about the host.

    IMPORTANT GUIDELINES FOR SPECIFIC OPERATIONS:

    1. DELETE OPERATIONS:
    - When user mentions "delete", "remove", "take down", etc.
    - Return: {{ "operation": "deleteMany", "filter": {{ "field": "value" }} }}
    - For single document deletion: {{ "operation": "deleteOne", "filter": {{ "field": "value" }} }}
    - For city-specific deletions, always include both "cityname" and "state" fields if both are specified
    - If only city is mentioned (e.g., "Washington"), use only cityname in the filter

    2. UPDATE OPERATIONS:
    - When user mentions "update", "change", "modify", etc.
    - For single document: {{ "operation": "updateOne", "filter": {{ "field": "value" }}, "update": {{ "$set": {{ "field": "new value" }} }} }}
    - For multiple documents: {{ "operation": "updateMany", "filter": {{ "criteria": "value" }}, "update": {{ "$set": {{ "field": "new value" }} }} }}

    3. INSERT OPERATIONS:
    - When user mentions "add", "create", "insert", etc.
    - Single document: {{ "operation": "insertOne", "document": {{ "all required fields": "values" }} }}
    - Multiple documents: {{ "operation": "insertMany", "documents": [{{ "doc1": "values" }}, {{ "doc2": "values" }}] }}

    4. LOOKUP OPERATIONS:
    - When user wants data that spans multiple collections (mentions hosts and listings, reviews and listings, etc.)
    - Use $lookup stage to join collections on their relation fields:
        - To join listings with hosts: join listing.host_id with host.host_id
        - To join listings with reviews: join listing.id with review.id
    - For complex relationships involving all three collections, use multiple $lookup stages
    - Include picture_url in projections ONLY if the user explicitly asks for images

    5. READ OPERATIONS:
    - When user wants to find information (no data modification)
    - Use aggregation pipeline with $match, $project, $group, etc. in an ARRAY format
    - Always include a $project stage to limit fields when returning many documents
    - Include picture_url in projections ONLY if the user explicitly asks for images

    Sample questions and appropriate MongoDB queries:
    {sample}

    Now, based on these instructions, analyze the following user question and return only the appropriate MongoDB query as a valid JSON:

    User question: {input_query}
    """

    try:
        messages = [HumanMessage(content=prompt)]
        response_text = llm.invoke(messages).content.strip()
        # 🔐 Check that it's valid JSON
        if not (response_text.startswith('{') or response_text.startswith('[')):
            #st.error("❌ LLM returned invalid format. Could not parse as JSON.")
            st.code(response_text)
            return
        if not (response_text.startswith('[') or response_text.startswith('{')):
            json_start = response_text.find('[')
            json_start2 = response_text.find('{')
            if json_start == -1: json_start = float('inf')
            if json_start2 == -1: json_start2 = float('inf')
            start_idx = min(json_start, json_start2)
            if start_idx != float('inf'):
                response_text = response_text[start_idx:]

        with st.expander("🧾 Raw LLM MongoDB Query"):
            st.text(response_text)

        query_response = json.loads(response_text)

        is_lookup_operation = isinstance(query_response, list) and any(
            '$lookup' in stage for stage in query_response if isinstance(stage, dict))

        if isinstance(query_response, list):
            if show_detailed_results and any("picture" in input_query.lower() for keyword in ["image", "photo", "show"]):
                for stage in query_response:
                    if isinstance(stage, dict) and "$project" in stage:
                        stage["$project"]["picture_url"] = 1

            results = listing_collection.aggregate(query_response)
            results_list = list(results)
            # 🗺️ Show Map (if applicable)
            display_map(results_list)
            display_results_with_images(results_list)

        elif isinstance(query_response, dict) and "operation" in query_response:
            # Simple insert/update/delete logic for this version
            operation = query_response["operation"]
            target_collection = listing_collection
            if operation == "insertOne":
                doc = query_response["document"]
                result = target_collection.insert_one(doc)
                st.success(f"✅ Inserted: {str(result.inserted_id)}")
            elif operation == "deleteOne":
                result = target_collection.delete_one(query_response["filter"])
                st.success(f"✅ Deleted: {result.deleted_count} document(s)")
            elif operation == "updateOne":
                result = target_collection.update_one(query_response["filter"], query_response["update"])
                st.success(f"✅ Updated: {result.modified_count} document(s)")
            else:
                st.warning("Operation not supported in this simplified version")
        else:
            st.warning("Unrecognized query format")

    except Exception as e:
        st.error(f"Error processing query: {str(e)}")  
        st.error(f"Response text that couldn't be parsed: {response_text}")
        results_list = [{"error": f"Failed to process query: {str(e)}"}]

    flat_docs = []
    for doc in results_list:
        if isinstance(doc, dict):
            flat_doc = ", ".join(f"{k}: {v}" for k, v in doc.items() if k != "_id")
            flat_docs.append(flat_doc)
        else:
            flat_docs.append(str(doc))

    combined = "\n".join(flat_docs)

    if combined.strip():

        result_context = f"""
        User Question: {input_query}

        Query Results:
        {combined}
        """

        if is_lookup_operation:
            summary_prompt = f"""
        {result_context}

        Based on the above, answer the user's question clearly in natural language. If this was an insert, update, or delete operation, explain what happened or what was modified in the database. 
        DO NOT mention anything about "lookup operations" unless this was specifically a query joining multiple collections.
        """
        else:
            summary_prompt = f"""
        {result_context}

        Based on the above, answer the user's question clearly in natural language. If this was an insert, update, or delete operation, explain what happened or what was modified in the database.
        """

        final_response = llm.invoke([HumanMessage(content=summary_prompt)]).content
        st.subheader("🧠  Natural Language Answer")
        st.write(final_response)
        pass
    
