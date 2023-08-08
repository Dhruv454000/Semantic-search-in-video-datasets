import re
import json
import argparse
import os
from extract_data_all_files import extract_metadata_and_sentences
from frame_desc_all import process_video_frames

def main(input_directory, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get the list of VRT files in the input directory
    vrt_files = [f for f in os.listdir(input_directory) if f.endswith('.vrt')]

    # Process each VRT file
    for file_name in vrt_files:
        # Create the input file path
        input_file = os.path.join(input_directory, file_name)

        # Extract metadata and sentences
        video_data = extract_metadata_and_sentences(input_file)

        # Create the output file path
        output_file = os.path.join(output_folder, f"{file_name[:-4]}.json")

        # Save the result as JSON
        with open(output_file, 'w') as file:
            json.dump(video_data, file, indent=1)

        print(f"Extraction completed. Output file: {output_file}")
    
    video_files = [f for f in os.listdir("videos_dhruv") if f.endswith('.mp4')]
    
    for file_name in video_files:
        input_file = os.path.join("videos_dhruv", file_name)
        json_file = os.path.join("output_data", f"{file_name[:-4]}.v4.json")
        process_video_frames(input_file, json_file, "frames/")
        

if __name__ == '__main__':
    # Parse the command-line arguments
    parser = argparse.ArgumentParser(description='Get all data from vrt files and videos and populate json files.')
    parser.add_argument('input_directory', type=str, help='Path to the input directory containing VRT files')
    parser.add_argument('output_folder', type=str, help='Path to the output folder')
    args = parser.parse_args()

    # Run the extraction
    main(args.input_directory, args.output_folder)