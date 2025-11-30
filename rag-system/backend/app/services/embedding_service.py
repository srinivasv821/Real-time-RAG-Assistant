import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from InstructorEmbedding import INSTRUCTOR
import hashlib

# Load model once at startup
model = INSTRUCTOR("hkunlp/instructor-xl")

#Instruction for embedding
INSTRUCTION  = "Represent the passage for retrieval:"

def embed_text(text: str):
    vector = model.encode([[INSTRUCTION, text]])
    return vector[0].tolist()

def get_embedding_id(text: str):
    """Create a stable hash ID for debuplication."""
    return hashlib.md5(text.encode()).hexdigest()