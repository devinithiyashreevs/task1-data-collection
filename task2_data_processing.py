import pandas as pd

# STEP 1: Load data
df = pd.read_json("data/trends.json")
print(f"Loaded {len(df)} stories")

# STEP 2: Remove duplicates
df = df.drop_duplicates(subset=["post_id"])
print(f"After removing duplicates: {len(df)}")

# STEP 3: Remove missing values
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# STEP 4: Fix numbers
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce")

df = df.dropna(subset=["score", "num_comments"])

df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# STEP 5: Remove low score
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# STEP 6: Clean title
df["title"] = df["title"].str.strip()

# STEP 7: Save cleaned file
df.to_csv("data/trends_clean.csv", index=False)
print(f"Saved {len(df)} rows to data/trends_clean.csv")

# STEP 8: Show summary
print("\nStories per category:")
for cat, count in df["category"].value_counts().items():
    print(cat, count)