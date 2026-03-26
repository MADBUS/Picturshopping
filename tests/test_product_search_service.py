"""통합 서비스 테스트 - 이미지 분석 + 쇼핑 검색"""
import pytest
from unittest.mock import patch, MagicMock


class TestProductSearchServiceExists:
    """ProductSearchService 클래스 존재 테스트"""

    @patch('src.product_search_service.ImageAnalyzer')
    @patch('src.product_search_service.NaverShopping')
    def test_service_class_exists(self, mock_naver, mock_analyzer):
        """ProductSearchService 클래스가 존재해야 함"""
        from src.product_search_service import ProductSearchService
        assert ProductSearchService is not None

    @patch('src.product_search_service.ImageAnalyzer')
    @patch('src.product_search_service.NaverShopping')
    def test_service_has_search_by_image_method(self, mock_naver, mock_analyzer):
        """search_by_image 메서드가 있어야 함"""
        from src.product_search_service import ProductSearchService
        service = ProductSearchService(
            gemini_api_key="test-key",
            naver_client_id="test-id",
            naver_client_secret="test-secret"
        )
        assert hasattr(service, 'search_by_image')
        assert callable(service.search_by_image)


class TestProductSearchServiceSearch:
    """ProductSearchService.search_by_image 테스트"""

    @patch('src.product_search_service.NaverShopping')
    @patch('src.product_search_service.ImageAnalyzer')
    def test_search_by_image_returns_results(self, mock_analyzer_cls, mock_naver_cls):
        """이미지로 검색하면 분석 결과와 상품 목록을 반환해야 함"""
        from src.product_search_service import ProductSearchService

        # Mock 설정
        mock_analyzer = MagicMock()
        mock_analyzer.analyze.return_value = {
            "product_name": "삼성 갤럭시 버즈",
            "brand": "삼성",
            "category": "이어폰",
            "keywords": ["무선", "이어폰", "블루투스"]
        }
        mock_analyzer_cls.return_value = mock_analyzer

        mock_naver = MagicMock()
        mock_naver.search.return_value = [
            {"title": "삼성 갤럭시 버즈2", "price": 150000, "link": "http://...", "mall_name": "쿠팡"}
        ]
        mock_naver_cls.return_value = mock_naver

        service = ProductSearchService(
            gemini_api_key="test-key",
            naver_client_id="test-id",
            naver_client_secret="test-secret"
        )
        result = service.search_by_image("test_image.jpg")

        assert "analysis" in result
        assert "products" in result
        assert result["analysis"]["product_name"] == "삼성 갤럭시 버즈"
        assert len(result["products"]) > 0
