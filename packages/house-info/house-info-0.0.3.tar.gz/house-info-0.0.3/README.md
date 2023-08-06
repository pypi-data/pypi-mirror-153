# house-info

## 공공 주택 정보 데이터 수집기

공공 주택 정보를 수집하기 위해서 만들었다.  
행복주택, 매입임대주택, 역세권 청년주택 모집 공고를 추적하기 위해서 개발하였다.  
공공 주택은 공고를 계속 추적하고, 지원 자격만 된다면 마구 지원하는 것이 당첨 확률을 높이는 것이다.  
SH, 마이홈, 역세권 청년주택 데이터를 가져올 수 있다. 역세권 청년주택의 경우는 민간 공급도 포함된다.

## 설치

```shell
pip install house-info
```

## 사용

마이홈과 역세권 청년주택데이터는 chromedriver가 필요하다.

```python
# SH 데이터
from house_info.sh import SHDataManager
from house_info.my_home import MyHomeDataManager
from house_info.station_area import StationAreaDataManager


manager = SHDataManager(page=3) # multi threading 사용은 thread=True
manager.export_csv("sh.csv")

# 마이홈 데이터
# types = "student" or "couple" -> 대학생, 신혼부부
# region = "seoul" or "kkd" -> 서울, 경기도
manager = MyHomeDataManager("./chromedriver.exe", 3, types="student", region="seoul")
manager.export_csv("myhome.csv")

# 역세권 청년주택 데이터
manager = StationAreaDataManager("./chromedriver.exe", 3)
manager.export_csv("sa.csv")
```
