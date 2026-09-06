import streamlit as st
import requests

# -----------------------------
# Page Settings
# ------------------------------
st.set_page_config(
    page_title="CarWise",
    page_icon="🚗",
    layout="centered"
)

# -----------------------------
# App Title
# -----------------------------
st.title("🚗 CarWise")
st.subheader("AI Car Advisor")

st.write(
    "Tell CarWise what kind of car you are looking for, "
    "and the AI agent will recommend the best options for you."
)

st.divider()

# -----------------------------
# User Request
# -----------------------------
user_request = st.text_area(
    "What are you looking for?",
    placeholder="مثال: أبغى سيارة عائلية اقتصادية، ميزانيتي 130 ألف ريال ومناسبة للسفر",
    height=120
)

# -----------------------------
# n8n Webhook URL
# -----------------------------
N8N_WEBHOOK_URL = "https://essa2030.app.n8n.cloud/webhook/3ba5a8f7-d092-4aad-a307-d3f694a9d6f3"

# -----------------------------
# Find Car Button
# -----------------------------
if st.button("🔎 Find My Car", use_container_width=True):

    if not user_request.strip():
        st.warning("Please enter your car requirements.")

    else:

        with st.spinner("CarWise is searching for the best cars..."):

            try:

                payload = {
                    "chatInput": user_request
                }

                response = requests.post(
                    N8N_WEBHOOK_URL,
                    json=payload,
                    timeout=60
                )

                if response.status_code == 200:

                    try:
                        result = response.json()

                        # Common n8n AI Agent response formats
                        if isinstance(result, dict):

                            if "output" in result:
                                answer = result["output"]

                            elif "text" in result:
                                answer = result["text"]

                            elif "answer" in result:
                                answer = result["answer"]

                            else:
                                answer = str(result)

                        else:
                            answer = str(result)

                    except:
                        answer = response.text

                    st.success("Recommendation completed.")

                    st.divider()

                    st.subheader("🤖 CarWise Recommendations")

                    st.write(answer)

                else:

                    st.error(
                        f"Request failed with status code: "
                        f"{response.status_code}"
                    )

                    st.write(response.text)

            except requests.exceptions.Timeout:

                st.error("The request took too long. Please try again.")

            except Exception as e:

                st.error("Something went wrong.")

                st.write(e)

# -----------------------------
# Footer
# -----------------------------
st.divider()

st.caption(
    "CarWise uses AI to analyze your requirements "
    "and recommend suitable cars from its database."
)
