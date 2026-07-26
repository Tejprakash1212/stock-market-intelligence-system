import numpy as np
import pandas as pd

"""##TASK 1: Fetch Stock Data
 5 years of historical data for 5 assets.
"""

!pip install yfinance
import yfinance as yf

assets = ['^BSESN', 'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS']
print(assets)

assets_five_year = yf.download(assets,period="5y",group_by="Ticker")
assets_five_year.head()

"""##TASK2:Fetch News Data
Fetch financial news headlines using NewsAPI.
"""

!pip install requests

import requests
import pandas as pd

API_KEY = "c08bb35f3dbc49d78f06f532c22b8032"

companies = {
    "^BSESN": "BSE Sensex",
    "RELIANCE.NS": "Reliance Industries",
    "TCS.NS": "Tata Consultancy Services",
    "INFY.NS": "Infosys",
    "HDFCBANK.NS": "HDFC Bank"
}

def fetch_news(company):

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": company,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 100,
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params)

    return response.json()

news = fetch_news("Reliance Industries")

print(news["status"])

print(news["totalResults"])

news["articles"][0]

## Fetching news for all companies
all_news = pd.DataFrame()

for ticker, company in companies.items():

    print(f"Fetching news for {company}")

    news = fetch_news(company)

    articles = news["articles"]

##Extract Important Information
    news_list = []

    for article in articles:

        news_list.append({
            "Ticker": ticker,
            "Company": company,
            "Title": article.get("title"),
            "Description": article.get("description"),
            "Author": article.get("author"),
            "Source": article.get("source", {}).get("name"),
            "PublishedAt": article.get("publishedAt"),
            "URL": article.get("url")
        })

all_news = pd.DataFrame()

for ticker, company in companies.items():

    print(f"Fetching news for {company}")

    news = fetch_news(company)
    articles = news["articles"]

    news_list = []

    for article in articles:

        news_list.append({
            "Ticker": ticker,
            "Company": company,
            "Title": article.get("title"),
            "Description": article.get("description"),
            "Author": article.get("author"),
            "Source": article.get("source", {}).get("name"),
            "PublishedAt": article.get("publishedAt"),
            "URL": article.get("url")
        })

    # These lines MUST be inside the loop
    company_df = pd.DataFrame(news_list)

    print(company_df.head())

    company_df.to_csv(f"{ticker}_news.csv", index=False)

    all_news = pd.concat([all_news, company_df], ignore_index=True)

print("Done!")

##save individual csv
company_df.to_csv(f"{ticker}_news.csv", index=False)

##Merging all companies
all_news = pd.concat([all_news, company_df], ignore_index=True)

##Saving Combined Dataset
all_news.to_csv("all_stock_news.csv", index=False)

all_news.head()

all_news["Ticker"].unique()

all_news["Ticker"].value_counts()

all_news.to_csv("all_stock_news.csv", index=False)

print("All news data saved successfully.")

"""##TASK3: Clean the Data


"""

assets_five_year.info()

assets_five_year.isnull().sum()

##FLATTENING THE COLUMN
if isinstance(assets_five_year.columns, pd.MultiIndex):

    assets_five_year.columns = [
        "_".join(col)
        for col in assets_five_year.columns
    ]

assets_five_year.columns

assets_five_year.isnull().sum()
assets_five_year.isnull().sum().sum()

#Checking where the values are missing
assets_five_year[
    assets_five_year.isnull().any(axis=1)
]

assets_five_year = assets_five_year.ffill()

assets_five_year.isnull().sum().sum()

"""News Data"""

all_news.info()

all_news.isnull().sum()

all_news["Description"] = all_news["Description"].fillna(
    "No Description Available"
)

all_news["Author"] = all_news["Author"].fillna(
    "Unknown"
)

all_news.isnull().sum()

all_news.info()

all_news["PublishedAt"] = pd.to_datetime(
    all_news["PublishedAt"]
)

all_news.info()

assets_five_year.to_csv(
    "cleaned_stock_data.csv"
)

all_news.to_csv(
    "cleaned_stock_news.csv",
    index=False
)

"""##TASK 4:Exploratory Data Analysis (EDA)"""

!pip install plotly

# Importing the required libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# PART 1 : PRICE TREND OF ALL ASSETS
# Selecting all the Closing Price columns

