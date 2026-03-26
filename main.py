"""전자제품 이미지 인식 & 쇼핑 검색 서비스"""
import os
from dotenv import load_dotenv
from src.product_search_service import ProductSearchService

# .env.dev 파일에서 환경변수 로드
load_dotenv(".env.dev")

# 이미지 검색 폴더
SEARCH_FOLDER = "searchfolder"


def format_price(price: int) -> str:
    """가격을 원화 형식으로 포맷팅"""
    return f"{price:,}원"


def get_image_files(folder: str) -> list:
    """폴더에서 이미지 파일 목록 가져오기"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    files = []

    if not os.path.exists(folder):
        return files

    for filename in os.listdir(folder):
        ext = os.path.splitext(filename)[1].lower()
        if ext in image_extensions:
            files.append(filename)

    return sorted(files)


def select_image(folder: str) -> str:
    """폴더 내 이미지 목록에서 선택"""
    images = get_image_files(folder)

    if not images:
        print(f"'{folder}' 폴더에 이미지가 없습니다.")
        return None

    print(f"\n['{folder}' 폴더의 이미지 목록]")
    print("-" * 40)
    for i, filename in enumerate(images, 1):
        print(f"  {i}. {filename}")
    print(f"  0. 직접 경로 입력")
    print("-" * 40)

    while True:
        choice = input("선택 (번호 입력): ").strip()

        if choice == '0':
            return input("이미지 경로 입력: ").strip()

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(images):
                return os.path.join(folder, images[idx])
            else:
                print("올바른 번호를 입력해주세요.")
        except ValueError:
            print("숫자를 입력해주세요.")


def print_results(result: dict) -> None:
    """검색 결과 출력"""
    analysis = result["analysis"]
    products = result["products"]

    print("\n" + "=" * 60)
    print("[이미지 분석 결과]")
    print("=" * 60)
    print(f"  제품명: {analysis.get('product_name', 'N/A')}")
    print(f"  브랜드: {analysis.get('brand', 'N/A')}")
    print(f"  카테고리: {analysis.get('category', 'N/A')}")
    print(f"  키워드: {', '.join(analysis.get('keywords', []))}")

    print("\n" + "=" * 60)
    print(f"[네이버 쇼핑 검색 결과] ({len(products)}개)")
    print("=" * 60)

    if not products:
        print("  검색 결과가 없습니다.")
        return

    for i, product in enumerate(products, 1):
        print(f"\n  [{i}] {product['title']}")
        print(f"      가격: {format_price(product['price'])}")
        print(f"      판매처: {product['mall_name']}")
        print(f"      링크: {product['link']}")


def run_demo():
    """CLI 데모 실행"""
    # 환경변수에서 API 키 로드
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    naver_client_id = os.environ.get("NAVER_CLIENT_ID")
    naver_client_secret = os.environ.get("NAVER_CLIENT_SECRET")

    # API 키 확인
    if not gemini_api_key or gemini_api_key == "your-gemini-api-key-here":
        print("오류: GEMINI_API_KEY를 .env.dev 파일에 설정해주세요.")
        return

    if not naver_client_id or not naver_client_secret:
        print("오류: NAVER_CLIENT_ID와 NAVER_CLIENT_SECRET을 .env.dev 파일에 설정해주세요.")
        return

    print("=" * 60)
    print("  전자제품 이미지 인식 & 쇼핑 검색 서비스")
    print("=" * 60)

    # 서비스 초기화
    service = ProductSearchService(
        gemini_api_key=gemini_api_key,
        naver_client_id=naver_client_id,
        naver_client_secret=naver_client_secret
    )

    while True:
        try:
            # 이미지 선택
            image_path = select_image(SEARCH_FOLDER)

            if not image_path:
                continue

            if image_path.lower() in ['quit', 'exit', 'q', '종료']:
                print("\n이용해주셔서 감사합니다!")
                break

            if not os.path.exists(image_path):
                print(f"파일을 찾을 수 없습니다: {image_path}")
                continue

            print(f"\n'{os.path.basename(image_path)}' 분석 중...")
            result = service.search_by_image(image_path)
            print_results(result)

            print("\n")
            cont = input("계속하시겠습니까? (y/n): ").strip().lower()
            if cont not in ['y', 'yes', '']:
                print("\n이용해주셔서 감사합니다!")
                break

        except KeyboardInterrupt:
            print("\n\n프로그램을 종료합니다.")
            break
        except Exception as e:
            print(f"\n오류 발생: {e}")


if __name__ == "__main__":
    run_demo()
