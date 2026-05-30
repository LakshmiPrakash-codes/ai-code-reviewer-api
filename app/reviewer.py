import anthropic
from .schemas import CodeReview

client = anthropic.Anthropic()

SYSTEM_PROMPT = """You are a senior software engineer doing a thorough code review.
Analyze the submitted code and return structured feedback.

- Use exact line numbers for bugs.
- Severity: "low" (style/minor), "medium" (logic error), "high" (crash or data loss risk).
- rewritten_code must be complete and runnable — fix every bug found.
- Complexity in Big O notation (O(n), O(1), O(n log n), etc.).
- Return empty lists for bugs/security_issues when none exist."""


def review_code(code: str, language: str) -> CodeReview:
    response = client.messages.parse(
        model="claude-haiku-4-5",
        max_tokens=4096,  # haiku caps at 4096 output tokens
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[
            {
                "role": "user",
                "content": f"Review this {language} code:\n\n```{language}\n{code}\n```",
            }
        ],
        output_format=CodeReview,
    )

    if response.parsed_output is None:
        raise ValueError("Failed to generate a structured review.")

    return response.parsed_output
