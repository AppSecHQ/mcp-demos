#!/usr/bin/env python3
import asyncio
import json
from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import feedparser
import httpx


# Create the MCP server
app = Server("news-server")


# News sources with their RSS feeds
NEWS_SOURCES = {
    "technology": {
        "techcrunch": "https://techcrunch.com/feed/",
        "theverge": "https://www.theverge.com/rss/index.xml",
        "wired": "https://www.wired.com/feed/rss",
    },
    "general": {
        "bbc": "https://feeds.bbci.co.uk/news/rss.xml",
        "reuters": "https://www.reutersagency.com/feed/",
    },
    "business": {
        "bloomberg": "https://www.bloomberg.com/feed/podcast/bloomberg-markets.xml",
        "wsj": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
    },
    "sports": {
        "espn": "https://www.espn.com/espn/rss/news",
    }
}


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available news tools."""
    return [
        Tool(
            name="get_headlines",
            description="Get latest news headlines by category",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "News category: technology, general, business, or sports",
                        "enum": ["technology", "general", "business", "sports"]
                    },
                    "limit": {
                        "type": "number",
                        "description": "Number of headlines to return (default: 5)",
                        "default": 5
                    }
                },
                "required": ["category"],
            },
        ),
        Tool(
            name="get_news_from_source",
            description="Get news from a specific source",
            inputSchema={
                "type": "object",
                "properties": {
                    "source": {
                        "type": "string",
                        "description": "News source: bbc, reuters, techcrunch, theverge, wired, espn, wsj",
                        "enum": ["bbc", "reuters", "techcrunch", "theverge", "wired", "espn", "wsj"]
                    },
                    "limit": {
                        "type": "number",
                        "description": "Number of headlines to return (default: 5)",
                        "default": 5
                    }
                },
                "required": ["source"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""

    if name == "get_headlines":
        category = arguments["category"]
        limit = arguments.get("limit", 5)

        # Get all sources for this category
        sources = NEWS_SOURCES.get(category, {})
        all_headlines = []

        # Fetch from each source
        for source_name, feed_url in sources.items():
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.get(feed_url)
                    feed = feedparser.parse(response.text)

                    for entry in feed.entries[:limit]:
                        all_headlines.append({
                            "source": source_name,
                            "title": entry.get("title", "No title"),
                            "link": entry.get("link", ""),
                            "published": entry.get("published", "Unknown date"),
                            "summary": entry.get("summary", "")[:200] + "..."  # First 200 chars
                        })
            except Exception as e:
                all_headlines.append({
                    "source": source_name,
                    "error": f"Failed to fetch: {str(e)}"
                })

        result = {
            "category": category,
            "headlines": all_headlines[:limit]
        }

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

    elif name == "get_news_from_source":
        source = arguments["source"]
        limit = arguments.get("limit", 5)

        # Find the feed URL for this source
        feed_url = None
        for category_sources in NEWS_SOURCES.values():
            if source in category_sources:
                feed_url = category_sources[source]
                break

        if not feed_url:
            raise ValueError(f"Unknown source: {source}")

        # Fetch the news
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(feed_url)
            feed = feedparser.parse(response.text)

        headlines = []
        for entry in feed.entries[:limit]:
            headlines.append({
                "title": entry.get("title", "No title"),
                "link": entry.get("link", ""),
                "published": entry.get("published", "Unknown date"),
                "summary": entry.get("summary", "")[:200] + "..."
            })

        result = {
            "source": source,
            "headlines": headlines
        }

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

    raise ValueError(f"Unknown tool: {name}")


async def main():
    """Run the server using stdio transport."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
