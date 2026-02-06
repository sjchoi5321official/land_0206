# 네이버 부동산 스크래핑 (Naver Real Estate Scraper)

## Context

### Original Request
네이버 부동산의 동 검색을 해서, 해당 매물 목록을 가져오는 파이썬 코드를 작성. 셀러니움으로 동작. venv 가상환경 사용.

### Interview Summary

**Key Discussions:**
- [params 설정]: 상단에 params 리스트로 하드코딩하여 한 번에 설정 가능하게
  - params = ["정왕동", "아파트", "매매", "10000", "50000"]
  - 최소/최소값은 만원 단위 (10000만원=1억 ~ 50000만원=5억)
- [동 코드]: 정왕동 코드(4117711300)를 하드코딩
- [데이터 추출]: 상세 정보 포함 (가격, 면적, 층, 주소, 매물유형, 거래유형, 중개업체 연락처)
- [저장 방식]: 콘솔 출력만 (파일 저장 X)
- [브라우저 모드]: 브라우저 보이기 (헤드리스 모드 X)
- [테스트 전략]: pytest 설치 후 TDD 적용

**Research Findings:**
- [site-structure]: 네이버 부동산은 m.land.naver.com (모바일)이 더 안정적
- [url-pattern]: `https://m.land.naver.com/cluster/ajax/articleList?cortarNo={code}&rletTpCd={type}&tradTpCd={trade}&dprcMin={min}&dprcMax={max}&page={page}`
- [trade-codes]: 매매=A1, 전세=B1, 월세=B2
- [building-codes]: 아파트=APT, 오피스텔=OPST, 빌라=VL, 원룸=OR, 상가=SG, 토지=TJ
- [anti-scraping]: Bearer token 없이도 API 접근 가능, rate limiting 존재 가능
- [best-practices]:
  - Selenium 4+: Selenium Manager가 드라이버 자동 관리 (webdriver-manager 불필요)
  - WebDriverWait 사용으로 동적 콘텐츠 로딩 대기 (time.sleep() 사용 금지)
  - BeautifulSoup으로 HTML 파싱 효율적
  - Explicit waits > Implicit waits
- [venv-status]: pip만 설치됨, Selenium, webdriver-manager, beautifulsoup4, pytest 필요

### Metis Review
**Note**: Metis consultation encountered technical issues. Self-analysis performed instead.

**Identified Gaps (addressed):**
- [Test framework]: pytest 설치 필요 확인 - 포함
- [Driver setup]: Selenium 4+ 자동 드라이버 관리 - 포함
- [Pagination handling]: 페이지네이션 처리 필요 - 포함
- [Error handling]: 네트워크 오류, 타임아웃 처리 - 포함
- [Empty results]: 매물이 없는 경우 처리 - 포함

---

## Work Objectives

### Core Objective
Selenium을 사용하여 네이버 부동산에서 정왕동 아파트 매매 매물(1억~5억) 목록을 스크래핑하고 상세 정보를 콘솔에 출력하는 파이썬 스크립트 작성

### Concrete Deliverables
- `naver_real_estate_scraper.py` - 메인 스크래핑 스크립트
- `test_scraper.py` - pytest 테스트 파일

### Definition of Done
- [ ] params 리스트로 동, 매물 유형, 거래 유형, 가격 범위 설정 가능
- [ ] 정왕동 아파트 매매 매물(1억~5억) 검색하여 매물 목록 추출
- [ ] 각 매물에서 상세 정보(가격, 면적, 층, 주소, 매물유형, 거래유형, 중개업체 연락처) 추출
- [ ] 추출한 정보를 콘솔에 출력
- [ ] TDD로 pytest 테스트 작성 및 통과
- [ ] 브라우저가 보이는 상태로 실행 (헤드리스 모드 X)

### Must Have
- params 리스트 상단 하드코딩
- 정왕동 코드(4117711300) 하드코딩
- 상세 정보 필드 모두 추출 (가격, 면적, 층, 주소, 매물유형, 거래유형, 중개업체 연락처)
- 콘솔 출력만 (파일 저장 X)
- 브라우저 보이기 (헤드리스 모드 X)
- TDD 적용 (pytest)

