import streamlit as st
from agents.research_agent import search_venues
from agents.design_agent import generate_theme
from agents.copy_agent import generate_copy
from agents.packaging_agent import generate_report
from agents.judge_agent import evaluate_plan

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EventForge AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap');

/* ── Root & Base ── */
:root {
    --bg:        #0a0a0f;
    --bg2:       #111118;
    --bg3:       #18181f;
    --border:    rgba(255,255,255,0.07);
    --border-hi: rgba(255,255,255,0.14);
    --accent:    #7c6aff;
    --accent2:   #ff6a9b;
    --accent3:   #6affcb;
    --text:      #e8e8f0;
    --muted:     #7a7a94;
    --radius:    14px;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2rem 2.5rem 4rem !important;
    max-width: 1400px !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .block-container {
    padding: 2rem 1.5rem !important;
}

/* ── Hero Header ── */
.hero {
    display: flex;
    align-items: flex-start;
    gap: 1.5rem;
    margin-bottom: 2.5rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid var(--border);
}
.hero-badge {
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    color: #fff;
    font-family: 'Syne', sans-serif;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.3rem 0.8rem;
    border-radius: 100px;
    display: inline-block;
    margin-bottom: 0.75rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: 3rem !important;
    font-weight: 800 !important;
    line-height: 1.05 !important;
    letter-spacing: -0.03em !important;
    color: #fff !important;
    margin: 0 0 0.5rem !important;
}
.hero h1 span {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero p {
    color: var(--muted);
    font-size: 1.05rem;
    font-weight: 300;
    line-height: 1.6;
    margin: 0;
    max-width: 520px;
}

/* ── Sidebar section label ── */
.sidebar-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 1.5rem 0 0.6rem;
}

/* ── Cards ── */
.card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}
.card:hover { border-color: var(--border-hi); }

