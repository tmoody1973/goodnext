"""Deterministic post-generation checks on a NoticePlanProposal (MOO-789).

PRD FR02, FR03, section 6: findings cite supplied passages; dates are literal
text from the letter or "not stated"; policy and routes come only from what the
tools returned this run; no eligibility, exemption or continuation verdicts.
A violating item is stripped and the answer returns as partial.
"""

from notice_tools import PHONE, NoticeContext, detect_letter_kind
from schemas import NoticePlanProposal


def _digits(text: str | None) -> str:
    return "".join(ch for ch in (text or "") if ch.isdigit())

# Verdicts the site never states (PRD section 3 exclusions). Whole phrase, any case.
NOTICE_NEVER_LIST = [
    "you are eligible",
    "you are not eligible",
    "you are exempt",
    "your benefits will continue",
    "your case is fixed",
    "you are approved",
    "guaranteed",
]
EXPLANATION_MAX_WORDS = 60


def _never_hit(text: str) -> str | None:
    low = text.lower()
    return next((t for t in NOTICE_NEVER_LIST if t in low), None)


def validate_notice_plan(proposal: NoticePlanProposal, ctx: NoticeContext) -> tuple[NoticePlanProposal, list[str]]:
    """Return a cleaned proposal and the violations found. Never mutates input."""
    violations: list[str] = []
    passages = ctx.passages

    def cited(ids: list[str], what: str) -> list[str]:
        valid = [i for i in ids if i in passages]
        if not valid:
            violations.append(f"{what}: cites no supplied passage")
        return valid

    def clean_text(text: str, what: str) -> bool:
        if hit := _never_hit(text):
            violations.append(f"{what}: never-list hit '{hit}'")
            return False
        return True

    kind = detect_letter_kind(list(passages.values()))
    if proposal.letter_kind != kind:
        violations.append(f"letter_kind {proposal.letter_kind} replaced by title-detected {kind}")
    screening = "more_information_needed" if kind == "unknown" else proposal.screening
    if kind == "unknown" and proposal.screening != "more_information_needed":
        violations.append("unknown letter: screening forced to more_information_needed")

    findings = []
    for f in proposal.findings:
        ids = cited(f.passage_ids, f"finding '{f.label}'")
        if ids and clean_text(f.text, f"finding '{f.label}'"):
            findings.append(f.model_copy(update={"passage_ids": ids}))

    next_step = None
    if proposal.next_step is not None:
        ids = cited(proposal.next_step.passage_ids, "next_step")
        if ids and clean_text(proposal.next_step.text, "next_step"):
            next_step = proposal.next_step.model_copy(update={"passage_ids": ids})

    tasks = []
    for t in proposal.tasks:
        ids = cited(t.passage_ids, f"task '{t.kind}'")
        if not ids or not clean_text(t.text, f"task '{t.kind}'"):
            continue
        # Literal means printed somewhere in the letter; the model may cite the wrong passage.
        letter_text = " ".join(p.text for p in passages.values())
        date_text, date_kind = t.date_text, t.date_kind
        if date_text != "not stated" and date_text not in letter_text:
            violations.append(f"task '{t.kind}': date '{date_text}' is not literal text of the letter")
            date_text, date_kind = "not stated", "unknown"
        tasks.append(t.model_copy(update={"passage_ids": ids, "date_text": date_text, "date_kind": date_kind}))

    questions = []
    for q in proposal.questions_to_ask:
        ids = [i for i in q.policy_ids if i in ctx.policy_returned]
        if not ids:
            violations.append(f"question '{q.text[:40]}': cites no returned policy passage")
        elif clean_text(q.text, "question"):
            questions.append(q.model_copy(update={"policy_ids": ids}))

    # A contact is real when its number or address came back from the tool, or its
    # number is printed in the letter; the model may reword the name.
    known_phones = {_digits(p) for p in ctx.routes_phones} | {_digits(m) for p in passages.values() for m in PHONE.findall(p.text)}
    known_urls = set(ctx.routes_urls)
    routes = []
    for r in proposal.routes:
        if r.name in ctx.routes_returned or (r.phone and _digits(r.phone) in known_phones) or (r.url and r.url in known_urls):
            routes.append(r)
        else:
            violations.append(f"route '{r.name}': not returned by resolve_help_route and not printed in the letter")

    unknowns = [u for u in proposal.unknowns if clean_text(u, "unknown")]

    explanation = proposal.explanation
    if not clean_text(explanation, "explanation"):
        explanation = ""
    elif len(explanation.split()) > EXPLANATION_MAX_WORDS:
        violations.append("explanation over 60 words; truncated")
        explanation = " ".join(explanation.split()[:EXPLANATION_MAX_WORDS])

    cleaned = proposal.model_copy(update={
        "letter_kind": kind,
        "screening": screening,
        "findings": findings,
        "next_step": next_step,
        "tasks": tasks,
        "questions_to_ask": questions,
        "routes": routes,
        "unknowns": unknowns,
        "explanation": explanation,
    })
    return cleaned, violations
