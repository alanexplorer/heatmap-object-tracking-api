from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from heatmap import generate_heatmap_local
from utils import list_objects_from_json

app = FastAPI()

@app.get("/generate")
async def generate(object_filter: str = Query(...)):
    json_path = "inputs/sample.json"
    image_path = "inputs/base_image.png"
    output_path = generate_heatmap_local(json_path, image_path, object_filter)
    return FileResponse(output_path, media_type="image/png", filename="output.png")

@app.get("/list_objects")
async def list_objects():
    return list_objects_from_json("inputs/sample.json")
