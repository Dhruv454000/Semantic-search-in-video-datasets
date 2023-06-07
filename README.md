# Semantic-search-in-video-datasets

I propose to create a semantic multimodal search engine for collections of transcribed and aligned videos using state-of-the-art artificial intelligence models of different types, including NLP (Large Language Models) for text generation and capturing the semantics of transcriptions, as well as image description models to understand what is being seen in the video. Only focusing on the transcribed text does not help much, considering the context, what is being shown in the video will be helpful. The search engine will list down the most closest matches to the user query containing the metadata like link to the video, video-id, timestamp, text. Users can also ask questions related to content of videos in the dataset and the search engine will return the most appropriate answer.

To use the script `extract_data_from_vrt.py` use the below command :

```

python3 src/extract_data_from_vrt.py videos_dhruv/2016-02-02_1800_US_CNN_Wolf.v4.vrt output_data

```
Here `videos_dhruv/2016-02-02_1800_US_CNN_Wolf.v4.vrt` is path to input vrt file and `outut_data` is the folder inside which `2016-02-02_1800_US_CNN_Wolf.v4.json` will be created.