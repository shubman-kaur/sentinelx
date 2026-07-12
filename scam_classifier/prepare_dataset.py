from red_flags import detect_red_flags
import pandas as pd
import re


rows = []
with open("data/fraudcall/fraud_call.tsv", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        line = line.rstrip("\n")
        if not line.strip():
            continue
        parts = line.split("\t", 1)  # split only on FIRST tab
        if len(parts) == 2:
            rows.append({"label": parts[0].strip(), "text": parts[1].strip()})

df1 = pd.DataFrame(rows)
df1["label"] = df1["label"].map({"fraud": "scam", "normal": "normal"})

with open("data/scam_conversations/English_Scam.txt", "r", encoding="utf-8") as f:
    content = f.read()


scam_entries = re.split(r'\n?\d+\.\s*', content)
scam_entries = [e.strip().replace("\n", " ") for e in scam_entries if e.strip()]
df2 = pd.DataFrame({"label": "scam", "text": scam_entries})

# --- 3. Load English_NonScam.txt (line-separated entries) ---
with open("data/scam_conversations/English_NonScam.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

nonscam_entries = [line.strip() for line in lines if line.strip()]
df3 = pd.DataFrame({"label": "normal", "text": nonscam_entries})

# --- 4. Combine all three ---
combined = pd.concat([df1, df2, df3], ignore_index=True)

# Drop empty or too-short entries
combined = combined[combined["text"].str.len() > 10]


red_flag_results = combined["text"].apply(detect_red_flags)
red_flag_df = pd.DataFrame(list(red_flag_results))

# Merge red flags as new columns
combined = pd.concat([combined.reset_index(drop=True), red_flag_df], axis=1)

# Save
combined.to_csv("data/combined_scam_dataset.csv", index=False)

print(f"Total entries: {len(combined)}")
print(combined["label"].value_counts())
print("\nSample rows:")
print(combined.head())