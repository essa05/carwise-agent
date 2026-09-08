import re
import html
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
# Parse AI Agent Output
# =========================
def parse_car_blocks(answer):

    blocks = re.findall(
        r"CAR_START(.*?)CAR_END",
        answer,
        re.IGNORECASE | re.DOTALL
    )

    cars = []

    for block in blocks:

        car = {}

        patterns = {
            "Brand": r"Brand:\s*(.*?)\s*Model:",
            "Model": r"Model:\s*(.*?)\s*Year:",
            "Year": r"Year:\s*(.*?)\s*Price:",
            "Price": r"Price:\s*(.*?)\s*BodyType:",
            "BodyType": r"BodyType:\s*(.*?)\s*BestUse:",
            "BestUse": r"BestUse:\s*(.*?)\s*FuelEconomy:",
            "FuelEconomy": r"FuelEconomy:\s*(.*?)\s*Transmission:",
            "Transmission": r"Transmission:\s*(.*?)\s*Seats:",
            "Seats": r"Seats:\s*(.*?)\s*Reason:",
            "Reason": r"Reason:\s*(.*?)\s*MatchScore:",
            "MatchScore": r"MatchScore:\s*(.*)"
        }

        for field, pattern in patterns.items():

            match = re.search(
                pattern,
                block,
                re.IGNORECASE | re.DOTALL
            )

            if match:
                car[field] = match.group(1).strip()

        if car:
            cars.append(car)

    return cars


# =========================
# Helpers
# =========================
def safe(value, default="—"):

    value = str(value or "").strip()

    if value:
        return html.escape(value)

    return default


def format_price(value):

    value = str(value or "")

    value = (
        value.replace("SAR", "")
        .replace("sar", "")
        .replace("ريال", "")
        .replace(",", "")
        .strip()
    )

    try:
        return f"{int(float(value)):,}"
    except Exception:
        return safe(value)


def get_score(value):

    match = re.search(
        r"\d+(?:\.\d+)?",
        str(value or "")
    )

    if not match:
        return 0

    try:
        score = int(float(match.group()))
    except Exception:
        return 0

    return max(0, min(100, score))


# =========================
# Render Car Card
# =========================
def render_car_card(car, rank):

    brand = safe(car.get("Brand"))
    model = safe(car.get("Model"))
    year = safe(car.get("Year"))
    price = format_price(car.get("Price"))
    body_type = safe(car.get("BodyType"))
    best_use = safe(car.get("BestUse"))
    fuel = safe(car.get("FuelEconomy"))
    transmission = safe(car.get("Transmission"))
    seats = safe(car.get("Seats"))
    reason = safe(car.get("Reason"))
    score = get_score(car.get("MatchScore"))

    badge = ""

    if rank == 1:
        badge = """
        <div class="best-badge">
            ⭐ أفضل تطابق
        </div>
        """

    st.markdown(
        f"""
        <div class="car-card" dir="rtl">

            <div class="card-header">

                <div>
                    <div class="car-name">
                        🚘 {brand} {model}
                    </div>

                    <div class="car-category">
                        {body_type} • موديل {year}
                    </div>
                </div>

                {badge}

            </div>

            <div class="price-section">

                <span class="price-number">
                    {price}
                </span>

                <span class="currency">
                    ر.س
                </span>

            </div>

            <div class="spec-grid">

                <div class="spec-box">
                    <div class="spec-icon">⛽</div>
                    <div class="spec-label">اقتصاد الوقود</div>
                    <div class="spec-value">
                        {fuel} كم/لتر
                    </div>
                </div>

                <div class="spec-box">
                    <div class="spec-icon">🪑</div>
                    <div class="spec-label">المقاعد</div>
                    <div class="spec-value">
                        {seats} مقاعد
                    </div>
                </div>

                <div class="spec-box">
                    <div class="spec-icon">⚙️</div>
                    <div class="spec-label">ناقل الحركة</div>
                    <div class="spec-value">
                        {transmission}
                    </div>
                </div>

                <div class="spec-box">
                    <div class="spec-icon">👨‍👩‍👧</div>
                    <div class="spec-label">الاستخدام</div>
                    <div class="spec-value">
                        {best_use}
                    </div>
                </div>

            </div>

            <div class="reason-box">

                <div class="reason-title">
                    ✨ لماذا اخترناها لك؟
                </div>

                <div class="reason-text">
                    {reason}
                </div>

            </div>

            <div class="match-section">

                <div class="match-header">

                    <span>
                        🎯 نسبة التطابق مع طلبك
                    </span>

                    <strong>
                        {score}%
                    </strong>

                </div>

                <div class="progress-bg">

                    <div
                        class="progress-bar"
                        style="width:{score}%"
                    ></div>

                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================
# Custom Design
# =========================
st.markdown("""
<style>

.block-container {
    max-width: 980px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

.carwise-title {
    text-align: center;
    font-size: 54px;
    font-weight: 900;
    margin-bottom: 5px;
}

.carwise-subtitle {
    text-align: center;
    font-size: 19px;
    color: #9CA3AF;
    margin-bottom: 30px;
}

.info-box {
    direction: rtl;
    text-align: right;
    padding: 20px 22px;
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 18px;
    margin-bottom: 25px;
    background: rgba(255,255,255,0.03);
    line-height: 1.9;
}

.stTextArea textarea {
    direction: rtl;
    text-align: right;
    border-radius: 16px !important;
    font-size: 17px !important;
}

.stButton > button {
    height: 56px;
    font-size: 18px;
    font-weight: 800;
    border-radius: 15px;
}

.results-title {
    direction: rtl;
    text-align: right;
    font-size: 31px;
    font-weight: 900;
    margin-top: 30px;
    margin-bottom: 5px;
}

.car-card {
    direction: rtl;
    margin-top: 22px;
    padding: 28px;
    border-radius: 26px;
    border: 1px solid rgba(255,255,255,0.12);

    background:
        radial-gradient(
            circle at top right,
            rgba(30,144,255,0.12),
            transparent 35%
        ),
        rgba(255,255,255,0.035);

    box-shadow:
        0 18px 45px rgba(0,0,0,0.24);
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 15px;
}

.car-name {
    font-size: 30px;
    font-weight: 900;
    margin-bottom: 5px;
}

.car-category {
    color: #9CA3AF;
    font-size: 15px;
}

.best-badge {
    padding: 8px 14px;
    border-radius: 30px;
    font-size: 13px;
    font-weight: 800;
    white-space: nowrap;
    background: rgba(255,193,7,0.13);
    border: 1px solid rgba(255,193,7,0.30);
}

.price-section {
    margin-top: 24px;
    margin-bottom: 22px;
    display: flex;
    align-items: baseline;
    gap: 8px;
}

.price-number {
    font-size: 42px;
    font-weight: 950;
    letter-spacing: -1px;
}

.currency {
    color: #AAB2BF;
    font-size: 17px;
    font-weight: 700;
}

.spec-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
}

.spec-box {
    text-align: center;
    padding: 15px 10px;
    border-radius: 17px;
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.07);
}

