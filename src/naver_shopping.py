"""Naver Shopping API Service"""
import requests
from typing import List, Dict, Any


class NaverShopping:
    """네이버 쇼핑 API를 사용하여 상품을 검색하는 서비스"""

    API_URL = "https://openapi.naver.com/v1/search/shop.json"

    def __init__(self, client_id: str, client_secret: str):
        """
        NaverShopping 초기화

        Args:
            client_id: 네이버 API Client ID
            client_secret: 네이버 API Client Secret
        """
        self.client_id = client_id
        self.client_secret = client_secret

    def search(self, query: str, display: int = 10) -> List[Dict[str, Any]]:
        """
        네이버 쇼핑에서 상품 검색

        Args:
            query: 검색어
            display: 검색 결과 개수 (기본값: 10)

        Returns:
            상품 목록 (title, price, link, mall_name 포함)
        """
        headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret
        }
        params = {
            "query": query,
            "display": display
        }

        response = requests.get(self.API_URL, headers=headers, params=params)
        data = response.json()

        products = []
        for item in data.get("items", []):
            products.append({
                "title": item.get("title", "").replace("<b>", "").replace("</b>", ""),
                "price": int(item.get("lprice", 0)),
                "link": item.get("link", ""),
                "mall_name": item.get("mallName", "")
            })

        return products
