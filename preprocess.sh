#!/usr/bin/expect -f

pip3 install kaggle

#  You need to create an API token on Kaggle.com
#  https://github.com/Kaggle/kaggle-api#api-credentials

mkdir dataset
cd dataset

#  Download dataset
kaggle dataset download -d grassknoted/asl-alphabet
kaggle dataset download -d kapillondhe/american-sign-language
kaggle dataset download -d joannracheljacob/american-sign-language-dataset

#  Unzip dataset
for filename in *; do
  unzip "$filename"
done

#  Create a directory to gather all files
mkdir image
for letter in {A..Z}; do
  mkdir image/${letter}
done

#  Move all files to the image directory
for letter in {A..Z}; do
  ls asl_alphabet_train/asl_alphabet_train/${letter} | sort -R | tail -500 | while read file; do
    cp asl_alphabet_train/asl_alphabet_train/${letter}/${file} image/${letter}/$(ls image/${letter} | wc -l).jpg
  done
  ls ASL_Dataset/Train/${letter} | sort -R | tail -500 | while read file; do
    cp ASL_Dataset/Train/${letter}/${file} image/${letter}/$(ls image/${letter} | wc -l).jpg
  done
  ls dataset/train/${letter} | sort -R | tail -500 | while read file; do
    cp dataset/train/${letter}/${file} image/${letter}/$(ls image/${letter} | wc -l).jpg
  done
done

#  Delete all files/directories except the image directory
ls | grep -xv image | xargs rm -r