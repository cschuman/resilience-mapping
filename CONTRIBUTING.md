# Contributing to Health Resilience Mapping

Thank you for your interest in contributing to this research project! This document provides guidelines for contributing to the codebase and research.

## Ways to Contribute

### Research Contributions
- **Community Stories**: Share qualitative insights about resilient communities
- **Data Validation**: Help verify findings with local knowledge
- **Literature Review**: Connect our findings with existing research
- **Methodology Review**: Suggest improvements to our statistical approach

### Technical Contributions
- **Bug Fixes**: Help fix issues in the web application or analysis scripts
- **Features**: Add new visualizations or analysis capabilities
- **Documentation**: Improve documentation for researchers and developers
- **Accessibility**: Help make the platform more accessible

## Getting Started

### Prerequisites
- Node.js 20+
- Python 3.8+ (for analysis scripts)
- Go 1.21+ (for API development)

### Development Setup

```bash
# Clone the repository
git clone https://github.com/cschuman/resilience-mapping.git
cd resilience-mapping

# Web application
cd app/web
npm install
npm run dev

# Python analytics
cd ../analytics
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running Tests

```bash
# Web application tests
cd app/web
npm test

# Go tests
go test ./...
```

## Submitting Changes

### Pull Request Process

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following the code style guidelines
3. **Add tests** for new functionality
4. **Update documentation** as needed
5. **Submit a pull request** with a clear description

### Commit Messages

Use clear, descriptive commit messages:

```
feat: Add filter for urban/rural tract classification
fix: Correct resilience score calculation for edge cases
docs: Update methodology section with statistical details
```

### Code Style

- **JavaScript/TypeScript**: Follow existing patterns, use Prettier
- **Python**: Follow PEP 8, use type hints where helpful
- **Go**: Use `gofmt` and follow standard Go conventions

## Research Ethics

This project involves data about communities. Please:

- **Respect privacy**: Don't identify individuals or small groups
- **Use dignity-first language**: Communities are resilient, not "poor" or "disadvantaged"
- **Consider impact**: Think about how findings might affect communities
- **Be accurate**: Double-check data interpretations

## Questions?

- Open a [Discussion](https://github.com/cschuman/resilience-mapping/discussions) for questions
- Check [existing issues](https://github.com/cschuman/resilience-mapping/issues) before creating new ones
- Review the [documentation](docs/) for methodology details

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
