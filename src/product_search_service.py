"""Product Search Service - 이미지 분석 + 쇼핑 검색 통합"""
from typing import Dict, Any
from src.image_analyzer import ImageAnalyzer
from src.naver_shopping import NaverShopping


class ProductSearchService:
    """이미지 분석과 쇼핑 검색을 통합한 서비스"""

    def __init__(
        self,
        gemini_api_key: str,
        naver_client_id: str,
        naver_client_secret: str
    ):
        """
        ProductSearchService 초기화

        Args:
            gemini_api_key: Gemini API 키
            naver_client_id: 네이버 API Client ID
            naver_client_secret: 네이버 API Client Secret
        """
        self.analyzer = ImageAnalyzer(api_key=gemini_api_key)
        self.shopping = NaverShopping(
            client_id=naver_client_id,
            client_secret=naver_client_secret
        )

    def search_by_image(self, image_path: str, num_results: int = 10) -> Dict[str, Any]:
        """
        이미지를 분석하고 유사 상품 검색

        Args:
            image_path: 분석할 이미지 경로
            num_results: 검색 결과 개수

        Returns:
            {
                "analysis": 이미지 분석 결과,
                "products": 쇼핑 검색 결과 목록
            }
        """
        # 1. 이미지 분석
        analysis = self.analyzer.analyze(image_path)

        # 2. 검색어 생성 (제품명 + 브랜드)
        search_query = f"{analysis.get('brand', '')} {analysis.get('product_name', '')}"
        if analysis.get('keywords'):
            search_query += " " + " ".join(analysis['keywords'][:2])

        # 3. 쇼핑 검색
        products = self.shopping.search(search_query.strip(), display=num_results)

        return {
            "analysis": analysis,
            "products": products
        }
