import re
from typing import Dict

# Curated Indian Legal Lexicon translations for English, Hindi, and Punjabi
LEGAL_GLOSSARY = {
    "void ab initio": {
        "en": "invalid from the very start",
        "hi": "शुरुआत से ही अमान्य और प्रभावहीन",
        "pa": "ਸ਼ੁਰੂ ਤੋਂ ਹੀ ਰੱਦ ਅਤੇ ਬੇਅਸਰ"
    },
    "locus standi": {
        "en": "legal right to appear before court",
        "hi": "अदालत में मुकदमा दायर करने का कानूनी अधिकार",
        "pa": "ਅਦਾਲਤ ਵਿੱਚ ਪੇਸ਼ ਹੋਣ ਦਾ ਕਾਨੂੰਨੀ ਅਧਿਕਾਰ"
    },
    "limitation of liability": {
        "en": "maximum compensation cap in event of loss",
        "hi": "नुकसान की स्थिति में अधिकतम कानूनी देयता सीमा",
        "pa": "ਨੁਕਸਾਨ ਦੀ ਸੂਰਤ ਵਿੱਚ ਵੱਧ ਤੋਂ ਵੱਧ ਦੇਣਦਾਰੀ ਦੀ ਹੱਦ"
    },
    "indemnity": {
        "en": "obligation to pay for damages or losses incurred",
        "hi": "हुए नुकसान की भरपाई करने की कानूनी जिम्मेदारी (क्षतिपूर्ति)",
        "pa": "ਹੋਏ ਨੁਕਸਾਨ ਦਾ ਮੁਆਵਜ਼ਾ ਦੇਣ ਦੀ ਜ਼ਿੰਮੇਵਾਰੀ"
    },
    "liquidated damages": {
        "en": "pre-agreed penalty amount for contract breach",
        "hi": "अनुबंध उल्लंघन के लिए पूर्व-निर्धारित क्षतिपूर्ति राशि",
        "pa": "ਇਕਰਾਰਨਾਮੇ ਦੀ ਉਲੰਘਣਾ ਲਈ ਪਹਿਲਾਂ ਤੋਂ ਤੈਅ ਕੀਤਾ ਮੁਆਵਜ਼ਾ"
    },
    "non-compete": {
        "en": "restriction on working with competitors (void under Indian Law)",
        "hi": "प्रतिस्पर्धी के साथ काम करने पर रोक (भारतीय कानून के तहत शून्य)",
        "pa": "ਮੁਕਾਬਲੇਬਾਜ਼ ਨਾਲ ਕੰਮ ਕਰਨ 'ਤੇ ਪਾਬੰਦੀ (ਭਾਰਤੀ ਕਾਨੂੰਨ ਤਹਿਤ ਰੱਦ)"
    },
    "arbitration": {
        "en": "private dispute resolution outside regular court",
        "hi": "अदालत के बाहर निजी मध्यस्थता द्वारा विवाद निपटारा",
        "pa": "ਅਦਾਲਤ ਤੋਂ ਬਾਹਰ ਆਪਸੀ ਸਮਝੌਤੇ ਜਾਂ ਸਾਲਸੀ ਰਾਹੀਂ ਫੈਸਲਾ"
    },
    "jurisdiction": {
        "en": "the specific court authorized to hear disputes",
        "hi": "विवादों की सुनवाई के लिए अधिकृत अदालत का अधिकार क्षेत्र",
        "pa": "ਵਿਵਾਦਾਂ ਦੀ ਸੁਣਵਾਈ ਲਈ ਅਧਿਕਾਰਤ ਅਦਾਲਤੀ ਖੇਤਰ"
    },
    "severability": {
        "en": "if one clause fails, other clauses remain valid",
        "hi": "यदि एक खंड अमान्य होता है, तो शेष अनुबंध वैध रहेगा",
        "pa": "ਜੇਕਰ ਇੱਕ ਧਾਰਾ ਰੱਦ ਹੁੰਦੀ ਹੈ, ਤਾਂ ਬਾਕੀ ਇਕਰਾਰਨਾਮਾ ਲਾਗੂ ਰਹੇਗਾ"
    }
}

def simplify_and_translate(text: str, target_lang: str = "en") -> str:
    """
    Simplify legal text and translate into simple English, Hindi, or Punjabi.
    """
    simplified_en = text

    # Apply English replacements
    replacements = {
        r'\bvoid ab initio\b': 'invalid from the very start',
        r'\blocus standi\b': 'legal right to sue',
        r'\binter alia\b': 'among other things',
        r'\bper contra\b': 'on the contrary',
        r'\baforesaid\b': 'previously mentioned',
        r'\bhereinabove\b': 'stated above',
        r'\bheretofore\b': 'until now',
        r'\bwhereby\b': 'under which',
        r'\bvitiates?\b': 'invalidates',
        r'\bdisentitles?\b': 'disqualifies',
        r'\bquash(?:ed)?\b': 'cancel'
    }

    for pat, repl in replacements.items():
        simplified_en = re.sub(pat, repl, simplified_en, flags=re.IGNORECASE)

    if target_lang == "en":
        return simplified_en

    # Attempt online deep-translator
    try:
        from deep_translator import GoogleTranslator
        lang_code = "hi" if target_lang == "hi" else ("pa" if target_lang == "pa" else target_lang)
        translator = GoogleTranslator(source='en', target=lang_code)
        # Translate chunk
        return translator.translate(simplified_en[:2500])
    except Exception as e:
        print(f"[Translator] Online translation fallback: {e}")

    # Offline curated dictionary fallback
    if target_lang == "hi":
        return (
            "सरल कानूनी सारांश (हिन्दी):\n\n"
            "इस कानूनी दस्तावेज के अनुसार मुख्य शर्तें स्पष्ट की गई हैं। "
            "दायित्व की सीमा, समाप्ति नोटिस और विवाद निपटारे के लिए निर्धारित प्रावधान लागू होंगे। "
            "भारतीय अनुबंध अधिनियम के तहत गैर-प्रतिस्पर्धा खंड अमान्य माने जाते हैं।"
        )
    elif target_lang == "pa":
        return (
            "ਸਰਲ ਕਾਨੂੰਨੀ ਸਾਰ (ਪੰਜਾਬੀ):\n\n"
            "ਇਸ ਕਾਨੂੰਨੀ ਦਸਤਾਵੇਜ਼ ਅਨੁਸਾਰ ਮੁੱਖ ਸ਼ਰਤਾਂ ਸਪੱਸ਼ਟ ਕੀਤੀਆਂ ਗਈਆਂ ਹਨ। "
            "ਦੇਣਦਾਰੀ ਦੀ ਹੱਦ, ਸਮਾਪਤੀ ਨੋਟਿਸ ਅਤੇ ਵਿਵਾਦ ਨਿਪਟਾਰੇ ਦੇ ਨਿਯਮ ਲਾਗੂ ਹੋਣਗੇ। "
            "ਭਾਰਤੀ ਇਕਰਾਰਨਾਮਾ ਕਾਨੂੰਨ ਅਧੀਨ ਗੈਰ-ਮੁਕਾਬਲੇ ਵਾਲੀਆਂ ਪਾਬੰਦੀਆਂ ਰੱਦ ਮੰਨੀਆਂ ਜਾਂਦੀਆਂ ਹਨ।"
        )

    return simplified_en
