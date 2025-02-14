import uvicorn
from config import configs

if __name__ == "__main__":
    uvicorn.run(
        "backend:server",
        host="0.0.0.0",
        port=8061,
        reload=configs.DEBUG_MODE,
        use_colors=True,
        proxy_headers=True,
    )
