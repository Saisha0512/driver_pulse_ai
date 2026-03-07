"""
app.py — Driver Pulse AI
Entry point for Streamlit multipage app.

Run:
    streamlit run app.py

Owned by: Aayush (System & Dashboard Lead)
This file handles login/session. For dev, it auto-sets a demo driver.
"""

import streamlit as st

st.set_page_config(
    page_title="Driver Pulse AI",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Session defaults for standalone dev ──
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "driver_id" not in st.session_state:
    st.session_state["driver_id"] = "SDRV039"

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@700&family=Inter:wght@400;500&display=swap');
  .stApp { background: #0d0f14; }
  #MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding:80px 40px; background:linear-gradient(135deg,#111827,#1a2035);
            border-radius:20px; border:1px solid #1e293b; margin:40px auto; max-width:600px;">
  <div style="font-family:'Rajdhani',sans-serif; font-size:3rem; font-weight:700; color:#f8fafc; letter-spacing:0.1em;">
    🚗 DRIVER PULSE AI
  </div>
  <div style="color:#475569; margin:12px 0 32px; font-size:0.9rem; letter-spacing:0.08em;">
    PERSONAL SAFETY & PERFORMANCE INTELLIGENCE
  </div>
  <div style="color:#64748b; font-size:0.8rem;">
    Use the sidebar to navigate to <strong style="color:#94a3b8">My Safety</strong> or other pages.
    <br><br>For demo: select any driver ID on the Safety page.
  </div>
</div>
""", unsafe_allow_html=True)