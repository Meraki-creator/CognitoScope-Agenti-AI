import streamlit as st
from config import ASSESSMENT_TYPES, LEVELS
from cognitive_agent import generate_question
from analyzer import analyze_response

st.set_page_config(
    page_title="CognitoScope",
    page_icon="🧠"
)

# Session State Initialization
if "started" not in st.session_state:
    st.session_state.started = False

if "question" not in st.session_state:
    st.session_state.question = ""

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
        st.write("Analyzing...")
        analysis = analyze_response(answer)

        st.write("### Analysis")

        st.info(analysis)