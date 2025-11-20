# Migration to Local HuggingFace Embeddings

## What Changed

DocBot now uses **local HuggingFace embeddings** instead of Google's embedding API. This means:

✅ **No API quota limits** - embeddings run entirely on your machine  
✅ **No API costs** - completely free to use  
✅ **Works offline** - no internet needed for embeddings  
✅ **Privacy** - your documents never leave your machine for embeddings  

**Note:** The LLM (Gemini) still uses Google's API for generating answers, but embeddings are now local.

## Installation

1. **Install new dependencies:**
   ```powershell
   cd backend
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

   This will install `sentence-transformers` which includes the embedding models.

2. **First run will download the model:**
   - The first time you start the server, it will download the embedding model (~80MB)
   - This happens automatically - just wait for it to complete
   - The model is cached locally, so subsequent runs are instant

## Configuration

The default embedding model is `sentence-transformers/all-MiniLM-L6-v2`:
- **Size:** ~80MB
- **Speed:** Very fast
- **Quality:** Good for most use cases

### Alternative Models

You can change the model in your `.env` file:

```env
# Faster, smaller (default)
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Better quality, larger (~420MB)
EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2

# Multilingual support
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

### Using GPU (Optional)

If you have an NVIDIA GPU with CUDA, you can speed up embeddings:

1. Install CUDA-enabled PyTorch (sentence-transformers will handle this)
2. Update `backend/services/vector_store.py`:
   ```python
   model_kwargs={"device": "cuda"}  # instead of "cpu"
   ```

## What You Need to Do

1. **Update your `.env` file** (optional - defaults work fine):
   ```env
   EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
   ```

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Restart your server:**
   ```powershell
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Clear old vector store** (if you had documents indexed with Google embeddings):
   - The old embeddings won't work with the new model
   - Delete the `chroma_db` folder or use the `/documents` DELETE endpoint
   - Re-upload your documents

## Performance Notes

- **First document upload:** Slower (model loads + processes)
- **Subsequent uploads:** Fast (model stays in memory)
- **Query speed:** Very fast (local processing)
- **Memory usage:** ~200-500MB depending on model

## Troubleshooting

### Model download fails
- Check your internet connection (needed only for first download)
- The model downloads from HuggingFace Hub

### Out of memory errors
- Use the smaller model: `all-MiniLM-L6-v2`
- Reduce `CHUNK_SIZE` in your `.env` file
- Process fewer documents at once

### Slow performance
- Use the smaller model (`all-MiniLM-L6-v2`)
- Consider using GPU if available
- Reduce `CHUNK_SIZE` to process smaller chunks

## Benefits Summary

| Feature | Google Embeddings | Local HuggingFace |
|--------|------------------|-------------------|
| API Key Required | ✅ Yes | ❌ No |
| Quota Limits | ✅ Yes | ❌ No |
| Cost | 💰 Per request | 🆓 Free |
| Internet Required | ✅ Yes | ❌ No (after download) |
| Privacy | ⚠️ Data sent to Google | ✅ 100% local |
| Speed | Fast | Fast (local) |

Enjoy unlimited document processing! 🎉

