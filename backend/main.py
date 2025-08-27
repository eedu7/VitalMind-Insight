import uvicorn


def main() -> None:
    uvicorn.run("core.server:app", reload=True)


if __name__ == "__main__":
    main()
