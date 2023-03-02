# 프로젝트 안내
이 프로젝트는 음원 사이트 지니뮤직에서 그룹 에픽하이의 전곡 음원 정보를 크롤링하고, 해당 정보를 활용하여 가사 등의 인상적인 정보를 추출하고 간단하게 분석하는 것을 목적으로 하였다.

# 프로젝트 파일 구성
- ```lytics_crawling.py``` : 지니뮤직에서 곡정보와 가사 크롤링
  - ```selenium```, ```Pandas``` 사용
  - 해당 파일을 통해 ```crawling_2.csv```, ```crawling_3_new.csv```, ```crawling_3.csv```, ```crawling_5.csv```, ```crawling_final.csv```를 추출
- ```lyrics_preprocessing.ipynb``` : 앞서 만든 ```crawling_final.csv``` 파일에서 중복된 곡을 제거하고 전곡 가사의 텍스트를 가공 후 저장
  - ```Pandas``` 사용
  - 해당 파일을 통해 가사 및 곡정보를 ```tracks_final.csv``` 로 정리
- ```lyrics_analysis_korean.ipynb``` : 한국어 가사 품사별 Tokenize & 분석
  - ```KoNLPy```의 ```Okt``` 사용
  - ```pos``` 메소드를 이용하여 단어를 품사별로 구별하고, ```Counter```를 이용하여 이를 품사별 단어 빈도수 순위를 매김
  - 다양한 단어의 가사 속 등장 빈도수와 그 순위, 순위의 상대적 위치(예: "사랑: 7등, 289회, 상위 0.15%")를 알아보며 그룹이 표현해 온 정서를 추측해 봄
  - 특정 곡 단위로 가사 텍스트를 가공해 봄
  - 등장 빈도가 적은 단어와 많은 단어의 규모를 각각 비교하여 단어 등장 빈도의 편중 현상을 짚어냄
- ```lyrics_analysis_album.ipynb``` : 앞서 만든 ```crawling_final.csv``` 파일을 앨범별로 분류
- ```lyrics_analysis_english.ipynb``` : 영어 가사 품사별 Tokenize & 분석
  - ```nltk``` 및 ```tensorflow``` 사용 예정
  
