# 전자제품 이미지 인식 & 쇼핑 검색 서비스

전자제품 사진을 업로드하면 Gemini Vision API로 제품을 인식하고, 네이버 쇼핑에서 유사 상품을 검색해주는 서비스입니다.

## 기능

1. **이미지 분석**: Gemini Vision API로 전자제품 사진 분석
2. **제품 정보 추출**: 제품명, 브랜드, 카테고리, 키워드 자동 추출
3. **쇼핑 검색**: 네이버 쇼핑 API로 유사 상품 검색
4. **가격 비교**: 여러 쇼핑몰의 가격 및 링크 제공

## 기술 스택

| 구성요소 | 기술 |
|----------|------|
| 언어 | Python |
| 이미지 분석 | Gemini 2.5 Flash (Vision) |
| 쇼핑 검색 | 네이버 쇼핑 API |
| 이미지 처리 | Pillow |

---

## 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. API 키 설정
`.env.dev` 파일 생성 후 API 키 입력:
```
GEMINI_API_KEY=your-gemini-api-key
NAVER_CLIENT_ID=your-naver-client-id
NAVER_CLIENT_SECRET=your-naver-client-secret
```

**API 키 발급:**
- Gemini: https://aistudio.google.com/app/apikey
- 네이버: https://developers.naver.com (검색 > 쇼핑 API)

### 3. 실행
```bash
python main.py
```

---

## 사용법

1. `searchfolder/` 폴더에 분석할 전자제품 이미지를 넣습니다
2. `python main.py` 실행
3. 목록에서 분석할 이미지 번호 선택
4. 분석 결과 및 쇼핑 검색 결과 확인

```
============================================================
  전자제품 이미지 인식 & 쇼핑 검색 서비스
============================================================

['searchfolder' 폴더의 이미지 목록]
----------------------------------------
  1. earphone.jpeg
  2. notebook.jpeg
  0. 직접 경로 입력
----------------------------------------
선택 (번호 입력): 1

'earphone.jpeg' 분석 중...

============================================================
[이미지 분석 결과]
============================================================
  제품명: 삼성 갤럭시 버즈
  브랜드: 삼성
  카테고리: 이어폰
  키워드: 무선, 블루투스, TWS

============================================================
[네이버 쇼핑 검색 결과] (10개)
============================================================

  [1] 삼성 갤럭시 버즈2 프로
      가격: 159,000원
      판매처: 삼성스토어
      링크: https://...
```

---

## 프로젝트 구조

```
pictureclass/
├── main.py                         # CLI 데모 실행 파일
├── src/
│   ├── image_analyzer.py           # Gemini Vision 이미지 분석
│   ├── naver_shopping.py           # 네이버 쇼핑 API 검색
│   └── product_search_service.py   # 통합 서비스
├── tests/                          # 테스트 코드
├── searchfolder/                   # 분석할 이미지 폴더
├── .env.dev                        # API 키 (git 제외)
└── requirements.txt                # 의존성
```

---

## 핵심 코드

### 이미지 분석 (image_analyzer.py)
```python
from src.image_analyzer import ImageAnalyzer

analyzer = ImageAnalyzer(api_key="your-gemini-key")
result = analyzer.analyze("earphone.jpeg")
# {
#     "product_name": "삼성 갤럭시 버즈",
#     "brand": "삼성",
#     "category": "이어폰",
#     "keywords": ["무선", "블루투스", "TWS"]
# }
```

### 쇼핑 검색 (naver_shopping.py)
```python
from src.naver_shopping import NaverShopping

shopping = NaverShopping(client_id="...", client_secret="...")
products = shopping.search("삼성 갤럭시 버즈")
# [
#     {"title": "갤럭시 버즈2", "price": 159000, "link": "...", "mall_name": "쿠팡"},
#     ...
# ]
```

### 통합 서비스 (product_search_service.py)
```python
from src.product_search_service import ProductSearchService

service = ProductSearchService(
    gemini_api_key="...",
    naver_client_id="...",
    naver_client_secret="..."
)
result = service.search_by_image("earphone.jpeg")
# {
#     "analysis": {...},   # 이미지 분석 결과
#     "products": [...]    # 쇼핑 검색 결과
# }
```

---

## 테스트 실행

```bash
python -m pytest tests/ -v
```

---

## 라이선스

MIT License
