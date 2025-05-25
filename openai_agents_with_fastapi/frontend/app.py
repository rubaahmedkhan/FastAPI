import streamlit as st
import requests
import json
import time
from typing import Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI backend URL
BACKEND_URL = "http://127.0.0.1:8000"  # Adjust if your backend is hosted elsewhere

# Streamlit page configuration
st.set_page_config(page_title="AI Agent Interface", page_icon="🤖", layout="wide")

# Title
st.title("AI Agent Query Interface")

# Initialize session state for storing responses
if "response" not in st.session_state:
    st.session_state.response = ""
if "streaming_response" not in st.session_state:
    st.session_state.streaming_response = ""

def call_non_streaming_endpoint(query: str) -> Dict[str, Any]:
    """Call the non-streaming /ask endpoint."""
    try:
        response = requests.post(
            f"{BACKEND_URL}/ask",
            json={"query": query},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling non-streaming endpoint: {e}")
        return {"error": str(e)}

def stream_response(query: str) -> None:
    """Stream response from /ask/stream endpoint."""
    try:
        response = requests.post(
            f"{BACKEND_URL}/ask/stream",
            json={"query": query},
            stream=True,
            headers={"Accept": "text/event-stream"},
            timeout=30
        )
        response.raise_for_status()

        # Clear previous streaming response
        st.session_state.streaming_response = ""
        
        # Placeholder for streaming response
        placeholder = st.empty()
        current_response = ""

        for line in response.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")
                if decoded_line.startswith("data:"):
                    try:
                        json_data = json.loads(decoded_line[5:].strip())
                        chunk = json_data.get("chunk", "")
                        current_response += chunk
                        placeholder.markdown(current_response)
                    except json.JSONDecodeError:
                        logger.error(f"Failed to decode JSON: {decoded_line}")
        st.session_state.streaming_response = current_response
    except requests.exceptions.RequestException as e:
        logger.error(f"Error streaming response: {e}")
        st.error(f"Streaming error: {e}")

# User input form
with st.form(key="query_form"):
    query = st.text_area("Enter your query:", height=100, placeholder="Ask about web development, mobile development, AI, or DevOps...")
    col1, col2 = st.columns(2)
    with col1:
        submit_button = st.form_submit_button("Ask (Non-Streaming)")
    with col2:
        stream_button = st.form_submit_button("Ask (Streaming)")

# Handle form submission
if submit_button and query.strip():
    with st.spinner("Fetching response..."):
        result = call_non_streaming_endpoint(query)
        if "error" in result:
            st.error(f"Error: {result['error']}")
        else:
            st.session_state.response = result.get("response", "No response received")
            st.markdown("**Non-Streaming Response:**")
            st.write(st.session_state.response)

if stream_button and query.strip():
    with st.spinner("Streaming response..."):
        stream_response(query)
        if st.session_state.streaming_response:
            st.markdown("**Streaming Response:**")
            st.write(st.session_state.streaming_response)
        else:
            st.error("No streaming response received")

# Sidebar for instructions
with st.sidebar:
    st.header("Instructions")
    st.markdown("""
    - **Non-Streaming**: Use for quick, complete responses.
    - **Streaming**: Use for real-time response updates.
    - Supported topics: Web Development, Mobile Development, AI, DevOps.
    - Ensure the backend server is running at `http://127.0.0.1:8000`.
    """)