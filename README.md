# 🤖 Multi-Source AI Research Agent

A sophisticated AI orchestration system built with **Python** and **LangChain**. This agent autonomously retrieves, processes, and analyzes data from three distinct sources: **PDFs**, **Google Sheets**, and **YouTube transcripts**, providing high-fidelity executive summaries and a real-time data dashboard.

## 🚀 Key Features
* **Multi-Source Ingestion:** Support for unstructured (PDF), structured (Google Sheets), and multimedia (YouTube) data.
* **LangChain Orchestration:** Utilizes **LCEL (LangChain Expression Language)** to chain prompts and LLMs for consistent, reproducible results.
* **Groq Inference Engine:** Powered by **Llama 3.3 (70B Versatile)** for ultra-fast, high-quality analysis.
* **Live Process Logging:** A real-time "Agent Log" that tracks every step of the retrieval and synthesis process.
* **Insights Dashboard:** Automated NLP analysis featuring word frequency metrics and data profiling.


---

## 🛠️ Technical Stack
* **Frontend:** [Streamlit](https://streamlit.io/)
* **AI Framework:** [LangChain](https://www.langchain.com/)
* **LLM Provider:** [Groq Cloud](https://groq.com/) (Llama-3.3-70b-versatile)
* **APIs:** Google Sheets API, YouTube Transcript API
* **Data Processing:** PyPDF2, Pandas, Regex (NLP)



---

## 📋 Objectives Met
1.  **Retrieval:** Successfully pulls data from cloud APIs (Sheets) and local file uploads.
2.  **Orchestration:** Uses a sophisticated LangChain pipeline to handle diverse content types.
3.  **Individual Processing:** Files are processed as unique entities before final synthesis.
4.  **Visual Dashboard:** Real-time metrics and charts profile the analyzed text data.
5.  **Automated Action:** System generates downloadable executive reports.
6.  **Reliability:** Implemented error handling for API connections and model decommissioning.

---

## ⚙️ Installation & Setup
1. **Create a Virtual Environment:**
   ```bash
    python -m venv venv 
    ```

2. **Activate the Environment:**
    ```bash
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
    .\venv\Scripts\Activate.ps1   #if using cmd promt: .\venv\Scripts\activate.bat
    
    ```
3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Run the App:**
    ```bash
    streamlit run app.py
    ```
