# QUICK COMMANDS - Recursive Logic Engine

## ⚡ FASTEST PATH (10 minutes total)

```bash
# Setup (1 min)
cd recursive-logic-engine
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Data (30 sec)
python scripts/download_datasets.py

# Train (5 min with demo data)
python scripts/train.py --config config/train.yaml

# Evaluate (1 min)
python scripts/evaluate.py --checkpoint outputs/checkpoints/best_model.pt

# Analyze (30 sec)
python scripts/analyze_results.py --output-dir outputs
```

---

## 📥 SETUP

```bash
# 1. Virtual environment
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Verify installation
python -c "import torch; print(torch.__version__)"
```

---

## 📊 DATA

```bash
# Prepare datasets
python scripts/download_datasets.py

# Check what was created
ls -la data/
cat data/logic_puzzles.jsonl | head -1
```

---

## 🧠 TRAINING

```bash
# Train with default config
python scripts/train.py --config config/train.yaml

# Train on CPU (if no GPU)
python scripts/train.py --config config/train.yaml --device cpu

# Train with custom config
python scripts/train.py --config your_config.yaml

# Multi-GPU training (4 GPUs)
torchrun --nproc_per_node=4 scripts/train.py --config config/train.yaml
```

---

## 📈 EVALUATION

```bash
# Evaluate best model
python scripts/evaluate.py --checkpoint outputs/checkpoints/best_model.pt

# View results
cat outputs/self_correction_traces.json | python -m json.tool
cat outputs/accuracy_table.json | python -m json.tool
```

---

## 📊 ANALYSIS

```bash
# Analyze results
python scripts/analyze_results.py --output-dir outputs

# View analysis report
cat outputs/analysis.log

# View specific metrics
grep "reward=" outputs/training.log
```

---

## 🐳 DOCKER

```bash
# Build image
docker build -t yourusername/recursive-logic-engine:latest -f docker/Dockerfile .

# Local development
docker-compose -f docker/docker-compose.yml up

# Run training in container
docker run -it --gpus all -v $(pwd):/app yourusername/recursive-logic-engine:latest \
  python scripts/train.py

# Push to Docker Hub
docker login
docker push yourusername/recursive-logic-engine:latest
```

---

## 🚀 GITHUB DEPLOYMENT

```bash
# Initialize git
cd recursive-logic-engine
git init

# Add files
git add .

# Commit
git commit -m "Initial commit: Recursive Logic Engine - GRPO + RLVR training system"

# Add remote (HTTPS)
git remote add origin https://github.com/YOUR_USERNAME/recursive-logic-engine.git

# Push
git branch -M main
git push -u origin main

# Create release
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0
```

---

## 🔧 MAKEFILE (Shorthand)

```bash
make help              # See all commands
make install           # Install dependencies
make download-data     # Prepare datasets
make train             # Train model
make eval              # Evaluate
make trace             # Generate traces
make analyze           # Analyze results
make clean             # Clean build artifacts
```

---

## 🧪 TESTING

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_training.py::test_grpo -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

---

## 📚 DOCUMENTATION

```bash
# View README
cat README.md | less

# View Architecture
cat ARCHITECTURE.md | less

# View Quick Start
cat QUICKSTART.md | less

# Search documentation
grep -r "GRPO" *.md
```

---

## 🔍 DEBUGGING

```bash
# Check Python version
python --version

# Check installed packages
pip list

# Check CUDA
python -c "import torch; print(torch.cuda.is_available())"

# Check GPUs
nvidia-smi

# View config
cat config/train.yaml

# Count lines of code
find src -name "*.py" | xargs wc -l | tail -1
```

---

## 📊 MONITORING

```bash
# View logs
tail -f outputs/training.log

# View last 50 lines
tail -50 outputs/training.log

# Extract metrics
grep "reward=" outputs/training.log

# Monitor GPU
watch -n 1 nvidia-smi

# Check memory
free -h

# Check disk
df -h
```

---

## ☁️ CLOUD DEPLOYMENT

### AWS ECR
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com
docker tag yourusername/recursive-logic-engine:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/recursive-logic-engine:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/recursive-logic-engine:latest
```

### Google Cloud Run
```bash
gcloud auth configure-docker
docker tag yourusername/recursive-logic-engine:latest gcr.io/your-project-id/recursive-logic-engine:latest
docker push gcr.io/your-project-id/recursive-logic-engine:latest
gcloud run deploy recursive-logic-engine --image gcr.io/your-project-id/recursive-logic-engine:latest --platform managed --region us-central1
```

### Azure Container Registry
```bash
az acr login --name youracregistry
docker tag yourusername/recursive-logic-engine:latest youracregistry.azurecr.io/recursive-logic-engine:latest
docker push youracregistry.azurecr.io/recursive-logic-engine:latest
```

---

## 🆘 TROUBLESHOOTING

```bash
# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall

# Run on CPU (if GPU issues)
python scripts/train.py --config config/train.yaml --device cpu

# Clean Docker
docker system prune -a

# Clean Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Check what's taking space
du -sh * | sort -hr

# Git config
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
```

---

## ⭐ MOST IMPORTANT COMMANDS

### To Train Locally:
```bash
python scripts/train.py --config config/train.yaml
```

### To Push to GitHub:
```bash
git init && git add . && git commit -m "Initial" && git remote add origin https://github.com/YOUR_USERNAME/recursive-logic-engine.git && git push -u origin main
```

### To Deploy Docker:
```bash
docker build -t you/recursive-logic-engine:latest -f docker/Dockerfile . && docker push you/recursive-logic-engine:latest
```

### To Evaluate:
```bash
python scripts/evaluate.py --checkpoint outputs/checkpoints/best_model.pt
```

---

## 📋 FULL WORKFLOW (Copy & Paste)

```bash
#!/bin/bash

# 1. Setup
cd recursive-logic-engine
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Data
python scripts/download_datasets.py

# 3. Train
python scripts/train.py --config config/train.yaml

# 4. Evaluate
python scripts/evaluate.py --checkpoint outputs/checkpoints/best_model.pt

# 5. Analyze
python scripts/analyze_results.py --output-dir outputs

# 6. GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/recursive-logic-engine.git
git branch -M main
git push -u origin main
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0

echo "✅ All done!"
```

---

**Save this and run step by step or use the workflow script!**
