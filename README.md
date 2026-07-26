# 📈 Stock Market Intelligence System

An AI-powered Stock Market Intelligence System that combines **Machine Learning**, **Financial News Analysis**, **Retrieval-Augmented Generation (RAG)**, and an interactive **Streamlit Dashboard** to provide stock movement predictions, explainability, and intelligent financial news-based question answering.

---

## 🚀 Project Overview

The Stock Market Intelligence System is an end-to-end data analytics and machine learning project designed to analyze historical stock market data and financial news.

The system performs stock price prediction using engineered financial features and a Random Forest classifier. It also integrates a Retrieval-Augmented Generation (RAG) chatbot that answers user queries based on the latest financial news articles using ChromaDB vector search and Cohere's Large Language Model.

The project includes an interactive Streamlit application with prediction visualization, chatbot support, and model comparison.

---

## ✨ Features

- 📊 Fetches 5 years of historical stock market data using Yahoo Finance
- 📰 Collects financial news using NewsAPI
- 🧹 Cleans and preprocesses stock and news datasets
- 📈 Performs Exploratory Data Analysis (EDA)
- ⚙️ Creates advanced financial features
- 🤖 Builds a Random Forest classification model
- 📉 Evaluates model performance using business metrics
- 🎯 Optimizes prediction threshold based on business cost
- 🔍 Explains predictions using SHAP Explainability
- 💬 Implements a RAG chatbot using ChromaDB + Cohere
- 🌐 Interactive Streamlit Dashboard

---

## 📁 Project Structure

```
Stock-Market-Intelligence-System/
│
├── app.py
├── requirements.txt
├── README.md
│
├── notebooks/
│   └── capstone_project.ipynb
│
├── screenshots/
│   ├── home.png
│   ├── prediction.png
│   ├── chatbot.png
│   └── comparison.png
│
├── cleaned_stock_data.csv
├── cleaned_stock_news.csv
├── all_stock_news.csv
│
└── assets/
```

---

## 🛠 Technologies Used

### Programming Language
- Python

### Libraries
- NumPy
- Pandas
- Scikit-learn
- Plotly
- SHAP
- Matplotlib
- Requests
- yfinance

### Machine Learning
- Random Forest Classifier
- Feature Engineering
- Threshold Tuning

### AI & RAG
- Sentence Transformers
- ChromaDB
- Cohere API

### Dashboard
- Streamlit

---

## 📊 Dataset

### Stock Data
- Source: Yahoo Finance
- Duration: Last 5 Years

Assets Used:
- BSE Sensex
- Reliance Industries
- Tata Consultancy Services (TCS)
- Infosys
- HDFC Bank

### News Data
- Source: NewsAPI
- Latest financial news headlines

---

## ⚙️ Machine Learning Pipeline

1. Data Collection
2. Data Cleaning
3. Exploratory Data Analysis
4. Feature Engineering
5. Model Training
6. Model Evaluation
7. Business Metrics
8. Threshold Optimization
9. SHAP Explainability
10. RAG Chatbot
11. Streamlit Dashboard

---

## 📈 Evaluation Metrics

The model is evaluated using:

- Accuracy
- Precision
- Recall
- F1 Score
- Business Cost Analysis

---

## 🧠 Explainable AI

The project uses **SHAP (SHapley Additive exPlanations)** to interpret the Random Forest model.

Visualizations include:

- Feature Importance
- Summary Plot
- Waterfall Plot
- Force Plot

---

## 💬 RAG Chatbot

The chatbot answers financial questions using Retrieval-Augmented Generation.

### Workflow

User Question

↓

Sentence Embedding

↓

ChromaDB Vector Search

↓

Relevant News Retrieval

↓

Cohere Large Language Model

↓

Final Answer

---

## 🖥 Streamlit Dashboard

The dashboard contains three main sections:

### 📈 Predictions
- Stock Prediction
- Confidence Score
- SHAP Explanation

### 💬 Chat
- Ask financial questions
- RAG-powered answers

### 📊 Comparison
- Compare predictions across multiple assets
- Model performance metrics

---

## ▶️ Installation

Clone the repository

```bash
git clone https://github.com/your-username/stock-market-intelligence-system.git
```

Move into the project folder

```bash
cd stock-market-intelligence-system
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the Streamlit application

```bash
streamlit run app.py
```

---

## 📷 Screenshots

Add screenshots of:

- Home Page
- Prediction Dashboard
- Chatbot
- Comparison Dashboard

---

## 🔮 Future Enhancements

- LSTM and Transformer-based prediction models
- Live stock market data integration
- Real-time financial news streaming
- Portfolio recommendation system
- Sentiment analysis of financial news
- Cloud deployment using Streamlit Community Cloud or Render
- User authentication and personalized watchlists

---

## 👨‍💻 Author

**Tej Prakash Mishra**

B.Tech Student | Data Analytics | Machine Learning | AI

---

## 📄 License

This project is developed for educational and academic purposes.
