import streamlit as st
import requests

# =========================
# Page Configuration
# =========================
st.set_page_config(
    page_title="CarWise | خبير السيارات",
    page_icon="🚗",
    layout="centered"
)

# =========================
# Custom Design
# =========================
st.markdown("""
<style>

.block-container {
    max-width: 900px;
    padding-top: 3rem;
}

.carwise-title {
    text-align: center;
    font-size: 48px;
    font-weight: 800;
    margin-bottom: 5px;
}

.carwise-subtitle {
    text-align: center;
    font-size: 20px;
    color: #9CA3AF;
    margin-bottom: 35px;
}

.info-box {
    padding: 18px;
    border: 1px solid #333;
    border-radius: 12px;
    margin-bottom: 25px;
}

.stButton > button {
    height: 52px;
    font-size: 18px;
    font-weight: 600;
    border-radius: 10px;
}

.result-box {
    padding: 25px;
    border: 1px solid #333;
    border-radius: 14px;
    margin-top: 15px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# Header
# =========================
st.markdown(
    '<div class="carwise-title">🚗 CarWise</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="carwise-subtitle">'
    'خبيرك الذكي لاختيار السيارة المناسبة'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="info-box" dir="rtl">
اكتب احتياجاتك وميزانيتك، وسيبحث CarWise في قاعدة بيانات السيارات
ويعرض لك أفضل الخيارات المطابقة.
</div>
""", unsafe_allow_html=True)

# =========================
# User Input
# =========================
user_request = st.text_area(
    "ما السيارة التي تبحث عنها؟",
    placeholder=(
        "مثال: أبغى سيارة عائلية اقتصادية، "
        "ميزانيتي 130 ألف ريال ومناسبة للسفر"
    ),
    height=130
)

# =========================
# n8n Production Webhook
# =========================

N8N_WEBHOOK_URL = "https://essa2030.app.n8n.cloud/webhook/3ba5a8f7-d092-4aad-a307-d3f694a9d6f3"

# =========================
# Search Button
# =========================
if st.button(
    "🔍 ابحث عن السيارة المناسبة",
    use_container_width=True
):

    if not user_request.strip():

        st.warning("اكتب متطلبات السيارة أولاً.")

    else:

        with st.spinner(
            "CarWise يبحث في قاعدة السيارات..."
        ):

            try:

                payload = {
                    "chatInput": user_request
                }

                response = requests.post(
                    N8N_WEBHOOK_URL,
                    json=payload,
                    timeout=90
                )

                if response.status_code == 200:

                    try:
                        result = response.json()

                        if isinstance(result, dict):

                            answer = (
                                result.get("output")
                                or result.get("text")
                                or result.get("answer")
                                or str(result)
                            )

                        else:
                            answer = str(result)

                    except Exception:
                        answer = response.text

                    st.success("تم العثور على النتائج")

                    st.markdown("## 🚘 توصيات CarWise")

                    st.markdown(
                        f"""
                        <div class="result-box" dir="rtl">
                        {answer}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    st.error(
                        f"حدث خطأ أثناء البحث "
                        f"({response.status_code})"
                    )

            except requests.exceptions.Timeout:

                st.error(
                    "استغرق البحث وقتًا أطول من المتوقع. "
                    "حاول مرة أخرى."
                )

            except Exception as e:

                st.error("تعذر الاتصال بخدمة CarWise.")
                st.caption(str(e))

# =========================
# Footer
# =========================
st.divider()

st.caption(
    "CarWise • AI Car Recommendation System"
)
