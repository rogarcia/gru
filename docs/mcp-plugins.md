# MCP Plugins

MCP (Model Context Protocol) extends Gru with additional tools. Optional but powerful.

## Setup

1. Install Node.js from [nodejs.org](https://nodejs.org)

2. Create `mcp_servers.json` in the gru folder:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/files"],
      "env": {}
    }
  }
}
```

3. Restart Gru

## Popular Servers

| Server | Purpose |
|--------|---------|
| `@modelcontextprotocol/server-filesystem` | Advanced file operations |
| `@modelcontextprotocol/server-github` | GitHub integration |
| `@modelcontextprotocol/server-postgres` | PostgreSQL database |
| `@modelcontextprotocol/server-puppeteer` | Browser automation |

See [github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) for more.

## Multiple Servers

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"],
      "env": {}
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxx"
      }
    }
  }
}
```

## Verification

When Gru starts with MCP servers configured:

```
MCP server 'filesystem' started with 14 tools
Started 1 MCP server(s)
```

[Back to README](../README.md)
