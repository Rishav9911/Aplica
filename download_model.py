from sentence_transformers import SentenceTransformer

# Load and save model locally
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
model.save("local_model")  # Saves the model locally
print("✅ Model downloaded and saved in 'local_model' directory.")
