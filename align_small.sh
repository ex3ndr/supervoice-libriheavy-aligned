set -e

mfa align "$PWD/processed_datasets/librilight" english_mfa english_mfa "$PWD/processed_datasets/librilight-aligned" -t "$PWD/.mfa/" -j 16