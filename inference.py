def _words(text: str) -> list[str]:
    return [w.strip(".,!?") for w in text.lower().split()]


def sentiment(text: str) -> tuple[str, float]:
    good = {"love", "great", "good", "amazing", "happy", "best"}
    bad = {"hate", "terrible", "bad", "awful", "worst", "sad"}
    words = _words(text)
    pos = sum(w in good for w in words)
    neg = sum(w in bad for w in words)
    if pos > neg:
        return "positive", round(pos / (pos + neg), 2)
    if neg > pos:
        return "negative", round(neg / (pos + neg), 2)
    return "neutral", 0.5


def toxicity(text: str) -> tuple[str, float]:
    toxic_words = {"idiot", "stupid", "dumb", "loser", "moron"}
    hits = sum(w in toxic_words for w in _words(text))
    if hits:
        return "toxic", round(min(0.99, 0.6 + 0.15 * hits), 2)
    return "non_toxic", 0.9


# Routing table: task name -> the function that handles it
MODELS = {"sentiment": sentiment, "toxicity": toxicity}