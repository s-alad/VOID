import fastapi as _fastapi
import blockchain as _blockchain

blockchain = _blockchain.Void()
app = _fastapi.FastAPI()

@app.post("/mine/")
def mine(data: str):
    if not blockchain.real():
        return _fastapi.HTTPException(status_code=400, detail="unreal")
    block = blockchain.mine(data=data)

    return block

@app.get("/chain/")
def chain():
    if not blockchain.real():
        return _fastapi.HTTPException(status_code=400, detail="unreal")
    return blockchain.chain

@app.get("/real/")
def validate():
    return blockchain.real()
