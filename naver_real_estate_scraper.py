from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import json
import requests
import time

# Search parameters
params = ["정왕동", "아파트", "매매", "30000", "100000"]

# Test with Samsung-dong (Gangnam-gu, Seoul) - a well-known area with many apartments
JUNGWANG_DONG_CODE = "1168010500"

# Property type mapping (Korean to API code)
property_type_map = {
    "아파트": "APT",
    "오피스텔": "OPST",
    "빌라": "VL",
    "원룸": "OR",
    "상가": "SG",
    "토지": "TJ"
}

# Trade type mapping (Korean to API code)
trade_type_map = {
    "매매": "A1",
    "전세": "B1",
    "월세": "B2",
    "단기임대": "B3"
}

def build_search_url(dong_code, property_type, trade_type, min_price, max_price, page=1):
    """Build Naver Real Estate search URL."""
    url = f"https://m.land.naver.com/cluster/ajax/articleList?cortarNo={dong_code}&rletTpCd={property_type}&tradTpCd={trade_type}&dprcMin={min_price}&dprcMax={max_price}&page={page}"
    return url

def init_driver():
    """Initialize Selenium WebDriver with Chrome options (headless DISABLED per requirements)."""
    options = Options()
    
    # Do NOT enable headless mode (browser must be visible per user requirement)
    # options.add_argument("--headless") # COMMENTED OUT per user requirement
    
    # Set window size
    options.add_argument("--window-size=1920,1080")
    
    # Use stable Chrome options
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Initialize driver (Selenium 4+ handles driver management automatically)
    driver = webdriver.Chrome(options=options)
    return driver

def fetch_articles(driver, url):
    """Fetch articles from Naver Real Estate AJAX endpoint using requests library."""
    try:
        # Make HTTP request with proper headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'ko-KR,ko;q=0.9,en;q=0.8',
            'Referer': 'https://m.land.naver.com/'
        }

        print(f"요청 URL: {url}")
        response = requests.get(url, headers=headers)

        # Check if request was successful
        if response.status_code != 200:
            print(f"HTTP 요청 실패: 상태 코드 {response.status_code}")
            print(f"URL: {url}")
            print(f"응답 내용: {response.text[:500]}")
            return []

        # Get response text
        response_text = response.text

        print(f"응답 길이: {len(response_text)}")
        print(f"응답 시작부: {response_text[:200]}")

        try:
            # Parse JSON from response
            json_data = json.loads(response_text)

            # Extract article list from JSON response
            articles = json_data.get("result", {}).get("list", [])

            print(f"찾은 매물 수: {len(articles)}")

            # Extract details for each article
            extracted_articles = []
            for article in articles:
                article_details = extract_article_details(article)
                extracted_articles.append(article_details)

            return extracted_articles

        except json.JSONDecodeError as e:
            print(f"JSON 파싱 오류: API 응답이 JSON 형식이 아닙니다.")
            print(f"URL: {url}")
            print(f"에러 위치: {e.pos}")
            # Print context around the error for debugging
            start = max(0, e.pos - 50)
            end = min(len(response_text), e.pos + 50)
            print(f"에러 근처 내용: ...{response_text[start:end]}...")
            return []

    except requests.RequestException as e:
        print(f"HTTP 요청 오류: {str(e)}")
        print(f"URL: {url}")
        return []

def extract_article_details(article_dict):
    """Extract property details from article dictionary returned by Naver Real Estate API."""
    article = {
        "price": article_dict.get("prc"),
        "area": article_dict.get("spc1"),
        "floor": article_dict.get("flrInfo"),
        "address": article_dict.get("atclNm"),
        "property_type": article_dict.get("rletTpCd"),
        "trade_type": article_dict.get("tradTpNm"),
        "broker_info": article_dict.get("blkkNo")
    }
    return article

def main():
    """
    Orchestrate entire Naver Real Estate scraping process.
    """
    # Read search parameters
    dong_name = params[0]
    property_type = params[1]
    trade_type = params[2]
    min_price = params[3]
    max_price = params[4]
    
    # Map to API codes
    property_type_kr = property_type_map.get(property_type, property_type)
    trade_type_kr = trade_type_map.get(trade_type, trade_type)
    
    # Build search URL
    url = build_search_url(JUNGWANG_DONG_CODE, property_type_kr, trade_type_kr, min_price, max_price, page=1)
    
    # Initialize driver
    driver = init_driver()
    
    try:
        # Fetch articles
        articles = fetch_articles(driver, url)
        
        # Display results
        if not articles:
            print("검색 결과가 없습니다.")
        else:
            for i, article in enumerate(articles, 1):
                print(f"\n=== 매물 {i} ===")
                print(f"가격: {article.get('prc')}")
                print(f"면적: {article.get('spc1')}")
                print(f"층: {article.get('flrInfo')}")
                print(f"주소: {article.get('atclNm')}")
                print(f"매물유형: {article.get('property_type')}")
                print(f"거래유형: {article.get('trade_type')}")
                print(f"중개업체 연락처: {article.get('blkkNo')}")
                print()
    finally:
        driver.quit()
    
if __name__ == "__main__":
    main()
