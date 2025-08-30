# utils/compare_handbook_versions.py

from pathlib import Path
from difflib import SequenceMatcher

#For similarity check
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

file1 = Path("Part1/Data_Acquisition/raw_data/Handbook/handbook_cleaned_FULL.txt")
file2 = Path("Part1/data/handbook_cleaned.txt")

def load_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

text1 = load_text(file1)
text2 = load_text(file2)

lines1 = text1.splitlines()
lines2 = text2.splitlines()

words1 = text1.split()
words2 = text2.split()

print("🔍 Basic Stats:")
print(f"{file1.name}: {len(lines1)} lines | {len(words1)} words")
print(f"{file2.name}: {len(lines2)} lines | {len(words2)} words")

# Unique section headers
headers1 = set(line for line in lines1 if line.startswith("## SECTION:"))
headers2 = set(line for line in lines2 if line.startswith("## SECTION:"))

print("\n📁 Section Header Comparison:")
print(f"{file1.name}: {len(headers1)} sections")
print(f"{file2.name}: {len(headers2)} sections")
print(f"New sections added in FULL: {len(headers2 - headers1)}")

# Paragraph-level uniqueness (basic)
paras1 = set(text1.split("\n\n"))
paras2 = set(text2.split("\n\n"))

common = paras1 & paras2
only_in_file1 = paras1 - paras2
only_in_file2 = paras2 - paras1

print("\n📄 Paragraph-Level Comparison:")
print(f"Common Paragraphs: {len(common)}")
print(f"Unique in {file1.name}: {len(only_in_file1)}")
print(f"Unique in {file2.name}: {len(only_in_file2)}")

# Overall similarity (optional)
vectorizer = TfidfVectorizer(max_features=5000)  # limit features for speed
tfidf = vectorizer.fit_transform([text1, text2])

cos_sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
print(f"\n📊 Cosine Similarity (TF-IDF): {cos_sim:.4f}")
