.PHONY: help install train eval trace analyze clean docs

help:
	@echo "Recursive Logic Engine - Common Commands"
	@echo "=========================================="
	@echo ""
	@echo "Setup:"
	@echo "  make install          Install dependencies"
	@echo "  make download-data    Download training datasets"
	@echo ""
	@echo "Training:"
	@echo "  make train            Train the model (default config)"
	@echo "  make train-custom     Train with custom config (CONFIG=path/to/config.yaml)"
	@echo ""
	@echo "Evaluation:"
	@echo "  make eval             Evaluate best model"
	@echo "  make trace            Generate self-correction traces"
	@echo ""
	@echo "Analysis:"
	@echo "  make analyze          Analyze results and generate report"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean            Remove artifacts and checkpoints"
	@echo "  make clean-all        Remove everything including data"

install:
	pip install -r requirements.txt

download-data:
	python scripts/download_datasets.py

train:
	python scripts/train.py --config config/train.yaml

train-custom:
	python scripts/train.py --config $(CONFIG)

eval:
	python scripts/evaluate.py --checkpoint outputs/checkpoints/best_model.pt

trace:
	python scripts/benchmark_trace.py --checkpoint outputs/checkpoints/best_model.pt

analyze:
	python scripts/analyze_results.py --wandb-project recursive-logic-engine

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf outputs/checkpoints/*.pt
	rm -f outputs/*.log

clean-all: clean
	rm -rf data/
	rm -rf outputs/

docs:
	@echo "Documentation: See README.md for full details"
	@echo "Config template: config/train.yaml"
	@echo "Architecture: See README.md project structure section"

.DEFAULT_GOAL := help
