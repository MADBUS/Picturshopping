"""Image Analyzer Service - Gemini Vision API"""
import json
from google import genai
from PIL import Image


ANALYSIS_PROMPT = """이 이미지에 있는 전자제품을 분석해주세요.
다음 JSON 형식으로만 답변해주세요 (다른 텍스트 없이):

{
    "product_name": "제품명",
    "brand": "브랜드명",
    "category": "카테고리 (예: 노트북, 스마트폰, 이어폰, 태블릿 등)",
    "keywords": ["검색에 사용할 키워드1", "키워드2", "키워드3"]
}

제품을 인식할 수 없으면 product_name을 "unknown"으로 설정해주세요."""


class ImageAnalyzer:
    """Gemini Vision API를 사용하여 이미지를 분석하는 서비스"""

    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        """
        ImageAnalyzer 초기화

        Args:
            api_key: Gemini API 키
            model: 사용할 모델 (기본값: gemini-2.5-flash)
        """
        self.api_key = api_key
        self.model = model
        self.client = genai.Client(api_key=api_key)

    def analyze(self, image_path: str) -> dict:
        """
        이미지를 분석하여 전자제품 정보 추출

        Args:
            image_path: 분석할 이미지 경로

        Returns:
            분석 결과 딕셔너리 (product_name, brand, category, keywords)
        """
        image = Image.open(image_path)

        response = self.client.models.generate_content(
            model=self.model,
            contents=[image, ANALYSIS_PROMPT]
        )

        result_text = response.text.strip()
        if result_text.startswith("```json"):
            result_text = result_text[7:]
        if result_text.startswith("```"):
            result_text = result_text[3:]
        if result_text.endswith("```"):
            result_text = result_text[:-3]

        return json.loads(result_text.strip())
