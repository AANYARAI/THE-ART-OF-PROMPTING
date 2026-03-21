def classify_prompt(prompt: str):
    length = len(prompt.split())

    if length < 5:
        return "Beginner"
    elif length < 12:
        return "Intermediate"
    else:
        return "Advanced"