from fastapi import FastAPI
import os
import json
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