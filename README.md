# ✨ Libriheavy Aligned

Alinged using MFA libriheavy dataset. Most of the dataset is aligned using version `2.2.17` of MFA and few files were aligned using `3.3.1`. Used ASR outputs, and NOT original text. I have found that original text contains mistakes (like page numbers) and can't always be aligned properly.

# Download

This dataset can be download directly or using my [datsets](https://github.com/ex3ndr/datasets) tool:

### Dataset ID

* `libriheavy-aligned` - small subset
* `libriheavy-aligned@medium` - medium subset
* `libriheavy-aligned@large` - large subset
* `libriheavy` - base libriheavy (without audio) library

# Reproduce

```bash
datasets sync
python ./cut_text.py
python ./cut_audio.py
./align_prepare.sh
./align_small.sh
./align_medium.sh
./align_large.sh
```

## License

MIT
