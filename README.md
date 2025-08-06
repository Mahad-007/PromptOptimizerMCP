# 🚀 Prompt Optimizer MCP

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-Protocol-green.svg)](https://modelcontextprotocol.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](tests/)
[![Deploy](https://img.shields.io/badge/Deploy-Smithery-orange.svg)](https://smithery.ai)

A **Model Context Protocol (MCP)** server that provides intelligent tools for optimizing and scoring LLM prompts using deterministic heuristics.

## 🎯 Overview

The **Prompt Optimizer MCP** server offers two powerful tools:

1. **`optimize_prompt`** - Generate 3 optimized variants of a raw LLM prompt in different styles
2. **`score_prompt`** - Evaluate the effectiveness of an improved prompt relative to the original

Perfect for developers, content creators, and AI practitioners who want to improve their prompt engineering workflow.

## ✨ Features

### 🎨 Prompt Optimization Styles

- **Creative**: Enhanced with descriptive adjectives and engaging language
- **Precise**: Concise and focused, removing redundant words
- **Fast**: Optimized for quick processing with shorter synonyms

### 📊 Intelligent Scoring Algorithm

The scoring system evaluates prompts based on:
- **Length optimization (40%)**: Prefers shorter, more concise prompts
- **Keyword preservation (30%)**: Maintains important terms from the original
- **Clarity improvement (30%)**: Reduces redundancy and improves structure

### 🔧 Technical Features

- ✅ **Stateless**: No external dependencies or state management
- ✅ **Deterministic**: Same inputs always produce same outputs
- ✅ **Error-free**: Comprehensive input validation and error handling
- ✅ **Fast**: Simple heuristics for quick processing
- ✅ **Extensible**: Easy to add new styles and scoring metrics
- ✅ **Dual Transport**: Supports both STDIO (MCP) and HTTP (deployment)

## 📁 Project Structure

```
prompt-optimizer-mcp/
├── 📄 README.md              # This file
├── 📄 server.py              # Main MCP server (STDIO transport)
├── 📄 http_server.py         # HTTP server for deployment
├── 📄 start.py               # Startup script (auto-detects mode)
├── 📄 requirements.txt       # Python dependencies
├── 📄 test_server.py         # Test script
├── 📄 deploy.py              # Deployment script
├── 📄 Dockerfile             # Container configuration
├── 📄 .gitignore             # Git ignore rules
├── 📁 tools/
│   ├── 📄 __init__.py        # Package initialization
│   └── 📄 optimize.py        # Core optimization logic
├── 📁 tests/
│   ├── 📄 __init__.py        # Test package initialization
│   └── 📄 test_optimize.py   # Unit tests
└── 📁 .github/
    └── 📁 workflows/
        └── 📄 ci.yml         # CI/CD pipeline
```

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Mahad-007/Prompt-Optimizer-MCP-for-LLMs.git
cd Prompt-Optimizer-MCP-for-LLMs
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Tests

```bash
python test_server.py
```

### 4. Start the Server

```bash
# For local development (STDIO mode)
python server.py

# For deployment (HTTP mode)
python start.py
```

## 🛠️ Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Install Dependencies

```bash
# Install from requirements.txt
pip install -r requirements.txt
```

## ⚙️ Configuration

### For Cursor IDE

Create `.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "prompt-optimizer": {
      "command": "python",
      "args": ["server.py"],
      "env": {}
    }
  }
}
```

### For Other MCP Clients

Configure your MCP client to use:
- **Command**: `python server.py`
- **Transport**: STDIO (default)

## 📖 Usage Examples

### Using the MCP Server

Once configured, you can use the tools through any MCP client:

#### Optimize a Prompt
```python
# Generate creative variants
variants = optimize_prompt(
    raw_prompt="Write a story about a cat",
    style="creative"
)
# Returns: [
#   "Craft a compelling story about a cat",
#   "Imagine you're an expert in this field. Write a story about a cat",
#   "Write a story about a cat. in a way that captivates and inspires"
# ]

# Generate precise variants
variants = optimize_prompt(
    raw_prompt="Please write a very detailed explanation about machine learning",
    style="precise"
)
# Returns: [
#   "Write a detailed explanation about machine learning",
#   "• Write a detailed explanation about machine learning",
#   "Write a detailed explanation about machine learning Be specific and concise."
# ]
```

#### Score a Prompt
```python
score = score_prompt(
    raw_prompt="Please write a very detailed explanation about machine learning",
    improved_prompt="Write an explanation about machine learning"
)
# Returns: 0.85 (high score due to length reduction and clarity improvement)
```

### HTTP API Usage

When deployed, the server also provides HTTP endpoints:

```bash
# Health check
curl http://localhost:8000/health

# Optimize prompt
curl -X POST http://localhost:8000/optimize \
  -H "Content-Type: application/json" \
  -d '{"raw_prompt": "Write about AI", "style": "creative"}'

# Score prompt
curl -X POST http://localhost:8000/score \
  -H "Content-Type: application/json" \
  -d '{"raw_prompt": "Write about AI", "improved_prompt": "Write about artificial intelligence"}'
```

### Direct Python Usage

```python
from tools.optimize import optimize_prompt, score_prompt

# Optimize a prompt
variants = optimize_prompt("Write about AI", "creative")
print(f"Optimized variants: {variants}")

# Score a prompt
score = score_prompt("Write about AI", "Write about artificial intelligence")
print(f"Score: {score}")
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
python test_server.py

# Run unit tests
python -m unittest tests.test_optimize -v

# Run specific test classes
python -m unittest tests.test_optimize.TestOptimizePrompt
python -m unittest tests.test_optimize.TestScorePrompt
python -m unittest tests.test_optimize.TestIntegration
```

## 🚀 Deployment

### Automated Deployment

Use the deployment script:

```bash
python deploy.py
```

This will:
1. Run all tests
2. Install dependencies
3. Run linting checks
4. Build Docker image (if available)
5. Create deployment package

### Manual Deployment

#### Deploy to Smithery

1. **Install Smithery CLI:**
   ```bash
   npm install -g @smithery/cli
   ```

2. **Authenticate:**
   ```bash
   smithery auth login
   ```

3. **Deploy:**
   ```bash
   # Windows
   .\deploy.bat
   
   # Linux/macOS
   chmod +x deploy.sh
   ./deploy.sh
   ```

#### Deploy with Docker

```bash
# Build the image
docker build -t prompt-optimizer-mcp:latest .

# Run the container
docker run -p 8000:8000 prompt-optimizer-mcp:latest
```

#### Deploy to Other Platforms

The server supports both STDIO (for MCP clients) and HTTP (for web deployment) transports:

- **STDIO Mode**: `python server.py` (for MCP clients)
- **HTTP Mode**: `python start.py` (for web deployment)

Your MCP server will be available at: `https://prompt-optimizer-mcp.smithery.ai`

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## 🔧 Development

### Adding New Optimization Styles

1. Add the new style to the `Literal` type in `server.py`
2. Implement the style function in `tools/optimize.py`
3. Add corresponding tests in `tests/test_optimize.py`

### Extending the Scoring Algorithm

Modify the `score_prompt` function in `tools/optimize.py` to include additional metrics or adjust weights.

### Running Locally

```bash
# Start the MCP server (STDIO mode)
python server.py

# Start the HTTP server (deployment mode)
python http_server.py

# Auto-detect mode based on environment
python start.py
```

## 📊 Performance

- **Response Time**: < 100ms for most operations
- **Memory Usage**: ~50MB typical
- **CPU Usage**: Minimal (stateless operations)
- **Scalability**: Auto-scales from 1-5 replicas on Smithery

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/Prompt-Optimizer-MCP-for-LLMs.git
cd Prompt-Optimizer-MCP-for-LLMs

# Install dependencies
pip install -r requirements.txt

# Run tests
python test_server.py

# Make your changes and test
python demo.py
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Model Context Protocol](https://modelcontextprotocol.io/) for the MCP specification
- [MCP Python SDK](https://github.com/microsoft/mcp) for the server framework
- [Smithery](https://smithery.ai) for deployment platform

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Mahad-007/Prompt-Optimizer-MCP-for-LLMs/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Mahad-007/Prompt-Optimizer-MCP-for-LLMs/discussions)
- **Documentation**: [DEPLOYMENT.md](DEPLOYMENT.md)

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Mahad-007/Prompt-Optimizer-MCP-for-LLMs&type=Date)](https://star-history.com/#Mahad-007/Prompt-Optimizer-MCP-for-LLMs&Date)

---

**Made with ❤️ for the AI community** 

[![smithery badge](https://smithery.ai/badge/@Mahad-007/prompt-optimizer-mcp-for-llms)](https://smithery.ai/server/@Mahad-007/prompt-optimizer-mcp-for-llms)