close_columns = [
    col for col in assets_five_year.columns
    if "Close" in col
]
# Creating an empty figure
fig = go.Figure()

# Adding a line graph for every asset
for col in close_columns:
    fig.add_trace(
       go.Scatter(
          x=assets_five_year.index,
          y=assets_five_year[col],
           mode="lines",
           name=col
)
    )
# Adding titles and labels

fig.update_layout(
  title="Closing Price Trend of All Assets",
    xaxis_title="Date",
    yaxis_title="Closing Price",
    template="plotly_white"

)


# Displaying the graph
fig.show()

# 2. Distribution of Daily Returns

# Calculating daily returns only for visualization
daily_returns = pd.DataFrame()

for col in close_columns:
    daily_returns[col] = assets_five_year[col].pct_change() * 100

daily_returns.dropna(inplace=True)

fig = go.Figure()

for col in daily_returns.columns:
    fig.add_trace(
        go.Histogram(
            x=daily_returns[col],
            name=col,
            opacity=0.6
        )
    )
fig.update_layout(
    title="Distribution of Daily Returns",
    xaxis_title="Daily Return (%)",
    yaxis_title="Frequency",
    barmode="overlay",
    template="plotly_white"
)

fig.show()

# 3. Trading Volume Trend
volume_columns = [col for col in assets_five_year.columns if "Volume" in col]
fig = go.Figure()

for col in volume_columns:
    fig.add_trace(
        go.Scatter(
            x=assets_five_year.index,
            y=assets_five_year[col],
            mode="lines",
            name=col
        )
    )

fig.update_layout(
    title="Trading Volume Trend of All Assets",
    xaxis_title="Date",
    yaxis_title="Trading Volume",
    template="plotly_white"
)

fig.show()

# 4. Correlation Heatmap
correlation_matrix = assets_five_year[close_columns].corr()

fig = px.imshow(
    correlation_matrix,
    text_auto=True,
    title="Correlation Heatmap of Closing Prices"
)

fig.show()

# 5. Summary Statistics Table
summary_statistics = assets_five_year[close_columns].describe().round(2)
summary_statistics

"""##TASK 5: Feature Engineering"""

# Selecting the required columns
close_columns = [col for col in assets_five_year.columns if "Close" in col]
high_columns = [col for col in assets_five_year.columns if "High" in col]
low_columns = [col for col in assets_five_year.columns if "Low" in col]
volume_columns = [col for col in assets_five_year.columns if "Volume" in col]

# Price Features
for col in close_columns:

    # Daily Return
    assets_five_year[f"{col}_Daily_Return"] = assets_five_year[col].pct_change()*100

    # Log Return
    assets_five_year[f"{col}_Log_Return"] = np.log(assets_five_year[col]/assets_five_year[col].shift(1))

    # 7 Day Moving Average
    assets_five_year[f"{col}_MA_7"] = assets_five_year[col].rolling(7).mean()

    # 14 Day Moving Average
    assets_five_year[f"{col}_MA_14"] = assets_five_year[col].rolling(14).mean()

    # 30 Day Moving Average
    assets_five_year[f"{col}_MA_30"] = assets_five_year[col].rolling(30).mean()

    # Price to Moving Average Ratio
    assets_five_year[f"{col}_Price_to_MA_Ratio"] = assets_five_year[col]/assets_five_year[f"{col}_MA_7"]


# High Low Ratio
for high_col, low_col in zip(high_columns, low_columns):
  stock_name = high_col.replace("_High", "")
  assets_five_year[f"{stock_name}_High_Low_Ratio"] = assets_five_year[high_col]/assets_five_year[low_col]


# Moving Average Crossover Signal
for col in close_columns:
  assets_five_year[f"{col}_MA_Crossover"] = (
        assets_five_year[f"{col}_MA_7"] >
        assets_five_year[f"{col}_MA_30"]
    ).astype(int)



# Volatility Features
for col in close_columns:

    # 7 Day Volatility
    assets_five_year[f"{col}_Volatility_7"] = assets_five_year[f"{col}_Daily_Return"].rolling(7).std()

    # 14 Day Volatility
    assets_five_year[f"{col}_Volatility_14"] = assets_five_year[f"{col}_Daily_Return"].rolling(14).std()


