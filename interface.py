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

/* ══════════════════════════════════════
   ABOUT / BENEFITS SECTION
══════════════════════════════════════ */

.about-divider {
    display: flex;
    align-items: center;
    gap: 20px;
    margin: 72px 0 56px;
}
.about-divider-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, #1e2229, transparent);
}
.about-divider-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #3a3e48;
    white-space: nowrap;
}

/* ── About intro ── */
.about-intro {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 48px;
    align-items: center;
    margin-bottom: 64px;
    background: #0e0f12;
    border: 1px solid #1a1d23;
    border-radius: 20px;
    padding: 52px 56px;
    position: relative;
    overflow: hidden;
}
.about-intro::after {
    content: '';
    position: absolute;
    bottom: -60px; right: -60px;
    width: 260px; height: 260px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(200,164,74,0.04) 0%, transparent 70%);
    pointer-events: none;
}
.about-intro-eyebrow {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #c8a44a;
    margin-bottom: 16px;
}
.about-intro-heading {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(1.6rem, 2.4vw, 2.2rem);
    color: #f0ebe0;
    line-height: 1.2;
    margin-bottom: 20px;
    letter-spacing: -0.02em;
}
.about-intro-heading em { font-style: italic; color: #c8a44a; }
.about-intro-body {
    font-size: 14.5px;
    color: #6a6e78;
    line-height: 1.8;
    margin-bottom: 28px;
}
.about-stat-row {
    display: flex;
    gap: 32px;
}
.about-stat-num {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: #f0ebe0;
    line-height: 1;
    margin-bottom: 4px;
}
.about-stat-num span { color: #c8a44a; }
.about-stat-label {
    font-size: 11px;
    color: #4a4e58;
    font-weight: 500;
    letter-spacing: 0.04em;
}
.about-intro-visual {
    background: #111317;
    border: 1px solid #1e2229;
    border-radius: 14px;
    padding: 32px;
    position: relative;
}
.pipeline-step {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    padding: 14px 0;
    border-bottom: 1px solid #1a1d23;
    position: relative;
}
.pipeline-step:last-child { border-bottom: none; }
.pipeline-dot {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: #0c0d0f;
    border: 1px solid #2a2e38;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    flex-shrink: 0;
    margin-top: 2px;
}
.pipeline-step-title {
    font-size: 13px;
    font-weight: 600;
    color: #d8d4cc;
    margin-bottom: 3px;
}
.pipeline-step-desc {
    font-size: 12px;
    color: #4a4e58;
    line-height: 1.5;
}

/* ── Benefits grid ── */
.benefits-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 64px;
}
.benefit-card {
    background: #0e0f12;
    border: 1px solid #1a1d23;
    border-radius: 16px;
    padding: 32px 28px;
    position: relative;
    overflow: hidden;
    transition: border-color .25s, transform .2s;
}
.benefit-card:hover {
    border-color: #2a2e3a;
    transform: translateY(-2px);
}
.benefit-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse 80% 60% at 20% 0%, rgba(200,164,74,0.03) 0%, transparent 60%);
    pointer-events: none;
}
.benefit-number {
    font-family: 'DM Serif Display', serif;
    font-size: 11px;
    color: #2a2e3a;
    font-weight: 400;
    margin-bottom: 20px;
    letter-spacing: 0.1em;
}
.benefit-icon {
    font-size: 26px;
    margin-bottom: 16px;
    display: block;
}
.benefit-title {
    font-family: 'DM Serif Display', serif;
    font-size: 18px;
    color: #f0ebe0;
    margin-bottom: 10px;
    line-height: 1.25;
}
.benefit-desc {
    font-size: 13px;
    color: #4a4e58;
    line-height: 1.7;
}
.benefit-tag {
    display: inline-block;
    margin-top: 16px;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #c8a44a;
    background: rgba(200,164,74,0.08);
    border-radius: 999px;
    padding: 3px 10px;
}

