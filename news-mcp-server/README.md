# News MCP Server

A Python-based MCP server that provides access to news headlines from various RSS feeds.

## Features

This server exposes two MCP tools:

### 1. `get_headlines`
Get the latest news headlines by category.

**Parameters:**
- `category` (required): News category - one of:
  - `technology`: Tech news from TechCrunch, The Verge, and Wired
  - `general`: General news from BBC and Reuters
  - `business`: Business news from Bloomberg and WSJ
  - `sports`: Sports news from ESPN
- `limit` (optional): Number of headlines to return (default: 5)

**Example:**
```json
{
  "category": "technology",
  "limit": 5
}
```

### 2. `get_news_from_source`
Get news from a specific source.

**Parameters:**
- `source` (required): News source - one of:
  - `bbc`: BBC News
  - `reuters`: Reuters
  - `techcrunch`: TechCrunch
  - `theverge`: The Verge
  - `wired`: Wired
  - `espn`: ESPN
  - `wsj`: Wall Street Journal
- `limit` (optional): Number of headlines to return (default: 5)

**Example:**
```json
{
  "source": "techcrunch",
  "limit": 5
}
```

## Installation

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Dependencies

- `mcp>=1.0.0`: MCP Python SDK
- `feedparser>=6.0.0`: RSS feed parser
- `httpx>=0.27.0`: Async HTTP client

## Testing

Test the server using the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector \
  /absolute/path/to/news-mcp-server/venv/bin/python \
  /absolute/path/to/news-mcp-server/news-server.py
```

## Configuration

Add to your `.mcp.json`:

```json
{
  "mcpServers": {
    "news": {
      "command": "./news-mcp-server/venv/bin/python",
      "args": ["news-mcp-server/news-server.py"]
    }
  }
}
```

## Implementation Details

- Uses `feedparser` to parse RSS feeds
- Makes async HTTP requests using `httpx`
- Returns structured JSON with title, link, publication date, and summary
- Handles errors gracefully for individual feed failures
- Implements proper MCP protocol with stdio transport
