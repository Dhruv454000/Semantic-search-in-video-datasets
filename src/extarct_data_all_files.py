import re
import json
import argparse
import os

def extract_metadata_and_sentences(input_file):
    print('input_file',input_file)
    # Read the input text from the file
    with open(input_file, 'r') as file:
        lines = file.readlines()
    with open(input_file, "r") as file:
        input_text = file.read()

    # regular expression pattern
    pattern = r'<text id="(.*?)" collection="(.*?)" file="(.*?)" date="(.*?)" year="(.*?)" month="(.*?)" day="(.*?)" time="(.*?)" duration="(.*?)" country="(.*?)" channel="(.*?)" title="(.*?)" video_resolution="(.*?)" video_resolution_original="(.*?)" language="(.*?)" recording_location="(.*?)" original_broadcast_date="(.*?)" original_broadcast_time="(.*?)" original_broadcast_timezone="(.*?)" local_broadcast_date="(.*?)" local_broadcast_time="(.*?)" local_broadcast_timezone="(.*?)">\n([\s\S]*?)\n<\/s>'
    ids = re.findall(r'<s id="(\d+)"', input_text)

    # Extracting the metadata using the above defined pattern
    match = re.search(pattern, input_text)
    if match:
        # Extract the metadata fields
        metadata = {
            "text_id": match.group(1),
            "collection": match.group(2),
            "file": match.group(3),
            "date": match.group(4),
            "year": match.group(5),
            "month": match.group(6),
            "day": match.group(7),
            "time": match.group(8),
            "duration": match.group(9),
            "country": match.group(10),
            "channel": match.group(11),
            "title": match.group(12),
            "video_resolution": match.group(13),
            "video_resolution_original": match.group(14),
            "language": match.group(15),
            "recording_location": match.group(16),
            "original_broadcast_date": match.group(17),
            "original_broadcast_time": match.group(18),
            "original_broadcast_timezone": match.group(19),
            "local_broadcast_date": match.group(20),
            "local_broadcast_time": match.group(21),
            "local_broadcast_timezone": match.group(22)
        }

    sentences = []
    current_sentence = ''
    count = 0
    starttime = ''
    endtime = ''
    prev_line = ''
    id_count = 0
    endtime_last_sid = ''
    all_verbs = []
    endtime_execption = ''
    
    # Iterate over each line in the file
    for line in lines:
        # extracting starttime of sentence
        if count == 1:
            words = line.split('\t')
            starttime = words[51].strip() + '.' + words[52].strip()
            count = 0
            
        # For the first sentence there will be no </s> tag before this so this condition. (refer vrt file format) 
        if id_count == 0:
            if re.match(r'</turn', line):
                words = prev_line.split('\t')
                endtime = words[53].strip() + '.' + words[54].strip()

        # For last sentence storing endtime_last_sid as it has different previous line. 
        if id_count == len(ids) - 1:
            if re.match(r'</turn', line):
                words = prev_line.split('\t')
                endtime_last_sid = words[53].strip() + '.' + words[54].strip()
                
        # extracting endtime of sentence
        if re.match(r'</s>', line) and prev_line != '</turn>\n' and prev_line != '</story>\n' and prev_line != '<turn>\n' and prev_line.strip() != '</turn>' and prev_line.strip() != '<turn>':
            words = prev_line.split('\t')           
            endtime = words[53].strip() + '.' + words[54].strip()
            
        # handling cases where endtime is 0.0, storing endtime of word appearing before '.'
        if re.match(r'[.].', line) and prev_line[0] != '<':
            words = prev_line.split('\t')
            endtime_execption = words[53].strip() + '.' + words[54].strip()
            
        # Add all sentence details when next <s> tag comes
        if re.match(r'<s id=', line):
            count = 1
            # Append the previous sentence to the list
            if current_sentence:
                if endtime == "0.0" or float(starttime) >= float(endtime):
                    endtime = endtime_execption
                current_sentence = current_sentence.replace('&apos;', "'")
                sentence_info = {
                    "sentence": current_sentence.strip(),
                    "starttime": starttime,
                    "endtime": endtime,
                    "verbs": all_verbs
                }
                sentences.append(sentence_info)
                id_count += 1
            current_sentence = ''
            all_verbs = []

        # this condition will match for all the words and will skip <s> tag line.
        if re.match(r'(?:\w+|\&apos;.|[.].)', line):
            first_word = re.search(r'^(.*?)(?:\s|$)', line)
            line_data = line.split('\t')
            # storing verb details
            if line_data[3] == "VERB":
                verb = {
                    "vword": line_data[0],
                    "vstart": line_data[51].strip() + '.' + line_data[52].strip(),
                    "vend": line_data[53].strip() + '.' + line_data[54].strip(),
                    "vpos": line_data[1]
                }
                all_verbs.append(verb)
            if first_word:
                word = first_word.group(1)
                current_sentence += word + ' '

        prev_line = line

    # Append the last sentence to the list
    if current_sentence:
        current_sentence = current_sentence.replace('&apos;', "'")
        sentence_info = {
            "sentence": current_sentence.strip(),
            "starttime": starttime,
            "endtime": endtime_last_sid,
            "verbs": all_verbs
        }
        sentences.append(sentence_info)

    video_data = {
        "metadata": metadata,
        "sentences": sentences
    }
    return video_data

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
        output_file = os.path.join(output_folder, f"{file_name}.json")

        # Save the result as JSON
        with open(output_file, 'w') as file:
            json.dump(video_data, file, indent=1)

        print(f"Extraction completed. Output file: {output_file}")


if __name__ == '__main__':
    # Parse the command-line arguments
    parser = argparse.ArgumentParser(description='Extract metadata and sentences from input VRT files.')
    parser.add_argument('input_directory', type=str, help='Path to the input directory containing VRT files')
    parser.add_argument('output_folder', type=str, help='Path to the output folder')
    args = parser.parse_args()

    # Run the extraction
    main(args.input_directory, args.output_folder)