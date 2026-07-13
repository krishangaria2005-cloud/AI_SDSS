import streamlit as st
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
import requests
import os

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

st.title("AI Strategic Decision Support System")

st.sidebar.title("Menu")

page = st.sidebar.radio(
    "Select",
    [
        "Dashboard",
        "Threat Analysis",
        "News",
        "AI Assistant"
    ]
)

if page == "Dashboard":

    st.header("Dashboard")

    c1, c2, c3 = st.columns(3)

    c1.metric("Threat Level", "Medium")
    c2.metric("Active Alerts", "5")
    c3.metric("Countries", "20")

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

    if country == "India":
        level = "Low"
        score = 20

    elif country == "China":
        level = "Medium"
        score = 60

    elif country == "Pakistan":
        level = "High"
        score = 90

    elif country == "USA":
        level = "Low"
        score = 15

    else:
        level = "Medium"
        score = 50

    st.subheader("Current Threat")

    st.write("Country :", country)
    st.write("Threat Level :", level)

    st.progress(score)

    st.subheader("Threat Data")

    data = pd.DataFrame({
        "Country": [
            "India",
            "China",
            "Pakistan",
            "USA",
            "Russia"
        ],
        "Threat": [
            20,
            60,
            90,
            15,
            50
        ]
    })

    st.bar_chart(data.set_index("Country"))

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

        st.write("Threat Level : Low")
        st.progress(20)
        st.success("Border situation is stable.")

    elif country == "China":

        st.write("Threat Level : Medium")
        st.progress(60)
        st.warning("Border monitoring is required.")

    elif country == "Pakistan":

        st.write("Threat Level : High")
        st.progress(90)
        st.error("High security alert.")

    elif country == "USA":

        st.write("Threat Level : Low")
        st.progress(15)
        st.success("No major security concern.")

    else:

        st.write("Threat Level : Medium")
       st.progress(50)
    
st.info("Regular monitoring is active.")

if page == "News":

    st.header("Latest Defense News")

    api_key = os.getenv("GNEWS_API_KEY")

    url = f"https://gnews.io/api/v4/search?q=defense&lang=en&max=5&apikey={api_key}"

    response = requests.get(url)

    if response.status_code == 200:

        data = response.json()

        articles = data.get("articles", [])

        if len(articles) == 0:
            st.info("No news found.")

        else:

            for article in articles:

                st.subheader(article["title"])

                if article["description"]:
                    st.write(article["description"])

                st.write(article["url"])

                st.write("--------------------------------")

    else:

        st.error("News could not be loaded.")
        st.write("Status Code :", response.status_code)


else:

    st.header("AI Assistant")

    question = st.text_area("Ask a defense or security related question")

    if st.button("Analyze"):

        if question.strip() == "":

            st.warning("Please enter your question.")

        else:

            try:

                response = model.generate_content(question)

                st.subheader("AI Response")

                st.write(response.text)

            except Exception as e:

                st.error("Something went wrong.")
                st.write(e)