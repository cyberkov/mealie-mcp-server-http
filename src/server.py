import logging
import os
import traceback

from dotenv import load_dotenv
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

from mealie import MealieFetcher
from tools import register_all_tools

# Load environment variables first
load_dotenv()

# Get log level from environment variable with INFO as default
log_level_name = os.getenv("LOG_LEVEL", "INFO")
log_level = getattr(logging, log_level_name.upper(), logging.INFO)

# Configure logging
logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("mealie_mcp_server.log")],
)
logger = logging.getLogger("mealie-mcp")

# Get configuration from environment
MEALIE_BASE_URL = os.getenv("MEALIE_BASE_URL")
MEALIE_API_KEY = os.getenv("MEALIE_API_KEY")
if not MEALIE_BASE_URL or not MEALIE_API_KEY:
    raise ValueError(
        "MEALIE_BASE_URL and MEALIE_API_KEY must be set in environment variables."
    )

# Get HTTP server configuration from environment
HTTP_HOST = os.getenv("HTTP_HOST", "0.0.0.0")
HTTP_PORT = int(os.getenv("HTTP_PORT", "8000"))

# Create FastMCP server with instructions
mcp = FastMCP(
    name="mealie",
    instructions="""
        This server provides access to Mealie recipe management and meal planning tools.
        Use the available tools to search recipes, manage meal plans, and organize your cooking.
    """,
)

# Add health check endpoint
@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    """Health check endpoint for monitoring."""
    return PlainTextResponse("OK")

# Initialize Mealie client
try:
    mealie = MealieFetcher(
        base_url=MEALIE_BASE_URL,
        api_key=MEALIE_API_KEY,
    )
    logger.info({"message": "Mealie client initialized successfully"})
except Exception as e:
    logger.error({"message": "Failed to initialize Mealie client", "error": str(e)})
    logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
    raise

# Register all components
register_all_tools(mcp, mealie)

if __name__ == "__main__":
    try:
        logger.info({
            "message": "Starting Mealie MCP Server with HTTP transport",
            "host": HTTP_HOST,
            "port": HTTP_PORT
        })
        # Run with HTTP streamable transport
        mcp.run(
            transport="http",
            host=HTTP_HOST,
            port=HTTP_PORT,
            log_level=log_level_name,
        )
    except Exception as e:
        logger.critical(
            {"message": "Fatal error in Mealie MCP Server", "error": str(e)}
        )
        logger.debug(
            {"message": "Error traceback", "traceback": traceback.format_exc()}
        )
        raise
