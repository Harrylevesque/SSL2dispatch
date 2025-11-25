from fastapi import FastAPI, HTTPException
import os
import json
import requests
app = FastAPI()


@app.get("/")
async def root():
    return {"status": "Working"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}





@app.get("/service/create/{sv_uuid}/{ipv4}")
async def create_service(sv_uuid: str, ipv4: str):
    service_file_dump = {
        "service_uuid": sv_uuid,
        "service_ip": ipv4
    }
    with open(f'{sv_uuid}.json', 'w', encoding='utf-8') as fp:
        json.dump(service_file_dump, fp, indent=2)
    return {"message": f"Service {sv_uuid} created with IP {ipv4}"}



@app.get("/service/find/{sv_uuid}/{svu_uuid}")
async def find_service(sv_uuid: str, svu_uuid: str):
    # basic path traversal protection
    if any(x in sv_uuid or x in svu_uuid for x in ("..", "/", "\\")):
        raise HTTPException(status_code=400, detail="Invalid identifiers")

    filepath = f"service/{sv_uuid}.json"
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Service not found")

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            servicefiledata = json.load(f)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to read service file")

    ip = servicefiledata.get("service_ip")
    if not ip:
        raise HTTPException(status_code=500, detail="Missing service_ip in service file")

    requests.get = f"https://{ip}/service/{sv_uuid}/user/find/{svu_uuid}"



    return {
        "status": "success",
        "service_uuid": sv_uuid,
        "service_ip": servicefiledata.get("service_ip"),
    }