# Time Based Features
assets_five_year["Day_of_Week"] = assets_five_year.index.dayofweek
assets_five_year["Month"] = assets_five_year.index.month
assets_five_year["Quarter"] = assets_five_year.index.quarter
assets_five_year["Is_Monday"] = (assets_five_year.index.dayofweek == 0).astype(int)
assets_five_year["Is_Friday"] = (assets_five_year.index.dayofweek == 4).astype(int)

# Volume Features
for col in volume_columns:

    # 7 Day Volume Moving Average
    assets_five_year[f"{col}_Volume_MA_7"] = assets_five_year[col].rolling(7).mean()

    # Volume Ratio
    assets_five_year[f"{col}_Volume_Ratio"] = assets_five_year[col]/assets_five_year[f"{col}_Volume_MA_7"]



# Target Variable
for col in close_columns:
    assets_five_year[f"{col}_Target"] = (
        assets_five_year[col].shift(-1) >
        assets_five_year[col]
    ).astype(int)


# Removing Missing Values
assets_five_year.dropna(inplace=True)


# Checking the Shape of Dataset
print("Shape of Dataset :", assets_five_year.shape)

# Displaying First Five Rows
assets_five_year.head()

"""##TASK 6: Build Model for a Single Asset"""

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,classification_report

# TASK 6 : BUILD MODEL FOR A SINGLE ASSET

def process_asset(asset_name):

    # Selecting the feature columns
    feature_columns=[f"{asset_name}_Daily_Return",
                     f"{asset_name}_Log_Return",
                     f"{asset_name}_MA_7",
                     f"{asset_name}_MA_14",
                     f"{asset_name}_MA_30",
                     f"{asset_name}_Price_to_MA_Ratio",
                     f"{asset_name.replace('_Close','')}_High_Low_Ratio",
                     f"{asset_name}_MA_Crossover",
                     f"{asset_name}_Volatility_7",
                     f"{asset_name}_Volatility_14",
                     "Day_of_Week",
                     "Month",
                     "Quarter",
                     "Is_Monday",
                     "Is_Friday",
                     f"{asset_name.replace('_Close','_Volume')}_Volume_MA_7",
                     f"{asset_name.replace('_Close','_Volume')}_Volume_Ratio"]

    # Creating Features and Target Variable
    X=assets_five_year[feature_columns]
    y=assets_five_year[f"{asset_name}_Target"]

    # Time Based Split (80%-20%)
    split_index=int(len(assets_five_year)*0.80)
    X_train=X.iloc[:split_index]
    X_test=X.iloc[split_index:]
    y_train=y.iloc[:split_index]
    y_test=y.iloc[split_index:]

    # Creating the Pipeline
    pipeline=Pipeline(steps=[
        ("scaler",StandardScaler()),
        ("classifier",RandomForestClassifier(random_state=42))
    ])

    # Training the Model
    pipeline.fit(X_train,y_train)

    # Making Predictions
    y_pred=pipeline.predict(X_test)

    # Calculating Accuracy
    accuracy=accuracy_score(y_test,y_pred)

    # Returning the Results
    return{
        "Model":pipeline,
        "Accuracy":accuracy,
        "Predictions":y_pred,
        "X_Test":X_test,
        "y_Test":y_test,
        "Classification_Report":classification_report(y_test,y_pred)
    }


# Example : Processing a Single Asset
infy_result=process_asset("INFY.NS_Close")

# Displaying the Results
print("Accuracy :",infy_result["Accuracy"])
print("\nClassification Report:\n")
print(infy_result["Classification_Report"])

print("Training Shape :",infy_result["X_Test"].shape)

"""##TASK 7: Run Model for All Assets"""

# List of all assets
assets=["INFY.NS_Close","TCS.NS_Close","RELIANCE.NS_Close","HDFCBANK.NS_Close","^BSESN_Close"]

# Creating an Empty Dictionary
all_results={}

# Processing All Assets
for asset in assets:
    all_results[asset]=process_asset(asset)

# Displaying Accuracy of All Assets
for asset in assets:
    print(f"{asset} Accuracy : {all_results[asset]['Accuracy']:.4f}")

