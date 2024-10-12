# PDF Processing Pipeline with Summarization and Keyword Extraction


# Project Overview
This project implements a custom pipeline that processes multiple PDF documents from a specified directory. It extracts the text content from the PDFs, generates domain-specific summaries, extracts the top 20 keywords, and stores the processed data in a MongoDB database. Additionally, the file metadata such as PDF size and file path are stored in the database.

The pipeline prioritizes efficiency, concurrency, and innovation, allowing it to handle PDFs of varying lengths and complexity.

# Features
Text Extraction: Extracts text from PDF documents.
Summarization: Generates a basic summary by extracting the first 1000 characters of text.
Keyword Extraction: Extracts the top 20 most relevant keywords using spaCy's NLP capabilities.
Metadata Storage: Stores additional metadata such as the file size and path.
MongoDB Integration: Saves the summary, keywords, and metadata to a MongoDB database.

# Project Structure
.
├── pdf_documents        # Directory where PDF files are stored
├── task.py      # Python script to run the pipeline
├── README.md            # Project documentation
├── requirements.txt     # Required dependencies
└── .gitignore           # Git ignored files and directories

# Prerequisites

Python 3.8+
MongoDB (Ensure MongoDB is installed and running locally or via cloud service)
Python Virtual Environment (optional but recommended)
Installation
Clone the repository:

git clone <your-repository-url>
cd <your-repository-directory>

Set up the virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install the dependencies:
pip install -r requirements.txt

Set up MongoDB:
Ensure you have MongoDB installed and running locally, or configure the connection to a MongoDB cloud service.

Place your PDF files:
Add the PDF documents you want to process inside the pdf_documents folder.

Usage
Run the pipeline:
To run the pipeline and process the PDFs, execute the following command:
task.py

The pipeline will:
Extract text from each PDF.
Generate a summary.
Extract the top 20 keywords.
Store the information in MongoDB along with metadata (file size and file path).

Viewing Results in MongoDB:
After running the pipeline, you can view the stored data in your MongoDB database. The MongoDB collection is pdf_summaries in the pdf_database.

Use a MongoDB client such as MongoDB Compass or connect via the shell:
mongo
use pdf_database
db.pdf_summaries.find().pretty()

Example MongoDB Document
json

{
    "_id": ObjectId("..."),
    "filename": "sample.pdf",
    "summary": "This is a sample summary of the extracted text...",
    "keywords": [
        "keyword1",
        "keyword2",
        "keyword3"
    ],
    "pdf_size": 102400, 
    "pdf_path": "path/to/sample.pdf"
}

# Configuration
Limit Keywords: By default, the pipeline extracts the top 20 keywords from each document. You can change this limit by modifying the limit argument in the extract_keywords() function within pdf_pipeline.py.
Dependencies

# The project relies on the following libraries:
pymongo
spacy
PyPDF2
collections
os
requests

# You can install all dependencies via:
pip install -r requirements.txt

# Troubleshooting
SSLError: If you encounter SSL certificate errors when downloading PDFs, ensure you have installed valid SSL certificates and consider using verify=False in the requests if necessary.
MongoDB Connection Issues: Check if MongoDB is running and properly configured. Ensure the connection string in pdf_pipeline.py points to your MongoDB instance.
# Limitations
The summarization is currently a simple truncation of the first 1000 characters. For more advanced summarization, you could integrate machine learning models like BART or T5.
The keyword extraction is based on a simple noun and proper noun extraction. Consider experimenting with more advanced NLP techniques for domain-specific keyword extraction.
# Future Improvements
Implement a more sophisticated summarization model.
Add support for parallel processing for increased speed with large document sets.
Improve the keyword extraction process using TF-IDF or topic modeling techniques.


# Contact
For any questions or suggestions, feel free to reach out at: [spathania18.sp@gmail.com].