import json
import re
from signalnoise.llm.groq_client import GroqClient
from signalnoise.signals.signal_model import Signal

def clean_json_content(content: str) -> str:
    content = content.strip()
    if content.startswith("```json"):
        content = content[7:]
    elif content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()
    
    first_brace = content.find('{')
    last_brace = content.rfind('}')
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        content = content[first_brace:last_brace+1]
    return content

def parse_multiple_json(content: str) -> list[dict]:
    content = content.strip()
    decoder = json.JSONDecoder()
    pos = 0
    results = []
    while pos < len(content):
        start = content.find('{', pos)
        if start == -1:
            break
        try:
            obj, end = decoder.raw_decode(content[start:])
            results.append(obj)
            pos = start + end
        except json.JSONDecodeError:
            pos = start + 1
    return results

class LLMSignalDetector():
    def __init__(self):
        super().__init__()

    def detect(self, query: str, user_query: str = None) -> list[Signal]:
        focus_instruction = ""
        if user_query:
            focus_instruction = f"""
[FOCUS QUERY]
Focus ONLY on identifying risks, blockers, or delivery issues that are relevant or related to the topic/query: "{user_query}".
If the text does not contain any risks, blockers, or delivery issues relevant to "{user_query}", return a single JSON object with signal_type set to "No Risk", severity set to "Low", confidence set to 0.0, empty evidence_chunks, and a summary stating no risk detected.
"""

        prompt = f"""
[ROLE]
You are an enterprise expert risk detector and analyst. Your goal is to identify project risks, team blockers, and potential delivery issues from communication logs.
{focus_instruction}
[TASK]
Analyze the following communication and identify any potential risks, blockers, or delivery issues:
"{query}"

[CONSTRAINTS & GUARDRAILS]
- Analyze the provided communication text only. Do not make assumptions or extrapolate beyond the provided text.
- Evidence chunks must consist ONLY of direct, exact quotes from the communication text.
- Confidence score must be a float between 0.0 (no confidence) and 1.0 (absolute certainty).
- The severity must be classified as one of: "Low", "Medium", or "High".
- Focus strictly on the topic/query if [FOCUS QUERY] is provided. Do not report unrelated risks.
- You must output ONLY a valid JSON object. Do not include any conversational text, explanations, or markdown code blocks (e.g., do not wrap the JSON in ```json ... ```).

[OUTPUT STRUCTURE]
Your output must be a single JSON object matching the following schema:
{{
    "signal_type": "string (the category of the detected risk, e.g., 'Dependency Risk', 'Testing Risk', 'Resource Risk')",
    "severity": "string ('Low', 'Medium', or 'High')",
    "confidence": "float (0.0 to 1.0)",
    "evidence_chunks": ["string (exact direct quotes from the input communication support this signal)"],
    "summary": "string (a concise explanation summarizing the detected risk)"
}}
"""
        response=GroqClient.get_response(prompt)
        
        content_str = response.content if isinstance(response.content, str) else str(response.content)
        data_list = parse_multiple_json(content_str)
        
        if not data_list:
            cleaned_content = clean_json_content(content_str)
            try:
                data_list = [json.loads(cleaned_content)]
            except json.JSONDecodeError:
                # Provide a fallback if LLM returned completely unparsable content
                data_list = [{
                    "signal_type": "General Risk",
                    "severity": "Medium",
                    "confidence": 0.8,
                    "evidence_chunks": [],
                    "summary": content_str[:200]
                }]
                
        signals = []
        for data in data_list:
            sig_type = data.get("signal_type", "General Risk")
            if sig_type.lower() in ("no risk", "none", "n/a", ""):
                continue
            signals.append(
                Signal(
                    signal_type=sig_type,
                    severity=data.get("severity", "Medium"),
                    confidence=float(data.get("confidence", 0.8)),
                    evidence_chunks=data.get("evidence_chunks", []),
                    summary=data.get("summary", "")
                )
            )
        return signals



