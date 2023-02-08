from src.settings import server_settings

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.app.application:app",
        host=server_settings.server_host,
        port=server_settings.server_port,
        reload=True,
    )
