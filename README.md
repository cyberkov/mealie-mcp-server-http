[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/rldiao-mealie-mcp-server-badge.png)](https://mseep.ai/app/rldiao-mealie-mcp-server)

# Mealie MCP Server (HTTP)

This project enables AI assistants to interact with your [Mealie](https://github.com/mealie-recipes/mealie) recipe database through MCP protocol over HTTP. Built with FastMCP framework.

## Features

- 🌐 HTTP streamable transport for web-based access
- 🔍 Recipe search and management
- 📅 Meal planning tools
- 🐳 Docker support
- 🏥 Health check endpoint
- 📝 Comprehensive logging

## Prerequisites

- Python 3.11+
- Running Mealie instance with API key
- Docker (optional, for containerized deployment)

## Quick Start

### Option 1: Docker with Pre-built Image (Easiest)

Use the pre-built Docker image from GitHub Container Registry:

```bash
docker run -d \
  --name mealie-mcp-server \
  -p 8000:8000 \
  -e MEALIE_BASE_URL=http://your-mealie-instance:9000 \
  -e MEALIE_API_KEY=your-api-key \
  ghcr.io/cyberkov/mealie-mcp-server-http:latest
```

The server will be available at `http://localhost:8000`

### Option 2: Docker Compose (Recommended for Local Development)

1. Clone the repository:
```bash
git clone <repository-url>
cd mealie-mcp-server-http
```

2. Create `.env` file from template:
```bash
cp .env.example .env
```

3. Edit `.env` with your Mealie instance details:
```env
MEALIE_BASE_URL=http://your-mealie-instance:9000
MEALIE_API_KEY=your-mealie-api-key
HTTP_HOST=0.0.0.0
HTTP_PORT=8000
LOG_LEVEL=INFO
```

4. Run with Docker Compose:
```bash
docker-compose up -d
```

The server will be available at `http://localhost:8000`

### Option 3: Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd mealie-mcp-server-http
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the server:
```bash
cd src
python server.py
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MEALIE_BASE_URL` | Mealie instance URL | Required |
| `MEALIE_API_KEY` | Mealie API key | Required |
| `HTTP_HOST` | Server bind address | `0.0.0.0` |
| `HTTP_PORT` | Server port | `8000` |
| `LOG_LEVEL` | Logging level | `INFO` |

### FastMCP Global Settings (Optional)

| Variable | Description | Default |
|----------|-------------|---------|
| `FASTMCP_LOG_LEVEL` | FastMCP logging level | `INFO` |
| `FASTMCP_MASK_ERROR_DETAILS` | Hide detailed errors | `False` |
| `FASTMCP_STRICT_INPUT_VALIDATION` | Strict input validation | `False` |
| `FASTMCP_INCLUDE_FASTMCP_META` | Include metadata | `True` |

## Usage with MCP Clients

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mealie": {
      "url": "http://localhost:8000/mcp/v1/"
    }
  }
}
```

### Other MCP Clients

Connect to the MCP endpoint at: `http://localhost:8000/mcp/v1/`

## API Endpoints

- **MCP Endpoint**: `http://localhost:8000/mcp/v1/`
- **Health Check**: `http://localhost:8000/health`

## Available Tools

### Recipe Tools
- `get_recipes` - Search and list recipes
- `get_recipe_concise` - Get basic recipe details
- `get_recipe_detailed` - Get full recipe information

### Meal Plan Tools
- `get_all_mealplans` - View existing meal plans
- `create_mealplan_bulk` - Add multiple recipes to a meal plan
- `get_todays_mealplan` - View today's planned meals

## Docker

### Published Images

Pre-built multi-platform Docker images are automatically published to GitHub Container Registry (GHCR):

- **Latest (main branch)**: `ghcr.io/cyberkov/mealie-mcp-server-http:latest`
- **Specific version**: `ghcr.io/cyberkov/mealie-mcp-server-http:v1.0.0`
- **Specific commit**: `ghcr.io/cyberkov/mealie-mcp-server-http:sha-<commit-sha>`

Supported platforms:
- `linux/amd64` (x86_64)
- `linux/arm64` (ARM64/aarch64)

### Pull Pre-built Image

```bash
docker pull ghcr.io/cyberkov/mealie-mcp-server-http:latest
```

### Docker Commands

### Build Image Locally (Optional)
```bash
docker build -t mealie-mcp-server .
```

### Run Container with Pre-built Image
```bash
docker run -d \
  --name mealie-mcp-server \
  -p 8000:8000 \
  -e MEALIE_BASE_URL=http://your-mealie:9000 \
  -e MEALIE_API_KEY=your-api-key \
  ghcr.io/cyberkov/mealie-mcp-server-http:latest
```

### Run Container with Local Build
```bash
docker run -d \
  --name mealie-mcp-server \
  -p 8000:8000 \
  -e MEALIE_BASE_URL=http://your-mealie:9000 \
  -e MEALIE_API_KEY=your-api-key \
  mealie-mcp-server
```

### View Logs
```bash
docker logs -f mealie-mcp-server
```

### Stop Container
```bash
docker stop mealie-mcp-server
```

## Development

### Project Structure
```
mealie-mcp-server-http/
├── src/
│   ├── server.py           # Main server entry point
│   ├── prompts.py          # Prompt definitions
│   ├── utils.py            # Utility functions
│   ├── mealie/             # Mealie client modules
│   ├── models/             # Data models
│   └── tools/              # MCP tools
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container definition
├── docker-compose.yml     # Docker Compose config
└── .env.example           # Environment template
```

### Running Tests

Health check test:
```bash
curl http://localhost:8000/health
```

### Logging

Logs are written to:
- Console (stdout)
- File: `mealie_mcp_server.log`

## Troubleshooting

### Connection Issues

1. Check Mealie is accessible:
```bash
curl http://your-mealie-instance:9000/api/app/about
```

2. Verify API key is correct
3. Check firewall settings
4. Review logs: `docker logs mealie-mcp-server`

### Health Check Fails

The health check endpoint should return "OK":
```bash
curl http://localhost:8000/health
```

If it fails, check:
- Server is running
- Port 8000 is not blocked
- Check logs for errors

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