/* ── Score Cards ── */
.score-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem;
    margin: 1.2rem 0;
}
.score-card {
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 0.75rem;
    text-align: center;
}
.score-card .score-num {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.score-card .score-label {
    font-size: 0.7rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
.score-high  { color: var(--accent3); }
.score-mid   { color: #ffd166; }
.score-low   { color: var(--accent2); }

/* ── Overall score banner ── */
.overall-score {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    background: linear-gradient(135deg, rgba(124,106,255,0.12), rgba(255,106,155,0.08));
    border: 1px solid rgba(124,106,255,0.25);
    border-radius: var(--radius);
    padding: 1.25rem 1.5rem;
    margin-bottom: 1.2rem;
}
.overall-score .big-num {
    font-family: 'Syne', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    line-height: 1;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.overall-score .score-meta h4 {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #fff;
    margin: 0 0 0.2rem;
}
.overall-score .score-meta p {
    font-size: 0.85rem;
    color: var(--muted);
    margin: 0;
    line-height: 1.5;
}

/* ── Step indicators ── */
.step-row {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 0.5rem;
}
.step-dot {
    width: 28px; height: 28px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    flex-shrink: 0;
}
.step-dot.done { background: var(--accent3); color: #000; }
.step-dot.active { background: var(--accent); color: #fff; }
.step-dot.idle { background: var(--bg3); color: var(--muted); border: 1px solid var(--border); }

/* ── Generate button ── */
div[data-testid="stButton"] > button {
    width: 100%;
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%) !important;
    color: #fff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.05em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 1.5rem !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.1s !important;
    margin-top: 0.5rem !important;
}
div[data-testid="stButton"] > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
div[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* ── Inputs ── */
div[data-testid="stSelectbox"] > div,
div[data-testid="stTextInput"] > div > div,
div[data-testid="stNumberInput"] > div {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}
div[data-testid="stSelectbox"] > div:focus-within,
div[data-testid="stTextInput"] > div > div:focus-within {
    border-color: var(--accent) !important;
}

/* ── Slider ── */
div[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
    background: var(--accent) !important;
    border-color: var(--accent) !important;
}

/* ── Download button ── */
div[data-testid="stDownloadButton"] > button {
    background: var(--bg3) !important;
    border: 1px solid var(--border-hi) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    border-radius: 8px !important;
    transition: border-color 0.2s !important;
}
div[data-testid="stDownloadButton"] > button:hover {
    border-color: var(--accent) !important;
    color: #fff !important;
}

/* ── Status/Spinner ── */
div[data-testid="stStatusWidget"] {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
}

/* ── Markdown output ── */
.output-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 2rem 2.5rem;
    margin-top: 1.5rem;
}
.output-card h1, .output-card h2, .output-card h3 {
    font-family: 'Syne', sans-serif !important;
    color: #fff !important;
}
.output-card h2 {
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.5rem;
    margin-top: 2rem;
}
.output-card table {
    width: 100%;
    border-collapse: collapse;
}
.output-card td, .output-card th {
    padding: 0.6rem 1rem;
    border: 1px solid var(--border);
    font-size: 0.9rem;
}
.output-card th {
    background: var(--bg3);
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted);
}

/* ── Tabs ── */
div[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: var(--bg2) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    border: 1px solid var(--border) !important;
    gap: 4px !important;
}
div[data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 7px !important;
    color: var(--muted) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
    padding: 0.4rem 1rem !important;
}
div[data-testid="stTabs"] [aria-selected="true"] {
    background: var(--bg3) !important;
    color: #fff !important;
}

/* ── Info box ── */
.info-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(124,106,255,0.1);
    border: 1px solid rgba(124,106,255,0.2);
    border-radius: 100px;
    padding: 0.3rem 0.8rem;
    font-size: 0.78rem;
    color: #a89fff;
    margin-bottom: 0.5rem;
}

/* ── Color palette display ── */
.palette {
    display: flex;
    gap: 0.4rem;
    margin: 0.75rem 0;
}
.swatch {
    width: 32px; height: 32px;
    border-radius: 6px;
    border: 1px solid rgba(255,255,255,0.1);
    display: inline-block;
    cursor: pointer;
    transition: transform 0.15s;
}
.swatch:hover { transform: scale(1.15); }

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1.5rem 0 !important;
}

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 5rem 2rem;
    color: var(--muted);
}
.empty-state .icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    opacity: 0.4;
}
.empty-state h3 {
    font-family: 'Syne', sans-serif;
    font-size: 1.2rem;
    color: var(--text);
    margin-bottom: 0.5rem;
}
.empty-state p {
    font-size: 0.9rem;
    line-height: 1.6;
    max-width: 380px;
    margin: 0 auto;
}

