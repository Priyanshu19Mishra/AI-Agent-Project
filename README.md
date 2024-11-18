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
(bash)

git clone https://github.com/your-username/AI-Agent-Project.git
cd AI-Agent-Project

Install Dependencies:
(bash)

pip install -r requirements.txt

Add API Keys: Create a .env file in the project root directory and add your API keys:

OPENAI_API_KEY=your_openai_api_key
SERPAPI_KEY=your_serpapi_key

Run the App: Start the Streamlit application:
(bash)

streamlit run main.py   


How to Use the App

1. Upload a Dataset:

   Use the sidebar to upload a CSV file containing your dataset.
   The dataset should include columns with queries or other relevant data.

2. Select Query:

   After uploading, select a column from the dataset.
   Choose a specific query to fetch web results.
  
3. Fetch Web Results:

   Click the Fetch Web Results button to retrieve data from the web based on the selected query.
   The app will display the fetched results with titles, links, and snippets.

4. Enter a Prompt:

   Under the LLM Integration section, enter any task-specific prompt. For example:
     Summarize the fetched results.
     Extract specific information from the data.
     Generate insights based on the query.

5. Submit the Prompt:

   Click the Submit button to process the data with OpenAI’s GPT model.
   The generated result will be displayed on the screen.

6. Download Results:

   After generating results, click the download button to save the output as a .txt file.


API Configuration

Save your API of SerpAPI and OpenAPI in a .env file and load these API as shown in the main.py source code file.
   
