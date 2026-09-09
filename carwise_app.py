import re
import html
import requests
import streamlit as st


# =========================================================
# إعدادات الصفحة
# =========================================================

st.set_page_config(
    page_title="CarWise",
    page_icon="🚘",
    layout="wide"
)


# =========================================================
# رابط Webhook
# =========================================================

N8N_WEBHOOK_URL = "https://essa2030.app.n8n.cloud/webhook/3ba5a8f7-d092-4aad-a307-d3f694a9d6f3"


# =========================================================
# CSS — تصميم احترافي
# =========================================================

st.markdown(
    """
<style>
:root{
    --bg:#08111f;
    --bg2:#0c1727;
    --panel:rgba(15,23,42,.78);
    --panel2:rgba(20,31,49,.82);
    --border:rgba(148,163,184,.15);
    --text:#f8fafc;
    --muted:#94a3b8;
    --green:#22c55e;
    --green2:#34d399;
    --cyan:#38bdf8;
}

html, body, [class*="css"]{
    font-family:"Segoe UI", Tahoma, Arial, sans-serif;
}

.stApp{
    direction:rtl;
    color:var(--text);
    background:
        radial-gradient(circle at 88% 7%, rgba(16,185,129,.13), transparent 25%),
        radial-gradient(circle at 10% 15%, rgba(56,189,248,.08), transparent 24%),
        linear-gradient(180deg,#07101d 0%,#08111f 45%,#0b1523 100%);
}

header[data-testid="stHeader"]{
    background:transparent;
}

.block-container{
    max-width:1180px;
    padding-top:1.8rem;
    padding-bottom:7rem;
}

/* =========================
   العلامة التجارية
========================= */

.logo-wrap{
    text-align:center;
    margin:6px auto 24px;
}

.logo-name{
    font-size:56px;
    line-height:1;
    font-weight:950;
    letter-spacing:-2px;
    color:#f8fafc;
    text-shadow:0 8px 26px rgba(0,0,0,.28);
}

.logo-name span{
    color:var(--green2);
}

.logo-tagline{
    margin-top:9px;
    color:#64748b;
    font-size:12px;
    font-weight:800;
    letter-spacing:4px;
}

.logo-line{
    width:150px;
    height:3px;
    margin:14px auto 0;
    border-radius:999px;
    background:linear-gradient(90deg,transparent,var(--green),transparent);
}

/* =========================
   Hero
========================= */

.hero{
    position:relative;
    overflow:hidden;
    border:1px solid var(--border);
    border-radius:30px;
    padding:38px 38px 34px;
    margin-bottom:22px;
    background:
        linear-gradient(135deg,rgba(16,185,129,.10),transparent 38%),
        linear-gradient(180deg,rgba(15,23,42,.92),rgba(10,18,31,.90));
    box-shadow:0 26px 70px rgba(0,0,0,.26);
}

.hero:before{
    content:"";
    position:absolute;
    width:320px;
    height:320px;
    border-radius:50%;
    left:-120px;
    top:-170px;
    background:rgba(34,197,94,.08);
    filter:blur(10px);
}

.hero-kicker{
    display:inline-flex;
    align-items:center;
    gap:8px;
    padding:7px 12px;
    border-radius:999px;
    margin-bottom:16px;
    font-size:13px;
    font-weight:800;
    color:#bbf7d0;
    background:rgba(34,197,94,.09);
    border:1px solid rgba(34,197,94,.22);
}

.hero-title{
    position:relative;
    z-index:1;
    font-size:38px;
    line-height:1.4;
    font-weight:950;
    margin:0 0 10px;
}

.hero-title span{
    color:var(--green2);
}

.hero-text{
    position:relative;
    z-index:1;
    max-width:820px;
    margin:0;
    font-size:18px;
    line-height:1.9;
    color:#cbd5e1;
}

.feature-grid{
    display:grid;
    grid-template-columns:repeat(4,minmax(0,1fr));
    gap:10px;
    margin-top:24px;
}

.feature{
    border:1px solid rgba(148,163,184,.10);
    border-radius:16px;
    padding:13px 14px;
    background:rgba(255,255,255,.025);
}

.feature-title{
    font-size:14px;
    font-weight:850;
    color:#f8fafc;
}

.feature-sub{
    margin-top:4px;
    font-size:12px;
    color:#94a3b8;
}

/* =========================
   Chat input
========================= */

div[data-testid="stChatInput"]{
    max-width:1180px;
    margin-left:auto;
    margin-right:auto;
}

div[data-testid="stChatInput"] > div{
    border-radius:18px !important;
    border:1px solid rgba(148,163,184,.18) !important;
    background:rgba(17,24,39,.93) !important;
    box-shadow:0 16px 40px rgba(0,0,0,.22);
}

div[data-testid="stChatInput"] textarea{
    font-size:17px !important;
    color:#f8fafc !important;
}

div[data-testid="stChatInput"] button{
    border-radius:12px !important;
}

/* =========================
   Chat messages
========================= */

[data-testid="stChatMessage"]{
    background:rgba(15,23,42,.48);
    border:1px solid rgba(148,163,184,.10);
    border-radius:18px;
    padding:8px 12px;
    margin-bottom:12px;
}

/* =========================
   النتائج
========================= */

.result-count{
    padding:13px 16px;
    border-radius:14px;
    margin:10px 0 16px;
    background:rgba(34,197,94,.09);
    border:1px solid rgba(34,197,94,.20);
    color:#dcfce7;
    font-weight:850;
    font-size:15px;
}

.results-title{
    font-size:26px;
    font-weight:950;
    margin:14px 0 16px;
}

.car-card{
    border:1px solid rgba(148,163,184,.14);
    border-radius:22px;
    padding:22px;
    margin-bottom:18px;
    background:
        linear-gradient(180deg,rgba(30,41,59,.68),rgba(15,23,42,.88));
    box-shadow:0 18px 42px rgba(0,0,0,.20);
}

.card-header{
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:14px;
    margin-bottom:12px;
}

.car-name{
    font-size:25px;
    font-weight:950;
    color:#f8fafc;
}

.best-badge{
    display:inline-flex;
    align-items:center;
    padding:7px 12px;
    border-radius:999px;
    font-size:12px;
    font-weight:850;
    color:#bbf7d0;
    background:rgba(34,197,94,.10);
    border:1px solid rgba(34,197,94,.24);
}

.price{
    font-size:24px;
    font-weight:950;
    color:#4ade80;
    margin-bottom:16px;
}

.spec-grid{
    display:grid;
    grid-template-columns:repeat(3,minmax(0,1fr));
    gap:10px;
    margin-bottom:16px;
}

.spec-item{
    border-radius:14px;
    padding:12px 13px;
    background:rgba(255,255,255,.03);
    border:1px solid rgba(255,255,255,.055);
}

.spec-label{
    font-size:12px;
    color:#94a3b8;
    margin-bottom:5px;
}

.spec-value{
    font-size:15px;
    font-weight:850;
    color:#e2e8f0;
}

.reason-box{
    border-radius:15px;
    padding:15px 16px;
    margin-top:10px;
    background:rgba(34,197,94,.05);
    border:1px solid rgba(34,197,94,.12);
    line-height:1.9;
    color:#e2e8f0;
    font-size:15px;
}

.match-row{
    margin-top:16px;
}

.match-title{
    display:flex;
    justify-content:space-between;
    margin-bottom:7px;
    font-size:13px;
    color:#cbd5e1;
}

.progress-bg{
    width:100%;
    height:9px;
    border-radius:999px;
    background:rgba(255,255,255,.08);
    overflow:hidden;
}

.progress-fill{
    height:100%;
    border-radius:999px;
    background:linear-gradient(90deg,#16a34a,#4ade80);
}

.text-response{
    padding:16px 18px;
    border-radius:15px;
    line-height:1.9;
    font-size:16px;
    color:#e2e8f0;
    background:rgba(30,41,59,.62);
    border:1px solid rgba(148,163,184,.12);
}

.no-match{
    padding:16px 18px;
    border-radius:15px;
    line-height:1.8;
    background:rgba(245,158,11,.08);
    border:1px solid rgba(245,158,11,.18);
}

.error-box{
    padding:16px 18px;
    border-radius:15px;
    background:rgba(239,68,68,.08);
    border:1px solid rgba(239,68,68,.18);
}

.small-note{
    margin-top:10px;
    font-size:12px;
    color:#64748b;
    text-align:center;
}

@media(max-width:850px){
    .feature-grid{
        grid-template-columns:1fr 1fr;
    }
    .spec-grid{
        grid-template-columns:1fr 1fr;
    }
    .logo-name{
        font-size:46px;
    }
    .hero-title{
        font-size:31px;
    }
}

@media(max-width:520px){
    .block-container{
        padding-top:1rem;
    }
    .logo-name{
        font-size:40px;
    }
    .hero{
        padding:26px 20px 24px;
    }
    .hero-title{
        font-size:27px;
    }
    .hero-text{
        font-size:16px;
    }
    .feature-grid,
    .spec-grid{
        grid-template-columns:1fr;
    }
    .card-header{
        align-items:flex-start;
        flex-direction:column;
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
        except Exception:
            pass

    return safe(value)


def get_score(value):
    try:
        match = re.search(r"\d+", str(value))
        score = int(match.group()) if match else 0
    except Exception:
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
        str(answer),
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

    # مهم: السبب يعرض كما أرسله الـAgent بدون استبدال أو تغيير
    reason = safe(car.get("Reason"))

    score = get_score(car.get("MatchScore"))

    badge = ""

    if index == 1 and show_best_badge:
        badge = '<span class="best-badge">أفضل تطابق</span>'

    card_html = f"""
<div class="car-card">
    <div class="card-header">
        <div class="car-name">{brand} {model}</div>
        {badge}
    </div>

    <div class="price">{price}</div>

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
        <strong>لماذا اخترناها لك؟</strong><br>
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

    st.html(card_html)


# =========================================================
# استخراج رد n8n
# =========================================================

def extract_agent_answer(response):
    try:
        data = response.json()
    except Exception:
        return response.text.strip()

    if isinstance(data, str):
        return data.strip()

    if isinstance(data, list):
        if len(data) > 0:
            first = data[0]

            if isinstance(first, dict):
                for key in ["output", "answer", "text", "response"]:
                    if key in first:
                        return str(first[key]).strip()

        return str(data)

    if isinstance(data, dict):
        for key in ["output", "answer", "text", "response"]:
            if key in data:
                return str(data[key]).strip()

    return str(data).strip()


# =========================================================
# عرض الرد
# =========================================================

def render_answer(answer, original_request):
    if str(answer).strip().upper() == "NO_MATCH":
        st.markdown(
            """
<div class="no-match">
لم أجد سيارة في قاعدة بيانات CarWise تحقق جميع الشروط المطلوبة.
جرّب تعديل أحد الشروط أو الميزانية.
</div>
""",
            unsafe_allow_html=True
        )
        return

    cars = remove_duplicate_cars(
        parse_car_blocks(answer)
    )

    if cars:
        show_all = wants_all_cars(original_request)

        if show_all:
            cars_to_show = cars
        else:
            cars_to_show = cars[:3]

        st.markdown(
            f"""
<div class="result-count">
تم العثور على {len(cars_to_show)} سيارة
</div>
""",
            unsafe_allow_html=True
        )

        if not show_all:
            st.markdown(
                '<div class="results-title">توصيات CarWise</div>',
                unsafe_allow_html=True
            )

        for index, car in enumerate(cars_to_show, start=1):
            render_car_card(
                car,
                index,
                show_best_badge=not show_all
            )

    else:
        clean_answer = html.escape(
            str(answer)
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


# =========================================================
# ذاكرة المحادثة داخل الجلسة
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# الواجهة
# =========================================================

st.html("""
<div class="logo-wrap">
    <div class="logo-name">Car<span>Wise</span></div>
    <div class="logo-tagline">AI CAR ADVISOR</div>
    <div class="logo-line"></div>
</div>

<div class="hero">
    <div class="hero-kicker">مستشارك الذكي للسيارات</div>
    <div class="hero-title">اختر السيارة المناسبة لك <span>بذكاء</span></div>
    <div class="hero-text">
        اكتب ميزانيتك واستخدامك واحتياجاتك، وسيبحث CarWise في قاعدة بيانات السيارات
        ليقترح عليك أفضل الخيارات المطابقة لشروطك.
    </div>

    <div class="feature-grid">
        <div class="feature">
            <div class="feature-title">توصيات مخصصة</div>
            <div class="feature-sub">بناءً على احتياجك الفعلي</div>
        </div>
        <div class="feature">
            <div class="feature-title">مقارنة دقيقة</div>
            <div class="feature-sub">السعر والمواصفات والاستخدام</div>
        </div>
        <div class="feature">
            <div class="feature-title">بحث ذكي</div>
            <div class="feature-sub">داخل قاعدة بيانات CarWise</div>
        </div>
        <div class="feature">
            <div class="feature-title">نتيجة واضحة</div>
            <div class="feature-sub">مع سبب الاختيار ونسبة التطابق</div>
        </div>
    </div>
</div>
""")


# =========================================================
# عرض المحادثة السابقة
# =========================================================

for message in st.session_state.messages:

    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])

    else:
        with st.chat_message("assistant"):
            render_answer(
                message["content"],
                message.get("request", "")
            )


