# Code Snippets and Line-by-Line Explanation

This document breaks down every important part of the code to help you understand exactly how this AI chatbot works. We'll go through both main files: the vector store builder and the chat application.

## File 1: extract_gitlab_direction.py - The Data Scraping Engine

## Import libraries
```
import requests
from bs4 import BeautifulSoup
import os

```

- **Line 1** : Lets us download webpages from the internet.
- **Line 2** : Lets us read & clean messy HTML code into plain text.
- **Line 3** :lets us work with files and folders on your computer.

**What would happen if we used something else:**
- Without requests → you cannot fetch the webpage.
- Without BeautifulSoup → you cannot clean the HTML.
- Without os → you cannot create folders or manage files.

## Define Url
```
url = "https://about.gitlab.com/direction/"
output_file = "Part1/data/Direction/direction_cleaned.txt"
os.makedirs("Part1/data/Direction", exist_ok=True)
```

- **Line 1** : Stores the website link we want to scrape in a variable.
- **Line 2** : Stores the location & name of the file where we’ll save the cleaned text.
- **Line 3** :Creates the folder if it doesn’t already exist. exist_ok=True  means don’t crash if the folder already exists.
# Download the Page
```
response = requests.get(url)
response.raise_for_status()
```
- **Line 1** : Downloads the webpage stored in url.
- **Line 2** : Checks if the download worked. If the site is down or URL is wrong, it stops the program with an error instead of saving garbage.

# Removing Useless elements from the Scraped data
```
def clean_html(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "footer", "header", "nav"]):
        tag.decompose()
    return soup.get_text(separator="\n", strip=True)

cleaned_text = clean_html(response.text)    

```
- **Line 1** : Defines a descriptive name for the function
- **Line 2** : Reads the raw HTML and turns it into a structured object.
- **Line 3-4** : Removes useless parts like scripts, styles, footers, headers, and navigation bars.
- **Line 5** : Extracts only visible text, separating lines with \n. 
- **Line 6** : Passes the downloaded HTML (response.text) into our clean_html function, and stores the cleaned plain text.

**What would happen if we used something else:**
- You’d just save messy, unreadable HTML instead of clean text.
- You’ll still have the webpage HTML, but not the cleaned version.

# Creats or opens a file
```
with open(output_file, "w", encoding="utf-8") as f:
    f.write("## SECTION: GitLab Direction Main Page\n\n")
    f.write(cleaned_text)

print(f"✅ Saved cleaned Direction content to: {output_file}")
```
- **Line 1** : "w" → write mode (overwrites if file already exists) and encoding="utf-8" → ensures all characters (like symbols, emojis, non-English letters) are saved properly.
- **Line 2-3** : f.write(...) → writes text into the file.First, it writes a title ## SECTION: GitLab Direction Main Page.Then, it writes the cleaned webpage text.
- **Line 4** : Prints a success message showing where the file was saved.


## File 2: enhance.py - Merge two GitLab Direction text files

This file takes two versions of text (a cleaned one and a raw one), removes junk, merges them, removes duplicates, and saves the result neatly.

---

## **What each line does**

```python
from pathlib import Path
import re
```
- **Line 1**: `from pathlib import Path` → imports a modern way to handle file paths (instead of plain strings).  
- **Line 2**: `import re` → imports **regular expressions** (patterns used to clean unwanted text).  

---

```python
# Input files
file1 = Path("Part1/Data_Acquisition/raw_data/Direction/direction_cleaned.txt")  
file2 = Path("Part1/Data_Acquisition/raw_data/Direction/raw_direction.txt")
```
- **Line 5**: Comment explaining that `file1` and `file2` are the input files.  
- **Line 6**: `file1 = Path(...)` → points to the first file (already cleaned, but maybe incomplete).  
- **Line 7**: `file2 = Path(...)` → points to the second file (raw dump, possibly has extra info but messy).  

---

