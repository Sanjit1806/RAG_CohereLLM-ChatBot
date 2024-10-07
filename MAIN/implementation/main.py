import cohere
import numpy as np
from annoy import AnnoyIndex
import PyPDF2
import warnings

warnings.filterwarnings('ignore')

# Initialize Cohere client
co = cohere.Client("Enter Cohere API Key")

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        
        for page in range(len(reader.pages)):
            page_obj = reader.pages[page]
            text += page_obj.extract_text()
    return text


# clean up
def prepare_text(text):
    texts = text.split('\n\n')
    texts = np.array([t.strip(' \n') for t in texts if t])
    return texts

# Embedding
def embed_text(texts):
    response = co.embed(texts=texts.tolist()).embeddings
    embeds = np.array(response)
    return embeds

# Annoy Index
def build_annoy_index(embeds):
    search_index = AnnoyIndex(embeds.shape[1], 'angular')
    for i in range(len(embeds)):
        search_index.add_item(i, embeds[i])
    search_index.build(10)  
    return search_index

# Search relevant text
def search_text(query, search_index, texts):
    query_embed = co.embed(texts=[query]).embeddings

    similar_item_ids = search_index.get_nns_by_vector(query_embed[0], 10, include_distances=True)
    search_results = texts[similar_item_ids[0]]
    return search_results

# LLM model
def ask_llm(question, search_index, texts, num_generations=1):
    results = search_text(question, search_index, texts)
    context = results

    prompt = f"""
    Answer the question based only on the following context:

    {context}

    ---

    Answer the question based on the above context: {question}

    If the text doesn't contain the answer, 
    reply that the answer is not available.
    """
    # If the answer is not up to the mark, respond with "Answer not available."

    # Cohere LLM
    prediction = co.generate(
        prompt=prompt,
        max_tokens=70,
        model="command-nightly",
        temperature=0.5,
        num_generations=num_generations
    )

    return prediction.generations


if __name__ == "__main__":
    pdf_path = "Enter file path"

    extracted_text = extract_text_from_pdf(pdf_path)

    texts = prepare_text(extracted_text)

    embeds = embed_text(texts)

    search_index = build_annoy_index(embeds)

    question = input("Enter the question: ")

    results = ask_llm(question, search_index, texts)

    print(f"Answer: {results[0].text.strip()}")