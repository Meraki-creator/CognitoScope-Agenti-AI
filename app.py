import streamlit as st
from config import ASSESSMENT_TYPES, LEVELS
from cognitive_agent import generate_question
from analyzer import analyze_response
from followup_generator import generate_followup
from profile_generator import generate_profile

st.set_page_config(
    page_title="CognitoScope",
    page_icon="🧠"
)

# Session State
if "started" not in st.session_state:
    st.session_state.started = False

if "question" not in st.session_state:
    st.session_state.question = ""

if "answers" not in st.session_state:
    st.session_state.answers = []

if "analyses" not in st.session_state:
    st.session_state.analyses = []

if "followup" not in st.session_state:
    st.session_state.followup = ""

if "question_count" not in st.session_state:
    st.session_state.question_count = 0

if "show_continue" not in st.session_state:
    st.session_state.show_continue = False

# Header
st.title("🧠 CognitoScope")
st.markdown(
    "### AI-Powered Cognitive Assessment Platform"
)
st.markdown("""
<style>

/* ===== Background ===== */

.stApp {

    background:
    radial-gradient(
        circle at 50% 15%,
        rgba(0,180,255,0.10),
        transparent 35%
    ),

    radial-gradient(
        circle at 90% 90%,
        rgba(255,255,255,0.03),
        transparent 30%
    ),

    #05070A;

    color: white;
}

/* Hide Streamlit Header */

header {
    visibility: hidden;
}

/* ===== Main Card ===== */

.hero-card {

    max-width: 850px;
    margin: 40px auto;

    padding: 50px;

    border-radius: 24px;

    background:
    rgba(255,255,255,0.03);

    backdrop-filter: blur(18px);

    border:
    1px solid rgba(255,255,255,0.08);

    box-shadow:
    0 0 50px rgba(0,180,255,0.05);
}

/* ===== Main Title ===== */

.hero-title {

    text-align: center;

    font-size: 5rem;

    font-weight: 800;

    letter-spacing: 10px;

    margin-bottom: 10px;

    color: white;
}

/* ===== Subtitle ===== */

.hero-tagline {

    text-align: center;

    font-size: 1.1rem;

    letter-spacing: 4px;

    color: #9ca3af;

    margin-bottom: 50px;
}

/* ===== Divider ===== */

.hero-line {

    width: 120px;

    height: 2px;

    background: rgba(255,255,255,0.15);

    margin: auto;

    margin-bottom: 30px;
}

/* ===== Buttons ===== */

.stButton > button {

    width: 100%;

    height: 55px;

    border-radius: 16px;

    background:
    rgba(255,255,255,0.04);

    color: white;

    border:
    1px solid rgba(255,255,255,0.08);

    transition: 0.3s;
}

.stButton > button:hover {

    transform:
    translateY(-3px);

    border:
    1px solid rgba(0,180,255,0.4);

    box-shadow:
    0 0 25px rgba(0,180,255,0.25);
}

</style>

<div class="hero-card">


<div class="hero-line"></div>

<div class="hero-tagline">
OBSERVE • REASON • EVOLVE
</div>

</div>

""", unsafe_allow_html=True)

assessment = st.selectbox(
    "Select Cognitive Domain",
    ASSESSMENT_TYPES
)

level = st.selectbox(
    "Calibration Level",
    LEVELS
)

# Start Assessment
if st.button("Initiate Cognitive Scan"):

    st.session_state.started = True

    st.session_state.question_count = 0
    st.session_state.answers = []
    st.session_state.analyses = []
    st.session_state.followup = ""
    st.session_state.show_continue = False

    st.session_state.question = generate_question(
        assessment
    )

# Assessment Screen
if st.session_state.started:

    st.write("### Cognitive Scan Active")

    st.write(
        f"Round {st.session_state.question_count + 1}/3"
    )

    st.progress(
        st.session_state.question_count / 3
    )

    st.info(
        st.session_state.question
    )

    answer = st.text_area(
        "Your Response"
    )

    if st.button("Submit Answer"):

        if not answer.strip():

            st.error(
                "Please enter a response."
            )

            st.stop()

        st.success(
            "Response Recorded"
        )

        st.write(
            "### Your Answer"
        )

        st.write(answer)

        with st.spinner(
            "Analyzing reasoning..."
        ):

            analysis = analyze_response(
                answer
            )

        st.write(
            "### Reasoning Analysis"
        )

        st.info(
            analysis
        )

        st.session_state.answers.append(
            answer
        )

        st.session_state.analyses.append(
            analysis
        )

        st.session_state.question_count += 1

        if st.session_state.question_count < 3:

            with st.spinner(
                "Generating follow-up..."
            ):

                try:

                    followup = generate_followup(
                        st.session_state.question,
                        answer
                    )

                except Exception:

                    followup = (
                        "Follow-up unavailable right now."
                    )

            st.session_state.followup = (
                followup
            )

            st.write(
                "### Neural Probe"
            )

            st.warning(
                st.session_state.followup
            )

            st.session_state.show_continue = True

        else:

            st.success(
                "Assessment Complete!"
            )

# Continue Button
if (
    st.session_state.started
    and st.session_state.show_continue
    and st.session_state.question_count < 3
):

    if st.button(
        "Continue to Next Round"
    ):

        st.session_state.question = (
            st.session_state.followup
        )

        st.session_state.show_continue = False

        st.rerun()

# Assessment Summary
if st.session_state.question_count >= 3:

    st.write("## Assessment Summary")

    for i, answer in enumerate(
        st.session_state.answers,
        start=1
    ):

        st.write(
            f"**Round {i}:**"
        )

        st.write(answer)

# Profile Generation
if st.session_state.question_count >= 3:

    if st.button(
        "Generate Cognitive Profile"
    ):

        with st.spinner(
            "Generating profile..."
        ):

            profile = generate_profile(
                st.session_state.answers
            )

        st.write(
            "## Cognitive Profile"
        )

        st.markdown(
            profile
        )

        report = f"""
COGNITOSCOPE REPORT

Answers:

{chr(10).join(st.session_state.answers)}

--------------------------------

{profile}
"""

        st.download_button(
            label="Download Cognitive Report",
            data=report,
            file_name="cognitoscope_report.txt",
            mime="text/plain"
        )

# Restart Assessment
if st.button(
    "Start New Assessment"
):

    st.session_state.started = False
    st.session_state.question = ""
    st.session_state.answers = []
    st.session_state.analyses = []
    st.session_state.followup = ""
    st.session_state.question_count = 0
    st.session_state.show_continue = False

    st.rerun()