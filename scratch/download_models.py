from fastembed import TextEmbedding, SparseTextEmbedding, LateInteractionTextEmbedding

def download():
    cache_dir = "./.fastembed_cache"
    print("Downloading dense model...")
    TextEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2", cache_dir=cache_dir)
    print("Downloading sparse model...")
    SparseTextEmbedding(model_name="Qdrant/bm25", cache_dir=cache_dir)
    print("Downloading colbert model...")
    LateInteractionTextEmbedding(model_name="colbert-ir/colbertv2.0", cache_dir=cache_dir)
    print("Done!")

if __name__ == "__main__":
    download()
