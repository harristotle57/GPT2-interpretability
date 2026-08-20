"""Hard-wrapping text to a fixed character width, and checking the result.

Was duplicated verbatim across studies/testing_gpt2_behavior.py and
studies/initial_linear_probe.py, with a third, buggier reimplementation
(generate_linewrap, which left a trailing space on wrapped lines) in
studies/gpt2_spacing_check.py. This is the one implementation now.
"""


def wrap_to_width(text: str, k: int) -> str:
    """Greedily reinsert newlines every k characters, snapped to the
    nearest word boundary <= k (same recipe as the linebreaks paper)."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = word if not current else current + " " + word
        if len(candidate) > k and current:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return "\n".join(lines)


def check_wrap_width(wrapped_text: str, k: int) -> bool:
    """True if every line of wrapped_text is within width k."""
    return all(len(line.strip()) <= k for line in wrapped_text.split("\n"))
