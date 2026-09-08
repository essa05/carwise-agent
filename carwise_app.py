import re
import html
import requests
import streamlit as st


# =========================================================
# إعدادات الصفحة
# =========================================================

st.set_page_config(
    page_title="CarWise",
    page_icon="🚗",
    layout="centered"
)


# =========================================================
# رابط Webhook
# =========================================================

N8N_WEBHOOK_URL = "https://essa2030.app.n8n.cloud/webhook/3ba5a8f7-d092-4aad-a307-d3f694a9d6f3"


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
<style>

.stApp {
    direction: rtl;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero-box {
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 22px;
    padding: 28px;
    margin-bottom: 28px;
    background: rgba(255,255,255,0.025);
}

.hero-title {
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 10px;
}

.hero-text {
    font-size: 16px;
    opacity: 0.85;
    line-height: 1.8;
}

.results-title {
    font-size: 25px;
    font-weight: 800;
    margin-top: 24px;
    margin-bottom: 20px;
}

.result-count {
    padding: 12px 16px;
    border-radius: 14px;
    margin-bottom: 20px;
    background: rgba(35, 170, 90, 0.13);
    border: 1px solid rgba(35, 170, 90, 0.30);
    font-weight: 700;
}

.car-card {
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 22px;
    margin-bottom: 20px;
    background: rgba(255,255,255,0.035);
}

.card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    margin-bottom: 16px;
}

.car-name {
    font-size: 24px;
    font-weight: 800;
}

.best-badge {
    display: inline-block;
    border-radius: 999px;
    padding: 6px 12px;
    font-size: 13px;
    font-weight: 700;
    background: rgba(35, 170, 90, 0.15);
    border: 1px solid rgba(35, 170, 90, 0.35);
}

.price {
    font-size: 23px;
    font-weight: 800;
    margin-bottom: 16px;
}

.spec-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
    margin-bottom: 18px;
}

.spec-item {
    border-radius: 12px;
    padding: 11px 13px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
}

.spec-label {
    font-size: 12px;
    opacity: 0.60;
    margin-bottom: 4px;
}

.spec-value {
    font-size: 14px;
    font-weight: 700;
}

.reason-box {
    border-radius: 13px;
    padding: 14px;
    margin-top: 10px;
    background: rgba(255,255,255,0.035);
    line-height: 1.8;
}

.match-row {
    margin-top: 16px;
}

.match-title {
    display: flex;
    justify-content: space-between;
    margin-bottom: 7px;
    font-size: 13px;
}

.progress-bg {
    width: 100%;
    height: 9px;
    border-radius: 999px;
    background: rgba(255,255,255,0.10);
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    border-radius: 999px;
    background: currentColor;
}

.text-response {
    padding: 20px;
    border-radius: 16px;
    line-height: 1.9;
    font-size: 16px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.10);
}

.no-match {
    padding: 20px;
    border-radius: 16px;
    line-height: 1.8;
    background: rgba(255, 180, 0, 0.08);
    border: 1px solid rgba(255, 180, 0, 0.25);
}

.error-box {
    padding: 18px;
    border-radius: 16px;
    background: rgba(255, 70, 70, 0.10);
    border: 1px solid rgba(255, 70, 70, 0.25);
}