```python
# Output file
output = Path("Part1/data/Direction/direction_final.txt")
output.parent.mkdir(exist_ok=True)
```
- **Line 10**: Comment → explains this is the final merged output file.  
- **Line 11**: `output = Path(...)` → defines the path for the final cleaned/merged text.  
- **Line 12**: `output.parent.mkdir(exist_ok=True)` → makes sure the **folder exists** before saving.  

---

```python
def clean_paragraph(para: str) -> str:
    para = para.strip()
    para = re.sub(r"\s+", " ", para)  # Normalize whitespace
    para = re.sub(r"©.*GitLab.*|Edit this page|Contact us|Get free trial", "", para, flags=re.IGNORECASE)
    para = para.strip("•")  # Clean bullets
    return para.strip()
```
- **Line 14**: Defines a function `clean_paragraph` to clean a single paragraph.  
- **Line 15**: `para.strip()` → removes spaces/newlines from start and end.  
- **Line 16**: `re.sub(r"\s+", " ", para)` → replaces multiple spaces/tabs/newlines with a **single space**.  
- **Line 17**: Removes common junk phrases like ©, “Edit this page”, “Contact us” etc.  
- **Line 18**: Removes stray bullet symbols (`•`).  
- **Line 19**: Returns the final cleaned paragraph.  

---

```python
def get_cleaned_paragraphs(text: str) -> set:
    paras = text.split("\n\n")
    return set(clean_paragraph(p) for p in paras if len(clean_paragraph(p)) > 50)
```
- **Line 21**: Defines a function `get_cleaned_paragraphs` to split a big text into cleaned paragraphs.  
- **Line 22**: Splits text into paragraphs wherever there are **two newlines** (`\n\n`).  
- **Line 23**: Cleans each paragraph and keeps only those longer than 50 characters. Stores them in a **set** (which removes duplicates automatically).  

---

```python
# Load and process both files
text1 = file1.read_text(encoding="utf-8")
text2 = file2.read_text(encoding="utf-8")
```
- **Line 26**: Comment → says we are loading both input files.  
- **Line 27**: Reads the content of `file1` as plain text.  
- **Line 28**: Reads the content of `file2` as plain text.  


```python
paras1 = get_cleaned_paragraphs(text1)
paras2 = get_cleaned_paragraphs(text2)
```
- **Line 30**: Cleans & extracts paragraphs from the first file.  
- **Line 31**: Cleans & extracts paragraphs from the second file.  

---

```python
# Merge and deduplicate
merged_paras = sorted(paras1.union(paras2))
```
- **Line 33**: Comment → we are merging both sets.  
- **Line 34**: `paras1.union(paras2)` merges both sets and removes duplicates. `sorted()` arranges them in alphabetical order.  

---

```python
# Write final output
with open(output, "w", encoding="utf-8") as f:
    f.write("## SECTION: GitLab Direction (Enhanced)\n\n")
    f.write("\n\n".join(merged_paras))
```
- **Line 37**: Comment → explains this block writes the merged result.  
- **Line 38**: Opens the final file in **write mode** with UTF-8 encoding.  
- **Line 39**: Writes a header `## SECTION: GitLab Direction (Enhanced)` at the top.  
- **Line 40**: Joins all cleaned paragraphs with two newlines (`\n\n`) between them and writes them.  

---

```python
print(f"✅ Final merged Direction file saved to: {output}")
print(f"📄 Total unique, cleaned paragraphs: {len(merged_paras)}")
```
- **Line 42**: Prints a success message showing where the file was saved.  
- **Line 43**: Prints how many unique paragraphs were kept.  

---

## ⚡ What would happen if we used something else?

- **Path vs normal strings:**  
   If we used `"Final_partitions_of..."` instead of `Path(...)`, it would still work for simple cases, but `Path` makes things easier (joining paths, creating parent dirs).  

- **set vs list in `get_cleaned_paragraphs`:**  
   If we used a list, duplicates wouldn’t be removed. Using `set` ensures only unique paragraphs remain.  

- **sorted vs unsorted:**  
   If we didn’t use `sorted()`, paragraphs would appear in **random order** depending on how sets stored them.  