/* ── Testimonial / quote strip ── */
.quote-strip {
    background: linear-gradient(135deg, #111317, #0e1018);
    border: 1px solid #1e2229;
    border-radius: 16px;
    padding: 48px 52px;
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 36px;
    align-items: center;
    margin-bottom: 64px;
    position: relative;
    overflow: hidden;
}
.quote-strip::before {
    content: '\201C';
    position: absolute;
    top: -10px; left: 36px;
    font-family: 'DM Serif Display', serif;
    font-size: 140px;
    color: #1a1e26;
    line-height: 1;
    pointer-events: none;
}
.quote-bar {
    width: 3px;
    height: 80px;
    background: linear-gradient(180deg, #c8a44a, transparent);
    border-radius: 999px;
    flex-shrink: 0;
}
.quote-text {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(1.1rem, 1.8vw, 1.4rem);
    color: #c8c4bc;
    font-style: italic;
    line-height: 1.5;
    margin-bottom: 14px;
}
.quote-author {
    font-size: 12px;
    color: #4a4e58;
    font-weight: 500;
    letter-spacing: 0.08em;
}
.quote-author span { color: #c8a44a; }

/* ── How it works ── */
.how-heading {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(1.5rem, 2.2vw, 2rem);
    color: #f0ebe0;
    text-align: center;
    margin-bottom: 8px;
    letter-spacing: -0.02em;
}
.how-sub {
    text-align: center;
    font-size: 14px;
    color: #4a4e58;
    margin-bottom: 40px;
}
.how-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 2px;
    margin-bottom: 64px;
}
.how-step {
    background: #0e0f12;
    border: 1px solid #1a1d23;
    padding: 28px 24px;
    position: relative;
    text-align: center;
}
.how-step:first-child { border-radius: 14px 0 0 14px; }
.how-step:last-child  { border-radius: 0 14px 14px 0; }
.how-step-num {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: #1e2229;
    margin-bottom: 12px;
    line-height: 1;
}
.how-step-icon { font-size: 22px; margin-bottom: 12px; display: block; }
.how-step-title {
    font-size: 13px;
    font-weight: 600;
    color: #d8d4cc;
    margin-bottom: 6px;
}
.how-step-desc { font-size: 12px; color: #3a3e48; line-height: 1.6; }
.how-arrow {
    position: absolute;
    right: -13px; top: 50%;
    transform: translateY(-50%);
    width: 24px; height: 24px;
    background: #1a1d23;
    border: 1px solid #2a2e38;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
    color: #c8a44a;
    z-index: 2;
}

/* ── Footer band ── */
.about-footer {
    border-top: 1px solid #1a1d23;
    padding-top: 36px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 16px;
    margin-bottom: 16px;
}
.about-footer-brand {
    font-family: 'DM Serif Display', serif;
    font-size: 18px;
    color: #3a3e48;
}
.about-footer-brand span { color: #c8a44a; }
.about-footer-copy {
    font-size: 12px;
    color: #2a2e38;
}
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


# ════════════════════════════════════════════════════════════════════════════
# ABOUT / BENEFITS SECTION  —  always rendered below the main content
# ════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="about-divider">
    <div class="about-divider-line"></div>
    <div class="about-divider-label">✦ About SIMKO AI</div>
    <div class="about-divider-line"></div>
</div>
""", unsafe_allow_html=True)


# ── Intro + pipeline visual ───────────────────────────────────────────────────
st.markdown("""
<div class="about-intro">
    <div>
        <div class="about-intro-eyebrow">What is SIMKO AI?</div>
        <h2 class="about-intro-heading">Your brand voice,<br><em>amplified by AI.</em></h2>
        <p class="about-intro-body">
            SIMKO AI is a multi-stage copywriting engine built specifically for e-commerce sellers.
            Unlike generic AI writing tools, it doesn't just rephrase a bullet list — it researches
            your product category, maps your audience's motivations, and crafts copy calibrated to
            your chosen brand tone before a single word reaches your screen.
        </p>
        <div class="about-stat-row">
            <div>
                <div class="about-stat-num">3<span>×</span></div>
                <div class="about-stat-label">Faster than manual writing</div>
            </div>
            <div>
                <div class="about-stat-num">6</div>
                <div class="about-stat-label">Brand tones supported</div>
            </div>
            <div>
                <div class="about-stat-num">2</div>
                <div class="about-stat-label">AI refinement passes</div>
            </div>
        </div>
    </div>
    <div class="about-intro-visual">
        <div style="font-size:10px;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:#3a3e48;margin-bottom:20px;">AI Pipeline</div>
        <div class="pipeline-step">
            <div class="pipeline-dot">🔍</div>
            <div>
                <div class="pipeline-step-title">Research Node</div>
                <div class="pipeline-step-desc">Analyses category trends, competitor positioning, and audience psychology.</div>
            </div>
        </div>
        <div class="pipeline-step">
            <div class="pipeline-dot">✍️</div>
            <div>
                <div class="pipeline-step-title">Draft Agent</div>
                <div class="pipeline-step-desc">Produces a structured first-pass using research insights and brand tone.</div>
            </div>
        </div>
        <div class="pipeline-step">
            <div class="pipeline-dot">✨</div>
            <div>
                <div class="pipeline-step-title">Refinement Agent</div>
                <div class="pipeline-step-desc">Polishes flow, strengthens hooks, and weaves in SEO signals.</div>
            </div>
        </div>
        <div class="pipeline-step">
            <div class="pipeline-dot">📋</div>
            <div>
                <div class="pipeline-step-title">Output Formatter</div>
                <div class="pipeline-step-desc">Delivers publish-ready copy with the draft and research for transparency.</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Benefits grid ─────────────────────────────────────────────────────────────
benefits = [
    ("✦", "01", "SEO-Optimised by Default",
     "Every description is structured around searchability — naturally incorporating high-intent keywords without keyword stuffing, so your listings rank and convert.",
     "Organic Traffic"),
    ("🎯", "02", "Audience-Aware Copy",
     "Specify your target demographic and the AI shifts its vocabulary, emotional hooks, and pain-point framing to speak directly to the people most likely to buy.",
     "Higher Relevance"),
    ("🎨", "03", "Six Distinct Brand Tones",
     "From Luxury to Rugged to Playful — each tone mode is a distinct writing personality, not just a style tweak. Your brand voice stays consistent across every listing.",
     "Brand Consistency"),
    ("⚡", "04", "Two-Stage AI Refinement",
     "A first draft is always improved by a second agent pass that tightens structure, sharpens the headline hook, and removes filler — so you never publish a first draft.",
     "Higher Quality"),
    ("🔍", "05", "Full Research Transparency",
     "See exactly what insights the AI used to build your copy. Understand the 'why' behind every word — and use those notes to brief your wider marketing team.",
     "Explainable AI"),
    ("🚀", "06", "Instant, Scalable Output",
     "Generate polished descriptions in under 30 seconds. Whether you're listing one product or a hundred, the pipeline scales without losing quality or consistency.",
     "Time Savings"),
]

st.markdown('<div class="benefits-grid">', unsafe_allow_html=True)
for (icon, num, title, desc, tag) in benefits:
    st.markdown(f"""
    <div class="benefit-card">
        <div class="benefit-number">{num}</div>
        <span class="benefit-icon">{icon}</span>
        <div class="benefit-title">{title}</div>
        <div class="benefit-desc">{desc}</div>
        <span class="benefit-tag">{tag}</span>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# ── Quote strip ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="quote-strip">
    <div class="quote-bar"></div>
    <div>
        <div class="quote-text">
            Good product copy doesn't describe what something is — it articulates what life
            looks like when you own it. That's the brief we gave the AI, and it's the standard
            every description is held to.
        </div>
        <div class="quote-author">The SIMKO AI team &nbsp;·&nbsp; <span>Built for sellers who take copy seriously</span></div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── How it works ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="how-heading">How it works</div>
<div class="how-sub">Four steps from product details to publish-ready copy</div>
<div class="how-grid">
    <div class="how-step">
        <div class="how-step-num">01</div>
        <span class="how-step-icon">📝</span>
        <div class="how-step-title">Enter Product Details</div>
        <div class="how-step-desc">Name, category, audience, tone, and key features — takes under a minute.</div>
        <div class="how-arrow">→</div>
    </div>
    <div class="how-step">
        <div class="how-step-num">02</div>
        <span class="how-step-icon">🔍</span>
        <div class="how-step-title">AI Researches</div>
        <div class="how-step-desc">The research node maps audience psychology and category positioning.</div>
        <div class="how-arrow">→</div>
    </div>
    <div class="how-step">
        <div class="how-step-num">03</div>
        <span class="how-step-icon">✍️</span>
        <div class="how-step-title">Draft & Refine</div>
        <div class="how-step-desc">Two AI agents collaborate — one drafts, one refines for tone and SEO.</div>
        <div class="how-arrow">→</div>
    </div>
    <div class="how-step">
        <div class="how-step-num">04</div>
        <span class="how-step-icon">🚀</span>
        <div class="how-step-title">Copy & Publish</div>
        <div class="how-step-desc">Your final description is ready to paste directly into any listing platform.</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Footer band ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="about-footer">
    <div class="about-footer-brand">SIMKO <span>AI</span></div>
    <div class="about-footer-copy">AI-powered copy for serious e-commerce sellers &nbsp;·&nbsp; Powered by multi-agent AI</div>
</div>
""", unsafe_allow_html=True)