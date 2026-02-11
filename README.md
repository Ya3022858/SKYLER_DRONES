# 📊 Monday.com Business Intelligence Agent

AI-powered conversational agent that analyzes business data from Monday.com boards and delivers executive-level insights.

Built for the **Skylark Drones Technical Assignment**.

---

## 🚀 Project Overview

This project implements an conversational AI Business Intelligence agent that integrates with Monday.com to answer founder-level questions about:

* Sales pipeline health
* Revenue performance
* Sector trends
* Operational work orders
* Leadership summaries

The agent dynamically fetches live data from Monday.com boards, cleans messy data, and generates actionable insights.

---

## ✨ Features

* Conversational BI assistant
* Live Monday.com API integration (read-only)
* Cross-board analytics (Deals + Work Orders)
* Data cleaning & normalization
* Executive-friendly summaries
* Error handling & resilience
* Leadership update generation

---

## 🏗 Architecture

User Query
→ AI Agent (Antigravity)
→ Monday.com API
→ Data Cleaning Layer
→ Analytics Engine
→ Insight Generation
→ Response

The system processes messy business data and converts it into structured executive insights.

---

## 🛠 Tech Stack

* AI Framework: Antigravity
* Backend: Python / Node.js
* API: Monday.com GraphQL API
* Environment Config: .env
* Hosting: (Add your platform here)

---

## 📦 Setup Instructions

### 1. Clone Repository

```
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

---

### 2. Install Dependencies

Python:

```
pip install -r requirements.txt
```

Node.js:

```
npm install
```

---

### 3. Configure Environment Variables

Create a `.env` file in the root folder:

```
MONDAY_API_KEY=your_api_key
WORK_ORDERS_BOARD_ID=your_work_orders_board_id
DEALS_BOARD_ID=your_deals_board_id
```

### How to get credentials:

* API Key → Monday.com → Admin → Developers → API Token
* Board ID → Copy from board URL

---

### 4. Import Sample Data

Import CSV files into Monday.com as separate boards:

* Work_Order_Tracker_Data.csv → Work Orders board
* Deal_funnel_Data.csv → Deals board

Ensure proper column mapping during import.

---

### 5. Run Application

Python:

```
python app.py
```

or

```
streamlit run app.py
```

Node.js:

```
npm run dev
```

Open the localhost link in your browser.

---

## 💬 Example Queries

* "How is our pipeline performing?"
* "Total expected revenue this quarter?"
* "Work order completion status?"
* "Prepare a leadership update."

---

## ⚠ Error Handling

The agent handles:

* Missing or incomplete data
* API failures
* Ambiguous queries
* Data inconsistencies

Clear explanations are provided to the user.

---

## 🔒 Security

* API keys stored in `.env`
* No hardcoded credentials
* Read-only Monday.com access

---

## 🔮 Future Improvements

* Dashboard visualization
* Forecasting models
* Automated reports
* Real-time alerts
* Multi-board scaling

---

## 👨‍💻 Author

Your Name

Skylark Drones — Technical Assignment

---

## 📄 License

MIT License


