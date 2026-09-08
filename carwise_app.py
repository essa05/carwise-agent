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
# Helpers
# =========================
def safe(value, default="—"):
    value = str(value or "").strip()
    return html.escape(value) if value else default


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
    match = re.search(r"\d+(?:\.\d+)?", str(value or ""))

    if not match:
        return 0

    try:
        return max(0, min(100, int(float(match.group()))))
    except Exception:
        return 0


# =========================
# Parse Agent Output
# =========================
def parse_car_blocks(answer):

    blocks = re.findall(
        r"CAR_START(.*?)CAR_END",
        answer,
        re.IGNORECASE | re.DOTALL
    )

    cars = []

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

    for block in blocks:

        car = {}

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
# Render Card
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
        badge = '<span class="best-badge">⭐ أفضل تطابق</span>'

    card_html = f"""
<div class="car-card" dir="rtl">

<div class="card-header">
<div>
<div class="car-name">🚘 {brand} {model}</div>
<div class="car-meta">{body_type} • موديل {year}</div>
</div>
{badge}
</div>

<div class="price-row">
<span class="price">{price}</span>
<span class="currency">ر.س</span>
</div>

<div class="spec-grid">

<div class="spec-box">
<div class="spec-icon">⛽</div>
<div class="spec-title">اقتصاد الوقود</div>
<div class="spec-value">{fuel} كم/لتر</div>
</div>

<div class="spec-box">
<div class="spec-icon">🪑</div>
<div class="spec-title">المقاعد</div>
<div class="spec-value">{seats}</div>
</div>

<div class="spec-box">
<div class="spec-icon">⚙️</div>
<div class="spec-title">ناقل الحركة</div>
<div class="spec-value">{transmission}</div>
</div>

<div class="spec-box">
<div class="spec-icon">👨‍👩‍👧</div>
<div class="spec-title">الاستخدام</div>
<div class="spec-value">{best_use}</div>
</div>

</div>

<div class="reason-box">
<div class="reason-title">✨ لماذا اخترناها لك؟</div>
<div class="reason-text">{reason}</div>
</div>

<div class="match-header">
<span>🎯 نسبة التطابق مع طلبك</span>
<strong>{score}%</strong>
</div>

<div class="progress">
<div class="progress-fill" style="width:{score}%"></div>
</div>

</div>
"""

    st.markdown(
        card_html,
        unsafe_allow_html=True
    )


# =========================
# Custom Design
# =========================
st.markdown("""
<style>

.block-container {
    max-width: 950px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.carwise-title {
    text-align: center;
    font-size: 52px;
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
    padding: 20px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,.10);
    background: rgba(255,255,255,.03);
    margin-bottom: 25px;
    line-height: 1.8;
}

.stTextArea textarea {
    direction: rtl;
    text-align: right;
    border-radius: 16px !important;
    font-size: 17px !important;
}

.stButton > button {
    height: 56px;
    border-radius: 14px;
    font-size: 18px;
    font-weight: 800;
}

.results-title {
    direction: rtl;
    text-align: right;
    font-size: 30px;
    font-weight: 900;
    margin-top: 30px;
}

.car-card {
    direction: rtl;
    margin-top: 20px;
    padding: 26px;
    border-radius: 24px;
    border: 1px solid rgba(255,255,255,.12);

    background:
        radial-gradient(
            circle at top right,
            rgba(44,130,255,.12),
            transparent 35%
        ),
        rgba(255,255,255,.035);

    box-shadow: 0 15px 40px rgba(0,0,0,.22);
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 15px;
}

.car-name {
    font-size: 28px;
    font-weight: 900;
}

.car-meta {
    margin-top: 5px;
    color: #9CA3AF;
    font-size: 14px;
}

.best-badge {
    padding: 8px 13px;
    border-radius: 999px;
    background: rgba(255,193,7,.15);
    border: 1px solid rgba(255,193,7,.35);
    font-size: 13px;
    font-weight: 800;
}

.price-row {
    margin: 22px 0;
    display: flex;
    align-items: baseline;
    gap: 8px;
}

.price {
    font-size: 40px;
    font-weight: 950;
}

.currency {
    color: #9CA3AF;
    font-size: 17px;
}

.spec-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
}

.spec-box {
    padding: 14px;
    border-radius: 16px;
    text-align: center;
    background: rgba(255,255,255,.045);
    border: 1px solid rgba(255,255,255,.07);
}

.spec-icon {
    font-size: 22px;
}

.spec-title {
    margin-top: 4px;
    font-size: 12px;
    color: #8F98A5;
}

.spec-value {
    margin-top: 4px;
    font-size: 14px;
    font-weight: 800;
}

.reason-box {
    margin-top: 18px;
    padding: 16px;
    border-radius: 16px;
    background: rgba(46,204,113,.06);
    border: 1px solid rgba(46,204,113,.17);
}

.reason-title {
    font-weight: 900;
    margin-bottom: 6px;
}

.reason-text {
    color: #D7DCE4;
    font-size: 14px;
    line-height: 1.8;
}

.match-header {
    display: flex;
    justify-content: space-between;
    margin-top: 18px;
    margin-bottom: 7px;
    color: #BCC3CD;
    font-size: 14px;
}

.progress {
    width: 100%;
    height: 10px;
    border-radius: 999px;
    overflow: hidden;
    background: rgba(255,255,255,.08);
}

.progress-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(
        90deg,
        #2ecc71,
        #3498db
    );
}

@media (max-width: 700px) {

    .carwise-title {
        font-size: 40px;
    }

    .spec-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .card-header {
        flex-direction: column;
    }

    .price {
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
    '<div class="carwise-subtitle">'
    'مستشارك الذكي لاختيار السيارة المناسبة'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="info-box">
<b>🚘 صف لنا السيارة التي تبحث عنها</b><br>
اكتب ميزانيتك واستخدامك واحتياجاتك،
وسيبحث CarWise عن أفضل السيارات المناسبة لك.
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
# Search
# =========================
if st.button(
    "🔍 ابحث عن السيارة المناسبة",
    use_container_width=True
):

    if not user_request.strip():

        st.warning("اكتب متطلبات السيارة أولاً.")

    else:

        with st.spinner(
            "CarWise يبحث عن أفضل السيارات..."
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


                    if "NO_MATCH" in answer.upper():

                        st.warning(
                            "لا توجد سيارة مطابقة بشكل مناسب "
                            "في قاعدة البيانات الحالية."
                        )

                    else:

                        cars = parse_car_blocks(answer)

                        if cars:

                            st.success(
                                f"✅ تم العثور على {len(cars[:3])} خيارات مناسبة"
                            )

                            st.markdown(
                                '<div class="results-title">'
                                '🚘 توصيات CarWise'
                                '</div>',
                                unsafe_allow_html=True
                            )

                            for index, car in enumerate(
                                cars[:3],
                                start=1
                            ):
                                render_car_card(
                                    car,
                                    index
                                )

                        else:

                            st.error(
                                "تعذر قراءة نتيجة CarWise."
                            )

                            st.code(answer)

                else:

                    st.error(
                        f"حدث خطأ أثناء البحث "
                        f"({response.status_code})"
                    )

            except requests.exceptions.Timeout:

                st.error(
                    "استغرق البحث وقتًا أطول من المتوقع."
                )

            except Exception as e:

                st.error(
                    "تعذر الاتصال بخدمة CarWise."
                )

                st.caption(str(e))


# =========================
# Footer
# =========================
st.divider()

st.caption(
    "CarWise • AI Car Recommendation System"
)