- **regex (`re.sub`) vs normal replace:**  
   If we used `.replace()`, it could only remove **exact words**, not patterns. Regex lets us remove multiple variations in one go (like “© GitLab 2024” or “Edit this page”).  

- **`len(p) > 50` filter:**  
   If we removed this, short junk lines (like “Contact us”) might still appear in the final file.  

---

# 📌 Script Explanation: `extract_gitlab_handbook_full.py`- Script to extract, clean, and combine all GitLab Handbook Markdown file

This script reads **all Markdown handbook files**, removes formatting, organizes them into **sections by file path**, merges them, and saves as one clean file.  

## **Code and Explanation**

```python
import os
import re
from pathlib import Path
```
- **Line 1**: `import os` → lets us interact with the operating system (like reading folders and joining file paths).  
- **Line 2**: `import re` → imports **regular expressions** to clean up text patterns.  
- **Line 3**: `from pathlib import Path` → a modern, cleaner way to handle file paths.  

# What If something else was used:*  
- Could use `glob` instead of `os.walk`, but it gives less control.  
- Could use plain string paths instead of `Path`, but `Path` is safer and more flexible.  

---

```python
HANDBOOK_DIR = "Part1/Data_Acquisition/raw_data/Handbook/content/handbook"
OUTPUT_FILE = "Part1/Data_Acquisition/data/Handbook/handbook_cleaned.txt"
```
- **Line 5**: Defines the folder containing the handbook Markdown files.  
- **Line 6**: Defines the path where the cleaned and merged output will be saved.  

# What if something else was used:*  
- If wrong path is given → script won’t find files.  
- If we didn’t define constants → paths would be repeated everywhere, making code messy.  

---

```python
def clean_markdown(text):
    # Remove YAML frontmatter
    text = re.sub(r"^---\s*\n.*?\n---\s*", "", text, flags=re.DOTALL | re.MULTILINE)
    # Remove image links
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
    # Convert links to just text
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
    # Inline code and bold/italic
    text = re.sub(r"`{1,3}(.*?)`{1,3}", r"\1", text)
    text = re.sub(r"[*_]{1,3}", "", text)
    text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)
    return text.strip()
```
- **Line 8**: Defines function `clean_markdown` to clean formatting from Markdown files.  
- **Line 9**: Removes **YAML metadata headers** (between `--- ... ---`).  
- **Line 11**: Removes image links (`![alt](url)`).  
- **Line 13**: Converts Markdown links `[text](url)` into just `text`.  
- **Line 15**: Removes inline code markers like `` `code` ``.  
- **Line 16**: Removes `*` or `_` used for bold/italic.  
- **Line 17**: Removes Markdown headings (`# Heading`).  
- **Line 18**: Returns cleaned text without extra spaces.  

# What if something else was used:*  
- Could use a Markdown library (`markdown` or `mistune`) to parse, but regex is faster and simpler here.  
- If we didn’t clean → final file would contain lots of formatting junk.  

---

```python
def get_logical_path(root, file):
    relative_path = os.path.relpath(os.path.join(root, file), HANDBOOK_DIR)
    return relative_path.replace("\\", "/")
```
- **Line 20**: Defines function `get_logical_path` to get the section path of each file relative to handbook folder.  
- **Line 21**: `os.path.relpath(...)` → makes the file path relative to `HANDBOOK_DIR`.  
- **Line 22**: Replaces `\` with `/` for consistency across OS.  

# What if something else was used:*  
- Could just use full path, but relative paths make sections cleaner.  
- Without `.replace(...)`, Windows paths would look messy with backslashes.  

---

```python
def extract_all_handbook():
    collected = []
    count = 0
    for root, _, files in os.walk(HANDBOOK_DIR):
        files = sorted(f for f in files if f.endswith(".md"))  # ✅ include everything
        for file in files:
            full_path = os.path.join(root, file)
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    raw = f.read()
                cleaned = clean_markdown(raw)
                section = get_logical_path(root, file)
                block = f"\n\n---\n## SECTION: {section}\n\n{cleaned}"
                collected.append(block)
                count += 1
            except Exception as e:
                print(f"❌ Failed to read {full_path}: {e}")

    print(f"✅ Processed {count} Markdown files.")
    return "\n".join(collected)
