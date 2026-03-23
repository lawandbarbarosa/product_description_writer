import streamlit as st
import requests
import time
from dotenv import load_dotenv

load_dotenv()

BACK_END_URL = "https://f23uvrabfm.us-east-1.awsapprunner.com"

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SIMKO AI · Product Copy",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0c0d0f !important;
    color: #e8e4dc !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: #111317 !important;
    border-right: 1px solid #222529 !important;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #0c0d0f 0%, #141720 50%, #0c0d0f 100%);
    border: 1px solid #1e2229;
    border-radius: 16px;
    padding: 52px 48px 44px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse 60% 50% at 80% 50%, rgba(255,200,80,0.06) 0%, transparent 70%);
    pointer-events: none;
}
.hero-tag {
    display: inline-block;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #c8a44a;
    background: rgba(200,164,74,0.1);
    border: 1px solid rgba(200,164,74,0.25);
    border-radius: 999px;
    padding: 4px 14px;
    margin-bottom: 20px;
}
.hero-title {
    font-family: 'DM Serif Display', serif !important;
    font-size: clamp(2rem, 4vw, 3.2rem);
    font-weight: 400;
    color: #f0ebe0;
    line-height: 1.15;
    margin: 0 0 14px;
    letter-spacing: -0.02em;
}
.hero-title em {
    font-style: italic;
    color: #c8a44a;
}
.hero-sub {
    font-size: 15px;
    color: #7a7e88;
    line-height: 1.6;
    max-width: 540px;
    margin: 0;
}
.hero-deco {
    position: absolute;
    right: 48px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 88px;
    opacity: 0.06;
    font-family: 'DM Serif Display', serif;
    user-select: none;
    line-height: 1;
}

/* ── Sidebar labels & inputs ── */
[data-testid="stSidebar"] label {
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #5a5f6b !important;
}
[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stTextArea textarea,
[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
    background: #0c0d0f !important;
    border: 1px solid #222529 !important;
    border-radius: 8px !important;
    color: #e8e4dc !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    transition: border-color .2s;
}
[data-testid="stSidebar"] .stTextInput input:focus,
[data-testid="stSidebar"] .stTextArea textarea:focus {
    border-color: #c8a44a !important;
    box-shadow: 0 0 0 3px rgba(200,164,74,0.12) !important;
}

/* ── Submit button ── */
[data-testid="stSidebar"] .stFormSubmitButton button {
    background: linear-gradient(135deg, #c8a44a, #e8c46a) !important;
    color: #0c0d0f !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    padding: 14px !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: opacity .2s, transform .15s !important;
}
[data-testid="stSidebar"] .stFormSubmitButton button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* ── Sidebar section header ── */
.sidebar-section {
    font-family: 'DM Serif Display', serif;
    font-size: 20px;
    color: #f0ebe0;
    margin: 0 0 24px;
    padding-bottom: 14px;
    border-bottom: 1px solid #1e2229;
}

/* ── Tone pill selector ── */
.tone-hint {
    font-size: 12px;
    color: #5a5f6b;
    margin-top: -6px;
    margin-bottom: 4px;
}

/* ── Result tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    background: #111317;
    border-radius: 10px;
    padding: 4px;
    border: 1px solid #1e2229;
    gap: 4px;
}
[data-testid="stTabs"] button[role="tab"] {
    border-radius: 7px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #5a5f6b !important;
    padding: 8px 16px !important;
    border: none !important;
    background: transparent !important;
    transition: all .2s !important;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    background: #1e2229 !important;
    color: #e8e4dc !important;
}

/* ── Result cards ── */
.result-card {
    background: #111317;
    border: 1px solid #1e2229;
    border-radius: 14px;
    padding: 32px 36px;
    margin-top: 16px;
    position: relative;
    overflow: hidden;
}
.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #c8a44a, transparent);
}
.result-card-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #c8a44a;
    margin-bottom: 16px;
}
.result-card p, .result-card li {
    font-size: 15px;
    line-height: 1.75;
    color: #c8c4bc;
}

