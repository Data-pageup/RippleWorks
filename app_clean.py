import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ---------------- Page setup ----------------
st.set_page_config(
    page_title="RippleWorks", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- Custom CSS for stunning UI ----------------
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Background with animated gradient */
        .stApp {
            background: linear-gradient(-45deg, #0a0e27, #16213e, #0f3460, #0e2954);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            color: white;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Main title with glow effect */
        .hero-title {
            font-family: 'Orbitron', monospace;
            font-size: 3.5em;
            font-weight: 900;
            text-align: center;
            background: linear-gradient(45deg, #64ffda, #00bcd4, #03dac6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(100, 255, 218, 0.3);
            margin-bottom: 0.5em;
            animation: glow 2s ease-in-out infinite alternate;
        }
        
        @keyframes glow {
            from { filter: drop-shadow(0 0 20px rgba(100, 255, 218, 0.3)); }
            to { filter: drop-shadow(0 0 30px rgba(100, 255, 218, 0.6)); }
        }
        
        .subtitle {
            font-family: 'Inter', sans-serif;
            font-size: 1.2em;
            text-align: center;
            color: #b0bec5;
            margin-bottom: 2em;
            font-weight: 300;
        }
        
        /* Glassmorphism cards */
        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 2em;
            margin: 1em 0;
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }
        
        .glass-card:hover {
            transform: translateY(-5px);
            box-shadow: 
                0 12px 40px rgba(0, 0, 0, 0.4),
                inset 0 1px 0 rgba(255, 255, 255, 0.2);
        }
        
        /* Style the column containers to look like cards */
        .stColumn > div {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 2em;
            margin: 1em 0;
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }
        
        .stColumn > div:hover {
            transform: translateY(-5px);
            box-shadow: 
                0 12px 40px rgba(0, 0, 0, 0.4),
                inset 0 1px 0 rgba(255, 255, 255, 0.2);
        }
        
        /* Input styling */
        .stNumberInput > div > div > input {
            background: rgba(255, 255, 255, 0.1) !important;
            border: 1px solid rgba(100, 255, 218, 0.3) !important;
            border-radius: 10px !important;
            color: white !important;
            font-family: 'Inter', sans-serif !important;
            transition: all 0.3s ease !important;
        }
        
        .stNumberInput > div > div > input:focus {
            border-color: #64ffda !important;
            box-shadow: 0 0 15px rgba(100, 255, 218, 0.3) !important;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(45deg, #64ffda, #00bcd4) !important;
            border: none !important;
            border-radius: 25px !important;
            padding: 0.75em 2em !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            font-size: 1.1em !important;
            color: #0a0e27 !important;
            box-shadow: 0 4px 20px rgba(100, 255, 218, 0.3) !important;
            transition: all 0.3s ease !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 6px 25px rgba(100, 255, 218, 0.5) !important;
        }
        
        /* Results styling */
        .result-card {
            background: linear-gradient(135deg, rgba(100, 255, 218, 0.1), rgba(0, 188, 212, 0.1));
            border: 2px solid rgba(100, 255, 218, 0.3);
            border-radius: 20px;
            padding: 2em;
            margin: 1em 0;
            text-align: center;
            animation: slideIn 0.6s ease-out;
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .metric-value {
            font-family: 'Orbitron', monospace;
            font-size: 2.5em;
            font-weight: 700;
            color: #64ffda;
            text-shadow: 0 0 15px rgba(100, 255, 218, 0.5);
        }
        
        .metric-label {
            font-family: 'Inter', sans-serif;
            font-size: 1.1em;
            color: #b0bec5;
            margin-bottom: 0.5em;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background: rgba(10, 14, 39, 0.8) !important;
            backdrop-filter: blur(20px) !important;
        }
        
        /* Parameter cards */
        .param-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 1.5em;
            margin: 0.8em 0;
            transition: all 0.3s ease;
        }
        
        .param-card:hover {
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(100, 255, 218, 0.3);
        }
        
        .param-icon {
            font-size: 1.5em;
            margin-right: 0.5em;
            color: #64ffda;
        }
        
        /* Quality indicator */
        .quality-excellent { color: #4caf50; }
        .quality-good { color: #8bc34a; }
        .quality-medium { color: #ff9800; }
        .quality-poor { color: #ff5722; }
        .quality-very-poor { color: #f44336; }
        
        /* Floating particles animation */
        .particle {
            position: fixed;
            pointer-events: none;
            opacity: 0.6;
            animation: float 6s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
        }
    </style>
""", unsafe_allow_html=True)

# Add floating particles
st.markdown("""
    <div class="particle" style="left: 10%; animation-delay: 0s;">💧</div>
    <div class="particle" style="left: 20%; animation-delay: 1s;">🌊</div>
    <div class="particle" style="left: 80%; animation-delay: 2s;">💧</div>
    <div class="particle" style="left: 90%; animation-delay: 3s;">🌊</div>
""", unsafe_allow_html=True)

# ---------------- Load models ----------------
@st.cache_resource
def load_models():
    models = {}
    scaler = None
    if os.path.exists("best_wqi_model.joblib"):
        models["wqi"] = joblib.load("best_wqi_model.joblib")
    else:
        models["wqi"] = None
    if os.path.exists("best_wqc_model.joblib"):
        models["wqc"] = joblib.load("best_wqc_model.joblib")
    else:
        models["wqc"] = None
    if os.path.exists("scaler.joblib"):
        scaler = joblib.load("scaler.joblib")
    return models, scaler

models, scaler = load_models()

# ---------------- Feature engineering ----------------
def engineer_features_row(d):
    out = dict(d)
    out["FecalColiform_log"] = np.log1p(out["FecalColiform"])
    out["TotalColiform_log"] = np.log1p(out["TotalColiform"])
    out["BOD_DO_ratio"] = out["BOD"] / (out["DissolvedOxygen"] + 1e-8)
    out["Coliform_ratio"] = out["FecalColiform"] / (out["TotalColiform"] + 1e-8)
    out["Cond_Nitrates"] = out["Conductivity"] * out["Nitrates"]
    out["pH_sq"] = (out["pH"] - 7.0) ** 2
    out["low_DO_flag"] = int(out["DissolvedOxygen"] < 3.0)
    return pd.Series(out)

def predict_row(df_row):
    features = engineer_features_row(df_row.to_dict())
    X = features.to_frame().T
    numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()

    if scaler is not None:
        try:
            X_input = scaler.transform(X[numeric_cols])
        except Exception:
            X_input = X[numeric_cols].values
    else:
        X_input = X[numeric_cols].values

    # WQI
    if models["wqi"] is not None:
        try:
            wqi_pred = float(models["wqi"].predict(X[numeric_cols])[0])
        except Exception:
            wqi_pred = float(models["wqi"].predict(X_input)[0])
    else:
        feats = ["DissolvedOxygen", "pH", "Conductivity", "BOD",
                 "Nitrates", "FecalColiform_log", "TotalColiform_log"]
        sub = X[feats].astype(float)
        norm = (sub - sub.min()) / (sub.max() - sub.min() + 1e-8)
        wqi_pred = float(norm.mean(axis=1).values[0] * 100)

    # WQC
    if models["wqc"] is not None:
        try:
            wqc_pred = models["wqc"].predict(X[numeric_cols])[0]
        except Exception:
            wqc_pred = models["wqc"].predict(X_input)[0]
    else:
        def classify_wqi(x):
            if x >= 90: return "Excellent"
            if x >= 70: return "Good"
            if x >= 50: return "Medium"
            if x >= 25: return "Poor"
            return "Very Poor"
        wqc_pred = classify_wqi(wqi_pred)

    return features.to_frame().T, wqi_pred, wqc_pred

def get_quality_color(wqc):
    colors = {
        "Excellent": "quality-excellent",
        "Good": "quality-good", 
        "Medium": "quality-medium",
        "Poor": "quality-poor",
        "Very Poor": "quality-very-poor"
    }
    return colors.get(wqc, "quality-medium")

def create_gauge_chart(value, title):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title, 'font': {'color': '#64ffda', 'size': 20}},
        delta = {'reference': 70},
        gauge = {
            'axis': {'range': [None, 100], 'tickcolor': '#64ffda'},
            'bar': {'color': "#64ffda"},
            'steps': [
                {'range': [0, 25], 'color': "rgba(244, 67, 54, 0.3)"},
                {'range': [25, 50], 'color': "rgba(255, 87, 34, 0.3)"},
                {'range': [50, 70], 'color': "rgba(255, 152, 0, 0.3)"},
                {'range': [70, 90], 'color': "rgba(139, 195, 74, 0.3)"},
                {'range': [90, 100], 'color': "rgba(76, 175, 80, 0.3)"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "#64ffda"},
        height=300
    )
    
    return fig

# ---------------- Main UI ----------------
# Header
st.markdown("<div class='hero-title'>🌊 AquaPredict Pro</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Advanced Water Quality Intelligence System by AG R</div>", unsafe_allow_html=True)

# Create columns for layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    <div class='glass-card'>
        <h3 style='color: #64ffda; margin-bottom: 1em;'>🔬 Water Parameters</h3>
    </div>
    """, unsafe_allow_html=True)
    
    T = st.number_input("🌡️ **Temperature** (°C)", value=25.0, step=0.1, help="Water temperature affects dissolved oxygen levels")
    DO = st.number_input("🫁 **Dissolved Oxygen** (mg/L)", value=6.0, step=0.1, help="Critical for aquatic life survival")
    pH = st.number_input("⚖️ **pH Level**", value=7.0, step=0.1, help="Measure of water acidity/alkalinity")
    Cond = st.number_input("🔌 **Conductivity** (µS/cm)", value=200.0, step=1.0, help="Measure of dissolved ionic substances")

with col2:
    st.markdown("""
    <div class='glass-card'>
        <h3 style='color: #64ffda; margin-bottom: 1em;'>🧪 Chemical & Biological</h3>
    </div>
    """, unsafe_allow_html=True)
    
    BOD = st.number_input("🧪 **BOD** (mg/L)", value=2.0, step=0.1, help="Biological Oxygen Demand - organic pollution indicator")
    NO3 = st.number_input("🧬 **Nitrates** (mg/L)", value=1.0, step=0.1, help="Nitrogen compounds from agricultural runoff")
    Fec = st.number_input("🦠 **Fecal Coliform** (CFU/100mL)", value=100.0, step=1.0, help="Indicator of sewage contamination")
    Tot = st.number_input("🦠 **Total Coliform** (CFU/100mL)", value=500.0, step=1.0, help="Overall bacterial contamination level")

# Prediction button
st.markdown("<div style='text-align: center; margin: 2em 0;'>", unsafe_allow_html=True)
run_single = st.button("🚀 **ANALYZE WATER QUALITY**", key="predict_btn")
st.markdown("</div>", unsafe_allow_html=True)

# Results section
if run_single:
    base = pd.Series({
        "Temperature": T, "DissolvedOxygen": DO, "pH": pH,
        "Conductivity": Cond, "BOD": BOD, "Nitrates": NO3,
        "FecalColiform": Fec, "TotalColiform": Tot
    })
    
    with st.spinner('🔄 Processing water quality data...'):
        Xfeat, wqi_pred, wqc_pred = predict_row(base)
    
    # Results display
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='metric-label'>Water Quality Index</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>{wqi_pred:.1f}</div>", unsafe_allow_html=True)
        st.plotly_chart(create_gauge_chart(wqi_pred, "WQI Score"), use_container_width=True)
    
    with col2:
        st.markdown("<div class='metric-label'>Water Quality Class</div>", unsafe_allow_html=True)
        quality_class = get_quality_color(wqc_pred)
        st.markdown(f"<div class='metric-value {quality_class}'>{wqc_pred}</div>", unsafe_allow_html=True)
        
        # Quality interpretation
        interpretations = {
            "Excellent": "🟢 Safe for all uses including drinking",
            "Good": "🔵 Suitable for most purposes",
            "Medium": "🟡 Requires treatment for sensitive uses",
            "Poor": "🟠 Limited use, treatment recommended",
            "Very Poor": "🔴 Requires significant treatment"
        }
        st.markdown(f"**{interpretations.get(wqc_pred, 'Unknown quality level')}**")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Feature analysis
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### 📊 **Detailed Analysis**")
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📈 Parameter Overview", "🔬 Engineered Features", "📋 Summary Report"])
    
    with tab1:
        # Create parameter visualization
        params = ['Temperature', 'DissolvedOxygen', 'pH', 'Conductivity', 'BOD', 'Nitrates', 'FecalColiform', 'TotalColiform']
        values = [T, DO, pH, Cond, BOD, NO3, Fec, Tot]
        
        fig = px.bar(x=params, y=values, title="Input Parameters", color=values, 
                    color_continuous_scale="viridis")
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "#64ffda"},
            title_font_color="#64ffda"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.dataframe(Xfeat.T.style.format("{:.4f}"), use_container_width=True)
    
    with tab3:
        st.markdown(f"""
        **Analysis Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**
        
        🎯 **Overall Score:** {wqi_pred:.1f}/100 ({wqc_pred})
        
        **Key Findings:**
        - pH Level: {'✅ Optimal' if 6.5 <= pH <= 8.5 else '⚠️ Outside optimal range'}
        - Dissolved Oxygen: {'✅ Healthy' if DO > 5.0 else '⚠️ Low levels detected'}
        - Bacterial Load: {'✅ Acceptable' if Fec < 200 else '⚠️ High contamination'}
        - Chemical Balance: {'✅ Good' if BOD < 5.0 else '⚠️ High organic pollution'}
        
        **Recommendations:**
        {f'🟢 Water quality is excellent - safe for all intended uses.' if wqc_pred == 'Excellent' else
         f'🔵 Good water quality - suitable for most purposes.' if wqc_pred == 'Good' else
         f'🟡 Moderate quality - monitor and consider treatment for sensitive applications.' if wqc_pred == 'Medium' else
         f'🟠 Poor quality - treatment recommended before use.' if wqc_pred == 'Poor' else
         f'🔴 Very poor quality - significant treatment required.'}
        """)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style='text-align: center; margin-top: 3em; padding: 2em; color: #64ffda; font-family: Inter, sans-serif;'>
        <div style='font-size: 0.9em; opacity: 0.7;'>
            🌊 Powered by Advanced ML Models | Real-time Water Quality Assessment
        </div>
    </div>
""", unsafe_allow_html=True)