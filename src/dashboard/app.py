import streamlit as st

st.set_page_config(
    page_title="Explainable Credit Risk Platform",
    page_icon="📊",
    layout="wide",
)

st.title("Explainable and Fair Credit Risk Decision System")
st.markdown(
    """
This dashboard provides:
- **Predictions** with transparent explanations
- **SHAP/LIME/DiCE** explanations and comparison
- **Counterfactuals** for actionable recourse
- **Fairness audit** with before/after metrics and accuracy trade-offs

Navigate using the sidebar to explore different sections.
"""
)
