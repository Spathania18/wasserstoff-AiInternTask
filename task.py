# %%
# Import necessary libraries
import requests
import pdfplumber
import json
import os
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor


# %%
# Load JSON file with PDF links
with open('Dataset.json', 'r') as file:
    data = json.load(file)

# Extract the PDF URLs from the JSON
pdf_links = list(data.values())  # Extract all the links

# %%
print(pdf_links)  # This will print the list of URLs

# %%
import requests
import os

def download_pdf(url, save_dir):
    try:
        response = requests.get(url, verify=False)  # Disable SSL verification
        # Extract a safe filename from the URL
        file_name = os.path.join(save_dir, url.split("/")[-1].split("?")[0] + ".pdf")
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {file_name}")
        return file_name
    except requests.exceptions.SSLError as e:
        print(f"SSL Error occurred while downloading {url}: {e}")
    except Exception as e:
        print(f"Error occurred while downloading {url}: {e}")

# Directory to store downloaded PDFs
save_dir = 'pdf_documents/'
os.makedirs(save_dir, exist_ok=True)

# Download PDFs
for link in pdf_links:
    download_pdf(link, save_dir)

# %%
# Text extraction from the pdf files

import pdfplumber

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() + '\n'
        return text

# Extract text from all downloaded PDFs
for pdf_file in os.listdir(save_dir):
    pdf_path = os.path.join(save_dir, pdf_file)
    text = extract_text_from_pdf(pdf_path)
    print(f"Text extracted from {pdf_file}: \n{text[:500]}")  # Print the first 500 characters


# %%
# Example of the summarization technique using sklearn 

from sklearn.feature_extraction.text import TfidfVectorizer

def extract_keywords(text, num_keywords=5):
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    dense = vectors.todense()
    keyword_indices = dense[0].argsort()[-num_keywords:][::-1]
    keywords = [feature_names[idx] for idx in keyword_indices]
    return keywords

# Example of summarizing and extracting keywords for each PDF
for pdf_file in os.listdir(save_dir):
    pdf_path = os.path.join(save_dir, pdf_file)
    text = extract_text_from_pdf(pdf_path)
    summary = text[:1000]  # This is just an example, you can implement a better summarizer
    keywords = extract_keywords(text)
    print(f"Summary for {pdf_file}:\n{summary[:300]}...\n")
    print(f"Keywords for {pdf_file}: {keywords}")


# %%
import os
import requests
from pymongo import MongoClient
import spacy
import numpy as np
import PyPDF2
from collections import Counter

# Initialize spaCy
nlp = spacy.load("en_core_web_sm")

# Set up MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['pdf_database']
collection = db['pdf_summaries']

def extract_text_from_pdf(pdf_path):
    # Check if the path is a URL or local file
    if pdf_path.startswith('http'):
        # Download PDF
        response = requests.get(pdf_path)
        with open('temp.pdf', 'wb') as f:
            f.write(response.content)
        pdf_path = 'temp.pdf'  # Update to the temporary file
    
    # Extract text from the PDF
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ''
        for page in reader.pages:
            text += page.extract_text() or ''
    return text

def summarize_text(text):
    # Tokenize and filter sentences
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    
    # Simple summarization by selecting the first few sentences
    summary = ' '.join(sentences[:3])  # Change the number of sentences as needed
    return summary

def extract_keywords(text, limit=20):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    # Extract keywords (nouns and proper nouns)
    keywords = [token.lemma_ for token in doc if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop]

    # Get the most common keywords, limited to the specified number
    most_common_keywords = [word for word, freq in Counter(keywords).most_common(limit)]
    
    return most_common_keywords

def save_to_mongodb(filename, summary, keywords, file_size, file_path):
    document = {
        'filename': filename,
        'summary': summary,
        'keywords': keywords,
        'file_size': file_size,
        'file_path': file_path
    }
    collection.insert_one(document)
    print(f"Saved {filename} to MongoDB.")

# Directory to save PDFs and process them
save_dir = r'C:\Users\spath\OneDrive\Desktop\task\pdf_documents'  # Change this to your actual directory

# Save summaries and keywords to MongoDB
for pdf_file in os.listdir(save_dir):
    pdf_path = os.path.join(save_dir, pdf_file)
    if pdf_file.endswith('.pdf'):
        text = extract_text_from_pdf(pdf_path)
        summary = summarize_text(text)
        keywords = extract_keywords(text)
        
        # Get file size in bytes
        file_size = os.path.getsize(pdf_path)
        
        # Save to MongoDB including metadata
        save_to_mongodb(pdf_file, summary, keywords, file_size, pdf_path)

# Clean up the temporary file
if os.path.exists('temp.pdf'):
    os.remove('temp.pdf')

# %%


