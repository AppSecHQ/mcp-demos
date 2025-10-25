#!/usr/bin/env node
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import fetch from 'node-fetch';
import { z } from 'zod';

// Create an MCP server
const server = new McpServer({
  name: 'weather-server',
  version: '1.0.0'
});

// Register the weather tool
server.registerTool(
  'get_weather',
  {
    title: 'Weather Tool',
    description: 'Get current weather for a city',
    inputSchema: {
      city: z.string().describe('City name (e.g., "San Francisco")')
    }
  },
  async ({ city }) => {
    // Fetch weather data from wttr.in
    const response = await fetch(`https://wttr.in/${encodeURIComponent(city)}?format=j1`);
    const data = await response.json();

    const current = data.current_condition[0];
    const weather = {
      city: city,
      temperature: `${current.temp_F}°F (${current.temp_C}°C)`,
      condition: current.weatherDesc[0].value,
      humidity: `${current.humidity}%`,
      wind: `${current.windspeedMiles} mph`
    };

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(weather, null, 2)
        }
      ]
    };
  }
);

// Start the server with stdio transport
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(console.error);
