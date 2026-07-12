"""
Step: Add Synthetic CBI/ED Scam Messages to Combined Dataset
- Reads the new synthetic messages (text only)
- Uses detect_red_flags() to compute red flags automatically (same logic as original data)
- Labels them as "scam" and appends to combined_scam_dataset.csv
- Saves an updated combined_scam_dataset.csv (backup of old one is also saved)
"""

import pandas as pd
from red_flags import detect_red_flags


combined_df = pd.read_csv("data/combined_scam_dataset.csv")
print("Existing dataset size:", len(combined_df))


synthetic_df = pd.read_csv("synthetic_scam_messages.csv")
print("New synthetic messages:", len(synthetic_df))


red_flag_rows = synthetic_df["text"].apply(detect_red_flags).apply(pd.Series)


synthetic_df["label"] = "scam"


final_synthetic_df = pd.concat([synthetic_df[["label", "text"]], red_flag_rows], axis=1)

print("\nRed flag counts in new synthetic data:")
print(red_flag_rows.sum())


combined_df.to_csv("data/combined_scam_dataset_backup.csv", index=False)


updated_df = pd.concat([combined_df, final_synthetic_df], ignore_index=True)
updated_df.to_csv("data/combined_scam_dataset.csv", index=False)

print("\nUpdated dataset size:", len(updated_df))
print("Updated label distribution:")
print(updated_df["label"].value_counts())
print("\nSaved: combined_scam_dataset.csv (updated)")
print("Backup saved: combined_scam_dataset_backup.csv (original, just in case)")