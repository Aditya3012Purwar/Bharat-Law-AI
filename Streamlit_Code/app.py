import streamlit as st
import pandas as pd
import sys
import os
import time

# Add current directory to path so we can import the main module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import functions from the main module
from ip_law_agent import answer_query, detect_language, classify_ip_domain

# Set page configuration
st.set_page_config(
    page_title="Multilingual IP Law Expert",
    page_icon="⚖️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .domain-badge {
        background-color: #4B5563;
        color: white;
        padding: 0.3rem 0.7rem;
        border-radius: 10px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 1rem;
    }
    .source-list {
        background-color: #F3F4F6;
        padding: 1rem;
        border-radius: 5px;
        margin-top: 1rem;
    }
    .language-indicator {
        font-size: 0.9rem;
        color: #4B5563;
        font-style: italic;
    }
    .stProgress > div > div > div > div {
        background-color: #3B82F6;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for storing conversation history
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Header
st.markdown("<h1 class='main-header'>Multilingual IP Law Expert</h1>", unsafe_allow_html=True)

# Sidebar with information
with st.sidebar:
    st.title("About")
    st.write("""
    This application provides expert answers to questions about Intellectual Property Law
    across multiple domains:
    
    - Copyright Law
    - Geographical Indications
    - Design Law
    - Patent Law
    - Trademark Law
    
    The system supports multiple languages and automatically detects and responds in the language of your query.
    """)
    
    st.subheader("How It Works")
    st.write("""
    1. Enter your question in any language
    2. Our system detects the language and IP domain
    3. Retrieves relevant legal information
    4. Provides an authoritative answer with source references
    5. Translates the response back to your original language
    """)
    
    # Clear history button
    if st.button("Clear Conversation History"):
        st.session_state.conversation_history = []
        st.success("Conversation history cleared!")

# Main area - split into two columns
col1, col2 = st.columns([2, 1])

with col1:
    # Main query input area
    st.subheader("Ask Your Intellectual Property Law Question")
    query = st.text_area("Enter your question in any language:", height=150)

    # Add examples with an expander
    with st.expander("See Example Questions"):
        examples = {
            "Copyright": "What are the requirements for copyright protection of software?",
            "Geographical Indications": "How can a local producer group register a new geographical indication?",
            "Design": "What is the difference between registered and unregistered design rights?",
            "Patent": "What is the standard for non-obviousness in patent applications?",
            "Trademark": "Can sounds be registered as trademarks? What are the requirements?"
        }
        
        # Create two columns for the example buttons
        col_a, col_b = st.columns(2)
        
        # Display example buttons in two columns
        for i, (domain, example) in enumerate(examples.items()):
            with col_a if i % 2 == 0 else col_b:
                if st.button(f"{domain} Example", key=domain):
                    st.session_state.query = example

    # Get query from session state if it exists
    if 'query' in st.session_state:
        query = st.session_state.query
        # Clear it after use
        st.session_state.query = ""

with col2:
    # Domain prediction area
    st.subheader("Domain Prediction")
    if query:
        try:
            # Display a spinner while predicting
            with st.spinner("Predicting domain..."):
                domain_prediction = classify_ip_domain(query)
            
            # Domain badge colors
            domain_colors = {
                "Copyright": "#1E40AF",  # Blue
                "GI": "#047857",  # Green
                "Design": "#9D174D",  # Pink
                "Patent": "#B45309",  # Amber
                "Trademark": "#4338CA"  # Indigo
            }
            color = domain_colors.get(domain_prediction, "#4B5563")  # Default gray
            
            # Display the prediction
            st.markdown(f"<div class='domain-badge' style='background-color: {color};'>Predicted Domain: {domain_prediction}</div>", 
                    unsafe_allow_html=True)
            
            # Display domain description
            domain_descriptions = {
                "Copyright": "Protection for original works of authorship including literary, dramatic, musical, and artistic works.",
                "GI": "Geographical Indications identify products with specific geographical origin and qualities or reputation due to that origin.",
                "Design": "Protection for the visual appearance of products, including shape, configuration, pattern, or ornament.",
                "Patent": "Exclusive rights granted for inventions that are new, useful, and non-obvious.",
                "Trademark": "Protection for brands, logos, symbols, words, or designs that distinguish products or services."
            }
            st.write(domain_descriptions.get(domain_prediction, ""))
        except Exception as e:
            st.error(f"Error predicting domain: {str(e)}")
    else:
        st.info("Enter a question to see the predicted IP law domain.")

# Function to process query
def process_query(query_text):
    try:
        # Direct call to the answer_query function from ip_law_expert.py
        return answer_query(query_text)
    except Exception as e:
        return {
            "result": f"Error processing query: {str(e)}",
            "domain": "Error",
            "sources": []
        }

# Submit button and processing
if st.button("Submit", type="primary") and query:
    # Add query to conversation history
    st.session_state.conversation_history.append({"role": "user", "content": query})
    
    # Create a progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Simulate progress steps
    status_text.text("Detecting language...")
    progress_bar.progress(20)
    time.sleep(0.5)
    
    status_text.text("Classifying domain...")
    progress_bar.progress(40)
    time.sleep(0.5)
    
    status_text.text("Retrieving knowledge...")
    progress_bar.progress(60)
    time.sleep(0.5)
    
    status_text.text("Generating response...")
    progress_bar.progress(80)
    time.sleep(0.5)
    
    # Process the query
    response = process_query(query)
    
    # Complete the progress
    progress_bar.progress(100)
    status_text.text("Done!")
    time.sleep(0.3)
    
    # Clear the progress indicators
    progress_bar.empty()
    status_text.empty()
    
    # Add response to conversation history
    st.session_state.conversation_history.append({
        "role": "assistant", 
        "content": response["result"],
        "domain": response["domain"],
        "sources": response["sources"]
    })

# Display conversation history
st.subheader("Conversation History")
if not st.session_state.conversation_history:
    st.info("No conversation yet. Start by asking a question!")
else:
    for i, message in enumerate(st.session_state.conversation_history):
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        else:
            # Get domain color
            domain_colors = {
                "Copyright": "#1E40AF",  # Blue
                "GI": "#047857",  # Green
                "Design": "#9D174D",  # Pink
                "Patent": "#B45309",  # Amber
                "Trademark": "#4338CA"  # Indigo
            }
            color = domain_colors.get(message["domain"], "#4B5563")  # Default gray
            
            # Display domain badge
            st.markdown(f"<div class='domain-badge' style='background-color: {color};'>Domain: {message['domain']}</div>", 
                      unsafe_allow_html=True)
            
            # Display the answer
            st.markdown(f"**Assistant:** {message['content']}")
            
            # Display sources if available
            if message.get("sources") and len(message["sources"]) > 0:
                with st.expander("View Sources"):
                    sources_df = pd.DataFrame({"Source": message["sources"]})
                    st.dataframe(sources_df, hide_index=True)
            
            st.markdown("---")
