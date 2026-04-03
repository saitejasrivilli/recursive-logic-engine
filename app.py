import streamlit as st
import json

st.set_page_config(page_title="Recursive Logic Engine", page_icon="🧠", layout="wide")

st.title("🧠 Recursive Logic Engine")
st.markdown("**Self-correcting reasoning specialist using GRPO + RLVR**")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Results", "🔍 Self-Correction", "📈 Algorithms", "⚡ Efficiency", "🛡️ Stability"])

with tab1:
    st.header("Performance Results")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Logic Accuracy", "68.7%", "+26.4%")
    col2.metric("Self-Correction", "35%", "✓")
    col3.metric("Training Speedup", "4x", "⚡")
    col4.metric("KL Divergence", "0.089", "✓ Stable")

with tab2:
    st.header("Self-Correction Examples")
    examples = [
        ("Logic", "If A > B and B > C, then A is ___ to C?", "A is greater than C"),
        ("Arithmetic", "What is 37 × 24?", "888"),
        ("Knowledge", "Capital of Australia?", "Canberra"),
    ]
    for cat, q, a in examples:
        with st.expander(f"{cat}: {q}"):
            st.success(f"✓ Answer: {a}")

with tab3:
    st.header("Algorithm Innovations")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("GRPO")
        st.write("Group Relative Policy Optimization - reduces variance, enables stable learning")
    with col2:
        st.subheader("RLVR")
        st.write("Reward & Loss Velocity Regularization - real-time stability monitoring")

with tab4:
    st.header("Data Efficiency")
    col1, col2, col3 = st.columns(3)
    col1.metric("Original", "40,000 samples")
    col2.metric("Filtered", "10,000 samples (25%)")
    col3.metric("Speedup", "4x faster")

with tab5:
    st.header("Catastrophic Forgetting Prevention")
    st.markdown("""
    **Without Monitoring:** General Knowledge drops 94.8% ✗
    **With RLVR:** General Knowledge preserved at 47.9% ✓
    
    Threshold: -5.0% | Safety Margin: 4.7%
    """)

st.markdown("---")
st.markdown("[📊 GitHub](https://github.com/saitejasrivilli/recursive-logic-engine)")
