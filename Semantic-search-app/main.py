from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from weaviate import Client as WeaviateClient
from sentence_transformers import SentenceTransformer

app = FastAPI()
weaviate = WeaviateClient("http://localhost:8080")
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081"], 
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/search")
def search(text_desc: str, video_desc: str):
    print(len(text_desc))
    print(len(video_desc))
    if(len(text_desc) != 0 and len(video_desc) != 0):
        combined_text = f"In the video you can hear: {text_desc} In the video you can see: {video_desc}"
        vector = model.encode(combined_text)

        response = weaviate.query.get("Video_text_description", ["text", "starttime", "endtime", "metadata", "video_id"]) \
            .with_near_vector({"vector": vector}) \
            .with_limit(5) \
            .with_additional(["distance"]) \
            .do()

        print(response)
        return response
    elif(len(text_desc) != 0):
        vector = model.encode(text_desc)
        response = weaviate.query.get("Video_text", ["text", "starttime", "endtime", "metadata", "video_id"]) \
            .with_near_vector({"vector": vector}) \
            .with_limit(5) \
            .with_additional(["distance"]) \
            .do()
        
        print(response)
        return response
    else:
        vector = model.encode(video_desc)
        response = weaviate.query.get("Video_text", ["text", "starttime", "endtime", "metadata", "video_id"]) \
            .with_near_vector({"vector": vector}) \
            .with_limit(5) \
            .with_additional(["distance"]) \
            .do()
        
        print(response)
        return response
        

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