/* ── How it works steps ── */
.how-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0.75rem;
    margin-top: 2rem;
}
.how-card {
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}
.how-card .num {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    color: var(--accent);
    margin-bottom: 0.3rem;
}
.how-card .how-title {
    font-size: 0.78rem;
    font-weight: 500;
    color: #fff;
    margin-bottom: 0.2rem;
}
.how-card .how-sub {
    font-size: 0.7rem;
    color: var(--muted);
    line-height: 1.4;
}
</style>
""", unsafe_allow_html=True)

# ── Session State ─────────────────────────────────────────────────────────────
if "final_report" not in st.session_state:
    st.session_state.final_report = None
if "evaluation" not in st.session_state:
    st.session_state.evaluation = None
if "theme_data" not in st.session_state:
    st.session_state.theme_data = None
if "venues_data" not in st.session_state:
    st.session_state.venues_data = None
if "event_meta" not in st.session_state:
    st.session_state.event_meta = None

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <div style="font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:800;color:#fff;letter-spacing:-0.02em;">
            EventForge <span style="color:#7c6aff;">AI</span>
        </div>
        <div style="font-size:0.75rem;color:#7a7a94;margin-top:0.2rem;">Multi-agent event planner</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-label">Event Details</div>', unsafe_allow_html=True)

    event_type = st.selectbox(
        "Event Type",
        ["College Tech Fest", "Cultural Night", "Seminar", "Alumni Meet", "Other"],
        label_visibility="collapsed"
    )

    st.markdown('<div class="sidebar-label">Location</div>', unsafe_allow_html=True)
    location = st.text_input("Location", "Austin, TX", label_visibility="collapsed")

    st.markdown('<div class="sidebar-label">Budget (USD)</div>', unsafe_allow_html=True)
    budget = st.number_input("Budget", min_value=100, max_value=50000, value=3000, step=100, label_visibility="collapsed")

    st.markdown('<div class="sidebar-label">Expected Guests</div>', unsafe_allow_html=True)
    guest_count = st.slider("Guests", 10, 500, 150, label_visibility="collapsed")

    st.markdown('<div class="sidebar-label">Theme Preference</div>', unsafe_allow_html=True)
    theme_pref = st.selectbox(
        "Theme",
        ["modern", "cyberpunk", "rustic", "elegant"],
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    generate_btn = st.button("Generate Event Plan →", type="primary")

    # Quick summary
    if generate_btn or st.session_state.final_report:
        st.markdown("---")
        st.markdown(f"""
        <div style="font-size:0.78rem;color:#7a7a94;line-height:1.8;">
            <div>📌 <b style="color:#e8e8f0;">{event_type}</b></div>
            <div>📍 {location}</div>
            <div>💰 ${budget:,}</div>
            <div>👥 {guest_count} guests</div>
            <div>🎨 {theme_pref.capitalize()} theme</div>
        </div>
        """, unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div>
        <div class="hero-badge">AI-Powered · Multi-Agent</div>
        <h1>Plan your event with <span>intelligence</span></h1>
        <p>Five specialized AI agents collaborate to research venues, design themes, write copy, build budgets, and evaluate quality — in one click.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Pipeline Run ──────────────────────────────────────────────────────────────
if generate_btn:
    st.session_state.final_report = None
    st.session_state.evaluation = None
    st.session_state.theme_data = None
    st.session_state.venues_data = None

    with st.spinner(""):
        col_prog, col_info = st.columns([2, 1])

        with col_prog:
            # Step 1
            with st.status("🔍  Research Agent — finding venues...", expanded=False) as s:
                venues = search_venues(event_type, location, budget)
                st.session_state.venues_data = venues
                s.update(label=f"✅  Research Agent — found {len(venues)} venue(s)", state="complete")

            # Step 2
            with st.status("🎨  Design Agent — generating theme...", expanded=False) as s:
                theme = generate_theme(venues, event_type, theme_pref)
                st.session_state.theme_data = theme
                s.update(label="✅  Design Agent — theme ready", state="complete")

            # Step 3
            with st.status("✍️  Copy Agent — writing content...", expanded=False) as s:
                copy = generate_copy(venues, theme, event_type, guest_count)
                s.update(label="✅  Copy Agent — content ready", state="complete")

            # Step 4
            with st.status("📦  Packaging Agent — assembling report...", expanded=False) as s:
                event_details = {
                    "event_type": event_type,
                    "budget": budget,
                    "location": location,
                    "guest_count": guest_count
                }
                st.session_state.event_meta = event_details
                report_text = generate_report({"venues": venues}, theme, copy, event_details)
                s.update(label="✅  Packaging Agent — report assembled", state="complete")

            # Step 5
            with st.status("🧠  Judge Agent — evaluating quality...", expanded=False) as s:
                evaluation = evaluate_plan(report_text, event_details)
                score = evaluation.get("overall_score", 0)
                final_output = report_text + f"""

---

## 🧠 AI Quality Evaluation

**Overall Score:** {score}/10 ⭐

| Criteria | Score |
|----------|-------|
| Completeness | {evaluation['breakdown']['completeness']}/10 |
| Creativity | {evaluation['breakdown']['creativity']}/10 |
| Budget Adherence | {evaluation['breakdown']['budget_adherence']}/10 |
| Clarity | {evaluation['breakdown']['clarity']}/10 |