# Displaying Classification Reports
for asset in assets:
 print(f"{asset}")
 print(all_results[asset]["Classification_Report"])
 print("\n")

"""##TASK 8:Calculate Business Metrics

"""

from sklearn.metrics import precision_score,recall_score,f1_score

# Calculating Business Metrics
for asset in assets:

    y_true=all_results[asset]["y_Test"]
    y_pred=all_results[asset]["Predictions"]

    all_results[asset]["Precision"]=precision_score(y_true,y_pred)
    all_results[asset]["Recall"]=recall_score(y_true,y_pred)
    all_results[asset]["F1_Score"]=f1_score(y_true,y_pred)

# Displaying Business Metrics

for asset in assets:
    print(f"Asset : {asset}")


    print(f"Accuracy : {all_results[asset]['Accuracy']:.4f}")
    print(f"Precision : {all_results[asset]['Precision']:.4f}")
    print(f"Recall : {all_results[asset]['Recall']:.4f}")
    print(f"F1 Score : {all_results[asset]['F1_Score']:.4f}")

    print("\n")

# Creating Comparison Table
comparison_table=[]
for asset in assets:
    comparison_table.append({

        "Asset":asset,
        "Accuracy":round(all_results[asset]["Accuracy"],4),
        "Precision":round(all_results[asset]["Precision"],4),
        "Recall":round(all_results[asset]["Recall"],4),
        "F1 Score":round(all_results[asset]["F1_Score"],4)

    })

comparison_table=pd.DataFrame(comparison_table)

comparison_table

"""##Task 9: Threshold Tuning"""

import plotly.express as px
from sklearn.metrics import confusion_matrix

# Defining the Business Costs
cost_fp=100
cost_fn=50

# Defining the Threshold Values
thresholds=np.arange(0.1,0.9,0.05)

# Calculating Prediction Probabilities
for asset in assets:
    probabilities=all_results[asset]["Model"].predict_proba(all_results[asset]["X_Test"])
    all_results[asset]["Probabilities"]=probabilities

# Selecting a Single Asset
asset="INFY.NS_Close"

# Extracting the Probability of UP
y_proba=all_results[asset]["Probabilities"][:,1]

# Extracting the Actual Values
y_test=all_results[asset]["y_Test"]

# Calculating the Total Cost for Every Threshold

costs=[]
for thresh in thresholds:
  y_pred=(y_proba>=thresh).astype(int)
  tn,fp,fn,tp=confusion_matrix(y_test,y_pred).ravel()
  total_cost=(fp*cost_fp)+(fn*cost_fn)
  costs.append(total_cost)

# Finding the Optimal Threshold

minimum_cost=min(costs)
optimal_threshold=thresholds[np.argmin(costs)]

print("Minimum Cost :",minimum_cost)
print("Optimal Threshold :",optimal_threshold)

# Creating the Cost Dataframe
cost_df=pd.DataFrame({
    "Threshold":thresholds,
    "Cost":costs
})

# Plotting Cost vs Threshold Graph
fig=px.line(cost_df,
            x="Threshold",
            y="Cost",
            title="Cost vs Threshold")

fig.show()

# Calculating the Default Threshold Cost
default_predictions=(y_proba>=0.50).astype(int)
tn,fp,fn,tp=confusion_matrix(y_test,default_predictions).ravel()
default_cost=(fp*cost_fp)+(fn*cost_fn)

print("Default Threshold :",0.50)
print("Default Cost :",default_cost)

# Calculating the Optimal Threshold Cost
optimal_predictions=(y_proba>=optimal_threshold).astype(int)
tn,fp,fn,tp=confusion_matrix(y_test,optimal_predictions).ravel()
optimal_cost=(fp*cost_fp)+(fn*cost_fn)

print("Optimal Threshold :",optimal_threshold)
print("Optimal Cost :",optimal_cost)

# Comparing the Thresholds

print("\nDefault Threshold :",0.50)
print("Default Cost :",default_cost)

print("\nOptimal Threshold :",optimal_threshold)
print("Optimal Cost :",optimal_cost)

"""##TASK10: Add SHAP Explainability"""

import shap

pip install shap

# Calculating SHAP Values for All Assets

