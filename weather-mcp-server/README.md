# Weather MCP Server

A Node.js-based MCP server that provides current weather information for any city worldwide.

## Features

This server exposes one MCP tool:

### `get_weather`
Get current weather conditions for a specified city.

**Parameters:**
- `city` (required): City name (e.g., "San Francisco", "Tokyo", "London")

**Example:**
```json
{
  "city": "San Francisco"
}
```

**Returns:**
```json
{
  "city": "San Francisco",
  "temperature": "62°F (17°C)",
  "condition": "Partly cloudy",
  "humidity": "75%",
  "wind": "8 mph"
}
```

## Installation

```bash
# Install dependencies
npm install
```

## Dependencies

- `@modelcontextprotocol/sdk`: MCP Node.js SDK
- `node-fetch`: HTTP client for fetching weather data
- `zod`: Schema validation

## Data Source

Weather data is fetched from [wttr.in](https://wttr.in), a free weather service that provides:
- Current conditions
- Temperature in both Fahrenheit and Celsius
- Weather description
- Humidity levels
- Wind speed

## Testing

Test the server using the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector \
  node \
  /absolute/path/to/weather-mcp-server/server.js
```

## Configuration

Add to your `.mcp.json`:

```json
{
  "mcpServers": {
    "weather": {
      "command": "node",
      "args": ["weather-mcp-server/server.js"]
    }
  }
}
```

## Implementation Details

- Uses `@modelcontextprotocol/sdk` for MCP protocol implementation
- Makes HTTP requests to wttr.in API
- Returns formatted weather data with temperature, conditions, humidity, and wind
- Implements proper MCP protocol with stdio transport
- Uses Zod for input schema validation
