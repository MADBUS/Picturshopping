"""이미지 분석 서비스 테스트"""
import pytest
from unittest.mock import patch, MagicMock


class TestImageAnalyzerExists:
    """ImageAnalyzer 클래스 존재 테스트"""

    @patch('src.image_analyzer.genai')
    def test_image_analyzer_class_exists(self, mock_genai):
        """ImageAnalyzer 클래스가 존재해야 함"""
        from src.image_analyzer import ImageAnalyzer
        assert ImageAnalyzer is not None

    @patch('src.image_analyzer.genai')
    def test_image_analyzer_has_analyze_method(self, mock_genai):
        """ImageAnalyzer에 analyze 메서드가 있어야 함"""
        from src.image_analyzer import ImageAnalyzer
        analyzer = ImageAnalyzer(api_key="test-key")
        assert hasattr(analyzer, 'analyze')
        assert callable(analyzer.analyze)


class TestImageAnalyzerAnalyze:
    """ImageAnalyzer.analyze 메서드 테스트"""

    @patch('src.image_analyzer.Image')
    @patch('src.image_analyzer.genai')
    def test_analyze_returns_product_info(self, mock_genai, mock_image):
        """analyze가 제품 정보를 반환해야 함"""
        from src.image_analyzer import ImageAnalyzer

        # Mock 설정
        mock_response = MagicMock()
        mock_response.text = '{"product_name": "삼성 갤럭시 버즈", "brand": "삼성", "category": "이어폰", "keywords": ["무선", "블루투스", "이어폰"]}'
        mock_genai.Client.return_value.models.generate_content.return_value = mock_response

        analyzer = ImageAnalyzer(api_key="test-key")
        result = analyzer.analyze("test_image.jpg")

        assert result is not None
        assert result["product_name"] == "삼성 갤럭시 버즈"
        assert result["brand"] == "삼성"
        assert result["category"] == "이어폰"
        assert "무선" in result["keywords"]

    @patch('src.image_analyzer.Image')
    @patch('src.image_analyzer.genai')
    def test_analyze_handles_json_code_block(self, mock_genai, mock_image):
        """analyze가 ```json 코드 블록을 처리해야 함"""
        from src.image_analyzer import ImageAnalyzer

        mock_response = MagicMock()
        mock_response.text = '```json\n{"product_name": "LG 그램", "brand": "LG", "category": "노트북", "keywords": ["노트북"]}\n```'
        mock_genai.Client.return_value.models.generate_content.return_value = mock_response

        analyzer = ImageAnalyzer(api_key="test-key")
        result = analyzer.analyze("test_image.jpg")

        assert result["product_name"] == "LG 그램"
