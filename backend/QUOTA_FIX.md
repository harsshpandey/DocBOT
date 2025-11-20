# Fixing Google Embeddings API Quota Error

## The Problem

You're seeing this error:
```
429 You exceeded your current quota
Quota exceeded for metric: generativelanguage.googleapis.com/embed_content_free_tier_requests, limit: 0
```

This means your Google Cloud project has **0 free tier requests** for embeddings, or you've exceeded the limit.

## Solutions

### Option 1: Enable Billing (Recommended for Production)

To get higher quotas, you need to enable billing in Google Cloud:

1. **Go to Google Cloud Console:**
   - Visit: https://console.cloud.google.com/

2. **Select your project** (or create one if you haven't)

3. **Enable the Generative AI API:**
   - Go to: https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com
   - Click "Enable"

4. **Enable Billing:**
   - Go to: https://console.cloud.google.com/billing
   - Link a billing account to your project
   - **Note:** Google provides free credits ($300) for new accounts

5. **Check Quota:**
   - Go to: https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas
   - Look for "Embed Content Requests" quotas
   - With billing enabled, you get much higher limits

### Option 2: Wait for Quota Reset

Free tier quotas typically reset:
- **Daily** (at midnight Pacific Time)
- **Monthly** (on the 1st of each month)

Check your current usage:
- https://ai.dev/usage?tab=rate-limit

### Option 3: Use a Different Google Cloud Project

If you have multiple Google accounts or projects:

1. Create a new Google Cloud project
2. Enable the Generative AI API
3. Generate a new API key
4. Update your `.env` file with the new key

### Option 4: Check API Key Permissions

Make sure your API key has the right permissions:

1. Go to: https://console.cloud.google.com/apis/credentials
2. Find your API key
3. Check that "Generative Language API" is enabled
4. Verify the key restrictions allow the API

## Pricing Information

Google's embedding API pricing (as of 2024):
- **Free tier:** Very limited (often 0 requests)
- **Paid tier:** ~$0.0001 per 1,000 characters
- **With billing enabled:** Much higher quotas

**Example costs:**
- 1,000 documents × 1,000 characters each = $0.10
- Very affordable for most use cases

## Temporary Workaround

While waiting for quota reset or setting up billing:

1. **Use the app for queries only** (if you already have documents indexed)
2. **Wait until quota resets** to upload new documents
3. **Enable billing** for immediate access

## Verify Your Setup

After enabling billing, test again:

```powershell
cd backend
python test_api_key.py
```

The embeddings test should pass if billing is enabled and quotas are available.

## Need Help?

- **Google Cloud Support:** https://cloud.google.com/support
- **API Documentation:** https://ai.google.dev/gemini-api/docs/rate-limits
- **Usage Dashboard:** https://ai.dev/usage?tab=rate-limit

