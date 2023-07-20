import os
import shutil
from bing_image_downloader import downloader


directory_list = [
    './custom_dataset/train/',
    './custom_dataset/test/',
]

# 초기 디렉토리 만들기
for directory in directory_list:
    if not os.path.isdir(directory):
        os.makedirs(directory)

# 수집한 이미지를 학습 데이터와 평가 데이터로 구분하는 함수
def dataset_split(query, train_cnt):
    # 학습 및 평가 데이터셋 디렉토리 만들기
    for directory in directory_list:
        if not os.path.isdir(directory + '/' + query):
            os.makedirs(directory + '/' + query)
    # 학습 및 평가 데이터셋 준비하기
    cnt = 0
    for file_name in os.listdir(query):
        if cnt < train_cnt:
            print(f'[Train Dataset] {file_name}')
            shutil.move(query + '/' + file_name, './custom_dataset/train/' + query + '/' + file_name)
        else:
            print(f'[Test Dataset] {file_name}')
            shutil.move(query + '/' + file_name, './custom_dataset/test/' + query + '/' + file_name)
        cnt += 1
    shutil.rmtree(query)

query = '마동석'
downloader.download(query, limit=200,  output_dir='./', adult_filter_off=True, force_replace=False, timeout=20)
dataset_split(query, 190)

query = '김종국'
downloader.download(query, limit=200,  output_dir='./', adult_filter_off=True, force_replace=False, timeout=20)
dataset_split(query, 190)

query = '이병헌'
downloader.download(query, limit=200,  output_dir='./', adult_filter_off=True, force_replace=False, timeout=20)
dataset_split(query, 190)

query = '조정석'
downloader.download(query, limit=200,  output_dir='./', adult_filter_off=True, force_replace=False, timeout=20)
dataset_split(query, 190)

query = '김희철'
downloader.download(query, limit=200,  output_dir='./', adult_filter_off=True, force_replace=False, timeout=20)
dataset_split(query, 190)

query = '김장훈'
downloader.download(query, limit=200,  output_dir='./', adult_filter_off=True, force_replace=False, timeout=20)
dataset_split(query, 190)

query = '민경훈'
downloader.download(query, limit=200,  output_dir='./', adult_filter_off=True, force_replace=False, timeout=20)
dataset_split(query, 190)

query = '황정민'
downloader.download(query, limit=200,  output_dir='./', adult_filter_off=True, force_replace=False, timeout=20)
dataset_split(query, 190)

query = '장동건'
downloader.download(query, limit=200,  output_dir='./', adult_filter_off=True, force_replace=False, timeout=20)
dataset_split(query, 190)