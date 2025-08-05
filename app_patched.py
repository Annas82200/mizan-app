
import streamlit as st
import pandas as pd
import os
import base64
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
from fpdf import FPDF

# --- Session Defaults ---
for key, default in {
    "is_admin": False,
    "assessment_complete": False,
    "company_setup": {},
    "org_structure_df": None,
    "ai_insight": "",
    "alignment_score": 0,
    "entropy_score": 0,
    "engagement": 0,
    "recognition": 0,
    "tensions": [],
    "gaps": [],
    "admin_password": "admin123"
}.items():
    st.session_state.setdefault(key, default)

# --- Validation Helpers ---
REQUIRED_RESPONSE_COLUMNS = ["Department", "Current Culture", "Alignment Score", "Entropy Score", "Engagement", "Recognition"]
REQUIRED_ORG_COLUMNS = ["Department", "Manager", "Role"]

def validate_responses_df(df):
    missing = [col for col in REQUIRED_RESPONSE_COLUMNS if col not in df.columns]
    if missing:
        st.error(f"❌ 'responses.csv' is missing columns: {', '.join(missing)}")
        return False
    return True

def validate_org_structure(df):
    missing = [col for col in REQUIRED_ORG_COLUMNS if col not in df.columns]
    if missing:
        st.error(f"❌ Uploaded file missing required columns: {', '.join(missing)}")
        return False
    return True

# --- Sidebar Admin Setup ---
with st.sidebar:
    st.header("🔧 Company Setup")

    company_vision = st.text_area("Company Vision", key="company_vision")
    company_mission = st.text_area("Company Mission", key="company_mission")
    company_values = st.text_area("Core Values (comma-separated)", key="company_values")
    company_strategy = st.text_area("Company Strategy", key="company_strategy")

    if st.button("💾 Save Setup"):
        st.session_state["company_setup"] = {
            "vision": company_vision,
            "mission": company_mission,
            "values": [v.strip() for v in company_values.split(",")],
            "strategy": company_strategy
        }
        st.success("✅ Setup saved successfully.")

    st.divider()
    st.header("🏗️ Company Structure Upload")

    uploaded_file = st.file_uploader("Upload Company Structure (CSV)", type="csv", key="company_csv_upload")

    if uploaded_file:
        try:
            org_df = pd.read_csv(uploaded_file)
            if validate_org_structure(org_df):
                st.session_state["org_structure_df"] = org_df
                st.success("✅ Structure uploaded successfully.")
                st.write("📊 Preview:")
                st.dataframe(org_df)
        except Exception as e:
            st.error(f"❌ Error reading file: {e}")

# Example chart using brand colors
st.subheader(" Mizan Culture Dashboard Example")
fig, ax = plt.subplots()
bar_data = pd.DataFrame({
    "Metric": ["Alignment", "Entropy", "Engagement", "Recognition"],
    "Score": [75, 22, 4.2, 3.9]
})
ax.barh(bar_data["Metric"], bar_data["Score"], color="#009688")  # Mizan green
ax.set_facecolor("#f2f9f8")
ax.set_xlim(0, 100)
ax.set_title("Mizan Culture Dashboard", fontsize=14, color="#004d40")
st.pyplot(fig)

def run_dashboard(insights, alignment, entropy, tensions, gaps):
    import streamlit as st
    import plotly.express as px
    import pandas as pd

    st.subheader(" AI-Generated Insights")
    st.markdown(f"**Alignment Score:** {alignment:.2f} / 100")
    st.markdown(f"**Cultural Entropy:** {entropy:.2f}%")

    st.write("### Summary Insights")
    st.write(insights)

    if tensions:
        st.write("### Tensions Identified")
        for t in tensions:
            st.error(f"- {t}")

    if gaps:
        st.write("### Value Gaps Between Levels")
        for g in gaps:
            st.warning(f"- {g}")

    # Optional: Visual bar chart if insights contain levels
    try:
        levels = ["Safety & Survival", "Belonging & Loyalty", "Growth & Achievement",
                  "Meaning & Contribution", "Integrity & Justice", "Wisdom & Compassion",
                  "Transcendence & Unity"]

        scores = [alignment * 0.1,  # dummy values based on alignment
                  alignment * 0.12,
                  alignment * 0.13,
                  alignment * 0.14,
                  alignment * 0.15,
                  alignment * 0.16,
                  alignment * 0.2]

        df = pd.DataFrame({"Mizan Level": levels, "Score": scores})
        fig = px.bar(df, x="Mizan Level", y="Score", color="Mizan Level",
                     title="Level-wise Alignment Distribution")
        st.plotly_chart(fig)
    except Exception as e:
        st.warning("Bar chart could not be generated.")
        st.text(str(e))