import os
import re
from typing import Optional

# Pre-defined keywords for scanning
TEAMS = [
    "payments", "platform", "billing", "operations", "security",
    "infrastructure", "data", "frontend", "backend", "fullstack",
    "mobile", "devops", "support", "customer profile"
]

DEPARTMENTS = [
    "engineering", "product", "sales", "marketing", "hr",
    "human resources", "finance", "legal", "operations", "support",
    "customer success"
]

def clean_value(val: Optional[str]) -> Optional[str]:
    if not val:
        return None
    val = val.strip().strip("-").strip(":").strip()
    return val if val else None

def extract_metadata(content: str, file_path: str) -> dict:
    file_name = os.path.basename(file_path)
    
    team = None
    department = None
    date = None

    # --- 1. Extract Team ---
    # Look for explicit indicators like "Team: Payments" or "Team Name: Payments"
    team_match = re.search(r'(?i)\b(?:team|team\s+name)\s*[:\-]\s*([a-zA-Z0-9_\s\-]+)', content)
    if team_match:
        team = clean_value(team_match.group(1).split('\n')[0])
    
    if not team:
        # Look for "Payments Team" style in content
        team_suffix_match = re.search(r'\b([A-Za-z0-9_\-]+)\s+Team\b', content)
        if team_suffix_match:
            team = clean_value(team_suffix_match.group(1))

    if not team:
        # Search for known teams in content
        content_lower = content.lower()
        for t in TEAMS:
            if t in content_lower:
                team = t.title()
                break

    if not team:
        # Search for known teams in file name
        file_name_lower = file_name.lower()
        for t in TEAMS:
            if t in file_name_lower:
                team = t.title()
                break

    # --- 2. Extract Department ---
    # Look for explicit indicators like "Department: Engineering" or "Dept: Engineering"
    dept_match = re.search(r'(?i)\b(?:department|dept)\s*[:\-]\s*([a-zA-Z0-9_\s\-]+)', content)
    if dept_match:
        department = clean_value(dept_match.group(1).split('\n')[0])

    if not department:
        # Search for known departments in content
        content_lower = content.lower()
        for d in DEPARTMENTS:
            if d in content_lower:
                department = d.title()
                break

    if not department:
        # Search for known departments in file name
        file_name_lower = file_name.lower()
        for d in DEPARTMENTS:
            if d in file_name_lower:
                department = d.title()
                break

    # --- 3. Extract Date ---
    # Look for explicit indicators like "Date: 2026-06-07"
    date_match = re.search(r'(?i)\bdate\s*[:\-]\s*([a-zA-Z0-9_\s\-\/,]+)', content)
    if date_match:
        date = clean_value(date_match.group(1).split('\n')[0])

    # Date regex patterns: YYYY-MM-DD, DD/MM/YYYY, Month DD YYYY etc.
    date_patterns = [
        r'\b\d{4}[-/]\d{2}[-/]\d{2}\b',
        r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b',
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b',
        r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\b'
    ]

    if not date:
        for pattern in date_patterns:
            m = re.search(pattern, content, re.IGNORECASE)
            if m:
                date = clean_value(m.group(0))
                break

    if not date:
        for pattern in date_patterns:
            m = re.search(pattern, file_name, re.IGNORECASE)
            if m:
                date = clean_value(m.group(0))
                break

    return {
        "file_name": file_name,
        "team": team,
        "department": department,
        "date": date
    }
