## About This README

This README walks you through the project’s file structure, explaining the key components, important files, and core operations that make up the project workflow.

## Project Structure

Part1/
├── Colab_Jupyter(ipynb)/          # Contains guide for running in Google Colab
│ ├── How-To-Run(ipynb).pdf        # Instructions to set up and run Part1.ipynb in Colab
│ └── Part1.ipynb                  # Main Colab notebook for this project
├── content.rar                    # Must be uploaded in Colab environment for Part1.ipynb to work
├── data/                          # Stores processed outputs for building FAISS index
│ ├── faiss_index/                 # Final vector index powering the RAG chatbot
│ ├── direction_final.txt          # Final output from enhance.py
│ └── handbook_cleaned.txt         # Final output from extract_gitlab_handbook_structured.py
├── Data_Acquisition/                 # Scripts to collect and process source data
│ ├── GitLab_Direction/               # Handles scraping GitLab direction docs
│ │ ├── enhance.py                    # Combines raw_direction.txt + direction_cleaned.txt → direction_final.txt
│ │ └── extract_gitlab_direction.py   # Extracts GitLab direction docs
│ ├── GitLab_Handbook/                # Handles processing GitLab handbook docs
│ │ ├── comp.py                       # Compares handbook_cleaned_FULL.txt → handbook_cleaned.txt
│ │ └── extract_gitlab_handbook_structured.py       # Generates handbook_cleaned.txt
│ └── raw_data/                                     # Raw scraped data before cleaning
│ ├── Direction/                                    # Stores raw and intermediate direction files
│ │ ├── direction_cleaned.txt                       # Cleaned version of raw GitLab direction data
│ │ └── raw_direction.txt              # Unprocessed GitLab direction data from scraping
│ └── Handbook/                        # Stores raw handbook files
├── content/                           # Downloaded intermediate outputs used in building FAISS index
├── handbook_cleaned_FULL.txt          # Full cleaned handbook used for comparison in comp.py
├── build_vector_store.py              # Builds FAISS index from final direction + handbook files
├── Code-snippets-explaination.md      # Notes explaining code snippets
├── Part1_report.docx                  # Report to be submitted to faculty
└── Readme.md                          # Project documentation



### **RAG Bot Project: Part 1 - Data Acquisition & Vector Store Creation**

This repository contains the foundational components for a Retrieval-Augmented Generation (RAG) bot. The project's primary goal is to acquire, process, and index documentation from **Gitlab's Direction and Handbook**, creating a **FAISS vector index** for efficient semantic search. The entire workflow is designed for reproducibility within a **Google Colab** environment.



## **1. Core Project Directories**

### `Part1/`
This is the project's root directory, encapsulating all the code, data, and documentation for this initial phase of the RAG bot's development. Its name, "Part1," suggests a modular approach to a larger project, focusing specifically on the crucial steps of data preparation and indexing.

### `Colab_Jupyter(ipynb)/`
This directory is critical for project execution, as it’s designed to run within the Google Colab environment. The files here ensure the project is easily reproducible by others.

* `Part1.ipynb`: This is the **master notebook**. It's the central hub that orchestrates the entire workflow. Its importance lies in its ability to run all scripts sequentially, manage dependencies, and display real-time output, making the project transparent and interactive.
* `How-To-Run(ipynb).pdf`: A vital piece of documentation that provides a step-by-step guide for setting up and running the main notebook. Its presence makes the project accessible to users who may not be familiar with the specific setup.
* `content.rar`: A compressed archive containing necessary files, likely including the raw data acquisition scripts and any other assets required by `Part1.ipynb`. Its purpose is to bundle all dependencies so the user can upload a single file to the Colab environment to get started.

### `data/`
This directory is the project's data repository, storing both the raw data and the final, processed outputs.

#### `faiss_index/`
This is the most crucial output directory. It's named after the **FAISS (Facebook AI Similarity Search)** library, a high-performance vector search engine.
* `direction_final.txt`: This file represents the final, cleaned, and enhanced data derived from the Gitlab Direction documentation. Its importance lies in being a high-quality, structured text file that is ready for embedding and indexing.
* `handbook_cleaned.txt`: The final, refined text from the Gitlab Handbook. Like its counterpart, it is a polished document ready for the next stage of the pipeline.

#### `Data_Acquisition/`
This is the data engineering hub of the project, housing all the scripts responsible for the **Extract, Transform, Load (ETL)** process.

* `GitLab_Direction/`: A sub-module dedicated to scraping and processing data from the Gitlab Direction source.
* `extract_gitlab_direction.py`: This Python script is the **workhorse of the data pipeline**. It uses web scraping techniques to pull unstructured text from the source, laying the foundation for all subsequent processing.
* `enhance.py`: A vital **transformation script**. Its role is to take the initial cleaned text and apply further refinements, such as normalization, entity recognition, or restructuring, to produce the final, high-quality data.
* `GitLab_Handbook/`: A parallel sub-module for the Gitlab Handbook, highlighting the project's ability to handle multiple data sources.
* `extract_gitlab_handbook_structured.py`: This script is specialized for the handbook, likely designed to maintain the structured nature of the source (e.g., sections, headers, and bullet points) to improve the quality of the final vector embeddings.
* `comp.py`: This script's purpose is to **compare** the initially cleaned handbook data (`handbook_cleaned_FULL.txt`) against a set of rules or a standard, ensuring consistency and accuracy before the data is finalized.

***

## **2. Key Scripts and Documentation**

### `build_vector_store.py`
This is the final and arguably most important script in the entire data pipeline. It takes the two refined text files (`direction_final.txt` and `handbook_cleaned.txt`) as input. Its job is to:
* Use a pre-trained **SentenceTransformer** model to convert the text into dense numerical vectors (**embeddings**).
* Index these vectors using the **FAISS library**, creating a highly optimized, searchable index.
The importance of this script is that it transforms raw text data into an **efficient knowledge base** that can be queried in milliseconds, forming the backbone of the RAG system.

### `Part1_report.docx`
This file serves as the formal project report. It details the methodologies, challenges, and outcomes of the project's first phase. Its purpose is to provide a professional summary for academic or professional review, showcasing the technical work performed.

### `Code-snippets-explanation.md`
This is a supplementary documentation file. It provides in-depth explanations of specific, complex code snippets used throughout the project. Its importance lies in enhancing the project's readability and providing clarity on key algorithms or functions.

