import json
import pathlib
import subprocess
import gradio as gr
import os
from PIL import Image
import open_clip
import torch
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

model, _, transform = open_clip.create_model_and_transforms(
    "coca_ViT-L-14",
    pretrained="mscoco_finetuned_laion2B-s13B-b90k"
)

def output_generate(image):
    im = transform(image).unsqueeze(0).to(device)
    with torch.no_grad(), torch.cuda.amp.autocast():
        generated = model.generate(im, seq_len=20)
    return open_clip.decode(generated[0].detach()).split("<end_of_text>")[0].replace
    ("<start_of_text>", "")

    return(output_generate(image))

folder_path = "frames"

def get_image(frames):
    ffmpeg_commands = []
    for i,frame in enumerate(frames):
        ffmpeg_commands.append(f"ffmpeg -ss {frame} -i ../videos_dhruv/2016-02-02_1500_US_KABC_Good_Morning_America.mp4 -vframes 1 ../frames/{i}.jpg")
    for command in ffmpeg_commands:
        subprocess.run(command, shell=True)

# Load data from JSON file
with open('../output_data/2016-02-02_1500_US_KABC_Good_Morning_America.v4.json') as f:
    data = json.load(f)

# Iterate over sentences
for sent in data['sentences']:
    frames = []
    starttime = sent['starttime']
    endtime = sent['endtime']
    frames.append(starttime)
    frames.append(endtime)
    
    # Calculate midtime
    midtime = (float(starttime) + float(endtime)) / 2
    
    frames.append(midtime)
    if(sent['verbs'] != []):
        for verb in sent['verbs']:
            frames.append(verb['vstart'])
            
    # Call get_image function with the calculated values
    get_image(frames)
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Check if the current item is a file
        if os.path.isfile(file_path):
            # Open the image using PIL
            image = Image.open(file_path)
            print(output_generate(image))
    break
        

        
     
    
    
    
