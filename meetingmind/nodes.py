import json
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from prompts import (
    SEGMENTER_SYSTEM, SEGMENTER_USER,
    SUMMARIZER_SYSTEM, SUMMARIZER_USER,
    ACTION_ITEMS_SYSTEM, ACTION_ITEMS_USER,
    DECISIONS_SYSTEM, DECISIONS_USER,
    REPORT_ASSEMBLER_SYSTEM, REPORT_ASSEMBLER_USER,
)


def _get_llm(api_key: str) -> ChatGroq:
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=api_key,
        temperature=0,
    )


def _invoke(llm: ChatGroq, system: str, user: str) -> str:
    messages = [SystemMessage(content=system), HumanMessage(content=user)]
    response = llm.invoke(messages)
    return response.content.strip()


def _parse_json(text: str) -> list:
    """Parse JSON from LLM output, stripping any accidental fences."""
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        # Drop opening fence line and closing fence line
        text = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
    return json.loads(text)


def run_segmenter(transcript: str, api_key: str) -> list:
    """Node 1: Split transcript into named topic sections."""
    llm = _get_llm(api_key)
    raw = _invoke(llm, SEGMENTER_SYSTEM, SEGMENTER_USER.format(transcript=transcript))
    return _parse_json(raw)


def run_summarizer(sections: list, api_key: str) -> list:
    """Node 2: Summarize each section."""
    llm = _get_llm(api_key)
    raw = _invoke(
        llm,
        SUMMARIZER_SYSTEM,
        SUMMARIZER_USER.format(sections_json=json.dumps(sections, indent=2)),
    )
    return _parse_json(raw)


def run_action_items_extractor(transcript: str, api_key: str) -> list:
    """Node 3: Extract action items from the full transcript."""
    llm = _get_llm(api_key)
    raw = _invoke(
        llm,
        ACTION_ITEMS_SYSTEM,
        ACTION_ITEMS_USER.format(transcript=transcript),
    )
    return _parse_json(raw)


def run_decisions_extractor(transcript: str, api_key: str) -> list:
    """Node 4: Extract decisions from the full transcript."""
    llm = _get_llm(api_key)
    raw = _invoke(
        llm,
        DECISIONS_SYSTEM,
        DECISIONS_USER.format(transcript=transcript),
    )
    return _parse_json(raw)


def run_report_assembler(
    summaries: list,
    action_items: list,
    decisions: list,
    api_key: str,
) -> str:
    """Node 5: Assemble the final markdown report."""
    llm = _get_llm(api_key)
    report = _invoke(
        llm,
        REPORT_ASSEMBLER_SYSTEM,
        REPORT_ASSEMBLER_USER.format(
            summaries_json=json.dumps(summaries, indent=2),
            action_items_json=json.dumps(action_items, indent=2),
            decisions_json=json.dumps(decisions, indent=2),
        ),
    )
    return report