**Feedback:** {evaluation['feedback']}
"""
                st.session_state.final_report = final_output
                st.session_state.evaluation = evaluation
                s.update(label=f"✅  Judge Agent — scored {score}/10", state="complete")

# ── Output Area ───────────────────────────────────────────────────────────────
if st.session_state.final_report:
    ev = st.session_state.evaluation or {}
    breakdown = ev.get("breakdown", {})
    score = ev.get("overall_score", 0)
    meta = st.session_state.event_meta or {}
    theme_d = st.session_state.theme_data or {}
    venues_d = st.session_state.venues_data or []

    def score_class(n):
        if n >= 8: return "score-high"
        if n >= 6: return "score-mid"
        return "score-low"

    # ── Top metric strip ──
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="card" style="text-align:center;padding:1rem;">
            <div style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;color:#fff;">
                {len(venues_d)}
            </div>
            <div style="font-size:0.72rem;color:#7a7a94;text-transform:uppercase;letter-spacing:0.1em;">Venues Found</div>
        </div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="card" style="text-align:center;padding:1rem;">
            <div style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;color:#fff;">
                ${meta.get('budget',0):,}
            </div>
            <div style="font-size:0.72rem;color:#7a7a94;text-transform:uppercase;letter-spacing:0.1em;">Total Budget</div>
        </div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="card" style="text-align:center;padding:1rem;">
            <div style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;color:#fff;">
                {meta.get('guest_count',0)}
            </div>
            <div style="font-size:0.72rem;color:#7a7a94;text-transform:uppercase;letter-spacing:0.1em;">Guests</div>
        </div>""", unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="card" style="text-align:center;padding:1rem;">
            <div style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;
                background:linear-gradient(135deg,#7c6aff,#ff6a9b);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
                {score}/10
            </div>
            <div style="font-size:0.72rem;color:#7a7a94;text-transform:uppercase;letter-spacing:0.1em;">AI Score</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tabs ──
    tab_plan, tab_score, tab_theme = st.tabs(["📄  Full Plan", "🧠  Quality Report", "🎨  Theme Preview"])

    # ── Tab 1: Full Plan ──
    with tab_plan:
        left, right = st.columns([3, 1])
        with left:
            st.markdown('<div class="output-card">', unsafe_allow_html=True)
            st.markdown(st.session_state.final_report)
            st.markdown('</div>', unsafe_allow_html=True)
        with right:
            st.markdown("""
            <div class="card">
                <div style="font-family:'Syne',sans-serif;font-size:0.8rem;font-weight:700;
                     color:#fff;margin-bottom:0.8rem;letter-spacing:0.05em;">EXPORT</div>
            """, unsafe_allow_html=True)
            st.download_button(
                label="⬇  Download as Markdown",
                data=st.session_state.final_report,
                file_name=f"{event_type.replace(' ','_').lower()}_plan.md",
                mime="text/markdown"
            )
            st.markdown("</div>", unsafe_allow_html=True)

            # Venue list card
            if venues_d:
                st.markdown("""
                <div class="card" style="margin-top:0.75rem;">
                    <div style="font-family:'Syne',sans-serif;font-size:0.8rem;font-weight:700;
                         color:#fff;margin-bottom:0.8rem;letter-spacing:0.05em;">VENUES</div>
                """, unsafe_allow_html=True)
                for v in venues_d[:3]:
                    name = v.get("name", "Venue")
                    addr = v.get("address", "")
                    st.markdown(f"""
                    <div style="padding:0.5rem 0;border-bottom:1px solid var(--border);">
                        <div style="font-size:0.82rem;font-weight:500;color:#fff;">{name}</div>
                        <div style="font-size:0.72rem;color:#7a7a94;">{addr}</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 2: Quality Report ──
    with tab_score:
        st.markdown(f"""
        <div class="overall-score">
            <div class="big-num">{score}<span style="font-size:1.2rem;font-weight:400;color:#7a7a94;">/10</span></div>
            <div class="score-meta">
                <h4>Overall Quality Score</h4>
                <p>{ev.get('feedback','No feedback available.')}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        c = breakdown
        st.markdown(f"""
        <div class="score-grid">
            <div class="score-card">
                <div class="score-num {score_class(c.get('completeness',0))}">{c.get('completeness',0)}</div>
                <div class="score-label">Completeness</div>
            </div>
            <div class="score-card">
                <div class="score-num {score_class(c.get('creativity',0))}">{c.get('creativity',0)}</div>
                <div class="score-label">Creativity</div>
            </div>
            <div class="score-card">
                <div class="score-num {score_class(c.get('budget_adherence',0))}">{c.get('budget_adherence',0)}</div>
                <div class="score-label">Budget Adherence</div>
            </div>
            <div class="score-card">
                <div class="score-num {score_class(c.get('clarity',0))}">{c.get('clarity',0)}</div>
                <div class="score-label">Clarity</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Score bar chart using Streamlit native
        st.markdown("<br>", unsafe_allow_html=True)
        import pandas as pd
        chart_data = pd.DataFrame({
            "Criteria": ["Completeness", "Creativity", "Budget Adherence", "Clarity"],
            "Score": [
                c.get("completeness", 0),
                c.get("creativity", 0),
                c.get("budget_adherence", 0),
                c.get("clarity", 0)
            ]
        })
        st.bar_chart(chart_data.set_index("Criteria"), color="#7c6aff", height=260)

    # ── Tab 3: Theme Preview ──
    with tab_theme:
        if theme_d:
            st.markdown(f"""
            <div class="card">
                <div style="font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:800;
                     color:#fff;margin-bottom:0.25rem;">{theme_d.get('theme_name','Theme')}</div>
                <div style="font-size:0.85rem;color:#7a7a94;margin-bottom:1rem;">
                    {', '.join(theme_d.get('mood_keywords', []))}
                </div>
            """, unsafe_allow_html=True)

            colors = theme_d.get("color_palette", [])
            if colors:
                swatches = "".join(
                    f'<span class="swatch" style="background:{c};" title="{c}"></span>'
                    for c in colors
                )
                st.markdown(f'<div class="palette">{swatches}</div>', unsafe_allow_html=True)
                hex_row = " · ".join(f'<code style="font-size:0.75rem;color:#7a7a94;">{c}</code>' for c in colors)
                st.markdown(f'<div style="margin-top:0.3rem;">{hex_row}</div>', unsafe_allow_html=True)

            layout = theme_d.get("layout_suggestion", "")
            if layout:
                st.markdown(f"""
                <div style="margin-top:1.2rem;padding:1rem;background:var(--bg3);
                     border-radius:8px;border:1px solid var(--border);">
                    <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.12em;
                         color:#7a7a94;margin-bottom:0.4rem;">Layout Suggestion</div>
                    <div style="font-size:0.9rem;color:#e8e8f0;line-height:1.6;">{layout}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

            # Color preview banner
            if colors and len(colors) >= 3:
                gradient = f"linear-gradient(135deg, {', '.join(colors)})"
                st.markdown(f"""
                <div style="height:120px;border-radius:12px;background:{gradient};
                     margin-top:1rem;border:1px solid var(--border);"></div>
                """, unsafe_allow_html=True)
        else:
            st.info("Generate a plan first to see the theme preview.")

else:
    # ── Empty State ───────────────────────────────────────────────────────────
    st.markdown("""
    <div class="empty-state">
        <div class="icon">🎯</div>
        <h3>Your event plan will appear here</h3>
        <p>Fill in the details on the left sidebar and click <strong>Generate Event Plan</strong> to get started.</p>
    </div>
    """, unsafe_allow_html=True)

    # How it works
    st.markdown("""
    <div style="margin-top:1rem;">
        <div style="font-family:'Syne',sans-serif;font-size:0.65rem;font-weight:700;
             letter-spacing:0.18em;text-transform:uppercase;color:#7a7a94;margin-bottom:1rem;">
            How it works
        </div>
        <div class="how-grid">
            <div class="how-card">
                <div class="num">01</div>
                <div class="how-title">Research</div>
                <div class="how-sub">Tavily finds real venues near you</div>
            </div>
            <div class="how-card">
                <div class="num">02</div>
                <div class="how-title">Design</div>
                <div class="how-sub">Gemini generates your visual theme</div>
            </div>
            <div class="how-card">
                <div class="num">03</div>
                <div class="how-title">Copy</div>
                <div class="how-sub">Invitations, scripts & social posts</div>
            </div>
            <div class="how-card">
                <div class="num">04</div>
                <div class="how-title">Package</div>
                <div class="how-sub">Budget breakdown + full report</div>
            </div>
            <div class="how-card">
                <div class="num">05</div>
                <div class="how-title">Evaluate</div>
                <div class="how-sub">AI scores the plan quality</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)