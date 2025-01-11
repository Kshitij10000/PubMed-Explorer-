import streamlit as st
import random
from db_utils import init_counter, update_visit_count
from Bio import Entrez, Medline
import pandas as pd
from llm_utils import summarize_text, simplify_text, answer_question, analyze_trends, recommend_articles

# Page configuration and base CSS with Google Fonts, branding, and layout styling
st.set_page_config(page_title="PubMed Explorer 🔬", page_icon="✅", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    
    /* Hide default menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Global font and background styling */
    html, body {
        font-family: 'Roboto', sans-serif;
        background: linear-gradient(to right, #fdfbfb, #ebedee);
    }
    
    /* Styling for compact info boxes in a single line */
    .info-container {
        display: flex;
        justify-content: flex-start;
        gap: 10px;
        align-items: center;
    }
    .info-box {
        text-align: center;
        padding: 5px;
        border-radius: 5px;
        font-size: 14px;
        font-weight: bold;
        width: 80px; /* Compact width */
        box-shadow: 1px 1px 5px rgba(0, 0, 0, 0.1);
    }
    .visitors-box {
        background-color: #e0f7fa;
        color: #006064;
    }
    .active-users-box {
        background-color: #7CFC00;
        color: #6d4c41;
    }
    
    /* Custom styling for expanders */
    .streamlit-expanderHeader {
        background-color: #ffecb3 !important; /* Light yellow header background */
        color: #6d4c41 !important; /* Brown text color */
        font-size: 18px !important;
        font-weight: bold !important;
        padding: 10px !important;
        border-radius: 5px;
    }
    .streamlit-expanderContent {
        background-color: #ffffff !important; /* White content background */
        padding: 10px !important;
        border: 1px solid #e0e0e0 !important; /* Light gray border */
        border-radius: 5px;
    }
    
    /* Custom button styles */
    .stButton>button {
        border-radius: 5px;
        padding: 8px 16px;
        font-size: 14px;
        font-weight: bold;
        margin-top: 5px;
        margin-bottom: 5px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
        display: block; /* Changed to block to make buttons vertical */
        width: fit-content; /* Ensure buttons are not full width by default */
    }

    .summarize-button {
        background-color: #4CAF50;
        color: white;
    }
    .summarize-button:hover {
        background-color: #367c39;
    }
    .simplify-button {
        background-color: #2196F3;
        color: white;
    }
    .simplify-button:hover {
        background-color: #1565c0;
    }
    .recommend-button {
        background-color: #FF9800;
        color: white;
    }
    .recommend-button:hover {
        background-color: #e67e00;
    }
    </style>
    <style>
    .button-container {
        background-color: #f8f9fa; /* Light gray background */
        padding: 15px;
        border: 1px solid #ddd; /* Light border */
        border-radius: 8px; /* Rounded corners */
        margin-bottom: 20px; /* Spacing below the container */
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1); /* Subtle shadow */
    }
    .button-container h4 {
        font-size: 18px;
        font-weight: bold;
        color: #333; /* Dark text */
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize counters
init_counter()
current_count = update_visit_count()

# Simulate active online users randomly between 1 and 10
active_users = random.randint(1, 10)

Entrez.email = "ruchirsarve@gmail.com"

# Refined header layout: smaller logo and compact info boxes

header_cols = st.columns([1, 4, 3])
with header_cols[0]:
    st.image("logo.png", width=80)  # Smaller logo size for compactness
with header_cols[1]:
    st.title("PubMed Explorer 🔬")
with header_cols[2]:
    # Side-by-side info boxes
    st.markdown(f"""
    <div class='info-container'>
        <div class='info-box visitors-box'>Visitors<br>{current_count}</div>
        <div class='info-box active-users-box'>Active<br>{active_users}</div>
    </div>
    """, unsafe_allow_html=True)

# Initialize session state variables
if 'query' not in st.session_state:
    st.session_state.query = ""
if 'records' not in st.session_state:
    st.session_state.records = []
if 'total_found' not in st.session_state:
    st.session_state.total_found = 0

# Layout with columns: number input and search query
col1, col2 = st.columns([1, 3])
with col1:
    num_articles = st.number_input("Number of articles to fetch", min_value=1, max_value=100, value=20, step=1)
with col2:
    query_input = st.text_input("Enter your search query 🔍", placeholder="e.g., 'cancer therapy' or 'gene editing'")

if query_input and query_input != st.session_state.query:
    st.session_state.query = query_input
    st.session_state.records = []
    st.session_state.total_found = 0

# Proceed with PubMed search if query exists
if st.session_state.query:
    with st.spinner("Searching PubMed... ⏳"):
        search_handle = Entrez.esearch(
            db="pubmed",
            term=st.session_state.query,
            retmax=str(num_articles),
            retstart=0
        )
        search_results = Entrez.read(search_handle)
        search_handle.close()

    st.session_state.total_found = int(search_results.get("Count", "0"))
    new_ids = search_results.get("IdList", [])

    if new_ids:
        with st.spinner("Fetching article details... 📚"):
            fetch_handle = Entrez.efetch(
                db="pubmed",
                id=",".join(new_ids),
                rettype="medline",
                retmode="text"
            )
            st.session_state.records = list(Medline.parse(fetch_handle))
            fetch_handle.close()

    st.metric(label="Total articles found", value=f"{st.session_state.total_found} 🎯")
    st.write(f"**Displaying {len(st.session_state.records)} of {st.session_state.total_found} articles...**")

    # Inside the loop for displaying articles:
    for record in st.session_state.records:
        pmid = record.get("PMID", "N/A")
        title = record.get("TI", "No title")
        authors = record.get("AU", [])
        journal = record.get("JT", "Unknown journal")
        year = record.get("DP", "Unknown date").split()[0]
        abstract = record.get("AB", "No abstract available.")
        doi = record.get("LID", "").split(" ")[0] if record.get("LID", "") else "N/A"
        pubmed_url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
        mesh_terms = record.get("MH", [])
        mesh_display = ", ".join(mesh_terms) if mesh_terms else "N/A"

        # Use plain text for the expander title
        with st.expander(title):
            # Inside the expander, style the title using Markdown/HTML
            st.markdown(f"<p style='font-size: 18px; font-weight: bold; color: #007BFF;'>{title}</p>", unsafe_allow_html=True)

            # Arrange metadata in two columns
            col1_meta, col2_meta = st.columns(2)
            with col1_meta:
                st.markdown(f"<p style='color: #007BFF; font-size: 16px;'><strong>PMID:</strong> {pmid}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: #28A745; font-size: 16px;'><strong>Journal:</strong> {journal}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: #6C757D; font-size: 16px;'><strong>Year:</strong> {year}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: #DC3545; font-size: 16px;'><strong>DOI:</strong> {doi}</p>", unsafe_allow_html=True)
            with col2_meta:
                st.markdown(f"<p style='color: #17A2B8; font-size: 16px;'><strong>Authors:</strong> {', '.join(authors) if authors else 'N/A'}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: #FFC107; font-size: 16px;'><strong>MeSH Terms:</strong> {mesh_display}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: #007BFF; font-size: 16px;'><strong>Link:</strong> <a href='{pubmed_url}' target='_blank' style='text-decoration: none; color: #007BFF;'>Original Article 🔗</a></p>", unsafe_allow_html=True)
            
            st.markdown(f"<p style='color: #343A40; font-size: 16px;'><strong>Abstract:</strong> {abstract}</p>", unsafe_allow_html=True)

            # Use a single column for the buttons for vertical alignment
            st.markdown("<div style='display: flex; flex-direction: column;'>", unsafe_allow_html=True)

            if st.button(f"Summarize 📝", key=f"summarize_{pmid}",  type="primary",  help="Summarize the abstract"):
               with st.spinner("Summarizing abstract... ⏳"):
                  try:
                       summary = summarize_text(abstract)
                       st.markdown(f"**Summary:** {summary}")
                  except Exception as e:
                        st.error(f"Summarization error: {e}")

            if st.button(f"Simplify 🤓", key=f"simplify_{pmid}", type="primary", help="Simplify the abstract"):
                with st.spinner("Simplifying abstract... 💡"):
                    try:
                       simple_text = simplify_text(abstract)
                       st.markdown(f"**Simplified Explanation:** {simple_text}")
                    except Exception as e:
                        st.error(f"Simplification error: {e}")
            
            if st.button(f"Recommend 📚", key=f"recommend_{pmid}", type="primary", help="Recommend articles based on the abstract"):
                with st.spinner("Generating recommendations... 🚀"):
                    try:
                       recommendations = recommend_articles(abstract)
                       st.markdown(f"**Recommendations:** {recommendations}")
                    except Exception as e:
                        st.error(f"Recommendation error: {e}")

            st.markdown("</div>", unsafe_allow_html=True)

            question = st.text_input(f"Ask a question about PMID {pmid}:", key=f"qa_{pmid}")
            if question:
                with st.spinner("Answering question... 🤔"):
                    try:
                        answer = answer_question(abstract, question)
                        st.markdown(f"**Answer:** {answer}")
                    except Exception as e:
                        st.error(f"Question answering error: {e}")

if st.session_state.records:
    # Container for Analyze Trends and CSV Export
    st.markdown("<div class='button-container'>", unsafe_allow_html=True)

    # Header for the container
    st.markdown("<h4>Bulk Actions 🚀</h4>", unsafe_allow_html=True)
    
    # Use a single column for the bulk action buttons
    st.markdown("<div style='display: flex; flex-direction: column;'>", unsafe_allow_html=True)

    # Analyze Trends Button
    if st.button("Analyze Trends in Loaded Articles 📈", type="primary",  help="Gives analysis of trends in the loaded articles"):
        with st.spinner("Analyzing trends... 📊"):
            try:
                abstracts = [rec.get("AB", "") for rec in st.session_state.records if rec.get("AB")]
                if abstracts:
                    trends_summary = analyze_trends(abstracts)
                    st.markdown(f"**Research Trends Summary:** {trends_summary}")
                else:
                    st.info("No abstracts available for trend analysis.")
            except Exception as e:
                st.error(f"Trend analysis error: {e}")

    # Export Results as CSV Button
    export_data = []
    for record in st.session_state.records:
        export_data.append({
            "PMID": record.get("PMID", ""),
            "Title": record.get("TI", ""),
            "Journal": record.get("JT", ""),
            "Year": record.get("DP", "").split()[0] if record.get("DP") else "",
            "Authors": "; ".join(record.get("AU", [])),
            "Abstract": record.get("AB", ""),
            "DOI": record.get("LID", "").split(" ")[0] if record.get("LID") else "",
            "PubMed URL": f"https://pubmed.ncbi.nlm.nih.gov/{record.get('PMID', '')}/"
        })
    df = pd.DataFrame(export_data)
    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="Download Results as CSV 💾",
        data=csv,
        file_name='pubmed_results.csv',
        mime='text/csv',
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # Close the styled container
    st.markdown("</div>", unsafe_allow_html=True)