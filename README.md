# PubMed Explorer 🔬

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://pubmed-explorer.streamlit.app/)

This is a Streamlit web application that allows users to search PubMed, explore research articles, summarize, simplify, answer questions, analyze trends and receive recommendations. It uses the NCBI Entrez API for fetching data and Google's Gemini Pro AI API for advanced text processing.

## Features

- **PubMed Search:** Search for articles using keywords, with options to specify the number of results.
- **Article Exploration:** Displays article details such as title, authors, journal, year, abstract, and DOI.
- **Text Summarization:** Summarize research abstracts using AI.
- **Text Simplification:** Simplify complex medical abstracts into easy-to-understand language.
- **Question Answering:** Get answers to questions based on the research abstracts.
- **Trend Analysis:** Analyze trends from a collection of abstracts.
- **Article Recommendation:** Get recommendations for related articles based on a given abstract.
- **CSV Export:** Export search results to a CSV file.
- **Interactive UI:** A clean, modern interface built with Streamlit, designed for ease of use.

## Technologies Used

-   **Python:** Core programming language.
-   **Streamlit:** For building the web application interface.
-   **Biopython:** For interacting with NCBI Entrez and parsing Medline data.
-   **Google Gemini Pro AI API:** For text summarization, simplification, question-answering, recommendations and trend analysis.
-   **Pandas:** For data manipulation and CSV export.

## Setup and Installation

Follow these steps to set up the application:

### 1. Clone the Repository

```bash
git clone https://github.com/Kshitij10000/PubMed-Explorer.git
```

2. Install Required Libraries
3. 
Make sure you have Python 3.8 or higher installed. We recommend using a virtual environment.
```code
python -m venv venv
source venv/bin/activate # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```
3. Set up API Key
```bash
Create a .streamlit/secrets.toml file in your project's root directory. Add your Google Gemini API key to this file:
```
```bash
[mongo]
uri = "mongodb+srv://<id>:<your password>@streamlitfree.cblfh.mongodb.net/?retryWrites=true&w=majority&appName=streamlitfree"

[GOOGLE_API_KEY]
value="YOUR_GOOGLE_GEMINI_API_KEY"
```
inside toml

Replace YOUR_GOOGLE_GEMINI_API_KEY with your actual API key.
Replace mongodb url with your actual url.

Security Note: Never commit your API key directly to your repository.

4. Run
5. the Streamlit App

```bash
streamlit run app.py
```

This will start the Streamlit app, and you can view it in your browser at the displayed URL (usually http://localhost:8501).

## Code Structure
app.py: The main Streamlit application code, handling the UI and data interaction.

llm_utils.py: Contains functions for text processing and interacting with the Gemini AI API.

db_utils.py: Contains the function to initialize and update the visit counter.

requirements.txt: Lists all the necessary Python libraries.

logo.png: Logo used in the app.

.streamlit/secrets.toml: (Not committed to Git) Stores the Google Gemini API key.

## Usage
Search: Enter your search query in the input field and hit enter to see a list of matching articles.

Article Details: Expand each article to view the full details, including title, authors, abstract, and more.

Actions: Use the buttons below each abstract to summarize, simplify, or get recommendations, ask a question, or export article data.

Analysis: Use the 'Analyze Trends in Loaded Articles' button at the end of the result to extract research trends in abstracts.

CSV Export: Use the 'Download Results as CSV' button to download all articles in CSV format.

## Important Notes
The Gemini API is rate-limited. If you encounter issues, ensure you are within the API's usage limits.

Error handling is in place, but the app may need additional adjustments to handle all cases.

Ensure the necessary API keys and libraries are properly set up before running the application.

This project is mainly for educational purposes and exploring the capabilities of PubMed and Gemini AI.

## Contributing
  Contributions are welcome! Please feel free to open issues or submit pull requests with improvements or bug fixes.

## License
This project is licensed under the MIT License.

## Future Enhancements
Add more search filters (date range, etc.).
Implement user authentication.
Provide a more visual way to display search results.
Add functionalities to explore related articles.
Create a database to store user data and search history.

## Contact
If you have any questions or suggestions, feel free to contact me at kshitijsarve2001@gmail.com.
