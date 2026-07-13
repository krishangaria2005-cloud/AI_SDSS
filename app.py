import streamlit as st
import pandas as pd
import google.generativeai as genai
import requests
import os
from dotenv import load_dotenv

# Load API Keys
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# Page Title
st.set_page_config(
    page_title="AI Strategic Decision Support System",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ AI Strategic Decision Support System")

# Sidebar
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "Dashboard",
        "Threat Analysis",
        "News",
        "AI Assistant"
    ]
)

# ===========================
# DASHBOARD
# ===========================

if page == "Dashboard":

    st.header("Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Threat Level", "Medium")
    col2.metric("Active Alerts", "5")
    col3.metric("Countries", "5")

    st.subheader("Threat Score")

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

    st.bar_chart(data.set_index("Country"))

    st.dataframe(data, use_container_width=True)
    # ===========================
# THREAT ANALYSIS
# ===========================

elif page == "Threat Analysis":

    st.header("Threat Analysis")

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

    if country == "India":
        st.success("Threat Level : Low")
        st.progress(20)
        st.write("Current Situation:")
        st.write("- Border is stable.")
        st.write("- Regular security monitoring is active.")
        st.write("- No major threats reported.")

    elif country == "China":
        st.warning("Threat Level : Medium")
        st.progress(60)
        st.write("Current Situation:")
        st.write("- Border activities are being monitored.")
        st.write("- Intelligence agencies remain alert.")
        st.write("- Increased surveillance is recommended.")

    elif country == "Pakistan":
        st.error("Threat Level : High")
        st.progress(90)
        st.write("Current Situation:")
        st.write("- High security alert.")
        st.write("- Border forces are on standby.")
        st.write("- Continuous monitoring is required.")

    elif country == "USA":
        st.success("Threat Level : Low")
        st.progress(15)
        st.write("Current Situation:")
        st.write("- No significant defense threat.")
        st.write("- Security status is stable.")

    else:
        st.info("Threat Level : Medium")
        st.progress(50)
        st.write("Current Situation:")
        st.write("- Monitoring international activities.")
        st.write("- Security agencies remain active.")
        # ===========================
# LATEST DEFENSE NEWS
# ===========================

elif page == "News":

    st.header("Latest Defense News")

    api_key = os.getenv("NEWS_API_KEY")

    if not api_key:
        st.error("NEWS_API_KEY not found. Please add it to your .env file.")

    else:

        url = (
            f"https://gnews.io/api/v4/search?"
            f"q=defense OR military&lang=en&max=8&apikey={api_key}"
        )

        try:
            response = requests.get(url)

            if response.status_code == 200:

                data = response.json()
                articles = data.get("articles", [])

                if not articles:
                    st.info("No news found.")

                else:

                    for article in articles:

                        st.subheader(article.get("title", "No Title"))

                        description = article.get("description")
                        if description:
                            st.write(description)

                        source = article.get("source", {}).get("name", "Unknown")
                        st.caption(f"Source: {source}")

                        if article.get("url"):
                            st.markdown(f"[Read Full Article]({article['url']})")

                        st.divider()

            else:
                st.error(f"News API Error : {response.status_code}")

        except Exception as e:
            st.error("Unable to fetch news.")
            st.write(e)
            # ===========================
# AI ASSISTANT
# ===========================

elif page == "AI Assistant":

    st.header("AI Defense Assistant")

    question = st.text_area(
        "Ask any defense, cybersecurity or military related question"
    )

    if st.button("Analyze"):

        if question.strip() == "":
            st.warning("Please enter your question.")

        else:

            try:

                prompt = f"""
You are an AI Strategic Decision Support Assistant.

Answer the following question in a simple and professional way.

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

                st.error("Something went wrong.")

                st.write(e)

# ===========================
# FOOTER
# ===========================

st.markdown("---")
st.caption("AI Strategic Decision Support System | BSERC Internship Project")