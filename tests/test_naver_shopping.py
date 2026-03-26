"""네이버 쇼핑 API 서비스 테스트"""
import pytest
from unittest.mock import patch, MagicMock


class TestNaverShoppingExists:
    """NaverShopping 클래스 존재 테스트"""

    def test_naver_shopping_class_exists(self):
        """NaverShopping 클래스가 존재해야 함"""
        from src.naver_shopping import NaverShopping
        assert NaverShopping is not None

    def test_naver_shopping_has_search_method(self):
        """NaverShopping에 search 메서드가 있어야 함"""
        from src.naver_shopping import NaverShopping
        client = NaverShopping(client_id="test-id", client_secret="test-secret")
        assert hasattr(client, 'search')
        assert callable(client.search)


class TestNaverShoppingSearch:
    """NaverShopping.search 메서드 테스트"""

    @patch('src.naver_shopping.requests')
    def test_search_returns_products(self, mock_requests):
        """search가 상품 목록을 반환해야 함"""
        from src.naver_shopping import NaverShopping

        # Mock API 응답
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "items": [
                {
                    "title": "삼성 갤럭시 버즈2 프로",
                    "link": "https://example.com/product1",
                    "lprice": "180000",
                    "mallName": "삼성스토어"
                },
                {
                    "title": "삼성 갤럭시 버즈 FE",
                    "link": "https://example.com/product2",
                    "lprice": "99000",
                    "mallName": "쿠팡"
                }
            ]
        }
        mock_response.status_code = 200
        mock_requests.get.return_value = mock_response

        client = NaverShopping(client_id="test-id", client_secret="test-secret")
        results = client.search("삼성 갤럭시 버즈")

        assert len(results) == 2
        assert results[0]["title"] == "삼성 갤럭시 버즈2 프로"
        assert results[0]["price"] == 180000
        assert "link" in results[0]
