# AI-Agent-Project

Project Overview
The AI Agent project demonstrates the integration of large language models (LLMs) with automated web searches to create an interactive AI tool. Users can upload a dataset, fetch relevant web data for specific queries, and interact with the retrieved data using custom prompts. The app utilizes OpenAI's GPT models for natural language processing and SerpAPI for web searches, all within a user-friendly Streamlit interface.

Key Features
1. CSV File Integration: Upload CSV files to explore and select queries for further analysis.
2. Web Search Automation: Use SerpAPI to fetch web results based on user-selected queries.
3. Custom Prompt Handling: Accept any user-defined prompt for operations on the fetched data.
4. LLM Integration: Leverage OpenAI's GPT to process web data and return meaningful insights based on the prompt.
5. Export Results: Download processed results as a .txt file for offline use.


Setup Instructions
Follow these steps to set up and run the application:

Prerequisites
1. Python 3.7 or higher installed on your machine.
2. Required Python libraries:

   streamlit
   
   pandas
   
   serpapi
   
   openai
   
   python-dotenv

Installation Steps

Clone the Repository:
bash
Copy code
git clone https://github.com/your-username/AI-Agent-Project.git
cd AI-Agent-Project

Install Dependencies:
bash
Copy code
pip install -r requirements.txt

Add API Keys: Create a .env file in the project root directory and add your API keys:
Copy code
OPENAI_API_KEY=your_openai_api_key
SERPAPI_KEY=your_serpapi_key

Run the App: Start the Streamlit application:
bash
Copy code
streamlit run main.py   
