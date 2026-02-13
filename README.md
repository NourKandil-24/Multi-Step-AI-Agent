# 🤖 Multi-Step AI Agent System

A sophisticated AI Orchestration system built with **Streamlit** and **Groq**. This agent handles end-to-end data processing: from retrieving data across various sources (PDF & Google Sheets) to generating executive summaries and automating report exports.

## 🚀 Key Features

* **Multi-Source Data Retrieval:** Supports unstructured data from **PDFs** and structured data from **Google Sheets**.
* **High-Speed Inference:** Powered by **Groq** (Llama 3 / Mixtral) for near-instant analysis.
* **Agentic Orchestration:** Features a Researcher Agent (Extraction) and a Writer Agent (Synthesis).
* **Automated Action:** Automatically generates, timestamps, and saves text reports to the local file system.
* **Interactive Dashboard:** Visualizes system performance and data metrics in real-time.

---

## 🛠️ Architecture & Logic

The system follows a sequential orchestration pattern:
1.  **Ingestion Layer:** Normalizes data from diverse formats into a text stream.
2.  **Logic Layer:** Validates data length and quality before passing it to the LLM.
3.  **Synthesis Layer:** Uses professional-grade prompting to transform raw data into executive reports.
4.  **Action Layer:** Triggers a local file system write and provides a UI download bridge.



---


