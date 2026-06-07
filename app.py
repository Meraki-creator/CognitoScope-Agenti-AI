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

# Session State Initialization
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

st.title("🧠 CognitoScope")
st.subheader("Reasoning Intelligence Engine")

assessment = st.selectbox(
    "Choose Assessment Type",
    ASSESSMENT_TYPES
)

level = st.selectbox(
    "Choose Experience Level",
    LEVELS
)

if st.button("Start Assessment"):

    st.session_state.started = True

    st.session_state.question = generate_question(
        assessment
    )

# Show assessment screen if started
if st.session_state.started:

    st.write("### Assessment Started")

    st.info(
        st.session_state.question
    )

    answer = st.text_area(
        "Your Response"
    )

    if st.button("Submit Answer"):

        st.success(
            "Response Recorded"
        )

        st.write(
            "Your Answer:"
        )

        st.write(answer)

        analysis = analyze_response(
            answer
        )

        st.write("### Analysis")

        st.info(
            analysis
        )

        st.session_state.answers.append(
            answer
        )

        st.session_state.analyses.append(
            analysis
        )

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
            "### Follow-up Question"
        )

        st.warning(
            st.session_state.followup
        )
        st.write("---")

if st.button("Generate Cognitive Profile"):

    profile = generate_profile(
        st.session_state.answers
    )

    st.write("## Cognitive Profile")

    st.success(profile)