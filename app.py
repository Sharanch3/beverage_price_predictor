import streamlit as st
import numpy as np
import pandas as pd
import joblib

st.set_page_config(
    page_title="Beverage Price Predictor",
    page_icon="🍷",
    layout="centered"
)

st.title("CodeX: Beverage Price Predictor")
st.write(" ")

# Load the pre-saved pipeline and label encoder
pipeline = joblib.load("./artifacts/best_pipeline.pkl")
le       = joblib.load("./artifacts/label_encoder.pkl")


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    bins   = [18, 26, 36, 46, 56, 71, 101]
    labels = ["18-25", "26-35", "36-45", "46-55", "56-70", "70+"]
    df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels, right=False)

    df["consume_frequency(weekly)"] = df["consume_frequency(weekly)"].map(
        {"0-2 times": 1, "3-4 times": 2, "5-7 times": 3})

    df["awareness_of_other_brands"] = df["awareness_of_other_brands"].map(
        {"0 to 1": 1, "2 to 4": 2, "above 4": 3})

    df["zone"] = df["zone"].map(
        {"Rural": 1, "Semi-Urban": 2, "Urban": 3, "Metro": 4})

    df["income_levels"] = df["income_levels"].map(
        {"not reported": 0, "<10L": 1, "10L - 15L": 2,
         "16L - 25L": 3, "26L - 35L": 4, "> 35L": 5})

    df["cf_ab_score"] = (
        df["consume_frequency(weekly)"] /
        (df["consume_frequency(weekly)"] + df["awareness_of_other_brands"])
    ).round(2)

    df["zas_score"] = df["zone"] * df["income_levels"]

    df["bsi"] = np.where(
        (df["current_brand"] != "Established") &
        (df["reasons_for_choosing_brands"].isin(["Price", "Quality"])),
        1, 0
    )

    df = df.drop(columns=["age"])
    return df


with st.form(key="Beverage Price Predictor"):

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        age       = st.number_input(label="Age", min_value=18, max_value=100, step=1)
        income    = st.selectbox(label="Income Level (in Lakhs)",
                                 options=["<10L", "10L - 15L", "16L - 25L", "26L - 35L", "> 35L"])
        awareness = st.selectbox(label="Awarness of other Brand",
                                 options=["0 to 1", "2 to 4", "above 4"])
        packaging = st.selectbox(label="Packaging Preferences",
                                 options=["Simple", "Premium", "Eco-Friendly"])

    with col2:
        gender       = st.selectbox(label="Gender", options=["M", "F"])
        consume_freq = st.selectbox(label="Consume Count (weekly)",
                                    options=["0-2 times", "3-4 times", "5-7 times"])
        reason       = st.selectbox(label="Reason for choosing brand",
                                    options=["Price", "Quality", "Availability", "Brand Reputation"])
        health       = st.selectbox(label="Health Concerns",
                                    options=["Low (Not very concerned)",
                                             "Medium (Moderately health-conscious)",
                                             "High (Very health-conscious)"])

    with col3:
        zone        = st.selectbox(label="Zone", options=["Urban", "Metro", "Rural", "Semi-Urban"])
        brand       = st.selectbox(label="Current Brand", options=["Newcomer", "Established"])
        flavor      = st.selectbox(label="Flavor Preferences", options=["Traditional", "Exotic"])
        typical_use = st.selectbox(label="Typical Use",
                                   options=["Active (eg. Sports, gym)",
                                            "Social (eg. Parties)",
                                            "Casual (eg. At home)"])

    with col4:
        occupation  = st.selectbox(label="Occupation",
                                   options=["Working Professional", "Student", "Entrepreneur", "Retired"])
        pref_size   = st.selectbox(label="Preferable Size",
                                   options=["Small (250 ml)", "Medium (500 ml)", "Large (1 L)"])
        purchase_ch = st.selectbox(label="Purchase Channel", options=["Online", "Retail Store"])

    st.write(" ")
    submitted = st.form_submit_button("Predict Price Range", type="primary")


if submitted:
    row = pd.DataFrame([{
        "age":                            age,
        "gender":                         gender,
        "zone":                           zone,
        "occupation":                     occupation,
        "income_levels":                  income,
        "consume_frequency(weekly)":      consume_freq,
        "current_brand":                  brand,
        "preferable_consumption_size":    pref_size,
        "awareness_of_other_brands":      awareness,
        "reasons_for_choosing_brands":    reason,
        "flavor_preference":              flavor,
        "purchase_channel":               purchase_ch,
        "packaging_preference":           packaging,
        "health_concerns":                health,
        "typical_consumption_situations": typical_use,
    }])

    row = engineer_features(row)

    prediction = le.inverse_transform(pipeline.predict(row))[0]
    st.success(body=f"Predicted Price Range: {prediction}", icon="🎯")


