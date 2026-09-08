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
        flags=re.IGNORECASE | re.DOTALL
    )

    cars = []

    fields = [
        "Brand",
        "Model",
        "Year",
        "Price",
        "BodyType",
        "BestUse",
        "FuelEconomy",
        "Transmission",
        "Seats",
        "Reason",
        "MatchScore"
    ]

    for block in blocks:
        car = {}

        for i, field in enumerate(fields):
            next_fields = fields[i + 1:]

            if next_fields:
                next_pattern = "|".join(
                    rf"{re.escape(f)}\s*:"
                    for f in next_fields
                )

                pattern = (
                    rf"{re.escape(field)}\s*:\s*"
                    rf"(.*?)"
                    rf"(?=\s*(?:{next_pattern})|$)"