# =========================================================
# إدخال المستخدم
# =========================================================

user_request = st.chat_input(
    "مثال: أبي سيارة عائلية اقتصادية سعرها 130 ألف..."
)


# =========================================================
# إرسال السؤال إلى n8n
# =========================================================

if user_request:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_request
        }
    )

    with st.chat_message("user"):
        st.markdown(user_request)

    with st.chat_message("assistant"):

        with st.spinner(
            "CarWise يبحث عن أفضل الخيارات..."
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

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "request": user_request
                    }
                )

                render_answer(
                    answer,
                    user_request
                )

            except requests.exceptions.Timeout:

                error_message = "استغرق CarWise وقتًا أطول من المتوقع. حاول مرة أخرى."

                st.markdown(
                    f'<div class="error-box">{error_message}</div>',
                    unsafe_allow_html=True
                )

            except requests.exceptions.RequestException:

                error_message = "تعذر الاتصال بـ CarWise حاليًا. حاول مرة أخرى."

                st.markdown(
                    f'<div class="error-box">{error_message}</div>',
                    unsafe_allow_html=True
                )

            except Exception:

                error_message = "حدث خطأ أثناء معالجة النتيجة."

                st.markdown(
                    f'<div class="error-box">{error_message}</div>',
                    unsafe_allow_html=True
                )


st.markdown(
    '<div class="small-note">CarWise • توصيات مبنية على بيانات قاعدة المشروع</div>',
    unsafe_allow_html=True
)