@media (max-width: 700px) {
    .spec-grid {
        grid-template-columns: 1fr;
    }

    .card-header {
        align-items: flex-start;
        flex-direction: column;
    }
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# دوال مساعدة
# =========================================================

def safe(value):
    if value is None:
        return "-"
    return html.escape(str(value).strip())


def format_price(value):
    if not value:
        return "-"

    text = str(value).replace(",", "").strip()
    match = re.search(r"\d+", text)

    if match:
        try:
            number = int(match.group())
            return f"{number:,} ريال"
        except:
            pass

    return safe(value)


def get_score(value):
    try:
        match = re.search(r"\d+", str(value))
        score = int(match.group()) if match else 0
    except:
        score = 0

    return max(0, min(score, 100))


def wants_all_cars(user_request):
    text = str(user_request or "").strip()

    phrases = [
        "جميع السيارات",
        "كل السيارات",
        "اعرض السيارات",
        "اعرض جميع السيارات",
        "اعرض كل السيارات",
        "السيارات الموجودة",
        "السيارات المتوفرة",
        "وش السيارات الموجودة",
        "قاعدة البيانات",
        "كل السيارات في قاعدة البيانات",
        "جميع السيارات في قاعدة البيانات"
    ]

    return any(phrase in text for phrase in phrases)


# =========================================================
# تحليل رد الوكيل
# =========================================================

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


# =========================================================
# إزالة السيارات المكررة
# =========================================================

def remove_duplicate_cars(cars):
    unique = []
    seen = set()

    for car in cars:
        key = (
            str(car.get("Brand", "")).strip().lower(),
            str(car.get("Model", "")).strip().lower(),
            str(car.get("Year", "")).strip()
        )

        if key not in seen:
            seen.add(key)
            unique.append(car)

    return unique


# =========================================================
# بطاقة السيارة
# =========================================================

def render_car_card(car, index, show_best_badge=True):
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
    if index == 1 and show_best_badge:
        badge = '<span class="best-badge">⭐ أفضل تطابق</span>'

    card_html = (
        f'<div class="car-card">'
        f'<div class="card-header">'
        f'<div class="car-name">🚘 {brand} {model}</div>'
        f'{badge}'
        f'</div>'
        f'<div class="price">💰 {price}</div>'
        f'<div class="spec-grid">'
        f'<div class="spec-item"><div class="spec-label">السنة</div><div class="spec-value">{year}</div></div>'
        f'<div class="spec-item"><div class="spec-label">نوع السيارة</div><div class="spec-value">{body_type}</div></div>'
        f'<div class="spec-item"><div class="spec-label">الاستخدام المناسب</div><div class="spec-value">{best_use}</div></div>'
        f'<div class="spec-item"><div class="spec-label">اقتصاد الوقود</div><div class="spec-value">{fuel}</div></div>'
        f'<div class="spec-item"><div class="spec-label">ناقل الحركة</div><div class="spec-value">{transmission}</div></div>'
        f'<div class="spec-item"><div class="spec-label">المقاعد</div><div class="spec-value">{seats}</div></div>'
        f'</div>'
        f'<div class="reason-box"><strong>لماذا تناسبك؟</strong><br>{reason}</div>'
        f'<div class="match-row">'
        f'<div class="match-title"><span>نسبة التطابق</span><span>{score}%</span></div>'
        f'<div class="progress-bg"><div class="progress-fill" style="width:{score}%"></div></div>'
        f'</div>'
        f'</div>'
    )

    st.markdown(
        card_html,
        unsafe_allow_html=True
    )


# =========================================================
# استخراج الرد من n8n
# =========================================================

def extract_agent_answer(response):
    try:
        data = response.json()
    except:
        return response.text.strip()

    if isinstance(data, str):
        return data.strip()

    if isinstance(data, list):
        if len(data) > 0:
            first = data[0]

            if isinstance(first, dict):
                for key in [
                    "output",
                    "answer",
                    "text",
                    "response"
                ]:
                    if key in first:
                        return str(first[key]).strip()

        return str(data)

    if isinstance(data, dict):
        for key in [
            "output",
            "answer",
            "text",
            "response"
        ]:
            if key in data:
                return str(data[key]).strip()

    return str(data).strip()


# =========================================================
# واجهة التطبيق
# =========================================================

st.markdown(
    """
<div class="hero-box">
<div class="hero-title">🚗 صف لنا السيارة التي تبحث عنها</div>
<div class="hero-text">
اكتب ميزانيتك واستخدامك واحتياجاتك،
وسيبحث CarWise عن أفضل السيارات المناسبة لك.
</div>
</div>
""",
    unsafe_allow_html=True
)


user_request = st.text_area(
    "ما السيارة التي تبحث عنها؟",
    height=120,
    placeholder="مثال: أبي سيارة عائلية اقتصادية سعرها 130 ألف"
)


search_button = st.button(
    "🔍 ابحث عن السيارة المناسبة",
    use_container_width=True
)


# =========================================================
# إرسال السؤال إلى n8n
# =========================================================

if search_button:

    if not user_request.strip():

        st.warning("اكتب طلبك أولًا.")

    else:

        with st.spinner("CarWise يبحث عن أفضل نتيجة..."):

            try:

                payload = {
                    "chatInput": user_request
                }

                response = requests.post(
                    N8N_WEBHOOK_URL,
                    json=payload,
                    timeout=90
                )

                response.raise_for_status()

                answer = extract_agent_answer(response)

                # =========================================
                # NO MATCH
                # =========================================

                if answer.strip().upper() == "NO_MATCH":

                    st.markdown(
                        '<div class="no-match">'
                        '🚗 لم أجد سيارة في قاعدة بيانات CarWise تحقق جميع الشروط المطلوبة.<br>'
                        'جرّب تعديل أحد الشروط أو الميزانية.'
                        '</div>',
                        unsafe_allow_html=True
                    )

                else:

                    # =====================================
                    # قراءة بطاقات السيارات
                    # =====================================

                    cars = parse_car_blocks(answer)
                    cars = remove_duplicate_cars(cars)

                    if cars:

                        show_all = wants_all_cars(user_request)

                        if show_all:
                            cars_to_show = cars
                        else:
                            cars_to_show = cars[:3]

                        st.markdown(
                            f'<div class="result-count">'
                            f'✅ تم العثور على {len(cars_to_show)} سيارة'
                            f'</div>',
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            '<div class="results-title">'
                            'توصيات CarWise'
                            '</div>',
                            unsafe_allow_html=True
                        )

                        for index, car in enumerate(
                            cars_to_show,
                            start=1
                        ):
                            render_car_card(
                                car,
                                index,
                                show_best_badge=not show_all
                            )

                    else:

                        # =================================
                        # رد نصي طبيعي
                        # سؤال خارج النطاق / غامض / توضيح
                        # =================================

                        clean_answer = html.escape(answer).replace(
                            "\n",
                            "<br>"
                        )

                        st.markdown(
                            f'<div class="text-response">'
                            f'{clean_answer}'
                            f'</div>',
                            unsafe_allow_html=True
                        )

            except requests.exceptions.Timeout:

                st.markdown(
                    '<div class="error-box">'
                    '⏱️ استغرق CarWise وقتًا أطول من المتوقع. حاول مرة أخرى.'
                    '</div>',
                    unsafe_allow_html=True
                )

            except requests.exceptions.RequestException:

                st.markdown(
                    '<div class="error-box">'
                    '⚠️ تعذر الاتصال بـ CarWise حاليًا. حاول مرة أخرى.'
                    '</div>',
                    unsafe_allow_html=True
                )

            except Exception:

                st.markdown(
                    '<div class="error-box">'
                    '⚠️ حدث خطأ أثناء معالجة النتيجة.'
                    '</div>',
                    unsafe_allow_html=True
                )
