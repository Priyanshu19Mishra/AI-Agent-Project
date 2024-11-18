import streamlit as st
import pandas as pd
from serpapi import GoogleSearch
from dotenv import load_dotenv
import os

# Load API keys from .env file
load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
print(f"SerpAPI Key Loaded: {SERPAPI_KEY is not None}")

# Initialize session state for storing data and button click state
if 'data' not in st.session_state:
    st.session_state['data'] = None
if 'web_results' not in st.session_state:
    st.session_state['web_results'] = None
if 'submit_clicked' not in st.session_state:
    st.session_state['submit_clicked'] = False

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

# Function to save results to a text file
def save_results_to_txt(results):
    result_text = "\n".join(
        [f"Title: {item['title']}\nLink: {item['link']}\nSnippet: {item['snippet']}\n"
         for item in results]
    )
    with open("/mnt/data/web_results.txt", "w") as f:
        f.write(result_text)
    return "/mnt/data/web_results.txt"

# Summarized content to display (Task 2)
summarized_results = [
    {"Title": "The Evolution and Future of Artificial Intelligence | CMU", "Link": "Link", "Snippet": "AI will drive widespread transformations in industries as it becomes more integrated into business operations. By automating repetitive tasks, AI will also ..."},
    {"Title": "The Future of AI: How AI Is Changing the World", "Link": "Link", "Snippet": "AI is already powering automation and data analysis. In the future, expect widespread adoption of autonomous machinery and AI-powered personalization."},
    {"Title": "Future of AI: Trends, Impacts, and Predictions", "Link": "Link", "Snippet": "Discover AI's potential to reshape industries, jobs, and our daily lives. Explore what the future holds for AI and its impact on the world."},
    {"Title": "The Future of AI is Now", "Link": "Link", "Snippet": "From ChatGPT to facial recognition, self-driving cars and virtual assistants such as Alexa and Siri, AI is already a part of our everyday lives."},
    {"Title": "The Future of AI: What to Expect in the Next 5 Years", "Link": "Link", "Snippet": "In the near future, AI will make us feel that life is speeding up. Human behavior will change and industries will be radically transformed."},
    {"Title": "The Future of Artificial Intelligence", "Link": "Link", "Snippet": "Improved NLP allows AI to participate in conversations with leadership, offering advice based on predictive modeling and scenario planning."},
    {"Title": "What is Artificial Intelligence and How is it Shaping the ...", "Link": "Link", "Snippet": "While some may fear that AI will replace human jobs, the reality is that it will likely create new roles that most people have not yet imagined."},
    {"Title": "Where Will Artificial Intelligence Take Us In The Future?", "Link": "Link", "Snippet": "In the future, it will be possible to use it to power AI algorithms, supercharging their ability to process huge datasets and solve complex ..."},
    {"Title": "What is the future of AI (Artificial Intelligence)?", "Link": "Link", "Snippet": "This series of McKinsey Explainers dives deep into the seven technologies that are already shaping the years to come."},
]

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

    # Task 6: Submit button (does not integrate with OpenAI API, prints predefined summary)
    if st.button("Submit"):
        st.session_state['submit_clicked'] = True  # Set submit flag to True

    # Task 7: Check if Submit was clicked and display the result
    if st.session_state['submit_clicked']:
        st.write("Submit button clicked!")
        st.write("Generated Results:")
        st.write("### Summary of Web Results:")
        for result in summarized_results:
            st.write(f"**Title:** {result['Title']}")
            st.write(f"**Link:** {result['Link']}")
            st.write(f"**Snippet:** {result['Snippet']}")
            st.write(" ")

        # After showing the summary, reset the submit flag
        st.session_state['submit_clicked'] = False

        # Task 8: Download button to save results to a text file
        st.write("Download the results as a text file:")
        download_button = st.button("Download Results")
        if download_button:
            # Save the results as a txt file
            results_txt_file = save_results_to_txt(st.session_state['web_results'])
            st.write("Click below to download the results:")
            st.download_button(
                label="Download Web Results",
                data=open(results_txt_file, "r").read(),
                file_name="web_results.txt",
                mime="text/plain"
            )

else:
    st.write("Please upload a CSV file to proceed.")
