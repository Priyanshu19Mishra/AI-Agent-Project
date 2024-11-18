import streamlit as st
import pandas as pd
from serpapi import GoogleSearch
from dotenv import load_dotenv
import os
import openai

# Load API keys from .env file
load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# Initialize session state for storing data and button click state
if 'data' not in st.session_state:
    st.session_state['data'] = None
if 'web_results' not in st.session_state:
    st.session_state['web_results'] = None
if 'fetched_results' not in st.session_state:
    st.session_state['fetched_results'] = None
if 'prompt_result' not in st.session_state:
    st.session_state['prompt_result'] = None

# Function to fetch web results using SerpAPI
def fetch_web_results(query):
    if not SERPAPI_KEY:
        return "Error: SerpAPI key not found."
    try:
        params = {
            "engine": "google",
            "q": query,
            "api_key": SERPAPI_KEY,
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        return results.get("organic_results", [])  # Return organic results
    except Exception as e:
        return f"Error: {e}"

# Function to process and extract relevant information from web results
def extract_display_results(results):
    if isinstance(results, list):  # Ensure results are iterable
        return [
            {
                "title": item.get("title", "N/A"),
                "link": item.get("link", "N/A"),
                "snippet": item.get("snippet", "N/A")
            }
            for item in results
        ]
    return "No results found."

# Function to save web results for the LLM
def save_results(results):
    result_text = "\n".join(
        [f"Title: {item['title']}\nLink: {item['link']}\nSnippet: {item['snippet']}\n"
         for item in results]
    )
    st.session_state['fetched_results'] = result_text  # Save to session state
    return result_text

# Function to process data using OpenAI's LLM
# Function to process the fetched web results with OpenAI
def process_with_llm(prompt, web_results):
    try:
        # Format the web results for input to OpenAI
        formatted_results = "\n".join(
            [f"Title: {item['title']}\nLink: {item['link']}\nSnippet: {item['snippet']}\n" for item in web_results]
        )
        # Create the prompt for OpenAI
        full_prompt = f"Here are the web results:\n{formatted_results}\n\nTask: {prompt}"

        # Call OpenAI Completion API
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=full_prompt,
            temperature=0.7,
            max_tokens=2000
        )

        # Debug: Print the response object to inspect its structure
        print("OpenAI Response Debug:", response)

        # Safely access the generated text
        if 'choices' in response and isinstance(response['choices'], list) and len(response['choices']) > 0:
            return response['choices'][0].get('text', '').strip()
        else:
            return "Error: Unexpected response structure from OpenAI API."

    except Exception as e:
        return f"Error while processing with LLM: {e}"


# Streamlit App
st.title("LLM-Based AI Agent")

# Sidebar for uploading CSV
st.sidebar.header("Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file:
    # Read uploaded file and store it in session state
    data = pd.read_csv(uploaded_file)
    st.session_state['data'] = data  # Store data in session state

# Retrieve data from session state
if st.session_state['data'] is not None:
    data = st.session_state['data']

    # Display uploaded data
    st.write("Uploaded Data:")
    st.dataframe(data.head())

    # Task 1: Ask user to select a column
    st.write("Select a Column:")
    selected_column = st.selectbox("Select column to choose from", data.columns)

    # Task 2: Ask user to select a particular query from the selected column
    st.write(f"Select a Query from the '{selected_column}' column:")
    selected_query = st.selectbox("Select a query:", data[selected_column].values)
    st.write(f"Selected Query: {selected_query}")

    # Task 3: Fetch web results for the selected query
    if st.button("Fetch Web Results"):
        with st.spinner("Fetching web results..."):
            web_results = fetch_web_results(selected_query)
            processed_results = extract_display_results(web_results)
            st.session_state['web_results'] = processed_results  # Store fetched results in session state
            save_results(processed_results)  # Save results for LLM
        st.success("Web results fetched successfully!")

    # Display fetched web results if available
    if 'web_results' in st.session_state and st.session_state['web_results'] is not None:
        st.write("Processed Web Results:")
        for result in st.session_state['web_results']:
            st.write(f"**Title:** {result['title']}")
            st.write(f"**Link:** [Link]({result['link']})")
            st.write(f"**Snippet:** {result['snippet']}")
            st.write(" ")

    # Task 4: LLM Integration Section
    st.subheader("LLM Integration")

    # Task 5: Text input box for prompt
    prompt = st.text_area("Enter your prompt for the selected query:", height=150)

    # Task 6: Submit button for processing prompt
    if st.button("Submit"):
        if 'fetched_results' in st.session_state and st.session_state['fetched_results'] is not None:
            with st.spinner("Processing with LLM..."):
                result = process_with_llm(prompt, st.session_state['fetched_results'])
                st.session_state['prompt_result'] = result  # Save result
            st.success("Processing complete!")

    # Task 7: Display the result
    if st.session_state['prompt_result']:
        st.write("Generated Results:")
        st.write(st.session_state['prompt_result'])

else:
    st.write("Please upload a CSV file to proceed.")
