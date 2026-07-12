import re

RED_FLAG_PATTERNS = {
    "Fake Authority Claim": [
        r"\b(bank manager|police|officer|cbi|ed\b|income tax|government department|customs|rbi|narcotics|cyber cell|court)\b",
        r"\bcalling from\b",
        r"\bthis is\b.*\b(department|company|bank|support|officer)\b",
        r"\bidentity card\b|\bid card\b|\bwarrant\b",
        # NEW: implicit-authority parcel/courier/customs scams (no explicit "customs" word used)
        r"\b(courier|parcel|shipment|package)\b.*\b(illegal|banned|prohibited|narcotics|drugs|contraband)\b",
        # NEW: implicit-authority "pending case / investigation" digital-arrest openers
        r"\b(pending case|case (has been )?registered|fir (has been )?filed|verification department|crime branch|investigation (department|team)|legal notice|legal matter)\b",
        r"\bunder investigation\b",
    ],
    "Threat Language": [
        r"\b(fir|arrest|legal action|blocked|suspended|penalty|court|jail|seize|freeze|confiscat\w*)\b",
        r"\bfailure to\b",
        r"\bwill be (blocked|suspended|terminated|arrested)\b",
        r"\bdigital arrest\b",
        r"\byour (account|number|card) (has been|will be)\b",
        # NEW: catches "pay a fine", "detained", "intercepted", "warrant" as a threat too
        r"\b(fine|warrant|detain\w*|intercept\w*)\b",
    ],
    "Payment Pressure": [
        r"\b(processing fee|pay immediately|urgent payment|transfer fee|activation fee|security deposit|clearance fee)\b",
        r"\b(credit card|bank account) (details|information|number)\b",
        r"\bpay\b.*\b(now|immediately|today|urgently)\b",
    ],
    "Remote Access Request": [
        r"\b(remote access|anydesk|teamviewer|screen sharing|screen share|install (this|the) app|quick support)\b",
        r"\bdownload\b.*\bapp\b",
    ],
    "OTP Request": [
        r"\b(otp|one time password|pin number|cvv|verification code|share.*code)\b",
    ],
    "Isolation Tactics": [
        r"\b(don'?t tell|keep this (confidential|secret)|do not share|between us|do not disconnect|stay on the line|don'?t hang up)\b",
        r"\balone\b|\bprivate(ly)?\b.*\b(talk|call|discuss)\b",
        r"\bdo not (inform|contact|call)\b",
        # NEW: video-call compliance / stay-engaged pressure (classic subtle digital-arrest opener)
        r"\b(join (the )?video( call)?|video verification|switch on your camera|remain (online|available)|stay online)\b",
    ],
}

def detect_red_flags(text):
    text_lower = text.lower()
    detected = {}
    for flag_name, patterns in RED_FLAG_PATTERNS.items():
        matched = any(re.search(pattern, text_lower) for pattern in patterns)
        detected[flag_name] = int(matched)  # 1 if matched, 0 if not
    return detected

if __name__ == "__main__":
    sample = "Hello, I am calling from the CBI department. Your account will be blocked unless you pay the processing fee immediately. Please share the OTP now. Don't tell anyone about this call."
    result = detect_red_flags(sample)
    for flag, val in result.items():
        print(f"{flag}: {val}")

    print()
    sample2 = "Your parcel contains illegal items, pay fine or face arrest."
    result2 = detect_red_flags(sample2)
    for flag, val in result2.items():
        print(f"{flag}: {val}")

    print()
    sample3 = "You have a pending case, join video call for verification."
    result3 = detect_red_flags(sample3)
    for flag, val in result3.items():
        print(f"{flag}: {val}")