import uvicorn

from billing.app import app

if __name__ == "__main__":
    # run server from command line for debug purpose
    uvicorn.run(app, host="0.0.0.0", port=8000)
