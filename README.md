# Semantic-search-in-video-datasets

I propose to create a semantic multimodal search engine for collections of transcribed and aligned videos using state-of-the-art artificial intelligence models of different types, including NLP (Large Language Models) for text generation and capturing the semantics of transcriptions, as well as image description models to understand what is being seen in the video. Only focusing on the transcribed text does not help much, considering the context, what is being shown in the video will be helpful. The search engine will list down the most closest matches to the user query containing the metadata like link to the video, video-id, timestamp, text. Users can also ask questions related to content of videos in the dataset and the search engine will return the most appropriate answer.

To get more details refer my detailed [blog.](https://dhruv-kunjadiya.notion.site/Semantic-search-in-video-datasets-3c73c303c56748b497a975b1397d84ef)


# Setting up the project

1. git clone https://github.com/Dhruv454000/Semantic-search-in-video-datasets.git

2. Install miniconda

3. conda create --name Semantic-search

4. conda activate Semantic-search
5. cd Semantic-search-in-video-datasets/

6. pip install -r requirements.txt

7. To Download videos :

   First do  ```mkdir videos_dhruv``` then ```cd videos_dhruv```

   Download videos from [here.](https://drive.google.com/drive/folders/1lreNRRVrBYWALZxHeQcsEcivk-jMTOQQ?usp=sharing)

8. Do ```mkdir frames``` in which ffmpeg frames will be temporarily stored.

# Running Scripts

1. We will first generate metadata and sentence start and end time using ```extract_data_all_files.py```.

    To run this script :

    ```
    python3 src/extract_data_all_files.py vrt_files/ output_data/ 
    ```
    You can also run single file using ```extract_data_from_vrt.py```.

2. After generating json files, we will use ffmpeg to extarct frames and generate frame descriptions and add it to our json files.

    To do this run :

    ```
    python3 src/frame_desc_all.py
    ```

    To run it for a single video file use this command :

    ```
    python3 src/frame_desc.py videos_dhruv/2016-02-02_1500_US_KABC_Good_Morning_America.mp4 output_data/2016-02-02_1500_US_KABC_Good_Morning_America.v4.json frames/
    ```

3. To connect to weaviate and populate data in weaviate see ```weaviate_data_populate.ipynb```

4. To use the app, visit (http://labyrinth01.inf.um.es:8030/)

5. To make any changes in the Semantic Search App

    cd Semantic-search-app

    mkdir weaviate_data  
    (after doing this open weaviate_data_populate notebook and run it once, so that your weaviate_data is stored, this is required only once in the start then next time weaviate will keep your data stored permanently)

    Do your changes

    docker compose build  (if it gives error do sudo docker compose build)

    docker compose up

    open (http://labyrinth01.inf.um.es:8030/) in your browser to see the app running.




