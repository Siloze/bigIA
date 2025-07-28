from web import web_search_and_extract
from history import get_last_messages
from rag import RAG, encode_chunks
from memory import init_semantic_memory_faiss

def generate_prompt_web(question: str, rag_class: RAG):
    docs = web_search_and_extract(question)
    data = []
    for doc in docs:
        print("content" + doc['content'])
        doc_name = doc['url']
        doc_content = doc['content']
        data.append({'name': doc_name, 'content': doc_content})

    web_rag = RAG(data, embedder= rag_class.embedder)
    web_rag_retreive_number = 1
    web_rag_prompt="Tu as des informations trouvé sur des sites internet, utilises les seulement si elles permettent de t'aider a répondre à la question posée. Sinon, n'en fais pas usage et n'en fais pas mention."
    
    question_embedding = encode_chunks(web_rag.embedder, [question])

    #Get sementic search from RAG data
    distances, rag_indices = web_rag.index.search(question_embedding, web_rag_retreive_number)
    rag_retrieved = [(web_rag.chunks[i]) for i in rag_indices[0]]

    rag_context = "\n\n---\n\n".join(txt for txt in rag_retrieved)

    return f"{web_rag_prompt}\n{rag_context}\n"

def generate_prompt_file(file_str: str, filename: str):
    return  f"Voici le contenue du fichier attaché à la demande, lis le et traite la question par rapport au contenue:\n{filename}\n{file_str}"

def generate_direct_memory_prompt(memory_prompt: str, memory_count: int, chat_id: int = 0) :
    if (memory_count > 0):
        last_mess = get_last_messages(chat_id, n=memory_count)
        for message in last_mess:
            question = message['question']
            answer = message['answer']
            memory_prompt = memory_prompt + "\n------\n" + "Question: " + question + "\nTa réponse: " + answer
        if (len(last_mess)):
            return memory_prompt + "\n------\n"
    return ""

def generate_semantic_memory_prompt(question: str, rag: RAG, memory_prompt: str, memory_count: int):
    if (memory_count > 0):
        question_embedding = encode_chunks(rag.embedder, [question])
        memory_index, memory_chunks = init_semantic_memory_faiss(rag.embedder)
        distances, memory_indices = memory_index.search(question_embedding, memory_count)
        memory_retrieved = [(memory_chunks[i]) for i in memory_indices[0]]

        #memory_prompt = "Voici des extraits de conversations que tu as eux avec l'utilisateur qui peuvent etre pertinent pour répondre."
        memory_context = "\n\n---\n\n".join(txt for txt in memory_retrieved)    
        return f"{memory_prompt}\n{memory_context}\n"
    return ""

def generate_rag_prompt(question: str, rag: RAG, rag_prompt: str, rag_count: int):
    if rag_count > 0:
        rag_retreive_number = rag_count
        question_embedding = encode_chunks(rag.embedder, [question])

        distances, rag_indices = rag.index.search(question_embedding, rag_retreive_number)
        rag_retrieved = [(rag.chunks[i]) for i in rag_indices[0]]
        rag_context = "\n\n---\n\n".join(txt for txt in rag_retrieved)
        return f"{rag_prompt}\n{rag_context}\n"
    return ""

def generate_final_prompt(full_prompt: str, question: str):
    full_prompt = f"[INST] {full_prompt}\n\nVoici la question: {question} [/INST]"
    return full_prompt





   
