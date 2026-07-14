import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import google.generativeai as genai
import requests
import os
from dotenv import load_dotenv

# ------------------------------------
# Load Environment Variables
# ------------------------------------
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# ------------------------------------
# Page Configuration
# ------------------------------------
st.set_page_config(
    page_title="AI Strategic Decision Support System",
    page_icon="🛡️",
    layout="wide"
)

# ------------------------------------
# Title
# ------------------------------------
st.title("🛡️ AI Strategic Decision Support System")

st.write("""
Monitor defense threats, analyze countries,
read live defense news and get AI-based recommendations.
""")

# ------------------------------------
# Sidebar
# ------------------------------------
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

    st.header("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Threat Level", "Medium")
    col2.metric("Active Alerts", "5")
    col3.metric("Countries", "5")

    st.success("🟢 System Status : Online")
    st.warning("🟡 Real-Time Threat Monitoring Enabled")

    data = pd.DataFrame({
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
    })

    st.subheader("Threat Score")

    st.bar_chart(data.set_index("Country"))

    st.subheader("Threat Distribution")

    fig, ax = plt.subplots(figsize=(5, 5))

    ax.pie(
        data["Threat Score"],
        labels=data["Country"],
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title("Threat Distribution")

    st.pyplot(fig)

    st.subheader("Threat Data")

    st.dataframe(data, use_container_width=True)

    st.subheader("🔍 Search Country")

    selected_country = st.selectbox(
        "Select Country",
        data["Country"]
    )

    st.dataframe(
        data[data["Country"] == selected_country],
        use_container_width=True
    )

    st.subheader("Threat Trend")

    trend_data = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Threat Score": [25, 40, 55, 48, 70, 60]
    })

    st.line_chart(trend_data.set_index("Month"))
    # ==================================================
# THREAT ANALYSIS
# ==================================================

elif page == "Threat Analysis":

    st.header("🌍 Threat Analysis")

    country = st.selectbox(
        "Choose Country",
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
            "status": "Border situation is stable."
        },
        "China": {
            "level": "Medium",
            "score": 60,
            "status": "Border monitoring is required."
        },
        "Pakistan": {
            "level": "High",
            "score": 90,
            "status": "High security alert."
        },
        "USA": {
            "level": "Low",
            "score": 15,
            "status": "No major security concern."
        },
        "Russia": {
            "level": "Medium",
            "score": 50,
            "status": "Situation is under observation."
        }
    }

    info = threat_data[country]

    st.subheader(f"{country} Threat Report")

    if info["level"] == "High":
        st.error(f"Threat Level : {info['level']}")

    elif info["level"] == "Medium":
        st.warning(f"Threat Level : {info['level']}")

    else:
        st.success(f"Threat Level : {info['level']}")

    st.progress(info["score"])

    st.write("### Current Status")
    st.write(info["status"])

    st.subheader("Threat Score")

    score_df = pd.DataFrame({
        "Category": [
            "Military",
            "Cyber",
            "Border",
            "Internal"
        ],
        "Score": [
            info["score"],
            max(info["score"] - 10, 0),
            max(info["score"] - 20, 0),
            max(info["score"] - 30, 0)
        ]
    })

    st.bar_chart(score_df.set_index("Category"))
    # ==================================================
# DEFENSE NEWS
# ==================================================

elif page == "News":

    st.header("📰 Latest Defense News")

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

                if len(articles) == 0:
                    st.info("No news available.")

                else:

                    for article in articles:

                        st.subheader(article.get("title", "No Title"))

                        if article.get("description"):
                            st.write(article["description"])

                        st.write("**Source:**", article["source"]["name"])

                        st.markdown(
                            f"[Read Full Article]({article['url']})"
                        )

                        st.divider()

            else:

                st.error(
                    f"News API Error : {response.status_code}"
                )

        except Exception as e:

            st.error("Unable to load latest news.")
            st.write(e)
            # ==================================================
# AI ASSISTANT
# ==================================================

elif page == "AI Assistant":

    st.header("🤖 AI Defense Assistant")

    question = st.text_area(
        "Ask your defense, military or cybersecurity question"
    )

    if st.button("Analyze"):

        if question.strip() == "":
            st.warning("Please enter a question.")

        else:

            with st.spinner("Analyzing..."):

                try:

                    prompt = f"""
You are an AI Strategic Decision Support Assistant.

Answer the user's question in this format:

1. Summary
2. Threat Level
3. Possible Impact
4. Recommendation

Question:
{question}
"""

                    response = model.generate_content(prompt)

                    st.subheader("AI Response")

                    st.write(response.text)

                except Exception as e:

                    st.error("Unable to generate AI response.")
                    st.write(e)
                    # ==================================================
# THREAT MAP
# ==================================================

elif page == "Threat Map":

    st.header("🌍 Global Threat Map")

    map_data = pd.DataFrame({
        "lat": [
            28.6139,
            39.9042,
            33.6844,
            38.9072,
            55.7558
        ],
        "lon": [
            77.2090,
            116.4074,
            73.0479,
            -77.0369,
            37.6173
        ],
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
    })

    st.write("### Countries Under Monitoring")

    st.map(map_data)

    st.dataframe(
        map_data[["Country", "Threat Score"]],
        use_container_width=True
    )

# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.caption(
    "🛡️ AI Strategic Decision Support System | BSERC Internship Project"
)

st.caption(
    "Developed by Krish Angaria"
)