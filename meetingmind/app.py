import streamlit as st
from dotenv import load_dotenv
import os

from nodes import (
    run_segmenter,
    run_summarizer,
    run_action_items_extractor,
    run_decisions_extractor,
    run_report_assembler,
)

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MeetingMind",
    page_icon="🧠",
    layout="wide",
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🧠 MeetingMind")
    st.markdown("AI-powered meeting analysis in 5 steps.")
    st.divider()

    # API key: prefer st.secrets → env var → sidebar input
    default_key = ""
    if hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
        default_key = st.secrets["GROQ_API_KEY"]
    elif os.environ.get("GROQ_API_KEY"):
        default_key = os.environ["GROQ_API_KEY"]

    groq_api_key = st.text_input(
        "Groq API Key",
        value=default_key,
        type="password",
        placeholder="gsk_...",
        help="Get your key at console.groq.com",
    )

    st.divider()
    st.markdown(
        """
**Pipeline Steps**
1. Segmenter
2. Summarizer
3. Action Items
4. Decisions
5. Report Assembler
"""
    )

# ── Main area ─────────────────────────────────────────────────────────────────
st.title("MeetingMind Agent")
st.markdown(
    "Paste your meeting transcript below and click **Analyse Meeting** "
    "to generate a structured report."
)

transcript = st.text_area(
    "Meeting Transcript",
    height=300,
    placeholder="Paste your meeting transcript here…",
)

analyse_btn = st.button("Analyse Meeting", type="primary", use_container_width=True)

# ── Pipeline execution ────────────────────────────────────────────────────────
if analyse_btn:
    # Validation
    if not groq_api_key:
        st.error("Please enter your Groq API key in the sidebar.")
        st.stop()
    if not transcript.strip():
        st.error("Please paste a meeting transcript.")
        st.stop()

    st.divider()
    st.subheader("Processing…")

    NODES = [
        ("Segmenting transcript into topic sections", "Segmenter"),
        ("Summarising each section", "Summarizer"),
        ("Extracting action items", "Action Items Extractor"),
        ("Extracting decisions", "Decisions Extractor"),
        ("Assembling final report", "Report Assembler"),
    ]

    # Placeholder slots for each node status
    status_slots = []
    for label, name in NODES:
        col1, col2 = st.columns([0.05, 0.95])
        spinner_slot = col1.empty()
        label_slot = col2.empty()
        label_slot.markdown(f"{label}")
        status_slots.append((spinner_slot, label_slot, label, name))

    results = {}

    def mark_running(idx):
        spinner_slot, label_slot, label, name = status_slots[idx]
        label_slot.markdown(f"**{label}**")

    def mark_done(idx):
        spinner_slot, label_slot, label, name = status_slots[idx]
        label_slot.markdown(f"{label}")

    try:
        # Node 1 — Segmenter
        mark_running(0)
        sections = run_segmenter(transcript, groq_api_key)
        results["sections"] = sections
        mark_done(0)

        # Node 2 — Summarizer
        mark_running(1)
        summaries = run_summarizer(sections, groq_api_key)
        results["summaries"] = summaries
        mark_done(1)

        # Node 3 — Action Items
        mark_running(2)
        action_items = run_action_items_extractor(transcript, groq_api_key)
        results["action_items"] = action_items
        mark_done(2)

        # Node 4 — Decisions
        mark_running(3)
        decisions = run_decisions_extractor(transcript, groq_api_key)
        results["decisions"] = decisions
        mark_done(3)

        # Node 5 — Report Assembler
        mark_running(4)
        report = run_report_assembler(summaries, action_items, decisions, groq_api_key)
        results["report"] = report
        mark_done(4)

    except Exception as e:
        st.error(f"Pipeline error: {e}")
        st.stop()

    # ── Render report ─────────────────────────────────────────────────────────
    st.divider()
    st.subheader("Meeting Report")
    st.markdown(results["report"])

    st.divider()
    st.download_button(
        label="Download Report (.md)",
        data=results["report"],
        file_name="meeting_report.md",
        mime="text/markdown",
        use_container_width=True,
    )
