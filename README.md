# Product Workflow Auto-Documentation

A tool that automatically generates comprehensive product research documentation by analyzing product demonstrations. The tool creates detailed documentation including workflow analysis, UI/UX insights, and technical observations.

## Features

- Automated workflow analysis
- Screenshot capture at key interaction points
- Detailed UI/UX documentation
- Technical implementation insights
- Professional documentation generation in Word format

## Directory Structure

```
.
├── src/              # Source code
├── tests/            # Test files
├── input/            # Input video files
├── output/           # Generated output files
└── logs/             # Application logs
```

## Requirements

- Python 3.9+
- Google Gemini API key
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/product_workflow_auto-documentation.git
cd product_workflow_auto-documentation
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API key
```

## Usage

1. Place your product demonstration file in the `input` directory.

2. Run the analysis:
```bash
python src/main.py --input your_file.mp4
```

3. Find the generated documentation in the `output` directory:
   - `product_research_[timestamp].docx`: The main research document
   - `analysis_[timestamp].json`: Raw analysis data
   - `screenshots_[timestamp]/`: Screenshots from key moments

## Configuration

The tool can be configured through:
- Environment variables (see `.env.example`)
- Command line arguments
- Configuration files (see `config.example.yaml`)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

