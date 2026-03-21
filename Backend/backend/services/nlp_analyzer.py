def analyze_prompt(prompt: str):
    words = prompt.split()
    word_count = len(words)

    clarity_score = min(10, word_count)

    keywords = words[:3]

    if word_count < 5:
        suggestion = "Prompt is too short. Add more details."
    else:
        suggestion = "Prompt looks good."

    return {
        "word_count": word_count,
        "clarity_score": clarity_score,
        "keywords": keywords,
        "suggestion": suggestion
    }