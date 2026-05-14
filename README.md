# Sarah

## Nouveau Mac — installation

### 0. Struture
mkdir Sarah

### 1. Cloner le repo
```bash
cd Sarah
git clone <ton-repo> app 
cd app
```

### 2. Installer Ollama
Télécharge sur ollama.com puis :
```bash
ollama pull mistral-nemo
ollama pull qwen3-embedding:4b
```

### 3. Installer Python 3.11
```bash
brew install python@3.11
```

### 4. Créer le venv
```bash
cd ..  # dans Sarah/
python3.11 -m venv venv
source venv/bin/activate
pip install flask ollama chromadb kokoro-onnx
```

### 5. Télécharger les modèles TTS
Lance Sarah une première fois — les fichiers sont déjà dans `app/tts-models/`.
Sur un nouveau Mac, il faudra les re-télécharger depuis HuggingFace ou les copier manuellement.

### 6. Lancer Sarah
```bash
cd app
python3 app.py
```

Ouvre `localhost:5001` dans le browser.
