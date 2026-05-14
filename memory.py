import uuid
import chromadb
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction

from config import CHROMA_PATH, CHROMA_COLLECTION, EMBEDDING_MODEL, OLLAMA_BASE_URL, MEMORY_SEARCH_LIMIT


class Memory:
    def __init__(self):
        self._client = chromadb.PersistentClient(path=CHROMA_PATH)
        self._embed = OllamaEmbeddingFunction(
            url=f"{OLLAMA_BASE_URL}/api/embeddings",
            model_name=EMBEDDING_MODEL,
        )
        self._collection = self._client.get_or_create_collection(
            name=CHROMA_COLLECTION,
            embedding_function=self._embed,
        )

    def store(self, user_input, reply):
        text = f"Augustin: {user_input}\nSarah: {reply}"
        self._collection.add(
            documents=[text],
            ids=[str(uuid.uuid4())],
        )

    def search(self, query):
        results = self._collection.query(
            query_texts=[query],
            n_results=min(MEMORY_SEARCH_LIMIT, self._collection.count()),
        )
        docs = results.get("documents", [[]])[0]
        return "\n\n".join(docs)
