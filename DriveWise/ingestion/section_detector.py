import re


SECTION_KEYWORDS = {
    "Exterior": [
        "exterior",
        "headlamp",
        "tail lamp",
        "grille",
        "alloy wheel",
        "outside door",
        "roof",
    ],

    "Interior": [
        "interior",
        "seat",
        "dashboard",
        "cockpit",
        "upholstery",
        "glovebox",
    ],

    "Comfort": [
        "comfort",
        "climate control",
        "air conditioner",
        "rear seat",
        "sunshade",
        "cruise control",
    ],

    "Performance": [
        "performance",
        "engine",
        "power",
        "torque",
        "displacement",
        "transmission",
    ],

    "Mileage": [
        "mileage",
        "fuel efficiency",
        "fuel economy",
    ],

    "Safety": [
        "safety",
        "airbag",
        "abs",
        "electronic stability",
        "esc",
        "parking sensor",
        "blind spot",
        "surround view",
    ],

    "ADAS": [
        "adas",
        "advanced driver assistance",
        "smart sense",
        "forward collision",
        "lane keeping",
        "lane departure",
    ],

    "Infotainment": [
        "infotainment",
        "android auto",
        "apple carplay",
        "bluetooth",
        "speaker",
        "display",
        "navigation",
    ],

    "Connectivity": [
        "connectivity",
        "bluelink",
        "connected car",
        "wireless",
        "usb",
    ],

    "Technology": [
        "technology",
        "digital cluster",
        "smart key",
        "wireless charging",
        "connected",
    ],

    "Dimensions": [
        "dimensions",
        "length",
        "width",
        "height",
        "wheelbase",
        "ground clearance",
    ],

    "Specifications": [
        "technical specifications",
        "specifications",
        "fuel tank",
        "tyre",
        "suspension",
        "brakes",
    ],

    "Variants": [
        "variants",
        "variant",
        "trim",
        "engine & trim plan",
        "key features",
    ],

    "Colours": [
        "colours",
        "colors",
        "exterior colours",
        "exterior colors",
    ],

    "Warranty": [
        "warranty",
        "extended warranty",
    ],
}


def detect_section(text: str) -> str:

    if not text:
        return "Other"

    text_lower = text.lower()

    scores = {}

    for section, keywords in SECTION_KEYWORDS.items():

        score = 0

        for keyword in keywords:

            if keyword in text_lower:
                score += 1

        if score > 0:
            scores[section] = score

    if not scores:
        return "Other"

    return max(scores, key=scores.get)