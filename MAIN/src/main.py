import PyPDF2
import cohere
import numpy as np
from annoy import AnnoyIndex

#Cohere API client
co = cohere.Client("Enter Cohere API Key")

texts = []
search_index = None


# Extract text from PDF
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in range(len(reader.pages)):
        page_obj = reader.pages[page]
        text += page_obj.extract_text()
    return text


def process_book(text):
    global texts, search_index

    # Clean up
    texts = text.split('\n \n')
    texts = np.array([t.strip() for t in texts if t])

    # Embedding
    embeddings = co.embed(texts=texts.tolist()).embeddings
    embeds = np.array(embeddings)

    # Annoy Index
    search_index = AnnoyIndex(embeds.shape[1], 'angular')
    for i in range(len(embeds)):
        search_index.add_item(i, embeds[i])
    search_index.build(10)


# Search relevant text
def search_text(query):
    query_embed = co.embed(texts=[query]).embeddings
    similar_item_ids = search_index.get_nns_by_vector(query_embed[0], 10)
    return texts[similar_item_ids[0]]

# Cohere LLM
def ask_question(question):
    context = search_text(question)

    prompt = f"""
    More information from the book: 

    {context}

    Question: {question}

    Provide the correct answer based on the content of the book.
    If the answer is not up to the mark, respond with "Answer not available.
    """

    response = co.generate(prompt=prompt, max_tokens=70, model="command-nightly", temperature=0.5)
    answer = response.generations[0].text.strip()
    
    return answer
