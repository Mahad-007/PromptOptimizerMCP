"""
Prompt optimization tools for the MCP server.

This module provides stateless, deterministic functions for optimizing and scoring LLM prompts.
"""

import re
from typing import List, Literal


def optimize_prompt(
    raw_prompt: str, style: Literal["creative", "precise", "fast"]
) -> List[str]:
    """
    Generate 3 optimized variants of the raw LLM prompt in the specified style.

    Args:
        raw_prompt: The original prompt to optimize
        style: The optimization style - 'creative', 'precise', or 'fast'

    Returns:
        List[str]: 3 optimized prompt variants

    Raises:
        TypeError: If inputs are not strings or style is invalid
    """
    # Input validation
    if not isinstance(raw_prompt, str):
        raise TypeError("raw_prompt must be a string")
    if not isinstance(style, str) or style not in ["creative", "precise", "fast"]:
        raise TypeError("style must be one of: 'creative', 'precise', 'fast'")

    # Clean and normalize the input prompt
    raw_prompt = raw_prompt.strip()
    if not raw_prompt:
        return ["", "", ""]

    # Split into sentences for better processing
    sentences = re.split(r"[.!?]+", raw_prompt)
    sentences = [s.strip() for s in sentences if s.strip()]

    if style == "creative":
        return _create_creative_variants(raw_prompt, sentences)
    elif style == "precise":
        return _create_precise_variants(raw_prompt, sentences)
    else:  # fast
        return _create_fast_variants(raw_prompt, sentences)


def _create_creative_variants(raw_prompt: str, sentences: List[str]) -> List[str]:
    """Create creative variants with enhanced adjectives and imaginative language."""
    if not sentences:
        return [raw_prompt, raw_prompt, raw_prompt]

    # Variant 1: Add descriptive adjectives
    enhanced_words = {
        "write": "craft a compelling",
        "create": "design an innovative",
        "explain": "elaborate on the fascinating",
        "describe": "paint a vivid picture of",
        "analyze": "dive deep into the intricate",
        "help": "assist with the remarkable",
        "show": "demonstrate the extraordinary",
        "tell": "share the captivating",
    }

    variant1 = raw_prompt
    for word, replacement in enhanced_words.items():
        if word in variant1.lower():
            variant1 = re.sub(
                rf"\b{word}\b", replacement, variant1, flags=re.IGNORECASE
            )
            break

    # Variant 2: Add engaging opening phrases
    engaging_starts = [
        "Imagine you're an expert in this field. ",
        "Picture yourself as a master of this subject. ",
        "As a seasoned professional, ",
        "With your deep expertise, ",
    ]
    variant2 = engaging_starts[0] + raw_prompt

    # Variant 3: Add creative modifiers
    creative_modifiers = [
        "in a way that captivates and inspires",
        "with creativity and originality",
        "in an engaging and memorable manner",
        "with flair and imagination",
    ]
    variant3 = raw_prompt + ". " + creative_modifiers[0]

    return [variant1, variant2, variant3]


def _create_precise_variants(raw_prompt: str, sentences: List[str]) -> List[str]:
    """Create precise variants with concise, focused language."""
    if not sentences:
        return [raw_prompt, raw_prompt, raw_prompt]

    # Variant 1: Remove redundant words
    redundant_patterns = [
        (r"\bvery\s+", ""),
        (r"\bquite\s+", ""),
        (r"\breally\s+", ""),
        (r"\bactually\s+", ""),
        (r"\bjust\s+", ""),
        (r"\bsimply\s+", ""),
        (r"\bkind of\s+", ""),
        (r"\bsort of\s+", ""),
    ]

    variant1 = raw_prompt
    for pattern, replacement in redundant_patterns:
        variant1 = re.sub(pattern, replacement, variant1, flags=re.IGNORECASE)

    # Variant 2: Use bullet points for clarity
    if len(sentences) > 1:
        variant2 = "• " + "\n• ".join(sentences)
    else:
        variant2 = raw_prompt

    # Variant 3: Add specific constraints
    constraint_phrases = [
        "Be specific and concise.",
        "Provide clear, actionable guidance.",
        "Focus on the most important aspects.",
    ]
    variant3 = raw_prompt + " " + constraint_phrases[0]

    return [variant1, variant2, variant3]


