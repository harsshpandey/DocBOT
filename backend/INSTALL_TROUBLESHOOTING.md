# Installation Troubleshooting

## Network Timeout Issues

If you're getting timeout errors when installing `sentence-transformers`, try these solutions:

### Solution 1: Increase pip timeout (Recommended)

```powershell
pip install --default-timeout=100 sentence-transformers
```

Or for all requirements:
```powershell
pip install --default-timeout=100 -r requirements.txt
```

### Solution 2: Install with retries

```powershell
pip install --retries 5 --timeout 100 sentence-transformers
```

### Solution 3: Install just sentence-transformers first

Sometimes installing the large package separately helps:

```powershell
pip install sentence-transformers
```

Then install the rest:
```powershell
pip install -r requirements.txt
```

### Solution 4: Use a different PyPI mirror

If you're in a region with slow PyPI access, try a mirror:

**China (if applicable):**
```powershell
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple sentence-transformers
```

**Or use pip config:**
```powershell
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### Solution 5: Install dependencies separately

If the full install fails, install in smaller chunks:

```powershell
pip install torch --default-timeout=100
pip install transformers --default-timeout=100
pip install sentence-transformers --default-timeout=100
```

### Solution 6: Check your internet connection

- Make sure you have a stable internet connection
- Try downloading from a different network (mobile hotspot, etc.)
- Check if your firewall/proxy is blocking pip

### Solution 7: Use pip cache (if available)

If you've downloaded packages before, use cache:

```powershell
pip install --cache-dir .pip-cache sentence-transformers
```

## What sentence-transformers needs

The `sentence-transformers` package will automatically download:
- PyTorch (large, ~500MB-2GB depending on CPU/GPU version)
- Transformers library
- The actual model files (downloaded on first use, ~80MB for default model)

## Alternative: Manual download

If network issues persist, you can:
1. Download the wheel file manually from PyPI
2. Install from local file: `pip install sentence-transformers-2.2.2-py3-none-any.whl`

## After successful installation

Once `sentence-transformers` is installed, the embedding model will download automatically on first use. This is a one-time download (~80MB).