```
- **Line 24**: Defines function `extract_all_handbook` to scan and clean all files.  
- **Line 25**: `collected = []` → list to store cleaned content.  
- **Line 26**: Counter to track processed files.  
- **Line 27**: `os.walk(HANDBOOK_DIR)` → walks through all folders and files.  
- **Line 28**: Filters only `.md` files and sorts them alphabetically.  
- **Line 29-30**: Loops over each Markdown file.  
- **Line 31**: Creates the absolute path.  
- **Line 32-37**: Opens file, reads content, cleans it, finds section name, and formats it with heading.  
- **Line 38**: Adds cleaned block to list.  
- **Line 39**: Increments counter.  
- **Line 40-41**: If something fails, prints error message.  
- **Line 43**: Prints total processed files.  
- **Line 44**: Returns everything as one big string separated by `
`.  

# What if something else was used:*  
- Could use `glob.glob("**/*.md", recursive=True)` instead of `os.walk`, but `os.walk` is more flexible.  
- Without `try-except`, the whole script would crash if one file is unreadable.  
- Without sorting, file order would be random.  

---

```python
# Write to file
Path(os.path.dirname(OUTPUT_FILE)).mkdir(exist_ok=True)
output_text = extract_all_handbook()
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(output_text)
```
- **Line 47**: Comment → this part saves the result.  
- **Line 48**: Creates output folder if not already present.  
- **Line 49**: Runs the function to get all cleaned text.  
- **Line 50-51**: Opens output file and writes everything into it.  

# What if something else was used:*  
- Without `mkdir(exist_ok=True)` → script crashes if folder doesn’t exist.  
- If mode `"a"` instead of `"w"` was used, content would be appended instead of overwritten.  

---

```python
print(f"✅ Saved complete structured content to {OUTPUT_FILE}")
```
- **Line 53**: Prints confirmation that everything worked.  

# What if something else was used:*  
- Without it, program still works but user won’t know if saving succeeded.  

---

# File 4 : `compare_handbook_versions.py`  - Script to compare two versions of the GitLab Handbook by analyzing lines, words, sections, paragraphs, and similarity.
  
This script compares **two handbook versions** by counting lines, words, sections, paragraphs, and calculating a **similarity score**, making it easy to track content differences.  


---

## **Code and Explanation**

```python
from pathlib import Path
from difflib import SequenceMatcher
```
- **Line 1**: Imports `Path` from `pathlib` for easy file path handling.  
- **Line 2**: Imports `SequenceMatcher` to calculate similarity between two text files.  

# What if something else was used:*  
- Could use `os.path` instead of `pathlib`, but it's less modern and lacks convenient methods.  
- Could use `Levenshtein` distance for faster similarity, but `difflib` is built-in.  

---

```python
file1 = Path("Part1/Data_Acquisition/raw_data/Handbook/handbook_cleaned.txt")
file2 = Path("Part1/data/handbook_cleaned_FULL.txt")
```
- **Line 4–5**: Defines the paths of the two handbook files to be compared.  

# What if something else was used:*  
- Could use plain strings (`"path/to/file"`) but then need `open()` everywhere manually.  
- `Path` makes code more readable and supports methods like `.read_text()`.  

---

```python
def load_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
```
- **Line 7**: Defines `load_text()` to read a file with UTF-8 encoding.  
- **Line 8**: Opens file in read mode.  
- **Line 9**: Reads the entire content and returns it.  

# What if something else was used:*  
- Could directly use `Path(path).read_text()` (shorter).  
- Could omit `encoding="utf-8"`, but might cause issues with special characters.  

---

```python
text1 = load_text(file1)
text2 = load_text(file2)
```
- **Line 11–12**: Reads both files into string variables `text1` and `text2`.  

---

```python
lines1 = text1.splitlines()
lines2 = text2.splitlines()