### Must NOT Have (Guardrails)
- 파일 저장 (CSV, JSON 등) - 콘솔 출력만
- 헤드리스 모드 - 브라우저를 보이게 실행
- time.sleep() 사용 - WebDriverWait로 대기 처리
- 수동 ChromeDriver 설치 - Selenium Manager 사용
- 파일 시스템 접근/쓰기 - 읽기만

---

## Verification Strategy (MANDATORY)

> TDD 전략: 각 작업은 RED-GREEN-REFACTOR 패턴을 따름

### Test Decision
- **Infrastructure exists**: NO (pip만 설치됨)
- **User wants tests**: YES (TDD with pytest)
- **Framework**: pytest
- **QA approach**: TDD

### TDD Workflow

각 작업은 다음 구조를 따름:

**RED 단계 (실패하는 테스트 작성):**
1. 테스트 파일에 테스트 케이스 작성
2. `pytest` 실행하여 테스트가 실패함을 확인
3. 구현 코드가 없으므로 실패해야 함

**GREEN 단계 (최소 구현으로 테스트 통과):**
1. 메인 코드에 최소한의 구현 추가
2. `pytest` 실행하여 테스트가 통과함을 확인

**REFACTOR 단계 (코드 정리):**
1. 코드 구조 개선, 변수명 명확화
2. `pytest` 재실행하여 여전히 통과하는지 확인

### Test Setup Task

스크래핑 작업 전에 테스트 인프라 설정:

- [ ] 0. Test Infrastructure Setup
  - Install: `./venv/Scripts/pip.exe install -U pytest pytest-selenium selenium beautifulsoup4`
  - Verify: `./venv/Scripts/pytest.exe --version` → pytest 버전 표시
  - Verify: `./venv/Scripts/python.exe -c "import selenium; import bs4; import pytest; print('OK')"` → OK 출력
  - Example test: `test_scraper.py`에 간단한 테스트 작성
  - Verify: `./venv/Scripts/pytest.exe test_scraper.py` → 1 test passed

---

## Task Flow

```
Task 0 (Test Setup) → Task 1 (RED) → Task 2 (GREEN) → Task 3 (GREEN) → Task 4 (GREEN)
                      ↓                  ↓                  ↓                  ↓
                   Task 5 (REFACTOR) → Task 6 (GREEN) → Task 7 (GREEN)
```

## Parallelization

| Group | Tasks | Reason |
|-------|-------|--------|
| N/A | Sequential | TDD는 순차적 접근 필요 |

---

## TODOs

