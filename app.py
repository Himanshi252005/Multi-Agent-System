import io
import sys

import streamlit as st

from pipeline import run_research_pipeline

st.set_page_config(
    page_title="Research Assistant",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ----------------------------------------------------------------------------
# Style — dark base, bold gradient headline, glowing bright accents
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stMarkdown, p, span, div {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    #MainMenu, header, footer { visibility: hidden; }

    .stApp {
        background: radial-gradient(circle at 20% 0%, #14121f 0%, #0a0a0d 45%);
        color: #eaeaea;
    }

    .block-container {
        max-width: 780px;
        padding-top: 2.5rem;
        padding-bottom: 8rem;
    }

    /* ---------------- Header ---------------- */
    .app-header {
        display: flex;
        align-items: center;
        gap: 0.7rem;
        margin-bottom: 0.4rem;
    }
    .app-header .mark {
        width: 34px;
        height: 34px;
        border-radius: 10px;
        background: linear-gradient(135deg, #4f6dff 0%, #b24fff 60%, #ff4fd8 100%);
        box-shadow: 0 0 24px rgba(124, 92, 255, 0.55);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
    }
    .app-header .brand {
        font-size: 1.05rem;
        font-weight: 700;
        letter-spacing: -0.01em;
        color: #f4f4f2;
    }

    /* ---------------- Hero ---------------- */
    .hero {
        padding: 3.2rem 0 2.6rem 0;
    }
    .hero .headline {
        font-size: 2.6rem;
        font-weight: 800;
        line-height: 1.12;
        letter-spacing: -0.02em;
        margin-bottom: 0.7rem;
        background: linear-gradient(100deg, #7c9bff 0%, #c07cff 45%, #ff7cd6 90%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero .subtext {
        font-size: 1.05rem;
        color: #9b9ba3;
        max-width: 32ch;
        line-height: 1.5;
    }

    /* ---------------- Chat bubbles ---------------- */
    div[class*="st-key-bubble-user"] {
        background: linear-gradient(135deg, #4f6dff 0%, #8a4fff 100%);
        color: #fdfdff;
        border-radius: 18px 18px 4px 18px;
        padding: 0.85rem 1.15rem;
        max-width: 76%;
        margin-left: auto;
        margin-bottom: 0.35rem;
        box-shadow: 0 4px 24px rgba(79, 109, 255, 0.25);
    }
    div[class*="st-key-bubble-user"] p {
        color: #fdfdff;
        margin: 0;
    }

    div[class*="st-key-bubble-assistant"] {
        background: #17161d;
        border: 1px solid #2a2933;
        color: #eaeaea;
        border-radius: 18px 18px 18px 4px;
        padding: 1.05rem 1.25rem;
        max-width: 84%;
        margin-right: auto;
        margin-bottom: 0.6rem;
    }
    div[class*="st-key-bubble-assistant"] p,
    div[class*="st-key-bubble-assistant"] li {
        color: #e2e2e6;
        line-height: 1.65;
    }
    div[class*="st-key-bubble-assistant"] h1,
    div[class*="st-key-bubble-assistant"] h2,
    div[class*="st-key-bubble-assistant"] h3 {
        color: #f4f4f2;
        font-weight: 700;
    }

    .meta-row {
        display: flex;
        gap: 0.5rem;
        margin: 0 0 1.6rem 0;
        max-width: 84%;
    }

    /* ---------------- Log box ---------------- */
    .log-box {
        background-color: #121116;
        border: 1px solid #26252d;
        border-radius: 10px;
        padding: 0.9rem 1rem;
        font-family: 'SFMono-Regular', Consolas, monospace;
        font-size: 0.76rem;
        line-height: 1.55;
        color: #9c9ba3;
        max-height: 260px;
        overflow-y: auto;
        white-space: pre-wrap;
    }

    /* ---------------- Expander ---------------- */
    [data-testid="stExpander"] {
        border: 1px solid #26252d;
        border-radius: 10px;
        background-color: #121116;
    }
    [data-testid="stExpander"] summary {
        color: #b7b6c0;
        font-size: 0.82rem;
        font-weight: 600;
    }

    /* ---------------- Chat input ---------------- */
    [data-testid="stChatInput"] {
        background-color: #16151b;
        border: 1.5px solid #2f2e38;
        border-radius: 28px;
        transition: box-shadow 0.15s ease, border-color 0.15s ease;
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: #8a4fff;
        box-shadow: 0 0 0 4px rgba(138, 79, 255, 0.18);
    }
    [data-testid="stChatInput"] textarea {
        color: #f0f0f2 !important;
        font-size: 0.97rem;
    }
    [data-testid="stBottomBlockContainer"] {
        background: linear-gradient(180deg, rgba(10,10,13,0) 0%, #0a0a0d 45%);
        max-width: 780px;
    }

    /* ---------------- Buttons ---------------- */
    .stButton button {
        background-color: transparent;
        border: 1px solid #2f2e38;
        color: #b7b6c0;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 500;
        padding: 0.35rem 1rem;
        transition: border-color 0.15s ease, color 0.15s ease;
    }
    .stButton button:hover {
        border-color: #8a4fff;
        color: #f4f4f2;
    }

    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-thumb { background: #2a2933; border-radius: 8px; }
    ::-webkit-scrollbar-track { background: transparent; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# State
# ----------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------------
left, right = st.columns([5, 1])
with left:
    st.markdown(
        """
        <div class="app-header">
            <div class="mark">✨</div>
            <div class="brand">Research Assistant</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with right:
    if st.button("New chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ----------------------------------------------------------------------------
# Hero (empty state)
# ----------------------------------------------------------------------------
if not st.session_state.messages:
    st.markdown(
        """
        <div class="hero">
            <div class="headline">What should<br>I research?</div>
            <div class="subtext">Give me a topic — I'll search the web, read the best source, and write you a full report.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ----------------------------------------------------------------------------
# Render history
# ----------------------------------------------------------------------------
for i, msg in enumerate(st.session_state.messages):
    with st.container(key=f"bubble-{msg['role']}-{i}"):
        st.markdown(msg["content"])

    if msg["role"] == "assistant":
        with st.container(key=f"meta-{i}"):
            if msg.get("feedback"):
                with st.expander("Critic feedback"):
                    st.markdown(msg["feedback"])
            if msg.get("log"):
                with st.expander("Research process"):
                    st.markdown(
                        f"<div class='log-box'>{msg['log']}</div>",
                        unsafe_allow_html=True,
                    )

# ----------------------------------------------------------------------------
# Input + pipeline run
# ----------------------------------------------------------------------------
class _StreamToPlaceholder(io.StringIO):
    """Mirrors print() output from the pipeline into a live-updating box."""

    def __init__(self, placeholder):
        super().__init__()
        self.placeholder = placeholder
        self.text = ""

    def write(self, s):
        self.text += s
        safe = (
            self.text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        self.placeholder.markdown(
            f"<div class='log-box'>{safe}</div>", unsafe_allow_html=True
        )
        return len(s)

    def flush(self):
        pass


prompt = st.chat_input("Ask me to research anything…")

if prompt:
    idx = len(st.session_state.messages)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.container(key=f"bubble-user-{idx}"):
        st.markdown(prompt)

    log_placeholder = st.empty()
    stream = _StreamToPlaceholder(log_placeholder)
    old_stdout = sys.stdout
    sys.stdout = stream

    try:
        with st.spinner("Researching…"):
            result = run_research_pipeline(prompt)
        error = None
    except Exception as exc:  # noqa: BLE001
        result = None
        error = str(exc)
    finally:
        sys.stdout = old_stdout

    log_placeholder.empty()

    a_idx = len(st.session_state.messages)

    if error:
        with st.container(key=f"bubble-assistant-{a_idx}"):
            st.error(f"Something went wrong while researching this topic:\n\n{error}")
        st.session_state.messages.append(
            {"role": "assistant", "content": f"⚠️ {error}"}
        )
    else:
        report = result.get("report", "")
        feedback = result.get("feedback", "")
        log_text = (
            stream.text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

        with st.container(key=f"bubble-assistant-{a_idx}"):
            st.markdown(report)

        with st.container(key=f"meta-{a_idx}"):
            with st.expander("Critic feedback"):
                st.markdown(feedback)
            with st.expander("Research process"):
                st.markdown(
                    f"<div class='log-box'>{log_text}</div>", unsafe_allow_html=True
                )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": report,
                "feedback": feedback,
                "log": log_text,
            }
        )