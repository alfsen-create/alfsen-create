index.html- coming-soon.png<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>MemoryChain – Personal AI Memory Vault</title>
  <style>
    body {
      font-family: 'Segoe UI', sans-serif;
      background: linear-gradient(to bottom, #0f0f0f, #1f1f1f);
      color: white;
      margin: 0;
      padding: 0;
      text-align: center;
    }
    header {
      padding: 80px 20px 20px;
    }
    h1 {
      font-size: 2.5rem;
      margin-bottom: 0.5rem;
      color: #6cf;
    }
    p {
      font-size: 1.2rem;
      max-width: 600px;
      margin: 0 auto 2rem;
      color: #ccc;
    }
    .button {
      background: #6cf;
      color: #000;
      padding: 0.8em 1.6em;
      font-weight: bold;
      border-radius: 8px;
      text-decoration: none;
      display: inline-block;
      margin-top: 20px;
    }
    .comingsoon {
      font-size: 1rem;
      color: #ff0;
      margin-top: 10px;
    }
    img.hero {
      max-width: 400px;
      width: 90%;
      margin: 40px auto;
    }
  </style>
</head>
<body>
  <header>
    <h1>🧠 MemoryChain</h1>
    <p>Encrypted, persistent, AI-friendly memory — on your terms.</p>
    <p><strong>Alpha by Louis Spires & ChatGPT</strong></p>
    <img class="hero" src="coming-soon.png" alt="Coming Soon" />
    <div class="comingsoon">Launching Summer 2025 · Free to explore · Built for Neural Labs</div>
    <a class="button" href="https://github.com/neurallabs-ai/memorychain-alpha" target="_blank">View Code on GitHub</a>
  </header>
</body>
</html>

.

<!---
alfsen-create/alfsen-create is a ✨ special ✨ repository because its `README.md` (this file) appears on your GitHub profile.
You can click the Preview link to take a look at your changes.
--->

## Local Memory Engine

This repository includes a lightweight REST API for storing and searching memories.

### Requirements
- Python 3.8+
- `flask`, `flask_cors`, `sentence-transformers`, `numpy`

### Usage
Run the server:

```bash
python alfred_transfer_api.py
```

Then POST conversations to `/api/memory`, search with `/api/search`, and prune old items with `/api/prune`.

