from fastapi import FastAPI


app = FastAPI()

@app.get(path="/health")
def health():
    return { "success": True, "message": "Api en ejecución" }