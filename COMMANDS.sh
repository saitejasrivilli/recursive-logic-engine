#!/bin/bash
# RECURSIVE LOGIC ENGINE - COMPLETE COMMAND REFERENCE
# All commands needed to set up, run, deploy, and use the project

################################################################################
# 📥 SETUP & INSTALLATION COMMANDS
################################################################################

# 1. Clone or extract the project
cd /path/to/download
tar -xzf recursive-logic-engine.tar.gz
cd recursive-logic-engine

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Verify installation
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import transformers; print(f'Transformers: {transformers.__version__}')"

################################################################################
# 📊 DATA PREPARATION COMMANDS
################################################################################

# 1. Download/prepare datasets (creates sample data)
python scripts/download_datasets.py

# 2. Check data directory structure
ls -la data/

# 3. View dataset samples
head -5 data/logic_puzzles.jsonl
head -5 data/general_knowledge.jsonl

################################################################################
# 🧠 TRAINING COMMANDS
################################################################################

# 1. Train with default config (demo data - 5 minutes)
python scripts/train.py --config config/train.yaml

# 2. Train with custom config
python scripts/train.py --config custom_config.yaml

# 3. Train on CPU (if no GPU)
python scripts/train.py --config config/train.yaml --device cpu

# 4. Train with specific output directory
python scripts/train.py \
  --config config/train.yaml \
  --output-dir /path/to/outputs

# 5. Train with debugging (verbose output)
python scripts/train.py \
  --config config/train.yaml \
  -v

# 6. Multi-GPU training (4 GPUs)
torchrun --nproc_per_node=4 scripts/train.py --config config/train.yaml

################################################################################
# 📈 EVALUATION COMMANDS
################################################################################

# 1. Evaluate best model
python scripts/evaluate.py \
  --checkpoint outputs/checkpoints/best_model.pt

# 2. Evaluate with custom output directory
python scripts/evaluate.py \
  --checkpoint outputs/checkpoints/best_model.pt \
  --output-dir eval_results

# 3. Evaluate on CPU
python scripts/evaluate.py \
  --checkpoint outputs/checkpoints/best_model.pt \
  --device cpu

# 4. Generate self-correction traces
python scripts/benchmark_trace.py \
  --checkpoint outputs/checkpoints/best_model.pt

################################################################################
# 📊 ANALYSIS COMMANDS
################################################################################

# 1. Analyze training results
python scripts/analyze_results.py --output-dir outputs

# 2. Generate report with W&B integration
python scripts/analyze_results.py \
  --output-dir outputs \
  --wandb-project recursive-logic-engine

# 3. View generated traces
cat outputs/self_correction_traces.json | python -m json.tool

# 4. View accuracy table
cat outputs/accuracy_table.json | python -m json.tool

# 5. View analysis log
cat outputs/analysis.log

################################################################################
# 🐳 DOCKER COMMANDS
################################################################################

# 1. Build Docker image locally
docker build -t yourusername/recursive-logic-engine:latest \
  -f docker/Dockerfile .

# 2. Build with specific tag
docker build -t yourusername/recursive-logic-engine:v1.0.0 \
  -f docker/Dockerfile .

# 3. Local development with docker-compose
docker-compose -f docker/docker-compose.yml up

# 4. Local development with GPU support
GPU=0 docker-compose -f docker/docker-compose.yml up

# 5. Run training in container
docker run -it \
  --gpus all \
  -v $(pwd):/app \
  yourusername/recursive-logic-engine:latest \
  python scripts/train.py

# 6. Run evaluation in container
docker run -it \
  --gpus all \
  -v $(pwd):/app \
  yourusername/recursive-logic-engine:latest \
  python scripts/evaluate.py --checkpoint outputs/checkpoints/best_model.pt

# 7. Push to Docker Hub
docker login
docker push yourusername/recursive-logic-engine:latest
docker push yourusername/recursive-logic-engine:v1.0.0

# 8. Push to AWS ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

docker tag yourusername/recursive-logic-engine:latest \
  123456789.dkr.ecr.us-east-1.amazonaws.com/recursive-logic-engine:latest

docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/recursive-logic-engine:latest

# 9. Push to Google Container Registry
gcloud auth configure-docker
docker tag yourusername/recursive-logic-engine:latest \
  gcr.io/your-project-id/recursive-logic-engine:latest
docker push gcr.io/your-project-id/recursive-logic-engine:latest

# 10. Push to Azure Container Registry
az acr login --name youracregistry
docker tag yourusername/recursive-logic-engine:latest \
  youracregistry.azurecr.io/recursive-logic-engine:latest
docker push youracregistry.azurecr.io/recursive-logic-engine:latest

################################################################################
# 📝 GIT & GITHUB COMMANDS
################################################################################

# 1. Initialize git repository
cd recursive-logic-engine
git init

# 2. Add all files
git add .

# 3. Create initial commit
git commit -m "Initial commit: Recursive Logic Engine - GRPO + RLVR training system

