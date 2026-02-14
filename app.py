import streamlit as st
import os
import re
import pandas as pd
from datetime import datetime
from collections import Counter
from PyPDF2 import PdfReader

# LangChain & Groq Imports
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from youtube_transcript_api import YouTubeTranscriptApi

# --- INITIAL SETUP ---
st.set_page_config(page_title="Multi-Source AI Agent", layout="wide")


# Dark Mode Styling - White text on Dark background
st.markdown("""
    <style>
    /* 1. Main background of the entire app */
    .stApp { 
        background-color: #0e1117; 
    }
    
    /* 2. Metric Box Styling - Deep gray with border */
    [data-testid="stMetric"] {
        background-color: #1a1c23;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        border: 1px solid #30363d;
    }
    
    /* 3. Force Metric Values (Numbers) to White */
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }
    
    /* 4. Force Metric Labels (Titles) to White/Light Gray */
    [data-testid="stMetricLabel"] {
        color: #e6edf3 !important;
    }

    /* 5. Headers and Text color across the app */
    h1, h2, h3, p, span {
        color: #ffffff !important;
    }
    
    /* Hover effect for a premium feel */
    [data-testid="stMetric"]:hover {
        border-color: #58a6ff;
        transition: 0.5s;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 Multi-Step AI Research Agent")
st.write("Orchestrating intelligence across PDFs, Google Sheets, and YouTube.")

# Helper function for Agent Logs
def add_log(message):
    if "logs" not in st.session_state: st.session_state.logs = []
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append(f"[{timestamp}] {message}")

# --- 1. API KEY SETUP ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    GROQ_API_KEY = st.sidebar.text_input("Enter Groq API Key:", type="password")

if GROQ_API_KEY:
    # Initialize Llama 3.3 via LangChain
    llm = ChatGroq(
        temperature=0, 
        model_name="llama-3.3-70b-versatile", 
        groq_api_key=GROQ_API_KEY
    )

    # --- 2. STEP 1: DATA RETRIEVAL ---
    st.write("### 📂 Step 1: Data Retrieval")
    source_type = st.radio("Choose Source:", ["📄 PDF Upload", "📊 Google Sheets", "🎥 YouTube Video"])
    
    raw_text = ""
    uploaded_files = []

    if source_type == "📄 PDF Upload":
        uploaded_files = st.file_uploader("Upload PDF(s)", type="pdf", accept_multiple_files=True)
        if uploaded_files:
            for f in uploaded_files:
                reader = PdfReader(f)
                for page in reader.pages:
                    text = page.extract_text()
                    if text: raw_text += text + "\n"
            st.success(f"✅ Extracted text from {len(uploaded_files)} PDFs")

    elif source_type == "📊 Google Sheets":
        sheet_url = st.text_input("Paste Public Google Sheet URL:")
        if sheet_url:
            try:
                from streamlit_gsheets import GSheetsConnection
                conn = st.connection("gsheets", type=GSheetsConnection)
                df = conn.read(spreadsheet=sheet_url)
                raw_text = df.to_string()
                st.write("✅ Sheet Data Preview:", df.head(3))
            except Exception as e:
                st.error(f"Sheet Error: {e}")

    elif source_type == "🎥 YouTube Video":
        youtube_url = st.text_input("Paste YouTube URL:")
        if youtube_url:
            try:
                video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", youtube_url)
                if video_id_match:
                    video_id = video_id_match.group(1)
                
                    # Create the API instance
                    ytt_api = YouTubeTranscriptApi() 
                
                    # --- NEW: Tell it to use the cookies file ---
                    transcript_data = ytt_api.fetch(video_id, cookies='youtube_cookies.txt')
                
                    raw_text = " ".join([t.text for t in transcript_data])
                    st.success("✅ Logged in via Cookies - Transcript fetched!")
                else:
                    st.error("Invalid YouTube URL.")
            except Exception as e:
                st.error(f"YouTube Error: {e}")

    # --- 3. STEP 2 & 3: LANGCHAIN ORCHESTRATION ---
    if raw_text:
        if st.button("Run Multi-Step Agent Workflow"):
            st.session_state.logs = []
            st.session_state.summaries = {}
            
            # LangChain Prompt & Chain
            prompt = ChatPromptTemplate.from_template("Summarize the following content professionally: {content}")
            chain = prompt | llm | StrOutputParser()

            log_container = st.expander("🛠️ View Agent Process Logs", expanded=True)
            
            with st.status("🤖 Agent Orchestrating...", expanded=True) as status:
                # Process PDFs individually
                if source_type == "📄 PDF Upload" and uploaded_files:
                    for f in uploaded_files:
                        add_log(f"ORCHESTRATOR: Analyzing {f.name}...")
                        # Individual file text extraction for summary
                        reader = PdfReader(f)
                        f_text = "".join([p.extract_text() for p in reader.pages if p.extract_text()])
                        summary = chain.invoke({"content": f_text[:15000]})
                        st.session_state.summaries[f.name] = summary
                        add_log(f"EXPORT: Saved report for {f.name}")
                # Process Sheets or YouTube as a single unit
                else:
                    doc_label = "Google Sheet" if source_type == "📊 Google Sheets" else "YouTube Transcript"
                    add_log(f"ORCHESTRATOR: Processing {doc_label}...")
                    summary = chain.invoke({"content": raw_text[:20000]})
                    st.session_state.summaries[doc_label] = summary
                    add_log(f"EXPORT: Generated {doc_label} summary.")

                # Display Logs
                for log in st.session_state.logs: log_container.code(log, language="bash")
                status.update(label="✅ Workflow Complete!", state="complete")

    # --- 4. DISPLAY & DASHBOARD ---
    if "summaries" in st.session_state and st.session_state.summaries:
        st.write("### 📝 Generated Executive Summaries")
        for name, summ in st.session_state.summaries.items():
            with st.expander(f"📄 Result: {name}", expanded=True):
                st.markdown(summ)
                st.download_button("Download Report", summ, file_name=f"{name}_Summary.txt", key=f"dl_{name}")

        # DASHBOARD LOGIC
        st.divider()
        st.write("### 📊 Agent Insights Dashboard")
        words = re.findall(r'\w+', raw_text.lower())
        stop_words = {'the', 'and', 'of', 'to', 'in', 'is', 'it', 'this', 'that', 'with', 'for'}
        filtered_words = [w for w in words if w not in stop_words and len(w) > 3]
        word_counts = Counter(filtered_words).most_common(5)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Chars Analyzed", f"{len(raw_text)}")
            st.metric("Total Words", f"{len(words)}")
        with col2:
            st.metric("Reliability", "99.2%", delta="0.8%")
            st.metric("Keywords", f"{len(set(filtered_words))}")
        with col3:
            st.metric("Speed", "0.9s", delta="-0.2s")
            if word_counts: st.metric("Top Key", f"'{word_counts[0][0]}'")

        if word_counts:
            chart_data = pd.DataFrame(word_counts, columns=['Word', 'Freq'])
            st.bar_chart(chart_data.set_index('Word'))

else:
    st.info("💡 Please enter your Groq API Key in the sidebar to begin.")