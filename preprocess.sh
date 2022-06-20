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
mkdir -p image/all/
for letter in {A..Z}; do
  mkdir image/all/${letter}
done

#  Move train dataset to the image directory
for letter in {A..Z}; do
  ls asl_alphabet_train/asl_alphabet_train/${letter} | sort -R | tail -500 | while read file; do
    cp asl_alphabet_train/asl_alphabet_train/${letter}/${file} image/all/${letter}/$(ls image/all/${letter} | wc -l).jpg
  done
  ls ASL_Dataset/Train/${letter} | sort -R | tail -500 | while read file; do
    cp ASL_Dataset/Train/${letter}/${file} image/all/${letter}/$(ls image/all/${letter} | wc -l).jpg
  done
  ls dataset/train/${letter} | sort -R | tail -500 | while read file; do
    cp dataset/train/${letter}/${file} image/all/${letter}/$(ls image/all/${letter} | wc -l).jpg
  done
done

#  Delete all files/directories except the image directory
ls | grep -xv image | xargs rm -r

#  Resize images to 200x200
cd image/all/
for letter in {A..Z}; do
  for filename in *; do
    if [ $(identify -format '%wx%h' ${filename}) != "200x200" ]; then
      convert ${filename} -resize 200x200 ${filename}
    fi
  done
done
cd ../

#  Split the dataset into train and test
mkdir test/
for letter in {A..Z}; do
  mkdir test/${letter}
done

cp -R all/ train/
for letter in {A..Z}; do
  ls train/${letter} | sort -R | tail -100 | while read file; do
    mv train/${letter}/${file} test/${letter}/${file}
  done
done

#  Convert images to csv files
mkdir -p csv/train/ csv/test/
python3 preprocess.py