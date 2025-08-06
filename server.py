from mcp.server.fastmcp import FastMCP
import os
from dotenv import load_dotenv

# Import your existing optimization functions
from tools.optimize import optimize_prompt, score_prompt

load_dotenv()

PORT = os.environ.get("PORT", 10000)
mcp = FastMCP("Prompt Optimizer MCP", host="0.0.0.0", port=PORT)

@mcp.tool()
def optimize_prompt_tool(raw_prompt: str, style: str) -> str:
    """
    Generate 3 optimized variants of the raw LLM prompt in a chosen style.
    Styles: creative, precise, fast.
    """
    try:
        variants = optimize_prompt(raw_prompt, style)
        return "\n\n".join(f"Variant {i+1}: {v}" for i, v in enumerate(variants))
    except Exception as e:
        return f"Prompt optimization failed: {str(e)}"

@mcp.tool()
def score_prompt_tool(raw_prompt: str, improved_prompt: str) -> str:
    """
    Score an improved prompt relative to the raw prompt.
    Returns an effectiveness score between 0 and 1.
    """
    try:
        score = score_prompt(raw_prompt, improved_prompt)
        return f"Effectiveness score: {score:.3f}"
    except Exception as e:
        return f"Prompt scoring failed: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
