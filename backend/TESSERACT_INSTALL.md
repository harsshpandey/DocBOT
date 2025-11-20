# Installing Tesseract OCR on Windows

Tesseract OCR is required for processing images (PNG, JPG, JPEG files) in DocBot.

## Option 1: Using Chocolatey (Recommended - Easiest)

If you have Chocolatey package manager installed:

```powershell
choco install tesseract
```

This automatically adds Tesseract to your PATH.

## Option 2: Manual Installation

1. **Download Tesseract:**
   - Go to: https://github.com/UB-Mannheim/tesseract/wiki
   - Download the Windows installer (e.g., `tesseract-ocr-w64-setup-5.x.x.exe`)

2. **Install:**
   - Run the installer
   - **Important:** During installation, check "Add to PATH" or note the installation path (usually `C:\Program Files\Tesseract-OCR`)

3. **Add to PATH (if not done during install):**
   - Open System Properties → Environment Variables
   - Add `C:\Program Files\Tesseract-OCR` to your PATH
   - Or add it via PowerShell:
     ```powershell
     [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\Tesseract-OCR", "User")
     ```

4. **Restart your terminal/PowerShell** after adding to PATH

## Option 3: Using Winget (Windows Package Manager)

If you have Windows 11 or Windows 10 with winget:

```powershell
winget install --id UB-Mannheim.TesseractOCR
```

## Verify Installation

After installation, verify Tesseract is in your PATH:

```powershell
tesseract --version
```

You should see version information. If you get "command not found", restart your terminal or add Tesseract to PATH manually.

## Note

- **PDF, DOCX, and TXT files work without Tesseract** - only images require it
- If you only need to process PDFs and documents, you can skip Tesseract installation
- The app will show a clear error message if you try to upload images without Tesseract installed