for asset in assets:

    print("="*70)
    print(f"SHAP Analysis : {asset}")
    print("="*70)

    # Extracting the Model
    model=all_results[asset]["Model"]

    # Extracting the Test Data
    X_test=all_results[asset]["X_Test"]

    # Extracting the Scaler
    scaler=model.named_steps["scaler"]

    # Extracting the Classifier
    classifier=model.named_steps["classifier"]

    # Scaling the Test Data
    X_test_scaled=scaler.transform(X_test)

    # Creating the SHAP Explainer
    explainer=shap.TreeExplainer(classifier)

    # Calculating SHAP Values
    shap_values=explainer.shap_values(X_test_scaled)

# Global Feature Importance Chart

for asset in assets:

    model=all_results[asset]["Model"]
    X_test=all_results[asset]["X_Test"]

    scaler=model.named_steps["scaler"]
    classifier=model.named_steps["classifier"]

    X_test_scaled=scaler.transform(X_test)

    explainer=shap.TreeExplainer(classifier)

    shap_values=explainer.shap_values(X_test_scaled)

    print(f"\nFeature Importance : {asset}\n")

    shap.summary_plot(
        shap_values,
        X_test_scaled,
        feature_names=X_test.columns,
        plot_type="bar"
    )

# SHAP Summary Dot Plot
for asset in assets:

    model=all_results[asset]["Model"]
    X_test=all_results[asset]["X_Test"]

    scaler=model.named_steps["scaler"]
    classifier=model.named_steps["classifier"]

    X_test_scaled=scaler.transform(X_test)

    explainer=shap.TreeExplainer(classifier)

    shap_values=explainer.shap_values(X_test_scaled)

    print(f"\nSHAP Summary Plot : {asset}\n")

    shap.summary_plot(
        shap_values,
        X_test_scaled,
        feature_names=X_test.columns
    )

# SHAP Waterfall Plot

for asset in assets:

    model=all_results[asset]["Model"]
    X_test=all_results[asset]["X_Test"]

    scaler=model.named_steps["scaler"]
    classifier=model.named_steps["classifier"]

    X_test_scaled=scaler.transform(X_test)

    explainer=shap.TreeExplainer(classifier)

    shap_values=explainer.shap_values(X_test_scaled)

    print(f"\nWaterfall Plot : {asset}\n")

    index=0

    shap.plots.waterfall(

        shap.Explanation(

            values=shap_values[:,:,1][index],
            base_values=explainer.expected_value[1],
            data=X_test_scaled[index],
            feature_names=X_test.columns

        )

    )

# SHAP Force Plot

for asset in assets:

    model=all_results[asset]["Model"]
    X_test=all_results[asset]["X_Test"]

    scaler=model.named_steps["scaler"]
    classifier=model.named_steps["classifier"]

    X_test_scaled=scaler.transform(X_test)

    explainer=shap.TreeExplainer(classifier)

    shap_values=explainer.shap_values(X_test_scaled)

    print(f"\nForce Plot : {asset}\n")

    index=0

    shap.force_plot(

        explainer.expected_value[1],

        shap_values[:,:,1][index],

        X_test.iloc[index],

        matplotlib=True

    )

"""##Task 11: Build RAG Pipeline"""

!pip install -q sentence-transformers chromadb cohere

import chromadb
import cohere

from sentence_transformers import SentenceTransformer

news_df = pd.read_csv("all_stock_news.csv")
news_df.head()

##Converting article into single document
news_df = news_df.fillna("")

news_documents = []
for _, row in news_df.iterrows():

    document = f"""
Company: {row['Company']}
Title: {row['Title']}
Description: {row['Description']}
Source: {row['Source']}
Published: {row['PublishedAt']}
"""

    news_documents.append(document)

print("Total Documents:", len(news_documents))
print(news_documents[0])

##creating embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(
    news_documents,
    show_progress_bar=True
)

print(embeddings.shape)

##storing embedding in chroma db
ids = [str(i) for i in range(len(news_documents))]

client = chromadb.Client()

collection = client.create_collection(
    name="news"
)

# Create unique IDs for every document
ids = [str(i) for i in range(len(news_documents))]

print(ids[:5])

collection.add(
    ids=ids,
    embeddings=embeddings.tolist(),
    documents=news_documents
)

print("Embeddings stored successfully.")

