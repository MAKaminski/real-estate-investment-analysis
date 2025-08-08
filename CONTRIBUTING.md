# Contributing to Real Estate Investment Analysis Tool

Thank you for your interest in contributing to the Real Estate Investment Analysis Tool! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Install dependencies**:
   ```bash
   pip install -r src/requirements.txt
   ```
4. **Run tests** to ensure everything works:
   ```bash
   python test_installation.py
   ```

## Development Guidelines

### Code Style
- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose

### Project Structure
- All source code goes in the `src/` directory
- Root level contains only entry points and documentation
- Use relative imports from `src/` for internal modules
- Maintain the four return metrics structure

### Financial Calculations
- All calculations must use `src/config.py` for assumptions
- Preserve the $20M monthly budget and 5% yield rate requirements
- Maintain property price range of $100K-$300K
- Keep the 1,000+ properties per run capability

### Testing
- Test your changes with `python test_installation.py`
- Run the example analysis: `python run_example.py`
- Ensure all four return metrics are calculated correctly
- Verify data export functionality works

## Making Changes

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the guidelines above

3. **Test your changes**:
   ```bash
   python test_installation.py
   python run_example.py
   ```

4. **Commit your changes** with a descriptive message:
   ```bash
   git commit -m "feat: add new financial calculation method"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** on GitHub

## Pull Request Guidelines

- Provide a clear description of the changes
- Include any relevant issue numbers
- Ensure all tests pass
- Update documentation if needed
- Follow the existing code style

## Areas for Contribution

### High Priority
- **Data Sources**: Add new property data sources
- **Financial Models**: Improve calculation accuracy
- **Performance**: Optimize for larger datasets
- **UI/UX**: Enhance the web dashboard

### Medium Priority
- **Documentation**: Improve README and docstrings
- **Testing**: Add more comprehensive tests
- **Configuration**: Add more customization options
- **Export Formats**: Add new output formats

### Low Priority
- **Code Style**: Refactor for better organization
- **Error Handling**: Improve error messages
- **Logging**: Add more detailed logging
- **Examples**: Add more example configurations

## Questions or Issues?

- **Bug Reports**: Use GitHub Issues with detailed descriptions
- **Feature Requests**: Open an issue with clear use cases
- **Questions**: Open a discussion on GitHub

## Code of Conduct

- Be respectful and inclusive
- Focus on the code and its functionality
- Provide constructive feedback
- Help others learn and grow

Thank you for contributing to the Real Estate Investment Analysis Tool!
