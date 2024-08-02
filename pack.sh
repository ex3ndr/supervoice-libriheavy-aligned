set -e

cd processed_datasets
# echo "Compressing librilight-aligned...."
# COPYFILE_DISABLE=1 tar -cf librilight-aligned.tar.gz librilight-aligned
# echo "Compressing librilight-medium-aligned...."
# COPYFILE_DISABLE=1 tar -cf librilight-medium-aligned.tar.gz librilight-medium-aligned
# echo "Compressing librilight-large-aligned...."
# COPYFILE_DISABLE=1 tar -cf librilight-large-aligned.tar.gz librilight-large-aligned

echo "Checksumming librilight-aligned.tar.gz..."
sha1=`shasum -a 1 librilight-aligned.tar.gz | cut -d ' ' -f 1`
sha256=`shasum -a 256 librilight-aligned.tar.gz | cut -d ' ' -f 1`
md5=`md5sum librilight-aligned.tar.gz | cut -d ' ' -f 1`
echo "sha1: $sha1"
echo "sha256: $sha256"
echo "md5: $md5"

echo "Checksumming librilight-medium-aligned.tar.gz..."
sha1=`shasum -a 1 librilight-medium-aligned.tar.gz | cut -d ' ' -f 1`
sha256=`shasum -a 256 librilight-medium-aligned.tar.gz | cut -d ' ' -f 1`
md5=`md5sum librilight-medium-aligned.tar.gz | cut -d ' ' -f 1`
echo "sha1: $sha1"
echo "sha256: $sha256"
echo "md5: $md5"

# echo "Checksumming librilight-large-aligned.tar..."
# sha1=`shasum -a 1 librilight-large-aligned.tar.gz | cut -d ' ' -f 1`
# sha256=`shasum -a 256 librilight-large-aligned.tar.gz | cut -d ' ' -f 1`
# md5=`md5sum librilight-large-aligned.tar.gz | cut -d ' ' -f 1`
# echo "sha1: $sha1"
# echo "sha256: $sha256"
# echo "md5: $md5"