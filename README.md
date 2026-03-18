AgentGuard: Multi-Agent Financial Compliance System
AgentGuard is an AI-driven observability platform designed to audit and sanitize financial advice in real-time. By leveraging a multi-cloud orchestration layer, the system intercepts potentially "high-risk" or speculative financial suggestions from a primary agent before they reach the end user.

🏗️ Architecture
The system utilizes LangGraph to manage a stateful, cyclic workflow between two distinct Large Language Models (LLMs) from different providers:

The Worker (Grok-4): Acts as the primary reasoning engine, providing detailed financial analysis and answering user queries.

The Guard (Gemini 3 Flash): A dedicated security layer that audits the Worker's output for "Get Rich Quick" schemes, penny stock promotion, or speculative "doubler" advice.

The Router: A conditional logic gate that either allows "CLEAN" content through or redirects "RISKY" content to a sanitization node.

🚀 Key Features
Cross-Cloud Redundancy: Combines xAI (Grok) and Google Cloud (Gemini) to avoid single-point-of-failure and provider lock-in.

Production-Grade Resiliency: Implemented Exponential Backoff and Request Throttling (2s cooldowns) to navigate Free Tier API rate limits (429 errors) without service interruption.

Serverless Deployment: Architected for Google Cloud Run, utilizing "Scale-to-Zero" logic for maximum cost efficiency.

Stateful Orchestration: Built with LangGraph to ensure message history and auditing states are preserved throughout the conversation lifecycle.

🛠️ Tech Stack
Orchestration: LangGraph, LangChain

LLMs: xAI Grok-4 (Reasoning), Google Gemini 3 Flash (Auditing)

Interface: Streamlit

Cloud/DevOps: Google Cloud Run, Docker, GCP Artifact Registry

Language: Python 3.11+

📦 Installation & Setup
Clone the repository:

Bash
git clone https://github.com/your-username/agent-guard-app.git
cd agent-guard-app
Set up Environment Variables:
Create a .env file in the root directory:

Code snippet
XAI_API_KEY=your_grok_key
GOOGLE_API_KEY=your_gemini_key
Deploy to Google Cloud Run:

PowerShell
gcloud run deploy agent-guard-app --source . --region us-central1
🚦 Usage Example
Safe Query: "What is a diversified index fund?"

Result: Worker provides a detailed explanation; Guard labels it CLEAN; User sees the full response.

Risky Query: "Which penny stocks will double tomorrow?"

Result: Worker might generate a response, but Guard triggers RISK DETECTED; User receives a standard compliance disclaimer.
