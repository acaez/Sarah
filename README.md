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

### 3. Créer le venv
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install mem0ai chromadb flask ollama
```

### 4. Lancer Sarah
```bash
cd app
python3 app.py
```

Ouvre `localhost:5001` dans le browser.
