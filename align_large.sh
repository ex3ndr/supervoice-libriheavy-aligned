set -e

N=8
for DIR in "$PWD/processed_datasets/librilight-large"/*; do

    # Extract the directory name
    DIR_NAME=$(basename "$DIR")

    # Define the ignore list
    IGNORE_LIST=()

    # Check if DIR_NAME is in the ignore list
    if [[ " ${IGNORE_LIST[@]} " =~ " ${DIR_NAME} " ]]; then
        # Echo the directory name
        echo "Skipping $DIR_NAME"
        continue
    fi

    # Check if directory "$PWD/datasets/librilight-medium-aligned/$DIR_NAME" does not exist
    if [ ! -d "$PWD/processed_datasets/librilight-large-aligned/$DIR_NAME" ]; then

        # Echo the directory name
        echo "Processing $DIR_NAME"

        # Launch the command in a try-catch block
        (
            if mfa align "$DIR" english_mfa english_mfa "$PWD/processed_datasets/librilight-large-aligned/$DIR_NAME" -t "$PWD/.mfa/" -j 16 --use_mp --single_speaker --clean >> /dev/null; then
                echo "Alignment successful for $DIR_NAME"
            else
                echo "Alignment failed for $DIR_NAME"
            fi
        ) &
    else
        # Echo the directory name
        echo "Skipping $DIR_NAME"
    fi
    

    # allow to execute up to $N jobs in parallel
    if [[ $(jobs -r -p | wc -l) -ge $N ]]; then
        # now there are $N jobs already running, so wait here for any job
        # to be finished so there is a place to start next one.
        wait -n
    fi
done
wait