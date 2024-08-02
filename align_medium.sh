set -e

for DIR in "$PWD/processed_datasets/librilight-medium"/*; do

    # Extract the directory name
    DIR_NAME=$(basename "$DIR")
    
    # Check if directory "$PWD/datasets/librilight-medium-aligned/$DIR_NAME" does not exist
    if [ ! -d "$PWD/processed_datasets/librilight-medium-aligned/$DIR_NAME" ]; then

        # Echo the directory name
        echo "Processing $DIR_NAME"

        # Launch the command in a try-catch block
        if mfa align "$DIR" english_mfa english_mfa "$PWD/processed_datasets/librilight-medium-aligned/$DIR_NAME" -t "$PWD/.mfa/" -j 64 --use_mp --single_speaker --clean; then
            echo "Alignment successful for $DIR_NAME"
        else
            echo "Alignment failed for $DIR_NAME"
        fi
    fi
done