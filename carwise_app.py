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
.stApp{direction:rtl;background:radial-gradient(circle at 85% 8%,rgba(34,197,94,.10),transparent 28%),linear-gradient(180deg,#0a0f1a 0%,#0b1220 100%);color:#f8fafc}
.block-container{max-width:980px;padding-top:2rem;padding-bottom:4rem}
header[data-testid="stHeader"]{background:transparent}
.hero-box{border:1px solid rgba(148,163,184,.16);border-radius:26px;padding:34px 32px;margin-bottom:26px;background:linear-gradient(135deg,rgba(34,197,94,.11),rgba(15,23,42,.96) 55%);box-shadow:0 18px 55px rgba(0,0,0,.28)}
.brand-row{display:flex;align-items:center;justify-content:space-between;gap:18px}.brand-copy{flex:1}
.brand-pill{display:inline-block;padding:7px 12px;border-radius:999px;margin-bottom:14px;font-size:13px;font-weight:700;color:#bbf7d0;background:rgba(34,197,94,.10);border:1px solid rgba(34,197,94,.24)}
.hero-title{font-size:34px;line-height:1.35;font-weight:900;margin:0 0 10px}.hero-title span{color:#4ade80}
.hero-text{font-size:16px;color:#cbd5e1;line-height:1.9;max-width:720px}.hero-icon{min-width:82px;width:82px;height:82px;border-radius:22px;display:flex;align-items:center;justify-content:center;font-size:42px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.09)}
div[data-testid="stTextArea"] label p{font-size:15px!important;font-weight:800!important;color:#e2e8f0!important}
div[data-testid="stTextArea"] textarea{min-height:135px!important;border-radius:18px!important;border:1px solid rgba(148,163,184,.18)!important;background:rgba(15,23,42,.78)!important;color:#f8fafc!important;font-size:16px!important;line-height:1.8!important;padding:16px 18px!important}
div[data-testid="stTextArea"] textarea:focus{border-color:rgba(34,197,94,.55)!important;box-shadow:0 0 0 3px rgba(34,197,94,.10)!important}
div.stButton>button{height:52px;border:0!important;border-radius:16px!important;font-size:16px!important;font-weight:900!important;color:#fff!important;background:linear-gradient(135deg,#22c55e,#16a34a)!important;box-shadow:0 10px 28px rgba(34,197,94,.18)}
.results-title{font-size:26px;font-weight:900;margin:28px 0 18px}.result-count{padding:13px 16px;border-radius:14px;margin:22px 0 16px;background:rgba(34,197,94,.10);border:1px solid rgba(34,197,94,.22);color:#dcfce7;font-weight:800}
.car-card{border:1px solid rgba(148,163,184,.16);border-radius:22px;padding:22px;margin-bottom:18px;background:linear-gradient(180deg,rgba(30,41,59,.66),rgba(15,23,42,.82));box-shadow:0 14px 34px rgba(0,0,0,.20)}
.card-header{display:flex;align-items:center;justify-content:space-between;gap:14px;margin-bottom:14px}.car-name{font-size:23px;font-weight:900;color:#f8fafc}
.best-badge{display:inline-block;border-radius:999px;padding:7px 12px;font-size:12px;font-weight:800;color:#bbf7d0;background:rgba(34,197,94,.10);border:1px solid rgba(34,197,94,.25)}
.price{font-size:22px;font-weight:900;color:#4ade80;margin-bottom:16px}.spec-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-bottom:16px}
.spec-item{border-radius:13px;padding:12px 13px;background:rgba(255,255,255,.035);border:1px solid rgba(255,255,255,.06)}.spec-label{font-size:11px;color:#94a3b8;margin-bottom:5px}.spec-value{font-size:14px;font-weight:800;color:#e2e8f0}
.reason-box{border-radius:14px;padding:14px 15px;margin-top:10px;line-height:1.8;color:#e2e8f0;background:rgba(34,197,94,.055);border:1px solid rgba(34,197,94,.12)}
.match-row{margin-top:16px}.match-title{display:flex;justify-content:space-between;margin-bottom:7px;font-size:13px;color:#cbd5e1}.progress-bg{width:100%;height:9px;border-radius:999px;background:rgba(255,255,255,.08);overflow:hidden}.progress-fill{height:100%;border-radius:999px;background:linear-gradient(90deg,#22c55e,#4ade80)}
.text-response,.no-match,.error-box{padding:18px 20px;border-radius:16px;line-height:1.9;font-size:16px}.text-response{background:rgba(30,41,59,.70);border:1px solid rgba(148,163,184,.16)}.no-match{background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.20)}.error-box{background:rgba(239,68,68,.08);border:1px solid rgba(239,68,68,.20)}
@media(max-width:700px){.hero-box{padding:24px 20px}.hero-title{font-size:27px}.hero-icon{display:none}.spec-grid{grid-template-columns:1fr 1fr}.card-header{align-items:flex-start;flex-direction:column}}
@media(max-width:480px){.spec-grid{grid-template-columns:1fr}}
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
        score = int(
            re.search(r"\d+", str(value)).group()
        )
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

    card_html = f"""
<div class="car-card">

<div class="card-header">
    <div class="car-name">🚘 {brand} {model}</div>
    {badge}
</div>

<div class="price">
    💰 {price}
</div>

<div class="spec-grid">

    <div class="spec-item">
        <div class="spec-label">السنة</div>
        <div class="spec-value">{year}</div>
    </div>

    <div class="spec-item">
        <div class="spec-label">نوع السيارة</div>
        <div class="spec-value">{body_type}</div>
    </div>

    <div class="spec-item">
        <div class="spec-label">الاستخدام المناسب</div>
        <div class="spec-value">{best_use}</div>
    </div>

    <div class="spec-item">
        <div class="spec-label">اقتصاد الوقود</div>
        <div class="spec-value">{fuel}</div>
    </div>

    <div class="spec-item">
        <div class="spec-label">ناقل الحركة</div>
        <div class="spec-value">{transmission}</div>
    </div>

    <div class="spec-item">
        <div class="spec-label">المقاعد</div>
        <div class="spec-value">{seats}</div>
    </div>

</div>

<div class="reason-box">
    <strong>لماذا تناسبك؟</strong><br>
    {reason}
</div>

<div class="match-row">

    <div class="match-title">
        <span>نسبة التطابق</span>
        <span>{score}%</span>
    </div>

    <div class="progress-bg">
        <div class="progress-fill" style="width:{score}%"></div>
    </div>

</div>

</div>
"""

    # هذا هو التعديل الوحيد في عرض البطاقة
    st.html(card_html)


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
    <div class="brand-row">
        <div class="brand-copy">
            <div class="brand-pill">CarWise • مستشارك الذكي للسيارات</div>
            <div class="hero-title">اختيار سيارتك صار <span>أسهل</span></div>
            <div class="hero-text">اكتب ميزانيتك واستخدامك واحتياجاتك، وسيبحث CarWise في قاعدة السيارات ليعرض لك أفضل الخيارات المناسبة لك.</div>
        </div>
        <div class="hero-icon">🚗</div>
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

        st.warning(
            "اكتب طلبك أولًا."
        )

    else:

        with st.spinner(
            "CarWise يبحث عن أفضل نتيجة..."
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

                response.raise_for_status()

                answer = extract_agent_answer(
                    response
                )

                # =========================================
                # NO MATCH
                # =========================================

                if answer.strip().upper() == "NO_MATCH":

                    st.markdown(
                        """
<div class="no-match">
🚗 لم أجد سيارة في قاعدة بيانات CarWise تحقق جميع الشروط المطلوبة.
جرّب تعديل أحد الشروط أو الميزانية.
</div>
""",
                        unsafe_allow_html=True
                    )

                else:

                    # =====================================
                    # محاولة قراءة بطاقات السيارات
                    # =====================================

                    cars = parse_car_blocks(
                        answer
                    )

                    cars = remove_duplicate_cars(
                        cars
                    )

                    if cars:

                        show_all = wants_all_cars(
                            user_request
                        )

                        if show_all:
                            cars_to_show = cars
                        else:
                            cars_to_show = cars[:3]

                        st.markdown(
                            f"""
<div class="result-count">
✅ تم العثور على {len(cars_to_show)} سيارة
</div>
""",
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            """
<div class="results-title">
توصيات CarWise
</div>
""",
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
                        # =================================

                        clean_answer = html.escape(
                            answer
                        ).replace(
                            "\n",
                            "<br>"
                        )

                        st.markdown(
                            f"""
<div class="text-response">
{clean_answer}
</div>
""",
                            unsafe_allow_html=True
                        )

            except requests.exceptions.Timeout:

                st.markdown(
                    """
<div class="error-box">
⏱️ استغرق CarWise وقتًا أطول من المتوقع. حاول مرة أخرى.
</div>
""",
                    unsafe_allow_html=True
                )

            except requests.exceptions.RequestException:

                st.markdown(
                    """
<div class="error-box">
⚠️ تعذر الاتصال بـ CarWise حاليًا. حاول مرة أخرى.
</div>
""",
                    unsafe_allow_html=True
                )

            except Exception:

                st.markdown(
                    """
<div class="error-box">
⚠️ حدث خطأ أثناء معالجة النتيجة.
</div>
""",
                    unsafe_allow_html=True
                )