def search_news(query, top_k=3):

    query_embedding = model.encode(query)

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )

    return results["documents"][0]

query = "Latest news about Reliance"

documents = search_news(query)

for i, doc in enumerate(documents, 1):

    print("="*60)
    print(f"Result {i}")
    print("="*60)
    print(doc)

import cohere

# Paste your Cohere API key below
COHERE_API_KEY = "IfCCFT9tuHPrCafFiiH60tcNsxI4Soqn2BUIoB4x"

co = cohere.Client(COHERE_API_KEY)

print("Cohere client initialized successfully!")

def generate_answer(question):

    # Retrieve top 3 relevant articles
    retrieved_docs = search_news(question)

    # Combine retrieved documents
    context = "\n\n".join(retrieved_docs)

    prompt = f"""
You are a financial news assistant.

Answer ONLY using the context below.

Context:
{context}

Question:
{question}
"""

    response = co.chat(
        model="c4ai-aya-expanse-32b",
        message=prompt,
        temperature=0.3
    )

    return response.text

question = "What is the latest news about Reliance Industries?"

answer = generate_answer(question)

print(answer)

"""##TASK 12: Create Streamlit App"""

!pip install -q streamlit pandas matplotlib
!npm install -g localtunnel

 
 %%writefile app.py

 import streamlit as st
 import pandas as pd
 
# # -----------------------------
# # PAGE TITLE
# # -----------------------------
st.title("Stock Market Intelligence System")
 
# # -----------------------------
# # SIDEBAR
# # -----------------------------
 st.sidebar.header("Asset Selection")
 
 asset = st.sidebar.selectbox(
  "Select Asset",
     ["Sensex", "Reliance", "TCS", "Infosys", "HDFC Bank"]
 )
 
# # -----------------------------
# # TABS
# # -----------------------------
 tab1, tab2, tab3 = st.tabs(
#     ["Predictions", "Chat", "Comparison"]
 )
 
# # =============================
# # TAB 1
# # =============================
 with tab1:
 
     st.header("Predictions")
 
     st.write("Selected Asset:", asset)

     price_data = pd.DataFrame({
         "Day":[1,2,3,4,5],
         "Price":[100,102,101,105,108]
     })
      st.subheader("Price Trend")
     st.line_chart(price_data.set_index("Day"))
 
     st.subheader("Prediction")
     st.success("UP")
 
     st.subheader("Confidence Score")
     st.write("87%")
 
     st.subheader("SHAP Feature Importance")
     st.info("SHAP Feature Importance Chart")
 
    st.subheader("SHAP Waterfall Plot")
     st.info("SHAP Waterfall Plot")
 
# # =============================
# # TAB 2
# # =============================
 with tab2:
 
     st.header("Chat")
 
     question = st.text_input("Ask your question")
 
     if "chat_history" not in st.session_state:
         st.session_state.chat_history = []
 
     if st.button("Ask"):
 
         # Temporary response
         answer = "This is a sample chatbot response."
 
         st.session_state.chat_history.append(("User", question))
         st.session_state.chat_history.append(("Assistant", answer))
 
     st.subheader("Chat History")
 
     for role, message in st.session_state.chat_history:
         st.write(f"**{role}:** {message}")
 
# # =============================
# # TAB 3
# # =============================
 with tab3:
 
     st.header("Comparison")
      comparison = pd.DataFrame({

         "Asset":[
             "Sensex",
             "Reliance",
             "TCS",
             "Infosys",
             "HDFC Bank"
         ],
 
         "Prediction":[
             "UP",
             "UP",
             "DOWN",
             "UP",
             "DOWN"
         ],
 
         "Accuracy":[
              0.76,
             0.81,
             0.79,
             0.83,
             0.80
        ]

     })
 
     st.subheader("Comparison Table")
     st.dataframe(comparison)
 
     st.subheader("Bar Chart")
     st.bar_chart(comparison.set_index("Asset")["Accuracy"])
 
     st.subheader("Prediction Comparison")
     st.dataframe(comparison[["Asset","Prediction"]])

!ls

!streamlit run app.py > streamlit.log 2>&1 &

!cat streamlit.log

!npx localtunnel --port 8501

!curl https://loca.lt/mytunnelpassword
