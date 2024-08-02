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

def encode_parallel(args):
    files, output_dir, index = args
    file = files[index]['path']
    cuts = files[index]['cuts']

    # Load sourceaudio
    source, sr = torchaudio.load(file)

    # Process cuts
    for cut in cuts:
        id, start, duration = cut
        wav = source[:, int(start * sr):int((start + duration) * sr)]

        # Save codecs
        output_file = Path(output_dir) / Path(id + ".wav")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        if output_file.exists():        
            print("File exists", output_file)
        torchaudio.save(output_file, wav, sr)

def execute_run():

    collections = (
        {
            "name": "small",
            "index_path": "./external_datasets/libriheavy/libriheavy_cuts_small.jsonl.gz",
            "files_path": "./external_datasets/librilight/",
            "output_path": "./processed_datasets/librilight/",
        },
        {
            "name": "medium",
            "index_path": "./external_datasets/libriheavy/libriheavy_cuts_medium.jsonl.gz",
            "files_path": "./external_datasets/librilight-medium/",
            "output_path": "./processed_datasets/librilight-medium/",
        },
        {
            "name": "large",
            "index_path": "./external_datasets/libriheavy/libriheavy_cuts_large.jsonl.gz",
            "files_path": "./external_datasets/librilight-large/",
            "output_path": "./processed_datasets/librilight-large/",
        }
    )

    for collection in collections:
        index_path, files_path, output_path = collection["index_path"], collection["files_path"], collection["output_path"]
        
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

                # Check if exists
                if (Path(output_path) / Path(id + ".pt")).exists():
                    continue

                # Find index
                if wav_id not in files_map:
                    files_map[wav_id] = len(files)
                    files.append({ "path": files_path + wav_id + ".flac", "cuts": []})
                index = files_map[wav_id]

                # Append
                files[index]['cuts'].append((id, start, duration))

        # Prepare directory
        prepared_dir = Path(output_path)
        prepared_dir.mkdir(parents=True, exist_ok=True)

        # Process all files    
        print("Processing...")
        with multiprocessing.Manager() as manager:
            files = manager.list(files)
            args_list = [(files, prepared_dir, i) for i in range(len(files))]
            with multiprocessing.Pool(processes=32) as pool:
                for result in tqdm(pool.imap_unordered(encode_parallel, args_list, chunksize=1), total=len(files)):
                    pass
    

if __name__ == "__main__":
    execute_run()