/* ── Info / status boxes ── */
[data-testid="stInfo"] {
    background: #111317 !important;
    border: 1px solid #1e2229 !important;
    border-radius: 10px !important;
    color: #7a7e88 !important;
}
[data-testid="stAlert"] {
    border-radius: 10px !important;
}

/* ── Metric strip ── */
.metric-strip {
    display: flex;
    gap: 12px;
    margin-bottom: 28px;
    flex-wrap: wrap;
}
.metric-pill {
    background: #111317;
    border: 1px solid #1e2229;
    border-radius: 999px;
    padding: 6px 16px;
    font-size: 12px;
    font-weight: 500;
    color: #5a5f6b;
    display: flex;
    align-items: center;
    gap: 6px;
}
.metric-pill span.val {
    color: #c8a44a;
    font-weight: 700;
}

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 80px 40px;
    border: 1px dashed #1e2229;
    border-radius: 16px;
    background: #0e0f12;
}
.empty-icon {
    font-size: 52px;
    margin-bottom: 20px;
    opacity: 0.5;
}
.empty-title {
    font-family: 'DM Serif Display', serif;
    font-size: 22px;
    color: #3a3e48;
    margin-bottom: 10px;
}
.empty-body {
    font-size: 14px;
    color: #3a3e48;
    max-width: 320px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ── Copy button ── */
.stButton button {
    background: transparent !important;
    border: 1px solid #2a2e38 !important;
    border-radius: 8px !important;
    color: #7a7e88 !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    padding: 6px 16px !important;
    transition: all .2s !important;
}
.stButton button:hover {
    border-color: #c8a44a !important;
    color: #c8a44a !important;
    background: rgba(200,164,74,0.05) !important;
}

/* ── Status widget ── */
[data-testid="stStatus"] {
    background: #111317 !important;
    border: 1px solid #1e2229 !important;
    border-radius: 12px !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0c0d0f; }
::-webkit-scrollbar-thumb { background: #222529; border-radius: 999px; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-section">Product Details</div>', unsafe_allow_html=True)

    with st.form("product_form"):
        product_name = st.text_input(
            "Product Name",
            placeholder="e.g. Apex Frontier Jeans"
        )

        col_a, col_b = st.columns(2)
        with col_a:
            product_category = st.text_input(
                "Category",
                placeholder="e.g. Menswear"
            )
        with col_b:
            target_audience = st.text_input(
                "Audience",
                placeholder="e.g. Ages 20–40"
            )

        tone = st.selectbox(
            "Brand Tone",
            ["Professional", "Rugged", "Luxury", "Playful", "Urgent", "Informative"],
            index=0,
            help="Sets the voice and energy of the generated copy."
        )

        tone_descriptions = {
            "Professional": "Clean, credible, and trustworthy",
            "Rugged": "Bold, gritty, built for the outdoors",
            "Luxury": "Elevated, aspirational, and refined",
            "Playful": "Fun, punchy, and full of personality",
            "Urgent": "High-energy, action-driven, FOMO-inducing",
            "Informative": "Detail-first, factual, and helpful",
        }
        st.markdown(f'<div class="tone-hint">↳ {tone_descriptions[tone]}</div>', unsafe_allow_html=True)

        features_text = st.text_area(
            "Key Features  (one per line)",
            placeholder="14oz Selvedge Denim\nDouble-stitched seams\nSlim fit\nWater-resistant finish",
            height=150,
        )

        st.divider()
        submit_button = st.form_submit_button("✦  Generate Description", use_container_width=True)


# ── Main area ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-tag">✦ AI Copywriting</div>
    <h1 class="hero-title">Words that <em>sell.</em><br>Copy that converts.</h1>
    <p class="hero-sub">Generate SEO-optimised, brand-consistent product descriptions in seconds — powered by a multi-stage AI pipeline.</p>
    <div class="hero-deco">✍</div>
</div>
""", unsafe_allow_html=True)


# ── Generate ──────────────────────────────────────────────────────────────────
if submit_button:
    if not product_name or not features_text:
        st.error("⚠️  Please provide at least a **Product Name** and **Key Features** before generating.")
    else:
        feature_list = [f.strip() for f in features_text.split("\n") if f.strip()]

        payload = {
            "product_name": product_name,
            "product_category": product_category,
            "key_features": feature_list,
            "target_audience": target_audience,
            "tone": tone,
        }

        with st.status("🤖  Agent pipeline running…", expanded=True) as status:
            st.write("📡  Sending data to research node…")
            time.sleep(0.4)
            st.write("🔍  Analysing product positioning…")
            time.sleep(0.4)
            st.write("✍️  Drafting first copy pass…")

            try:
                response = requests.post(f"{BACK_END_URL}/generate", json=payload)

                if response.status_code == 200:
                    data = response.json()
                    st.write("🔄  Refining and polishing copy…")
                    time.sleep(0.3)
                    status.update(label="✅  Description ready!", state="complete", expanded=False)

                    # ── Metric strip ──
                    word_count = len(data.get("final_description", "").split())
                    feature_count = len(feature_list)
                    st.markdown(f"""
                    <div class="metric-strip">
                        <div class="metric-pill">Product <span class="val">{product_name}</span></div>
                        <div class="metric-pill">Tone <span class="val">{tone}</span></div>
                        <div class="metric-pill">Features <span class="val">{feature_count}</span></div>
                        <div class="metric-pill">Words <span class="val">~{word_count}</span></div>
                    </div>
                    """, unsafe_allow_html=True)

                    # ── Tabs ──
                    tab1, tab2, tab3 = st.tabs(["✨  Final Copy", "✍️  First Draft", "🔍  Research Notes"])

                    with tab1:
                        st.markdown('<div class="result-card"><div class="result-card-label">Ready to publish</div>', unsafe_allow_html=True)
                        st.markdown(data.get("final_description", ""))
                        st.markdown("</div>", unsafe_allow_html=True)
                        st.button("⎘  Copy to clipboard", key="copy_final")
                        st.caption("Tip: Click copy, then paste directly into your product listing.")

                    with tab2:
                        st.markdown('<div class="result-card"><div class="result-card-label">Initial draft · pre-refinement</div>', unsafe_allow_html=True)
                        st.info("This is the raw first pass before the AI refines tone, flow, and SEO structure.")
                        st.markdown(data.get("draft_description", ""))
                        st.markdown("</div>", unsafe_allow_html=True)

                    with tab3:
                        st.markdown('<div class="result-card"><div class="result-card-label">AI research insights</div>', unsafe_allow_html=True)
                        st.write("The agent gathered these insights before writing your copy:")
                        st.markdown(data.get("research_notes", ""))
                        st.markdown("</div>", unsafe_allow_html=True)

                else:
                    status.update(label="❌  Generation failed", state="error")
                    st.error(f"API returned an error: {response.text}")

            except Exception as e:
                status.update(label="❌  Connection error", state="error")
                st.error(f"Could not reach the backend service: {e}")

else:
    # ── Empty state ──
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">✦</div>
        <div class="empty-title">Ready when you are</div>
        <div class="empty-body">Fill in your product details in the sidebar and hit <strong>Generate Description</strong> to get started.</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Feature showcase ──
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    cards = [
        ("🔍", "Research-First", "The agent analyses your product category and audience before writing a single word."),
        ("✍️", "Two-Stage Drafting", "A raw draft is produced, then refined for tone, flow, and SEO in a second pass."),
        ("📋", "Ready to Publish", "Output is formatted and ready to paste directly into your store listings."),
    ]
    for col, (icon, title, desc) in zip([c1, c2, c3], cards):
        with col:
            st.markdown(f"""
            <div class="result-card" style="text-align:center; padding: 28px 24px;">
                <div style="font-size:28px; margin-bottom:12px;">{icon}</div>
                <div style="font-family:'DM Serif Display',serif; font-size:17px; color:#f0ebe0; margin-bottom:8px;">{title}</div>
                <div style="font-size:13px; color:#5a5f6b; line-height:1.6;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)