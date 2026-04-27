import streamlit as st
import pandas as pd
import joblib

# =========================
# 🚀 Load Model
# =========================
model = joblib.load("credit_model_pipeline.pkl")
threshold = joblib.load("threshold.pkl")

# =========================
# 🎨 Page Config
# =========================
st.set_page_config(
    page_title="Credit Risk Predictor System",
    page_icon="💳",
    layout="wide"
)

# =========================
# 🎨 Custom Fintech Styling
# =========================
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
.card {
    background-color: #161b22;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.4);
}
.metric-title {
    font-size: 14px;
    color: #9aa0a6;
}
.metric-value {
    font-size: 22px;
    font-weight: bold;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 🏷️ Header
# =========================
st.markdown("""
<h1 style='text-align: center;'>💳 Credit Risk Predictor System</h1>
<p style='text-align: center; color: gray;'>ML-powered Loan Approval Dashboard</p>
""", unsafe_allow_html=True)

st.markdown("---")

# =========================
# 🧾 Sidebar
# =========================
st.sidebar.markdown("## 💳 Credit Risk Engine")
st.sidebar.markdown("---")
st.sidebar.write("Model: Random Forest (Tuned)")
st.sidebar.write(f"Threshold: {threshold}")
st.sidebar.write("Goal: Balance Risk + Business")
st.sidebar.markdown("👨‍💻 **Prepared by Dharmesh Parmar**")

# =========================
# 🧾 Input Section
# =========================
st.subheader("📝 Customer Profile")

col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age", 18, 75, 30)
    job = st.selectbox("Job Level", [0, 1, 2, 3])
    housing = st.selectbox("Housing", ["own", "rent", "free"])
    saving = st.selectbox("Saving Accounts", ["little", "moderate", "quite rich", "rich"])

with col2:
    checking = st.selectbox("Checking Account", ["little", "moderate", "rich"])
    credit_amount = st.number_input("Credit Amount", 1000, 20000, 5000)
    duration = st.slider("Loan Duration (Months)", 6, 72, 24)
    purpose = st.selectbox("Purpose", [
        "car", "furniture/equipment", "radio/TV",
        "business", "education", "repairs", "vacation/others"
    ])

sex = st.radio("Gender", ["male", "female"])

# =========================
# 🔮 Prediction
# =========================
if st.button("🔍 Evaluate Risk"):

    # Feature Engineering
    credit_per_month = credit_amount / duration
    credit_income_proxy = credit_amount / (age + 1)

    age_group = (
        "young" if age < 30 else
        "adult" if age < 45 else
        "mature" if age < 60 else
        "senior"
    )

    # DataFrame
    input_df = pd.DataFrame({
        "Age": [age],
        "Sex": [sex],
        "Job": [job],
        "Housing": [housing],
        "Saving accounts": [saving],
        "Checking account": [checking],
        "Credit amount": [credit_amount],
        "Duration": [duration],
        "Purpose": [purpose],
        "credit_per_month": [credit_per_month],
        "credit_income_proxy": [credit_income_proxy],
        "age_group": [age_group]
    })

    # Prediction
    prob = model.predict_proba(input_df)[:, 1][0]
    pred = int(prob > threshold)
    risk_percent = int(prob * 100)

    st.markdown("---")

    # =========================
    # 📊 KPI CARDS
    # =========================
    col1, col2, col3 = st.columns(3)

    col1.markdown(f"""
    <div class="card">
        <div class="metric-title">Risk Score</div>
        <div class="metric-value">{risk_percent}%</div>
    </div>
    """, unsafe_allow_html=True)

    col2.markdown(f"""
    <div class="card">
        <div class="metric-title">Decision</div>
        <div class="metric-value">{'Rejected' if pred==1 else 'Approved'}</div>
    </div>
    """, unsafe_allow_html=True)

    col3.markdown(f"""
    <div class="card">
        <div class="metric-title">Model Confidence</div>
        <div class="metric-value">{round(prob,2)}</div>
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # 📈 Risk Display
    # =========================
    st.markdown("### 📊 Risk Level")

    if pred == 1:
        st.error(f"⚠️ High Risk Customer ({risk_percent}%)")
    else:
        st.success(f"✅ Low Risk Customer ({risk_percent}%)")

    st.progress(risk_percent)

    # =========================
    # 💼 Decision
    # =========================
    st.markdown("### 💼 Loan Decision")

    if pred == 1:
        st.markdown("<div style='color:red; font-size:18px;'>❌ Loan Rejected</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='color:green; font-size:18px;'>✅ Loan Approved</div>", unsafe_allow_html=True)

    # =========================
    # 🧠 Explanation
    # =========================
    st.markdown("### 🧠 Key Risk Drivers")

    reasons = []

    if credit_amount > 5000:
        reasons.append("High loan amount increases risk")

    if duration > 36:
        reasons.append("Long duration increases default probability")

    if saving == "little":
        reasons.append("Low savings indicate weak financial stability")

    if checking == "little":
        reasons.append("Low account balance increases risk")

    if housing == "free":
        reasons.append("No owned assets increases risk")

    if not reasons:
        reasons.append("Customer shows stable financial indicators")

    for r in reasons:
        st.markdown(f"""
        <div class="card" style="margin-bottom:10px;">
            {r}
        </div>
        """, unsafe_allow_html=True)

# =========================
# 📌 Footer
# =========================
st.markdown("---")
st.markdown(
    """
    <div style="
        text-align: center;
        font-family: 'Segoe UI';
        color: #9aa0a6;
        margin-top: 20px;
    ">
        <div style="font-size: 16px; font-weight: 600; color: white;">
            💳 Credit Risk Predictor System
        </div>
        <div style="margin-top: 8px;">
            Prepared by 
            <span style="
                font-weight: 700;
                color: white;
                background-color: #0d6efd;
                padding: 5px 12px;
                border-radius: 6px;
            ">
                Dharmesh Parmar
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)