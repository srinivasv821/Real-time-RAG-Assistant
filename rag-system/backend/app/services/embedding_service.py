from InstructorEmbedding import INSTRUCTOR
import hashlib

# Load model once at startup
model = INSTRUCTOR("hkunlp/instructor-xl")

#Instruction for embedding
INSTRUCTION  = "Represent the passage for retrieval:"

def get_embedding(text: str):
    embedding = model.encode([[INSTRUCTION , text]])
    return embedding[0].tolist()

def get_embedding_id(text: str):
    """Create a stable hash ID for debuplication."""
    return hashlib.md5(text.encode()).hexdigest()