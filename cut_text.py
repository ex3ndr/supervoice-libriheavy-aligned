# Ignore warnings
import warnings
warnings.filterwarnings("ignore")

# Imports
import gzip
import torch
import torchaudio
from pathlib import Path
from tqdm import tqdm
import multiprocessing
import os
import json
import math

def clean_text(s: str) -> str:
    table = str.maketrans("’‘，。；？！（）：-《》、“”【】", "'',.;?!(): <>/\"\"[]")
    s = s.translate(table)
    return s.strip()

def execute_run():

    # Small
    # index_path = "./external_datasets/libriheavy/libriheavy_cuts_small.jsonl.gz"
    # files_path = "./external_datasets/librilight/"
    # output_path = "./processed_datasets/librilight/"

    # Medium
    # index_path = "./external_datasets/libriheavy/libriheavy_cuts_medium.jsonl.gz"
    # files_path = "./external_datasets/librilight-medium/"
    # output_path = "./processed_datasets/librilight-medium/"

    # Large
    index_path = "./external_datasets/libriheavy/libriheavy_cuts_large.jsonl.gz"
    files_path = "./external_datasets/librilight-large/"
    output_path = "./processed_datasets/librilight-large/"

    # Indexing files
    print("Build file index...")
    files = []
    files_map = {}
    existing_id = {}
    with gzip.open(index_path, "r") as f:
        for line in f:
            cut = json.loads(line)
            start = math.floor(1000 * cut["start"]) / 1000
            duration = math.floor(1000 * cut["duration"]) / 1000

            # Load audio
            wav_id = cut["recording"]["id"]
            id = cut["supervisions"][0]["id"]
            if wav_id.startswith("small/"):
                wav_id = wav_id[len("small/"):]
            if wav_id.startswith("medium/"):
                wav_id = wav_id[len("medium/"):]
            if wav_id.startswith("large/"):
                wav_id = wav_id[len("large/"):]
            if id.startswith("small/"):
                id = id[len("small/"):]
            if id.startswith("medium/"):
                id = id[len("medium/"):]
            if id.startswith("large/"):
                id = id[len("large/"):]

            # Check ID
            if id in existing_id:
                print("ID exists", id)
            existing_id[id] = True

            # Load text
            text = cut["supervisions"][0]["custom"]["texts"][1]
            text = clean_text(text)
            text_source = cut["supervisions"][0]["custom"]["texts"][0]
            text_source = clean_text(text_source)
        
            # Find index
            if wav_id not in files_map:
                files_map[wav_id] = len(files)
                files.append({ "path": files_path + wav_id + ".flac", "cuts": []})
            index = files_map[wav_id]

            # Append
            files[index]['cuts'].append((id, text, text_source))

    # Prepare directory
    prepared_dir = Path(output_path)
    prepared_dir.mkdir(parents=True, exist_ok=True)

    # Process all files    
    print("Processing...")
    for file in tqdm(files):
        for cut in file['cuts']:
            id, text, text_source = cut
            output_file = Path(output_path) / Path(id + ".txt")
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, "w") as f:
                f.write(text)
            output_file = Path(output_path) / Path(id + ".source.txt")
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, "w") as f:
                f.write(text_source)

if __name__ == "__main__":
    execute_run()