import streamlit as st
import pandas as pd
import google.generativeai as genai
import requests
import os
from dotenv import load_dotenv

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Strategic Decision Support System",
    page_icon="🛡️",
    layout="wide"
)

# -----------------------------
# Title
# -----------------------------
st.title("🛡️ AI Strategic Decision Support System")

st.write(
    """
This system helps monitor defense threats, analyze countries,
view defense news, and answer military related questions using AI.
"""
)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose Module",
    [
        "Dashboard",
        "Threat Analysis",
        "News",
        "AI Assistant",
        "Threat Map"
    ]
)

# ==================================================
# DASHBOARD
# ==================================================

if page == "Dashboard":

    st.header("Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Threat Level", "Medium")
    col2.metric("Active Alerts", "5")
    col3.metric("Countries", "5")

    st.success("System Status : Online")
    st.warning("Real-Time Threat Monitoring Enabled")

    st.subheader("Threat Score")

    data = pd.DataFrame(
        {
            "Country": [
                "India",
                "China",
                "Pakistan",
                "USA",
                "Russia"
            ],
            "Threat Score": [
                20,
                60,
                90,
                15,
                50
            ]
        }
    )

    st.bar_chart(data.set_index("Country"))

    st.dataframe(data, use_container_width=True)
    st.subheader("Threat Trend Analysis")

trend_data = pd.DataFrame({
    "Month": [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun"
    ],
    "Threat Score": [
        25,
        40,
        55,
        48,
        70,
        60
    ]
})

st.line_chart(trend_data.set_index("Month"))

    # ==================================================
# THREAT ANALYSIS
# ==================================================

if page == "Threat Analysis":

    st.header("Threat Analysis")

    country = st.selectbox(
        "Select Country",
        [
            "India",
            "China",
            "Pakistan",
            "USA",
            "Russia"
        ]
    )

    threat_data = {
        "India": {
            "level": "Low",
            "score": 20,
            "message": "Border situation is stable."
        },
        "China": {
            "level": "Medium",
            "score": 60,
            "message": "Border monitoring is required."
        },
        "Pakistan": {
            "level": "High",
            "score": 90,
            "message": "High security alert."
        },
        "USA": {
            "level": "Low",
            "score": 15,
            "message": "No major security concern."
        },
        "Russia": {
            "level": "Medium",
            "score": 50,
            "message": "Situation is under observation."
        }
    }

    info = threat_data[country]

    st.subheader(f"{country} Threat Report")

    st.write("Threat Level :", info["level"])

    st.progress(info["score"])

    if info["level"] == "High":
        st.error(info["message"])

    elif info["level"] == "Medium":
        st.warning(info["message"])

    else:
        st.success(info["message"])
        # ==================================================
# DEFENSE NEWS
# ==================================================

elif page == "News":

    st.header("Latest Defense News")

    api_key = os.getenv("NEWS_API_KEY")

    if not api_key:
        st.error("NEWS_API_KEY not found in .env file.")

    else:

        url = (
            f"https://gnews.io/api/v4/search?"
            f"q=defense&lang=en&max=5&apikey={api_key}"
        )

        try:

            response = requests.get(url)

            if response.status_code == 200:

                news = response.json()
                articles = news.get("articles", [])

                if not articles:
                    st.info("No news available.")

                else:

                    for article in articles:

                        st.subheader(article.get("title"))

                        if article.get("description"):
                            st.write(article.get("description"))

                        st.write("**Source:**", article["source"]["name"])

                        st.markdown(
                            f"[Read Full Article]({article.get('url')})"
                        )

                        st.divider()

            else:

                st.error("Unable to load news.")

        except Exception as e:

            st.error("Something went wrong while loading news.")
            st.write(e)
            # ==================================================
# AI ASSISTANT
# ==================================================

elif page == "AI Assistant":

    st.header("AI Defense Assistant")

    question = st.text_area(
        "Ask a question about defense, military or cybersecurity"
    )

    if st.button("Analyze"):

        if question.strip() == "":
            st.warning("Please enter a question.")

        else:

            with st.spinner("Generating AI response..."):

                try:

                    prompt = f"""
You are an AI Strategic Decision Support Assistant.

Answer the question in a clear and simple format.

Question:
{question}

Provide:
1. Summary
2. Risk Level
3. Possible Impact
4. Recommendation
"""

                    response = model.generate_content(prompt)

                    st.subheader("AI Response")
                    st.write(response.text)

                except Exception as e:

                    st.error("Unable to generate response.")
                    st.write(e)
                    # ===========================
# THREAT MAP
# ===========================

st.markdown("---")
st.header("🌍 Global Threat Map")

map_data = pd.DataFrame({
    "lat": [28.6139, 39.9042, 33.6844, 38.9072, 55.7558],
    "lon": [77.2090, 116.4074, 73.0479, -77.0369, 37.6173],
    "Country": ["India", "China", "Pakistan", "USA", "Russia"],
    "Threat": [20, 60, 90, 15, 50]
})

st.map(map_data)