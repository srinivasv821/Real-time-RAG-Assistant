print("Starting test_chroma.py")

from app.services.chroma_service import similarity_search

print("Imported similarity_search")

query = "main topic of the document"
results = similarity_search(query, top_k=1)

print("Results type:", type(results))
print("Results length:", len(results))

print("Results raw:", results)

for r in results:
    print("----")
    print("Metadata:", r["metadata"])
    print("Text preview:", r["text"][:300])