def _create_fast_variants(raw_prompt: str, sentences: List[str]) -> List[str]:
    """Create fast variants optimized for quick processing."""
    if not sentences:
        return [raw_prompt, raw_prompt, raw_prompt]

    # Variant 1: Use shorter synonyms
    short_synonyms = {
        "utilize": "use",
        "implement": "use",
        "demonstrate": "show",
        "illustrate": "show",
        "elaborate": "explain",
        "comprehensive": "complete",
        "subsequently": "then",
        "furthermore": "also",
        "additionally": "also",
        "nevertheless": "but",
    }

    variant1 = raw_prompt
    for long_word, short_word in short_synonyms.items():
        variant1 = re.sub(
            rf"\b{long_word}\b", short_word, variant1, flags=re.IGNORECASE
        )

    # Variant 2: Use imperative form
    variant2 = raw_prompt
    # Convert "Please write..." to "Write..."
    variant2 = re.sub(r"\bplease\s+", "", variant2, flags=re.IGNORECASE)
    # Convert "Could you..." to direct commands
    variant2 = re.sub(r"\bcould you\s+", "", variant2, flags=re.IGNORECASE)
    variant2 = re.sub(r"\bwould you\s+", "", variant2, flags=re.IGNORECASE)

    # Variant 3: Add speed indicators
    speed_indicators = ["Quick response: ", "Fast answer: ", "Brief: ", "Short: "]
    variant3 = speed_indicators[0] + raw_prompt

    return [variant1, variant2, variant3]


def score_prompt(raw_prompt: str, improved_prompt: str) -> float:
    """
    Evaluate the effectiveness of an improved prompt relative to the original.

    Scoring is based on:
    - Length optimization (40%): Shorter prompts are generally better
    - Keyword preservation (30%): Important terms should be maintained
    - Clarity improvement (30%): Reduced redundancy and improved structure

    Args:
        raw_prompt: The original prompt
        improved_prompt: The optimized version to evaluate

    Returns:
        float: Effectiveness score between 0.0 and 1.0

    Raises:
        TypeError: If inputs are not strings
    """
    # Input validation
    if not isinstance(raw_prompt, str) or not isinstance(improved_prompt, str):
        raise TypeError("Both raw_prompt and improved_prompt must be strings")

    # Handle edge cases
    if not raw_prompt.strip():
        return 0.0 if improved_prompt.strip() else 1.0

    if not improved_prompt.strip():
        return 0.0

    # Normalize prompts
    raw_prompt = raw_prompt.strip()
    improved_prompt = improved_prompt.strip()

    # Calculate length score (40% weight)
    raw_length = len(raw_prompt.split())
    improved_length = len(improved_prompt.split())

    if raw_length == 0:
        length_score = 1.0
    else:
        # Prefer shorter prompts, but not too short (maintain at least 50% of original length)
        length_ratio = improved_length / raw_length
        if length_ratio <= 0.5:
            length_score = 0.3  # Penalty for being too short
        elif length_ratio <= 0.8:
            length_score = 1.0  # Optimal range
        elif length_ratio <= 1.2:
            length_score = 0.8  # Slightly longer is acceptable
        else:
            length_score = 0.4  # Too long gets penalized

    # Calculate keyword preservation score (30% weight)
    raw_words = set(re.findall(r"\b\w+\b", raw_prompt.lower()))
    improved_words = set(re.findall(r"\b\w+\b", improved_prompt.lower()))

    if not raw_words:
        keyword_score = 1.0
    else:
        # Calculate Jaccard similarity
        intersection = raw_words.intersection(improved_words)
        union = raw_words.union(improved_words)
        keyword_score = len(intersection) / len(union) if union else 0.0

    # Calculate clarity score (30% weight)
    # Count redundant phrases and filler words
    redundant_patterns = [
        r"\bvery\s+",
        r"\bquite\s+",
        r"\breally\s+",
        r"\bactually\s+",
        r"\bjust\s+",
        r"\bsimply\s+",
        r"\bkind of\s+",
        r"\bsort of\s+",
        r"\bplease\s+",
        r"\bcould you\s+",
        r"\bwould you\s+",
    ]

    raw_redundant = sum(
        len(re.findall(pattern, raw_prompt, re.IGNORECASE))
        for pattern in redundant_patterns
    )
    improved_redundant = sum(
        len(re.findall(pattern, improved_prompt, re.IGNORECASE))
        for pattern in redundant_patterns
    )

    # Fewer redundant words = better clarity
    if raw_redundant == 0:
        clarity_score = 1.0 if improved_redundant == 0 else 0.7
    else:
        improvement_ratio = (raw_redundant - improved_redundant) / raw_redundant
        clarity_score = max(0.0, min(1.0, 0.5 + improvement_ratio * 0.5))

    # Calculate weighted final score
    final_score = length_score * 0.4 + keyword_score * 0.3 + clarity_score * 0.3

    return round(final_score, 3)
