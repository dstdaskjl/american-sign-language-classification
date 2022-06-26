#!/usr/bin/expect -f

#  You need to create an API token on Kaggle.com
#  https://github.com/Kaggle/kaggle-api#api-credentials

pip3 install kaggle
mkdir dataset
cd dataset

#  Download dataset
kaggle datasets download -d grassknoted/asl-alphabet
kaggle datasets download -d kapillondhe/american-sign-language
kaggle datasets download -d joannracheljacob/american-sign-language-dataset

#  Unzip dataset
for filename in *; do
  unzip "$filename"
done

#  Create a directory to gather all files
mkdir train/
for letter in {A..Z}; do
  mkdir train/${letter}
done

#  Move train dataset to the image directory
for letter in {A..Z}; do
  ls asl_alphabet_train/asl_alphabet_train/${letter} | sort -R | tail -500 | while read file; do
    cp asl_alphabet_train/asl_alphabet_train/${letter}/${file} train/${letter}/$(ls train/${letter} | wc -l).jpg
  done
  ls ASL_Dataset/Train/${letter} | sort -R | tail -500 | while read file; do
    cp ASL_Dataset/Train/${letter}/${file} train/${letter}/$(ls train/${letter} | wc -l).jpg
  done
  ls dataset/train/${letter} | sort -R | tail -500 | while read file; do
    cp dataset/train/${letter}/${file} train/${letter}/$(ls train/${letter} | wc -l).jpg
  done
done

#  Delete all files/directories except the train directory
ls | grep -xv train | xargs rm -r

#  Resize images to 100x100
cd train/
for letter in {A..Z}; do
  echo ${letter}
  for filename in ${letter}/*; do
    if [ $(identify -format '%wx%h' ${filename}) != "100x100" ]; then
      convert ${filename} -resize 100x100 ${filename}
    fi
  done
done
cd ../

#  Split the dataset into train dataset and test dataset
mkdir test/
for letter in {A..Z}; do
  mkdir test/${letter}
done

for letter in {A..Z}; do
  ls train/${letter} | sort -R | tail -300 | while read file; do
    mv train/${letter}/${file} test/${letter}/${file}
  done
done

cd ../