- GRPO algorithm for variance reduction
- RLVR loss for training stability
- Quality filter for data pre-processing
- Catastrophic forgetting detection
- Production-grade architecture"

# 4. Add remote (HTTPS)
git remote add origin https://github.com/YOUR_USERNAME/recursive-logic-engine.git

# 5. Add remote (SSH - if configured)
git remote set-url origin git@github.com:YOUR_USERNAME/recursive-logic-engine.git

# 6. Push to GitHub
git branch -M main
git push -u origin main

# 7. Create version tag
git tag -a v1.0.0 -m "Initial release: GRPO + RLVR implementation"

# 8. Push tag to GitHub
git push origin v1.0.0

# 9. Push all tags
git push origin --tags

# 10. View remote
git remote -v

# 11. Check git status
git status

# 12. View commit history
git log --oneline

################################################################################
# 🔧 MAKEFILE COMMANDS (Shorthand)
################################################################################

# 1. View all available commands
make help

# 2. Install dependencies
make install

# 3. Download datasets
make download-data

# 4. Train the model
make train

# 5. Train with custom config
make train-custom CONFIG=path/to/config.yaml

# 6. Evaluate model
make eval

# 7. Generate traces
make trace

# 8. Analyze results
make analyze

# 9. Clean build artifacts
make clean

# 10. Clean everything (including data)
make clean-all

################################################################################
# 🧪 TESTING COMMANDS
################################################################################

# 1. Run all tests
pytest tests/ -v

# 2. Run specific test file
pytest tests/test_training.py -v

# 3. Run specific test function
pytest tests/test_training.py::test_grpo -v

# 4. Run with coverage
pytest tests/ --cov=src --cov-report=html

# 5. Run with verbose output
pytest tests/ -vv

# 6. Run with short summary
pytest tests/ -q

# 7. Run with parallel execution (faster)
pytest tests/ -n auto

# 8. Run specific test class
pytest tests/test_training.py::TestGRPO -v

# 9. Run with markers
pytest tests/ -m "not slow" -v

# 10. Run with timeout
pytest tests/ --timeout=300 -v

################################################################################
# 📚 DOCUMENTATION COMMANDS
################################################################################

# 1. View README
cat README.md | less

# 2. View Architecture guide
cat ARCHITECTURE.md | less

# 3. View Quick Start
cat QUICKSTART.md | less

# 4. Search in documentation
grep -r "GRPO" *.md

# 5. Generate documentation (if sphinx installed)
cd docs
make html

# 6. View generated docs
open docs/_build/html/index.html

################################################################################
# 🔍 INSPECTION & DEBUGGING COMMANDS
################################################################################

# 1. Check Python version
python --version

# 2. Check installed packages
pip list

# 3. Show installed torch version
python -c "import torch; print(torch.__version__)"

# 4. Check CUDA availability
python -c "import torch; print(torch.cuda.is_available())"

# 5. Check GPU info
nvidia-smi

# 6. Check available GPUs
python -c "import torch; print(f'GPUs: {torch.cuda.device_count()}')"

# 7. View config file
cat config/train.yaml

# 8. Pretty print YAML
python -c "import yaml; print(yaml.dump(yaml.safe_load(open('config/train.yaml'))))"

# 9. Check directory structure
tree -L 3 -I '__pycache__|*.pyc'

# 10. Count lines of code
find src -name "*.py" | xargs wc -l | tail -1

################################################################################
# 📊 MONITORING & LOGGING COMMANDS
################################################################################

# 1. View training logs
tail -f outputs/training.log

# 2. View last 50 lines of logs
tail -50 outputs/training.log

# 3. Search logs for specific metrics
grep "reward=" outputs/training.log

# 4. Extract metrics to CSV
grep "reward=" outputs/training.log | sed 's/.*reward=//; s/ .*//' > rewards.csv

# 5. Plot metrics (if matplotlib installed)
python -c "
import json
import matplotlib.pyplot as plt
with open('outputs/training.log') as f:
    lines = f.readlines()
    # Parse and plot
"

# 6. Monitor GPU during training
watch -n 1 nvidia-smi

# 7. Check memory usage
free -h

# 8. Monitor disk space
df -h

################################################################################
# 🌐 WEIGHTS & BIASES (W&B) COMMANDS
################################################################################

# 1. Login to W&B
wandb login

# 2. Set API key as environment variable
export WANDB_API_KEY=your_key_here

# 3. Enable offline mode
export WANDB_MODE=offline

# 4. Set project name
export WANDB_PROJECT=recursive-logic-engine

# 5. View W&B dashboard
open https://wandb.ai/your-username/recursive-logic-engine

# 6. Pull logged artifacts
wandb artifact get your-username/recursive-logic-engine/model:latest

# 7. Logout from W&B
wandb logout

################################################################################
# 🚀 CLOUD DEPLOYMENT COMMANDS
################################################################################

# AWS SAGEMAKER
# 1. Create training job
aws sagemaker create-training-job \
  --training-job-name recursive-logic-v1 \
  --role-arn arn:aws:iam::123456789:role/SageMakerRole \
  --algorithm-specification TrainingImage=123456789.dkr.ecr.us-east-1.amazonaws.com/recursive-logic-engine:latest

