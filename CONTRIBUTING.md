# Contributing to Recursive Logic Engine

Thank you for your interest in contributing! This document outlines how to contribute to the project.

## Code of Conduct

Be respectful and constructive in all interactions with other contributors.

## Getting Started

### 1. Fork the Repository
```bash
# Click "Fork" on GitHub
git clone https://github.com/yourusername/recursive-logic-engine.git
cd recursive-logic-engine
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-description
```

## Development Workflow

### Before Making Changes

1. **Check for existing issues/PRs** to avoid duplicate work
2. **Open an issue first** for major changes to discuss approach
3. **Update from main branch** to ensure you're current

```bash
git fetch origin
git rebase origin/main
```

### Making Changes

1. **Write code** following the style guide (see below)
2. **Add tests** for new functionality
3. **Update documentation** if needed
4. **Keep commits atomic** (one feature per commit)

### Code Style

We use:
- **Black** for formatting: `black src/`
- **isort** for imports: `isort src/`
- **Flake8** for linting: `flake8 src/`
- **MyPy** for type checking: `mypy src/`

```bash
# Format and check code
make lint

# Or manually
black src/ tests/
isort src/ tests/
flake8 src/ tests/
mypy src/
```

### Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_training.py::test_grpo -v

# With coverage
pytest tests/ --cov=src --cov-report=html
```

Every pull request must have:
- ✓ Tests for new functionality
- ✓ All tests passing
- ✓ >80% code coverage (for new code)

## Commit Messages

Use clear, descriptive commit messages:

```bash
# Good
git commit -m "Add GRPO group normalization implementation

- Implement group_relative_advantage computation
- Add tests for different group sizes
- Update documentation with algorithm overview"

# Avoid
git commit -m "fixed stuff"
git commit -m "WIP"
git commit -m "asdf"
```

## Pull Request Process

1. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request** on GitHub with:
   - Clear title describing what changed
   - Description of changes and why
   - Link to related issue (if any)
   - Screenshots/results (if applicable)

3. **Respond to reviews**
   - Address feedback constructively
   - Push new commits to update PR
   - Don't force-push after review starts

4. **Merge**
   - Use "Squash and merge" for single-purpose PRs
   - Use "Create a merge commit" for larger changes
   - Delete branch after merging

## Areas for Contribution

### High Priority
- [ ] Beam search decoding implementation
- [ ] Few-shot prompting support
- [ ] Performance optimizations
- [ ] Additional benchmarks

### Medium Priority
- [ ] Docker deployment improvements
- [ ] API documentation
- [ ] Example notebooks
- [ ] Video tutorials

### Low Priority
- [ ] Code style improvements
- [ ] Comment clarification
- [ ] README improvements

## Reporting Issues

**Found a bug?** Please open an issue with:
1. Clear title
2. Reproduction steps
3. Expected vs actual behavior
4. Environment (OS, GPU, Python version)
5. Relevant error logs

**Have a feature request?** Please include:
1. Clear description of feature
2. Why it would be useful
3. Example usage

## Questions?

- **Discussions**: [GitHub Discussions](https://github.com/yourusername/recursive-logic-engine/discussions)
- **Issues**: [GitHub Issues](https://github.com/yourusername/recursive-logic-engine/issues)
- **Email**: your.email@example.com

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- README.md acknowledgments
- Release notes

Thank you for contributing! 🙏