words1 = text1.split()
words2 = text2.split()
```
- **Line 14–15**: Splits each text into a list of lines.  
- **Line 17–18**: Splits each text into a list of words using whitespace as a delimiter.  

# What if something else was used:*  
- Could use `split("\n")` for lines, but `splitlines()` handles all newline variations.  
- For words, could use `re.split()` for more control (e.g., punctuation handling).  

---

```python
print("🔍 Basic Stats:")
print(f"{file1.name}: {len(lines1)} lines | {len(words1)} words")
print(f"{file2.name}: {len(lines2)} lines | {len(words2)} words")
```
- **Line 20–22**: Prints basic statistics (line count & word count) for both files.  

---

```python
headers1 = set(line for line in lines1 if line.startswith("## SECTION:"))
headers2 = set(line for line in lines2 if line.startswith("## SECTION:"))
```
- **Line 25–26**: Extracts section headers starting with `"## SECTION:"`.  

# What if something else was used:*  
- Could use regex `re.findall(r"## SECTION:.*", text)` for more flexibility.  

---

```python
print("\n📁 Section Header Comparison:")
print(f"{file1.name}: {len(headers1)} sections")
print(f"{file2.name}: {len(headers2)} sections")
print(f"New sections added in FULL: {len(headers2 - headers1)}")
```
- **Line 28–31**: Prints section header counts and number of new sections in the second file.  

---

```python
paras1 = set(text1.split("\n\n"))
paras2 = set(text2.split("\n\n"))

common = paras1 & paras2
only_in_file1 = paras1 - paras2
only_in_file2 = paras2 - paras1
```
- **Line 34–36**: Splits both texts into paragraphs based on double newlines and converts them into sets.  
- **Line 38–40**: Finds common and unique paragraphs using set operations.  

# What if something else was used:*  
- Could use a more advanced paragraph segmentation algorithm (e.g., `nltk.sent_tokenize()`).  

---

```python
print("\n📄 Paragraph-Level Comparison:")
print(f"Common Paragraphs: {len(common)}")
print(f"Unique in {file1.name}: {len(only_in_file1)}")
print(f"Unique in {file2.name}: {len(only_in_file2)}")
```
- **Line 42–45**: Prints paragraph-level differences between the two files.  

---

```python
similarity = SequenceMatcher(None, text1, text2).ratio()
print(f"\n📊 Overall Text Similarity Score: {similarity:.4f}")
```
- **Line 48–49**: Computes and prints overall similarity score (0 = completely different, 1 = identical).  

# What if something else was used:*  
- Could use cosine similarity or Jaccard similarity for more nuanced text comparison.  

---




## File 1: build_vector_store.py - The Data Preparation Engine

This file takes raw text documents and transforms them into a searchable AI database.




### Import Section
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from pathlib import Path
```
**What each line does:**
- **Line 1**: Imports a smart text splitter that breaks documents into chunks while keeping related sentences together
- **Line 2**: Imports the system that converts text into mathematical vectors (embeddings) using HuggingFace models
- **Line 3**: Imports FAISS, a high-performance database for storing and searching through vectors
- **Line 4**: Imports Path for easy file handling

**What would happen if we used something else:**
- Without RecursiveCharacterTextSplitter, we might break sentences in the middle, making the AI give incomplete answers
- Without HuggingFace embeddings, we'd need to train our own model (extremely expensive and time-consuming)
- Without FAISS, simple keyword search would miss the meaning and context of questions 





### Loading the Documents
```python
handbook_text = Path("Part1/data/handbook_cleaned_FULL.txt").read_text(encoding="utf-8")
direction_text = Path("Part2/data/direction_final.txt").read_text(encoding="utf-8")
```

**What each line does:**
- **Line 1**: Reads the entire GitLab handbook (500,000+ words) into memory as a string
- **Line 2**: Reads GitLab's strategic direction document into memory

**What would happen if we used something else:**
- If we didn't specify `encoding="utf-8"`, special characters might display incorrectly
- If we tried to process the files line by line instead of loading completely, we'd lose the ability to understand context across paragraphs.






