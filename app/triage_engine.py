"""
Rule-based, NON-DIAGNOSTIC symptom triage.

Deliberately not a machine-learned diagnostic model: SIH judges will ask about
AI safety, and "we call a black-box model to diagnose people" is a hard
question to defend. A transparent keyword -> urgency mapping is explainable,
auditable, needs no API key or GPU, and is honest about what it actually does:
it routes people to the right *kind* of care, it does not tell them what is
wrong with them.

Extending it:
- Add more keywords per language to RULES.
- Add a new language by adding a new key to RULES with the same urgency levels.
- Swap this whole module for a real ML classifier later if you want to
  incorporate one that HAS been signed off with the intended safety review
  and clinical mitigation the pitch talks about. The router calling this
  module doesn't need to change.
"""

from dataclasses import dataclass


@dataclass
class TriageResult:
    urgency: str  # "emergency" | "urgent" | "moderate" | "self_care"
    message: str
    suggested_facility_type: str


RULES = {
    "en": {
        "emergency": ["chest pain", "can't breathe", "cannot breathe", "unconscious", "severe bleeding", "not breathing", "heart attack", "stroke"],
        "urgent": ["high fever", "severe pain", "vomiting blood", "difficulty breathing", "broken bone", "fracture"],
        "moderate": ["fever", "pain", "cough", "cold", "headache", "vomiting", "diarrhea", "weakness"],
    },
    "hi": {
        "emergency": ["सांस नहीं", "बेहोश", "सीने में दर्द", "बहुत खून", "हार्ट अटैक"],
        "urgent": ["तेज़ बुखार", "तेज़ दर्द", "खून की उल्टी", "हड्डी टूट"],
        "moderate": ["बुखार", "दर्द", "खांसी", "सर्दी", "सिरदर्द", "उल्टी", "कमजोरी"],
    },
}

MESSAGES = {
    "emergency": {
        "en": "This sounds urgent. Please go to the nearest hospital or emergency room right now, or call for emergency help. This is not a diagnosis.",
        "hi": "यह गंभीर लग रहा है। कृपया तुरंत नज़दीकी अस्पताल या इमरजेंसी में जाएं, या आपातकालीन सहायता के लिए कॉल करें। यह निदान नहीं है।",
    },
    "urgent": {
        "en": "You should see a doctor today. We suggest visiting a Community Health Centre or hospital. This is not a diagnosis.",
        "hi": "आपको आज ही डॉक्टर से मिलना चाहिए। सामुदायिक स्वास्थ्य केंद्र या अस्पताल जाने की सलाह है। यह निदान नहीं है।",
    },
    "moderate": {
        "en": "We suggest visiting a Primary Health Centre within the next day or two. This is not a diagnosis.",
        "hi": "अगले एक-दो दिन में प्राइमरी हेल्थ सेंटर जाने की सलाह है। यह निदान नहीं है।",
    },
    "self_care": {
        "en": "This doesn't sound urgent based on what you described. Rest, stay hydrated, and monitor how you feel. If it gets worse, contact a health worker. This is not a diagnosis.",
        "hi": "आपके बताए अनुसार यह गंभीर नहीं लगता। आराम करें, पानी पीते रहें और ध्यान रखें। यदि बिगड़े तो स्वास्थ्यकर्मी से संपर्क करें। यह निदान नहीं है।",
    },
}

FACILITY_BY_URGENCY = {
    "emergency": "Hospital",
    "urgent": "CHC",
    "moderate": "PHC",
    "self_care": "PHC",
}


def run_triage(text: str, lang: str = "en") -> TriageResult:
    lang = lang if lang in RULES else "en"
    text_lower = text.lower()
    rules = RULES[lang]

    for urgency in ("emergency", "urgent", "moderate"):
        for keyword in rules[urgency]:
            if keyword.lower() in text_lower:
                return TriageResult(
                    urgency=urgency,
                    message=MESSAGES[urgency][lang],
                    suggested_facility_type=FACILITY_BY_URGENCY[urgency],
                )

    return TriageResult(
        urgency="self_care",
        message=MESSAGES["self_care"][lang],
        suggested_facility_type=FACILITY_BY_URGENCY["self_care"],
    )