.spec-icon {
    font-size: 22px;
    margin-bottom: 4px;
}

.spec-label {
    color: #8F98A5;
    font-size: 12px;
    margin-bottom: 5px;
}

.spec-value {
    font-size: 14px;
    font-weight: 800;
}

.reason-box {
    margin-top: 18px;
    padding: 17px 18px;
    border-radius: 17px;
    background: rgba(46,204,113,0.055);
    border: 1px solid rgba(46,204,113,0.15);
}

.reason-title {
    font-weight: 900;
    margin-bottom: 7px;
}

.reason-text {
    font-size: 14px;
    line-height: 1.8;
    color: #D8DEE7;
}

.match-section {
    margin-top: 20px;
}

.match-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
    color: #B9C0CA;
    font-size: 14px;
}

.progress-bg {
    height: 10px;
    width: 100%;
    border-radius: 30px;
    background: rgba(255,255,255,0.08);
    overflow: hidden;
}

.progress-bar {
    height: 100%;
    border-radius: 30px;
    background:
        linear-gradient(
            90deg,
            #2ecc71,
            #22a7f0
        );
}

@media (max-width: 700px) {

    .carwise-title {
        font-size: 40px;
    }

    .card-header {
        flex-direction: column;
    }

    .spec-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .car-name {
        font-size: 25px;
    }

    .price-number {
        font-size: 34px;
    }
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
    """
    <div class="carwise-subtitle">
        مستشارك الذكي لاختيار السيارة المناسبة
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<div class="info-box">

<b>🚘 صف لنا السيارة التي تبحث عنها</b><br>

حدد ميزانيتك واستخدامك،
وسيبحث CarWise في قاعدة السيارات
ويختار لك أفضل الخيارات المناسبة.

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
N8N_WEBHOOK_URL = (
    "https://essa2030.app.n8n.cloud/"
    "webhook/3ba5a8f7-d092-4aad-a307-d3f694a9d6f3"
)


# =========================
# Search Button
# =========================
if st.button(
    "🔍 ابحث عن السيارة المناسبة",
    use_container_width=True
):

    if not user_request.strip():

        st.warning(
            "اكتب متطلبات السيارة أولاً."
        )

    else:

        with st.spinner(
            "CarWise يحلل طلبك ويبحث عن أفضل السيارات..."
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


                    # =========================
                    # Results
                    # =========================

                    st.success(
                        "✨ تم العثور على أفضل الخيارات"
                    )

                    st.markdown(
                        """
                        <div class="results-title">
                        🚘 توصيات CarWise
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if "NO_MATCH" in answer.upper():

                        st.warning(
                            "لا توجد سيارة مطابقة بشكل مناسب "
                            "في قاعدة البيانات الحالية."
                        )

                    else:

                        cars = parse_car_blocks(answer)

                        if cars:

                            for index, car in enumerate(
                                cars[:3],
                                start=1
                            ):

                                render_car_card(
                                    car,
                                    index
                                )

                        else:

                            st.warning(
                                "وصلت نتيجة من CarWise، "
                                "لكن تنسيق البيانات غير متوقع."
                            )

                            st.code(answer)

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

                st.error(
                    "تعذر الاتصال بخدمة CarWise."
                )

                st.caption(
                    str(e)
                )


# =========================
# Footer
# =========================
st.divider()

st.caption(
    "CarWise • AI Car Recommendation System"
)
