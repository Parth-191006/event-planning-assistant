import streamlit as st
from agents.research_agent import search_venues
from agents.design_agent import generate_theme
from agents.copy_agent import generate_copy
from agents.packaging_agent import generate_report
from agents.judge_agent import evaluate_plan

# Page Config
st.set_page_config(page_title="🎓 Event Planning Assistant", page_icon="🎓", layout="wide")
st.title("🎓 Event Planning Assistant")
st.markdown("*AI-powered event planning — in one click.*")

# Initialize Session State (Memory Box)
if 'final_report' not in st.session_state:
    st.session_state.final_report = None
if 'evaluation' not in st.session_state:
    st.session_state.evaluation = None

# Sidebar Inputs
with st.sidebar:
    st.header("📋 Event Details")
    event_type = st.selectbox("Event Type", ["College Tech Fest", "Cultural Night", "Seminar", "Alumni Meet", "Other"])
    location = st.text_input("Location / City", "Austin, TX")
    budget = st.number_input("Budget ($)", min_value=100, max_value=50000, value=3000, step=100)
    guest_count = st.slider("Expected Guests", 10, 500, 150)
    theme_pref = st.selectbox("Theme Preference", ["modern", "cyberpunk", "rustic", "elegant"])
    generate_btn = st.button("🚀 Generate Event Plan", type="primary")

# Main Logic
if generate_btn:
    with st.spinner("🤖 Agents are working..."):
        
        # 1. Research
        with st.status("🔍 Researching venues...", expanded=True) as status:
            venues = search_venues(event_type, location, budget)
            status.update(label=f"✅ Found {len(venues)} venues", state="complete")
        
        # 2. Design
        with st.status("🎨 Creating theme...", expanded=True) as status:
            theme = generate_theme(venues, event_type, theme_pref)
            status.update(label="✅ Theme ready", state="complete")
        
        # 3. Copy
        with st.status("✍️ Writing copy...", expanded=True) as status:
            copy = generate_copy(venues, theme, event_type, guest_count)
            status.update(label="✅ Copy ready", state="complete")
        
        # 4. Package & Judge
        with st.status("📦 Creating report & evaluating...", expanded=True) as status:
            event_details = {
                "event_type": event_type,
                "budget": budget,
                "location": location,
                "guest_count": guest_count
            }
            
            # Generate Report
            report_text = generate_report({"venues": venues}, theme, copy, event_details)
            
            # Evaluate Report (LLM-as-Judge)
            evaluation_result = evaluate_plan(report_text, event_details)
            
            # Append Evaluation to Report
            final_output = report_text + f"""
---

## 🧠 AI Quality Evaluation

**Overall Score:** {evaluation_result['overall_score']}/10 ⭐

| Criteria | Score |
|----------|-------|
| Completeness | {evaluation_result['breakdown']['completeness']}/10 |
| Creativity | {evaluation_result['breakdown']['creativity']}/10 |
| Budget Adherence | {evaluation_result['breakdown']['budget_adherence']}/10 |
| Clarity | {evaluation_result['breakdown']['clarity']}/10 |

**Feedback:** {evaluation_result['feedback']}
"""
            
            # Save to Memory Box
            st.session_state.final_report = final_output
            st.session_state.evaluation = evaluation_result
            
            status.update(label="✅ Done!", state="complete")

# Display Results from Memory Box
if st.session_state.final_report:
    st.subheader("📄 Your Event Plan")
    st.markdown(st.session_state.final_report)
    
    st.download_button(
        label="📥 Download as Markdown",
        data=st.session_state.final_report,
        file_name=f"{event_type.replace(' ', '_').lower()}_plan.md",
        mime="text/markdown"
    )
else:
    st.info("👈 Fill in details on the left, then click **Generate Event Plan**")
    st.markdown("""
    ### How It Works:
    1. 🔍 Research Agent finds venues
    2. 🎨 Design Agent creates theme
    3. ✍️ Copy Agent writes invitations & scripts
    4. 📦 Packaging Agent combines everything
    5. 🧠 Judge Agent scores the quality
    """)