### Setting Up the Text Splitter
```python
splitter = RecursiveCharacterTextSplitter(
    chunk_size=750,
    chunk_overlap=150,
    length_function=len,
)
```

**What each line does:**
- **Line 1**: Creates an intelligent text splitter object
- **Line 2**: Sets each chunk to about 750 characters (roughly 150 words)
- **Line 3**: Makes chunks overlap by 150 characters to preserve context between chunks
- **Line 4**: Uses simple character counting to measure length

**What would happen if we used different numbers:**
- **Smaller chunk_size (300)**: More precise retrieval but might lose broader context
- **Larger chunk_size (1500)**: Better context but might include irrelevant information
- **No overlap (0)**: Risk of splitting important information across chunks
- **Too much overlap (400)**: Redundant information, slower search, higher costs

### The Chunking Function with Metadata
```python
def chunk_with_metadata(text, source_label):
    sections = text.split("## SECTION:")
    documents = []

    for section in sections:
        if not section.strip():
            continue
        header, *content = section.strip().split("\n", 1)
        body = content[0] if content else ""
        chunks = splitter.create_documents([body])
        for chunk in chunks:
            chunk.metadata = {
                "source": source_label,
                "section": header.strip()
            }
        documents.extend(chunks)
    return documents
```

**Breaking this down line by line:**

**Line 1**: Defines a function that takes text and a label for where it came from
**Line 2**: Splits the text at "## SECTION:" markers (this is how the documents are organized)
**Line 3**: Creates an empty list to store the processed document chunks

**Line 5**: Starts a loop through each section
**Line 6-7**: Skips empty sections to avoid processing nothing
**Line 8**: Separates the section header from the content using Python's unpacking
**Line 9**: Gets the body text, or empty string if there's no content
**Line 10**: Uses the text splitter to break the section into appropriately-sized chunks
**Line 11-15**: Adds metadata to each chunk so we know where it came from
**Line 16**: Adds all chunks from this section to our master list
**Line 17**: Returns all the processed documents

**What would happen with different approaches:**
- **Without metadata**: The AI couldn't tell users where information came from
- **Without section splitting**: Related information might be scattered across random chunks
- **Different splitting markers**: Would need to match how the source documents are actually formatted




### Creating the Documents
```python
handbook_docs = chunk_with_metadata(handbook_text, "handbook")
direction_docs = chunk_with_metadata(direction_text, "direction")
all_docs = handbook_docs + direction_docs
print(f"✅ Total chunks: {len(all_docs)}")
```
**What each line does:**
- **Line 1**: Processes the handbook text into searchable chunks tagged as "handbook"
- **Line 2**: Processes the direction text into searchable chunks tagged as "direction"
- **Line 3**: Combines both sets of documents into one master collection
- **Line 4**: Prints how many chunks were created (helps verify the process worked)




### Creating the Embeddings Model
```python
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
```

**What this line does:**
- Creates an embedding model that converts text into 384-dimensional vectors
- Uses a pre-trained model that's good at understanding sentence meaning
- This specific model is fast, lightweight, and works well for question-answering

**What would happen with different models:**
- **Larger models (all-mpnet-base-v2)**: Better accuracy but slower and more memory-intensive
- **Smaller models**: Faster but might miss subtle meaning differences
- **OpenAI embeddings**: More expensive, requires API calls, but might be more accurate  



### Creating and Saving the Vector Database
```python
vectordb = FAISS.from_documents(all_docs, embedding_model)
vectordb.save_local("data/faiss_index")
print("✅ FAISS index saved to: data/faiss_index/")
```
**What each line does:**
- **Line 1**: Creates a FAISS vector database from all documents using the embedding model
- **Line 2**: Saves the database to disk so we don't have to rebuild it every time
- **Line 3**: Confirms the save was successful

**What's happening behind the scenes:**
1. Each text chunk gets converted to a 384-dimensional vector
2. FAISS builds an index that allows fast similarity search
3. The index and metadata get saved as files on disk

---