- [ ] 0. Test Infrastructure Setup

  **What to do**:
  - pytest, pytest-selenium, selenium, beautifulsoup4 설치
  - 간단한 예제 테스트 작성하여 테스트 인프라 동작 확인

  **Must NOT do**:
  - webdriver-manager 설치 (Selenium 4+에서 자동 관리됨)
  - 파일 시스템에 쓰기 (파일 저장 금지)

  **Parallelizable**: NO (must run first)

  **References**:

  **Pattern References**: None (first task)

  **API/Type References**: None

  **Test References**:
  - [pytest documentation](https://docs.pytest.org/en/latest/) - pytest 기본 사용법
  - [pytest-selenium](https://pytest-selenium.readthedocs.io/) - Selenium과 pytest 통합

  **Documentation References**:
  - [Selenium Python Documentation](https://selenium.dev/selenium/docs/api/py/) - Selenium API 레퍼런스
  - [BeautifulSoup4 Docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - HTML 파싱

  **External References**:
  - Official docs: `https://selenium.dev/selenium/docs/api/py/` - Selenium 4+ Python API
  - Official docs: `https://docs.pytest.org/en/latest/` - pytest 문서

  **Acceptance Criteria**:

  **RED:**
  - [ ] Test file created: `test_scraper.py`
  - [ ] Test covers: pytest import and basic assertion
  - [ ] `./venv/Scripts/pytest.exe test_scraper.py -v` → FAIL (implementation doesn't exist yet)

  **GREEN:**
  - [ ] Install command executed: `./venv/Scripts/pip.exe install -U pytest pytest-selenium selenium beautifulsoup4`
  - [ ] Verify pytest: `./venv/Scripts/pytest.exe --version` → pytest version displayed
  - [ ] Verify imports: `./venv/Scripts/python.exe -c "import selenium; import bs4; import pytest; print('OK')"` → OK
  - [ ] Example test in `test_scraper.py`:
    ```python
    import pytest

    def test_example():
        assert True
    ```
  - [ ] `./venv/Scripts/pytest.exe test_scraper.py -v` → PASS (1 test passed)

  **Manual Execution Verification**:
  - [ ] Command: `./venv/Scripts/pip.exe list | findstr "pytest selenium beautifulsoup4"`
  - [ ] Expected: All packages listed with versions

  **Commit**: NO (infrastructure setup, groups with task 1)

---

- [ ] 1. Create Main Scraper Module (RED)

  **What to do**:
  - `naver_real_estate_scraper.py` 파일 생성
  - params 리스트 정의
  - 정왕동 코드 하드코딩
  - URL 빌드 함수 정의 (아직 구현 X)
  - Selenium driver 초기화 함수 정의 (아직 구현 X)

  **Must NOT do**:
  - 실제 기능 구현 (테스트만 작성)

  **Parallelizable**: NO (depends on 0)

  **References**:

  **Pattern References**: None (first code task)

  **API/Type References**: None

  **Test References**:
  - `test_scraper.py:TestScraper` - 테스트 구조 팔로우

  **Documentation References**:
  - [Naver Land URL Pattern](https://github.com/OHSEHOON99/naver-map-real-estate-scraper-selenium) - URL 구조 참고
  - [Selenium WebDriver](https://selenium.dev/selenium/docs/api/py/) - driver 초기화

  **External References**:
  - GitHub repo: `https://github.com/parkbsn1/landCrawling` - 네이버 부동산 스크래핑 예제

  **Acceptance Criteria**:

  **RED:**
  - [ ] File created: `naver_real_estate_scraper.py`
  - [ ] params defined: `params = ["정왕동", "아파트", "매매", "10000", "50000"]`
  - [ ] Jungwang-dong code: `JUNGWANG_DONG_CODE = "4117711300"`
  - [ ] URL builder function defined (no implementation)
  - [ ] Driver init function defined (no implementation)
  - [ ] Test file updated: `test_scraper.py` with tests for module structure
  - [ ] `./venv/Scripts/pytest.exe test_scraper.py -v -k test_scraper_module` → FAIL (implementation missing)

  **GREEN:**
  - [ ] Module exists at expected path
  - [ ] All constants defined correctly
  - [ ] `./venv/Scripts/pytest.exe test_scraper.py -v -k test_scraper_module` → PASS

  **REFACTOR:**
  - [ ] Code organized with clear constants section
  - [ ] Comments added for each constant purpose
  - [ ] `./venv/Scripts/pytest.exe test_scraper.py -v -k test_scraper_module` → PASS

  **Manual Execution Verification**:
  - [ ] Command: `./venv/Scripts/python.exe -c "import naver_real_estate_scraper; print(naver_real_estate_scraper.params)"`
  - [ ] Expected: `['정왕동', '아파트', '매매', '10000', '50000']`

  **Commit**: NO (groups with task 2)

---

- [ ] 2. Implement URL Builder Function (RED → GREEN)

  **What to do**:
  - URL 빌드 함수 구현
  - params에서 값을 읽어 URL 생성
  - 정왕동 코드, 아파트(APT), 매매(A1), 가격 범위 적용
  - 페이지네이션 지원 (page parameter)

  **Must NOT do**:
  - 실제 HTTP 요청 (URL 빌드만)

  **Parallelizable**: NO (depends on 1)

  **References**:

  **Pattern References**:
  - GitHub: `parkbsn1/landCrawling:landCrawling_ad.py` - URL 구축 패턴 참고

  **API/Type References**:
  - URL format: `https://m.land.naver.com/cluster/ajax/articleList?cortarNo={code}&rletTpCd={type}&tradTpCd={trade}&dprcMin={min}&dprcMax={max}&page={page}`

  **Test References**:
  - `test_scraper.py:test_url_builder` - URL 빌더 테스트

  **Documentation References**:
  - [URL Encoding](https://docs.python.org/3/library/urllib.parse.html) - URL 파라미터 인코딩

  **External References**:
  - Example repo: `https://github.com/parkbsn1/landCrawling` - URL 파라미터 구성 참고

  **Acceptance Criteria**:

  **RED:**
  - [ ] Test written: `test_url_builder()` in `test_scraper.py`
  - [ ] Test covers: URL generation with correct parameters
  - [ ] Test covers: page parameter handling
  - [ ] `./venv/Scripts/pytest.exe test_scraper.py -v -k test_url_builder` → FAIL (function not implemented)

  **GREEN:**
  - [ ] Function implemented: `build_search_url(dong_code, property_type, trade_type, min_price, max_price, page=1)`
  - [ ] Returns correct URL format
  - [ ] params[0] → 동 이름 (정왕동), params[1] → 매물 유형 (아파트→APT), params[2] → 거래 유형 (매매→A1), params[3] → 최소 가격, params[4] → 최대 가격
  - [ ] `./venv/Scripts/pytest.exe test_scraper.py -v -k test_url_builder` → PASS

  **Manual Execution Verification**:
  - [ ] Command: `./venv/Scripts/python.exe -c "from naver_real_estate_scraper import build_search_url; print(build_search_url('4117711300', 'APT', 'A1', 10000, 50000, 1))"`
  - [ ] Expected: URL containing all correct parameters

  **Commit**: NO (groups with task 3)

---

- [ ] 3. Implement Driver Initialization (RED → GREEN)

  **What to do**:
  - Selenium WebDriver 초기화 함수 구현
  - Chrome options 설정 (헤드리스 모드 비활성화)
  - window size 설정
  - driver 반환

  **Must NOT do**:
  - 자동화 방지 감지 우회 (정상적인 user-agent 사용)

  **Parallelizable**: NO (depends on 1)

  **References**:

  **Pattern References**:
  - GitHub examples: `ParisNeo/lollms-webui:internet.py:prepare_chrome_driver()` - Chrome options 패턴
  - GitHub examples: `seleniumbase/SeleniumBase:fundamentals.py` - browser launch pattern

  **API/Type References**:
  - [Selenium Options](https://selenium.dev/selenium/docs/api/py/webdriver_chrome/selenium.webdriver.chrome.options.Options.html) - ChromeOptions 사용법
  - [WebDriver](https://selenium.dev/selenium/docs/api/py/webdriver_remote/selenium.webdriver.remote.webdriver.html) - WebDriver 인터페이스

  **Test References**:
  - `test_scraper.py:test_driver_init` - 드라이버 초기화 테스트

  **Documentation References**:
  - [Selenium Quick Start](https://selenium.dev/selenium/docs/api/py/getting_started.html) - 기본 설정

  **External References**:
  - Example repo: `https://github.com/ParisNeo/lollms-webui` - Chrome driver setup

  **Acceptance Criteria**:

  **RED:**
  - [ ] Test written: `test_driver_init()` in `test_scraper.py`
  - [ ] Test covers: driver instance creation
  - [ ] Test covers: headless mode disabled
  - [ ] `./venv/Scripts/pytest.exe test_scraper.py -v -k test_driver_init` → FAIL (function not implemented)

  **GREEN:**
  - [ ] Function implemented: `init_driver()`
  - [ ] Returns webdriver.Chrome instance
  - [ ] Headless mode: NOT enabled (browser visible)
  - [ ] Window size: 1920x1080 (or reasonable size)
  - [ ] `./venv/Scripts/pytest.exe test_scraper.py -v -k test_driver_init` → PASS

  **Manual Execution Verification**:
  - [ ] Command: `./venv/Scripts/python.exe -c "from naver_real_estate_scraper import init_driver; driver = init_driver(); print(type(driver)); driver.quit()"`
  - [ ] Expected: `<class 'selenium.webdriver.chrome.webdriver.WebDriver'>`

  **Commit**: NO (groups with task 4)

---

- [ ] 4. Implement Article List Fetching (RED → GREEN)

  **What to do**:
  - Selenium으로 URL 접근
  - WebDriverWait로 매물 목록 로딩 대기
  - HTML 파싱 (BeautifulSoup)
  - 매물 아이템 리스트 추출
  - 페이지네이션 처리 (첫 페이지만 또는 지정된 페이지)

  **Must NOT do**:
  - time.sleep() 사용 (WebDriverWait 사용)
  - 파일에 저장 (메모리에만 유지)

  **Parallelizable**: NO (depends on 1, 2, 3)

  **References**:

  **Pattern References**:
  - GitHub: `parkbsn1/landCrawling:landCrawling_ad.py` - 매물 리스트 추출 패턴
  - GitHub: `DevKCS/NaverLand:index.js` - API 호출 및 파싱 패턴

  **API/Type References**:
  - [WebDriver.get()](https://selenium.dev/selenium/docs/api/py/webdriver_remote/selenium.webdriver.remote.webdriver.html#selenium.webdriver.remote.webdriver.WebDriver.get) - URL 접근
  - [WebDriverWait](https://selenium.dev/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.ui.WebDriverWait.html) - 대기 처리
  - [Expected Conditions](https://selenium.dev/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.expected_conditions.html) - EC 사용법
  - [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - HTML 파싱

  **Test References**:
  - `test_scraper.py:test_fetch_articles` - 매물 목록 가져오기 테스트

  **Documentation References**:
  - [Explicit Waits Guide](https://www.browserstack.com/guide/selenium-wait-for-page-to-load) - WebDriverWait 사용법
  - [BeautifulSoup Selectors](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#searching-the-tree) - CSS selector 사용

  **External References**:
  - Naver API example: `https://github.com/DevKCS/NaverLand/blob/main/index.js` - 매물 API 구조

  **Acceptance Criteria**:

  **RED:**
  - [ ] Test written: `test_fetch_articles()` in `test_scraper.py`
  - [ ] Test covers: fetching article list from URL
  - [ ] Test covers: parsing HTML with BeautifulSoup
  - [ ] `./venv/Scripts/pytest.exe test_scraper.py -v -k test_fetch_articles` → FAIL (function not implemented)

  **GREEN:**
  - [ ] Function implemented: `fetch_articles(driver, url)`
  - [ ] Uses driver.get() to access URL
  - [ ] Uses WebDriverWait to wait for elements
  - [ ] Uses BeautifulSoup to parse HTML
  - [ ] Returns list of article elements
  - [ ] `./venv/Scripts/pytest.exe test_scraper.py -v -k test_fetch_articles` → PASS

  **Manual Execution Verification**:
  - [ ] Command: `./venv/Scripts/python.exe -c "from naver_real_estate_scraper import fetch_articles, init_driver, build_search_url; driver = init_driver(); articles = fetch_articles(driver, build_search_url('4117711300', 'APT', 'A1', 10000, 50000, 1)); print(len(articles)); driver.quit()"`
  - [ ] Expected: Number of articles (0 or more) displayed

  **Commit**: YES
  - Message: `feat: implement article list fetching with Selenium`
  - Files: `naver_real_estate_scraper.py`, `test_scraper.py`
  - Pre-commit: `./venv/Scripts/pytest.exe test_scraper.py`

---

- [ ] 5. Code Refactoring - Extract Article Details (REFACTOR)

  **What to do**:
  - 코드 구조 개선
  - 각 매물에서 상세 정보 추출 함수 별도 분리
  - 함수명 명확화
  - 주석 추가

  **Must NOT do**:
  - 기능 변경 (구조만 개선)

  **Parallelizable**: NO (depends on 4)

  **References**:

  **Pattern References**:
  - GitHub: `parkbsn1/landCrawling` - 데이터 추출 함수 패턴

  **API/Type References**: None (refactoring only)

  **Test References**:
  - `test_scraper.py:test_extract_article_details` - 상세 정보 추출 테스트

  **Documentation References**:
  - [Clean Code](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882) - 리팩토링 원칙

  **External References**: None (refactoring best practices)

  **Acceptance Criteria**:

  **REFACTOR:**
  - [ ] Function extracted: `extract_article_details(article_element)`
  - [ ] Extracts: price (가격), area (면적), floor (층), address (주소), property_type (매물유형), trade_type (거래유형), broker_info (중개업체 연락처)
  - [ ] All functions have clear docstrings
  - [ ] Code organized into logical sections
  - [ ] `./venv/Scripts/pytest.exe test_scraper.py -v` → PASS (all tests)

  **Manual Execution Verification**:
  - [ ] Command: `./venv/Scripts/python.exe naver_real_estate_scraper.py`
  - [ ] Expected: Scraper runs successfully, outputs article details

  **Commit**: NO (groups with task 6)

---

- [ ] 6. Implement Article Detail Extraction (RED → GREEN)

  **What to do**:
  - 각 매물 요소에서 상세 정보 추출
  - 가격, 면적(공급/전용), 층, 주소, 매물유형, 거래유형, 중개업체 연락처
  - 딕셔너리 형태로 반환

  **Must NOT do**:
  - 파일 저장
  - 불필요한 데이터 추출 (요구사항에 있는 필드만)

  **Parallelizable**: NO (depends on 5)

  **References**:

  **Pattern References**:
  - GitHub: `DevKCS/NaverLand:index.js` - 매물 필드 추출 패턴
  - GitHub: `0115seed-sketch/naver-real-estate-scraper:content_script.js` - 상세 정보 필드

  **API/Type References**:
  - [BeautifulSoup.select()](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find) - CSS selector 사용
  - [Element.get_text()](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#get-text) - 텍스트 추출

  **Test References**:
  - `test_scraper.py:test_extract_article_details` - 상세 정보 추출 테스트

  **Documentation References**:
  - [BeautifulSoup Data Extraction](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#searching-the-tree) - 데이터 추출 방법

  **External References**:
  - Example: `https://github.com/0115seed-sketch/naver-real-estate-scraper/blob/main/content_script.js` - 필드 매핑 참고

  **Acceptance Criteria**:

  **RED:**
  - [ ] Test written: `test_extract_article_details()` in `test_scraper.py`
  - [ ] Test covers: extracting all required fields (price, area, floor, address, property_type, trade_type, broker_info)
  - [ ] `./venv/Scripts/pytest.exe test_scraper.py -v -k test_extract_article_details` → FAIL (function not implemented)

  **GREEN:**
  - [ ] Function implemented: `extract_article_details(article_element)`
  - [ ] Returns dict with keys: 'price', 'area', 'floor', 'address', 'property_type', 'trade_type', 'broker_info'
  - [ ] Price: 매물 가격 (만원 또는 원 단위)
  - [ ] Area: 공급면적/전용면적 (평 또는 m²)
  - [ ] Floor: 층 정보
  - [ ] Address: 주소
  - [ ] Property type: 아파트/오피스텔 등
  - [ ] Trade type: 매매/전세/월세
  - [ ] Broker info: 중개업체 연락처
  - [ ] `./venv/Scripts/pytest.exe test_scraper.py -v -k test_extract_article_details` → PASS

  **Manual Execution Verification**:
  - [ ] Command: `./venv/Scripts/python.exe naver_real_estate_scraper.py`
  - [ ] Expected: All article details printed to console with all required fields

  **Commit**: YES
  - Message: `feat: extract article details (price, area, floor, address, property_type, trade_type, broker_info)`
  - Files: `naver_real_estate_scraper.py`, `test_scraper.py`
  - Pre-commit: `./venv/Scripts/pytest.exe test_scraper.py`

---

- [ ] 7. Implement Console Output (RED → GREEN)

  **What to do**:
  - 메인 함수 구현
  - params 읽어서 URL 빌드
  - driver 초기화
  - 매물 목록 가져오기
  - 각 매물 상세 정보 추출
  - 콘솔에 출력 (형식화)
  - driver 종료

  **Must NOT do**:
  - 파일 저장
  - 불필요한 포맷팅 (가독성 위주)

  **Parallelizable**: NO (depends on 1, 2, 3, 4, 5, 6)

  **References**:

  **Pattern References**:
  - GitHub examples: `parkbsn1/landCrawling` - 메인 함수 패턴

  **API/Type References**:
  - [print()](https://docs.python.org/3/library/functions.html#print) - 콘솔 출력

  **Test References**:
  - `test_scraper.py:test_main` - 메인 함수 테스트

  **Documentation References**:
  - [Python Main Function](https://docs.python.org/3/library/__main__.html) - 모듈 실행

  **External References**:
  - Example: `https://github.com/parkbsn1/landCrawling` - 메인 실행 로직 참고

  **Acceptance Criteria**:

  **RED:**
  - [ ] Test written: `test_main()` in `test_scraper.py`
  - [ ] Test covers: main function execution flow
  - [ ] Test covers: console output (captured with capsys)
  - [ ] `./venv/Scripts/pytest.exe test_scraper.py -v -k test_main` → FAIL (function not implemented)

  **GREEN:**
  - [ ] Main function implemented: `main()` or `__main__` block
  - [ ] Reads params from module
  - [ ] Builds search URL using params
  - [ ] Initializes driver
  - [ ] Fetches article list
  - [ ] Extracts details for each article
  - [ ] Prints to console with formatted output
  - [ ] Closes driver with `driver.quit()`
  - [ ] `./venv/Scripts/pytest.exe test_scraper.py -v -k test_main` → PASS

  **Manual Execution Verification**:
  - [ ] Command: `./venv/Scripts/python.exe naver_real_estate_scraper.py`
  - [ ] Expected output example:
    ```
    매물 1:
      가격: 300,000 만원
      면적: 84.5m² (25.5평)
      층: 8/15
      주소: 경기도 시흥시 정왕동 OOO 아파트
      매물유형: 아파트
      거래유형: 매매
      중개업체: OOO 부동산 (02-1234-5678)
    ```
  - [ ] Browser opens and shows Naver Real Estate page
  - [ ] All article details printed to console

  **Commit**: YES
  - Message: `feat: implement main function with console output`
  - Files: `naver_real_estate_scraper.py`, `test_scraper.py`
  - Pre-commit: `./venv/Scripts/pytest.exe test_scraper.py`

---

## Commit Strategy

| After Task | Message | Files | Verification |
|------------|---------|-------|--------------|
| 0 | `chore: setup test infrastructure (pytest, selenium, beautifulsoup4)` | test_scraper.py, requirements.txt | pytest test_scraper.py |
| 1 | `feat: create scraper module with params and constants` | naver_real_estate_scraper.py | pytest test_scraper.py |
| 2 | `feat: implement URL builder function` | naver_real_estate_scraper.py | pytest test_scraper.py |
| 3 | `feat: implement Selenium driver initialization` | naver_real_estate_scraper.py | pytest test_scraper.py |
| 4 | `feat: implement article list fetching with Selenium` | naver_real_estate_scraper.py, test_scraper.py | pytest test_scraper.py |
| 5 | `refactor: extract article detail extraction function` | naver_real_estate_scraper.py | pytest test_scraper.py |
| 6 | `feat: implement article detail extraction` | naver_real_estate_scraper.py, test_scraper.py | pytest test_scraper.py |
| 7 | `feat: implement main function with console output` | naver_real_estate_scraper.py, test_scraper.py | pytest test_scraper.py |

---

## Success Criteria

### Verification Commands
```bash
# Install dependencies
./venv/Scripts/pip.exe install -U pytest pytest-selenium selenium beautifulsoup4

# Run tests
./venv/Scripts/pytest.exe test_scraper.py -v

# Run scraper
./venv/Scripts/python.exe naver_real_estate_scraper.py
```

### Final Checklist
- [ ] params 리스트 상단에 정의
- [ ] 정왕동 코드(4117711300) 하드코딩
- [ ] 정왕동 아파트 매매 매물(1억~5억) 검색
- [ ] 모든 매물에서 상세 정보 추출 (가격, 면적, 층, 주소, 매물유형, 거래유형, 중개업체 연락처)
- [ ] 콘솔에 모든 매물 상세 정보 출력
- [ ] 브라우저 보이는 상태로 실행 (헤드리스 모드 X)
- [ ] 모든 pytest 테스트 통과
- [ ] 파일 저장 X (콘솔 출력만)
