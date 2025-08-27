import uvicorn


def main() -> None:
    uvicorn.run("core.server:app")


if __name__ == "__main__":
    main()
