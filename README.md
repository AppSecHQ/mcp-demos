# MCP Server Demos

Example MCP (Model Context Protocol) servers demonstrating how to build custom integrations for Claude Code and other MCP clients.

## What is MCP?

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io) is an open standard that enables AI applications to securely connect to external data sources and tools. It provides a universal interface for AI assistants to interact with various systems.

## Demo Servers

This repository contains two example MCP servers:

### 1. News Server (Python)
**Location:** `news-mcp-server/`

A Python-based MCP server that fetches news headlines from RSS feeds.

**Tools:**
- `get_headlines`: Get latest news by category (technology, general, business, sports)
- `get_news_from_source`: Get news from specific sources (BBC, Reuters, TechCrunch, The Verge, Wired, ESPN, WSJ)

**Tech Stack:** Python 3, mcp SDK, feedparser, httpx

### 2. Weather Server (Node.js)
**Location:** `weather-mcp-server/`

A Node.js-based MCP server that provides current weather information.

**Tools:**
- `get_weather`: Get current weather for any city worldwide

**Tech Stack:** Node.js, @modelcontextprotocol/sdk, wttr.in API

## Quick Start

### Prerequisites
- Python 3.8+ (for news server)
- Node.js 18+ (for weather server)
- [Claude Code](https://claude.ai/code) or another MCP client
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector) (optional, for testing)

### Installation

#### News Server (Python)

```bash
cd news-mcp-server

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Weather Server (Node.js)

```bash
cd weather-mcp-server

# Install dependencies
npm install
```

## Configuration

This repository includes a `.mcp.json` configuration file that works when you use the repository as your working directory in Claude Code.

### Using the Included Configuration

The `.mcp.json` file in the repository root is configured to work with relative paths:

```json
{
  "mcpServers": {
    "news": {
      "command": "./news-mcp-server/venv/bin/python",
      "args": ["news-mcp-server/news-server.py"]
    },
    "weather": {
      "command": "node",
      "args": ["weather-mcp-server/server.js"]
    }
  }
}
```

**To use this configuration:**
1. Make sure both servers are installed (see Installation section above)
2. Open Claude Code in the `mcp-demos` directory
3. Restart Claude Code to load the configuration

### Alternative: CLI Configuration

You can also add these servers using the Claude Code CLI:

```bash
# Add news server (use absolute path to venv python)
claude mcp add --transport stdio news \
  -- /absolute/path/to/mcp-demos/news-mcp-server/venv/bin/python \
  news-mcp-server/news-server.py

# Add weather server
claude mcp add --transport stdio weather \
  -- node weather-mcp-server/server.js
```

### Verify Installation

```bash
claude mcp list
```

You should see both `news` and `weather` servers listed.

## Testing with MCP Inspector

The [MCP Inspector](https://github.com/modelcontextprotocol/inspector) is a browser-based tool for testing MCP servers.

### Test News Server

```bash
# From the repository root
npx @modelcontextprotocol/inspector \
  /absolute/path/to/mcp-demos/news-mcp-server/venv/bin/python \
  /absolute/path/to/mcp-demos/news-mcp-server/news-server.py
```

**Note:** You must use absolute paths with the Inspector. Replace `/absolute/path/to/mcp-demos` with the actual path.

### Test Weather Server

```bash
# From the repository root
npx @modelcontextprotocol/inspector \
  node \
  /absolute/path/to/mcp-demos/weather-mcp-server/server.js
```

The Inspector will:
1. Start your MCP server
2. Launch a web UI at `http://localhost:6274`
3. Allow you to interactively test tools and view logs

## Usage Examples

Once configured in Claude Code, you can ask:

- "What's the weather in Tokyo?"
- "Get me the latest tech news"
- "Show me sports headlines"
- "What's the news from BBC?"

## Project Structure

```
mcp-demos/
├── README.md
├── .mcp.json                # MCP server configuration
├── news-mcp-server/
│   ├── news-server.py       # Python MCP server implementation
│   ├── requirements.txt     # Python dependencies
│   └── venv/                # Python virtual environment (created during setup)
└── weather-mcp-server/
    ├── server.js            # Node.js MCP server implementation
    ├── package.json         # Node.js dependencies
    ├── package-lock.json    # Locked dependency versions
    └── node_modules/        # Node.js packages (created during setup)
```

## Troubleshooting

### News Server Issues

**Module not found errors:**
```bash
# Make sure virtual environment is activated and dependencies installed
cd news-mcp-server
source venv/bin/activate
pip install -r requirements.txt
```

**Server not responding:**
- Check that the venv is created and activated
- Verify all dependencies are installed
- Check Claude Code logs for error messages
- Ensure you're running Claude Code from the mcp-demos directory

### Weather Server Issues

**Module not found errors:**
```bash
# Reinstall dependencies
cd weather-mcp-server
npm install
```

**Server not responding:**
- Verify Node.js version is 18 or higher: `node --version`
- Check that node_modules directory exists
- Ensure network access to wttr.in API

### Inspector Connection Errors

**"Connection Error" in browser:**
- Ensure you're using absolute paths, not relative paths
- Check that the command is on one line or uses backslashes for line continuation
- Verify the server process starts without errors

**"spawn ENOENT" error:**
- Double-check file paths are correct
- Use absolute paths to avoid ambiguity
- Verify you're in the correct working directory

### Configuration Issues

**Servers not showing up in Claude Code:**
- Verify `.mcp.json` exists in your project root
- Check JSON syntax is valid (no trailing commas, proper quotes)
- Ensure you've restarted Claude Code after configuration changes
- Run `claude mcp list` to see if servers are loaded
- Make sure venv is created for Python server
- Make sure node_modules is installed for Node.js server

## Learn More

- [Model Context Protocol Documentation](https://modelcontextprotocol.io)
- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector)

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
