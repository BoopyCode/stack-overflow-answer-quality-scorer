#!/usr/bin/env python3
"""
Answer Quality Scorer - Because Stack Overflow roulette shouldn't be this stressful.
"""

import re
from datetime import datetime
from typing import Dict, Any


def score_answer(answer_data: Dict[str, Any]) -> float:
    """
    Scores an answer from 0-10 where 0 = 'will break production', 10 = 'actually works'.
    """
    score = 5.0  # Start with 'meh, might work'
    
    # 1. Age check (because 2012 jQuery answers won't save your React app)
    if 'creation_date' in answer_data:
        age_years = (datetime.now().timestamp() - answer_data['creation_date']) / (365 * 24 * 3600)
        if age_years > 5:
            score -= 2  # Ancient wisdom, probably outdated
        elif age_years < 1:
            score += 1  # Fresh code, might actually compile
    
    # 2. Length check (TL;DR vs 'just use console.log')
    if 'body' in answer_data:
        body = answer_data['body']
        word_count = len(re.findall(r'\w+', body))
        
        if word_count < 10:
            score -= 1  # 'Just google it' energy
        elif word_count > 500:
            score += 1  # Someone actually tried to help
        else:
            score += 0.5  # Goldilocks zone
        
        # 3. Code block check (actual code > philosophical debate)
        code_blocks = len(re.findall(r'```[\s\S]*?```', body)) + len(re.findall(r'<code>[\s\S]*?</code>', body))
        if code_blocks > 0:
            score += 1  # Show me the code!
        
        # 4. 'Update:' detection (someone cared enough to fix their mistakes)
        if re.search(r'update[^\w]|edit[^\w]|note:', body, re.IGNORECASE):
            score += 0.5  # Self-awareness bonus
    
    # 5. Score boundaries (can't have negative quality... or can we?)
    score = max(0.0, min(10.0, score))
    
    return round(score, 1)


def get_quality_label(score: float) -> str:
    """Translates numbers to developer emotions."""
    if score >= 9:
        return "🔥 Production-ready (probably)"
    elif score >= 7:
        return "👍 Might work, worth a try"
    elif score >= 5:
        return "🤷 Could work, could also break everything"
    elif score >= 3:
        return "⚠️  Risky business"
    else:
        return "💀 Abandon all hope"


if __name__ == "__main__":
    # Example usage with a mock answer (because real API calls would require effort)
    mock_answer = {
        "body": "Here's a solution:\n```python\nprint('Hello World')\n```\n\nUpdate: Fixed syntax error",
        "creation_date": datetime.now().timestamp() - (2 * 365 * 24 * 3600)  # 2 years old
    }
    
    score = score_answer(mock_answer)
    label = get_quality_label(score)
    
    print(f"Answer Score: {score}/10")
    print(f"Verdict: {label}")
    print("\nDisclaimer: This tool is 87% accurate, which is 13% better than guessing!")
