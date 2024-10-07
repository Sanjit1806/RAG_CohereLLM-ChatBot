# Retrieval Augmented Generation using Cohere LLM

PDF-based Question Answering RAG System using Cohere LLM. This project uses **Cohere's Large language Model** to extract, embed, and search through text from PDF files. It enables users to ask questions based on the content of the PDF and receive answers using embeddings and search indexing techniques.

## Project Structure

```bash
📂 project-folder
├── 📂 implementation
│   ├── imp_main.py
│   └── story.pdf
├── 📂 src
    ├── 📂 frontend
    │   ├── ask.html
    │   ├── index.html
    │   └── style.css
    ├── app.py
    └── main.py
```

## Key Features

- **PDF Text Extraction**: Extracts text from a PDF using `PyPDF2`.
- **Text Embeddings**: Utilizes Cohere's API to generate embeddings for paragraphs of text.
- **Annoy Search Index**: Constructs an Annoy index to perform fast nearest neighbor searches on the embeddings.
- **Question Answering**: Uses Cohere's language model to generate context-aware answers to user queries.

## Requirements

- Python 3
- Libraries: `cohere`, `numpy`, `annoy`, `PyPDF2`, `flask`
- API key from [Cohere](https://cohere.ai)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/pdf-question-answering.git
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set your Cohere API key:
    Add your own Cohere API key during initialization

## Usage

### 1. Running Locally via Command Line

1. Specify the path to your PDF file in the `main.py`:
    ```python
    pdf_path = "/path/to/your/pdf_file.pdf"
    ```

2. Run the program:
    ```bash
    python imp_main.py
    ```

3. Enter a question when prompted:
    ```bash
    Enter the question: What is the main theme of the story?
    ```

### 2. Running the Web App using Flask

The project includes a basic frontend to ask questions through a web interface served using Flask.

1. Navigate to the `frontend` folder where the `app.py` is located.

2. Run the Flask app:
    ```bash
    python frontend/app.py
    ```

3. Open your web browser and go to `http://127.0.0.1:5000`.

## Files

- **ask.html**: A form to input questions.
- **index.html**: Homepage.
- **style.css**: Styling for the web interface.
- **app.py**: Backend for handling the web requests.
- **main.py**: Contains all the relavent functions to extract, embed, and search

## Technologies Used

- **Cohere**: For generating embeddings and interacting with the language model.
- **Annoy**: For fast nearest neighbor search in high-dimensional spaces.
- **PyPDF2**: For extracting text from PDFs.
- **HTML/CSS**: For the web-based frontend.

---

Developed by [github.com/Sanjit1806](https://github.com/Sanjit1806)
