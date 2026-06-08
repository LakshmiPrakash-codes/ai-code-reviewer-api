import json
from groq import Groq
from .schemas import CodeReview

client = Groq()

SYSTEM_PROMPT = """You are a senior software engineer doing a thorough code review.
Analyze the submitted code and return structured feedback as JSON.

- Use exact line numbers for bugs.
- Severity: "low" (style/minor), "medium" (logic error), "high" (crash or data loss risk).
- rewritten_code must be complete and runnable — fix every bug found.
- Complexity in Big O notation (O(n), O(1), O(n log n), etc.).
- Return empty lists for bugs/security_issues when none exist.

Return a JSON object with exactly these fields:
{
  "quality_score": <int 1-10>,
  "summary": <string>,
  "bugs": [{"line_number": <int>, "description": <string>, "severity": <string>}],
  "security_issues": [{"description": <string>, "severity": <string>, "recommendation": <string>}],
  "suggestions": [<string>],
  "complexity": {"time_complexity": <string>, "space_complexity": <string>, "explanation": <string>},
  "rewritten_code": <string>
}"""


def review_code(code: str, language: str) -> CodeReview:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=4096,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Review this {language} code:\n\n```{language}\n{code}\n```"},
        ],
    )

    content = response.choices[0].message.content
    if not content:
        raise ValueError("Failed to generate a structured review.")

    data = json.loads(content)
    return CodeReview(**data)