# GOOGLE CLOUD RUN
# 1. Deploy to Cloud Run
gcloud run deploy recursive-logic-engine \
  --image gcr.io/your-project-id/recursive-logic-engine:latest \
  --platform managed \
  --region us-central1 \
  --memory 16Gi \
  --timeout 3600

# AZURE CONTAINER INSTANCES
# 1. Deploy container
az container create \
  --resource-group myResourceGroup \
  --name recursive-logic-engine \
  --image youracregistry.azurecr.io/recursive-logic-engine:latest \
  --memory 16

################################################################################
# 🔄 COMMON WORKFLOWS
################################################################################

# WORKFLOW 1: Complete Setup & Training
echo "=== Setting up project ==="
cd recursive-logic-engine
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "=== Preparing data ==="
python scripts/download_datasets.py

echo "=== Starting training ==="
python scripts/train.py --config config/train.yaml

echo "=== Evaluating model ==="
python scripts/evaluate.py --checkpoint outputs/checkpoints/best_model.pt

echo "=== Analyzing results ==="
python scripts/analyze_results.py --output-dir outputs

echo "=== Done! ==="

# WORKFLOW 2: GitHub Deployment
echo "=== Pushing to GitHub ==="
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/recursive-logic-engine.git
git push -u origin main
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0
echo "=== On GitHub! ==="

# WORKFLOW 3: Docker Deployment
echo "=== Building Docker image ==="
docker build -t yourusername/recursive-logic-engine:latest -f docker/Dockerfile .

echo "=== Running in container ==="
docker run -it --gpus all -v $(pwd):/app yourusername/recursive-logic-engine:latest bash

echo "=== Pushing to Docker Hub ==="
docker login
docker push yourusername/recursive-logic-engine:latest
echo "=== On Docker Hub! ==="

# WORKFLOW 4: Cloud Deployment (AWS)
echo "=== Pushing to AWS ECR ==="
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com
docker tag yourusername/recursive-logic-engine:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/recursive-logic-engine:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/recursive-logic-engine:latest
echo "=== On AWS ECR! ==="

################################################################################
# 🎯 QUICK REFERENCE
################################################################################

# SHORTEST PATH TO RUNNING EVERYTHING:

# 1. Setup (1 minute)
cd recursive-logic-engine && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# 2. Data (30 seconds)
python scripts/download_datasets.py

# 3. Train (5 minutes with demo data)
python scripts/train.py --config config/train.yaml

# 4. Evaluate (1 minute)
python scripts/evaluate.py --checkpoint outputs/checkpoints/best_model.pt

# 5. Analyze (30 seconds)
python scripts/analyze_results.py --output-dir outputs

# 6. GitHub (2 minutes)
git init && git add . && git commit -m "Initial commit" && git remote add origin https://github.com/YOUR_USERNAME/recursive-logic-engine.git && git push -u origin main

# TOTAL TIME: ~10 minutes to setup, train (demo), evaluate, and deploy to GitHub!

################################################################################
# 📝 HELPFUL ALIASES (Add to ~/.bashrc or ~/.zshrc)
################################################################################

# Training shortcuts
alias train-demo="python scripts/train.py --config config/train.yaml"
alias train-cpu="python scripts/train.py --config config/train.yaml --device cpu"
alias train-full="python scripts/train.py --config config/train.yaml --device cuda"

# Evaluation shortcuts
alias eval-model="python scripts/evaluate.py --checkpoint outputs/checkpoints/best_model.pt"
alias analyze="python scripts/analyze_results.py --output-dir outputs"

# Docker shortcuts
alias docker-build="docker build -t yourusername/recursive-logic-engine:latest -f docker/Dockerfile ."
alias docker-run="docker run -it --gpus all -v $(pwd):/app yourusername/recursive-logic-engine:latest"

# Git shortcuts
alias git-push-all="git add . && git commit -m 'Update' && git push"
alias git-tag="git tag -a v1.0.0 -m 'Release' && git push origin v1.0.0"

# Viewing
alias show-config="cat config/train.yaml"
alias show-logs="tail -f outputs/training.log"
alias show-results="cat outputs/accuracy_table.json | python -m json.tool"

################################################################################
# 🆘 TROUBLESHOOTING COMMANDS
################################################################################

# If imports fail:
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall

# If CUDA not found:
python scripts/train.py --config config/train.yaml --device cpu

# If memory issues:
# Edit config/train.yaml and reduce batch_size

# If Git auth fails:
git config --global user.email "you@example.com"
git config --global user.name "Your Name"

# If Docker build fails:
docker build --no-cache -t yourusername/recursive-logic-engine:latest -f docker/Dockerfile .

# Check what's taking space:
du -sh * | sort -hr

# Clean up Docker
docker system prune -a

# Clean up Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

################################################################################
# END OF COMMAND REFERENCE
################################################################################
