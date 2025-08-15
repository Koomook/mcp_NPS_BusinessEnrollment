# MCP NPS Business Enrollment Server

국민연금 가입 사업장 내역 API를 MCP(Model Context Protocol) 서버로 제공하는 Python 패키지입니다.

## 개요

이 프로젝트는 공공데이터포털에서 제공하는 [국민연금공단의 사업장 정보조회 서비스](https://www.data.go.kr/data/3046071/openapi.do)를 MCP 서버로 구현한 것입니다. Claude Desktop 및 기타 MCP 호환 클라이언트에서 국민연금 가입 사업장 정보를 쉽게 조회할 수 있습니다.

## MCP Tools

1. **search_business** 
  - 사업장 정보 조회
  - 지역별, 사업장명, 사업자등록번호로 검색
  - 페이지네이션 지원

2. **get_business_detail** 
  - 사업장 상세정보 조회
  - 업종코드, 가입자수, 당월고지금액 등 상세정보

3. **get_period_status** 
  - 기간별 현황 정보 조회
  - 월별 취득자/상실자 현황

## MCP 클라이언트에 빠른 설치

### Claude Desktop

**가장 간단한 방법 - PyPI 패키지 사용:**

1. Claude Desktop 설정 파일 열기:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. 다음 설정 추가:
```json
{
  "mcpServers": {
    "nps-business": {
      "command": "uvx",
      "args": ["mcp-nps-business-enrollment"],
      "env": {
        "ENCODING_API_KEY": "your_encoded_api_key",
        "DECODING_API_KEY": "your_decoded_api_key"
      }
    }
  }
}
```

3. Claude Desktop 재시작

### Claude Code

```bash
claude mcp add nps-business \
  --env ENCODING_API_KEY="your_encoded_api_key" \
  --env DECODING_API_KEY="your_decoded_api_key" \
  -- uvx mcp-nps-business-enrollment
```

## 개발자용 설치

### PyPI에서 설치

```bash
# pip 사용
pip install mcp-nps-business-enrollment

# 또는 uv 사용 (권장)
uv pip install mcp-nps-business-enrollment
```

### 개발 환경 설정

```bash
# 프로젝트 클론
git clone https://github.com/yourusername/mcp-nps-business-enrollment.git
cd mcp-nps-business-enrollment

# uv를 사용한 개발 환경 설정
uv sync

# 개발 모드로 설치
uv pip install -e .

# MCP 서버로 테스트
uv run mcp-nps-business-enrollment
```

## 환경 설정

### 1. API 키 발급

[공공데이터포털](https://www.data.go.kr)에서 "국민연금 가입 사업장 내역" API 활용 신청 후 인증키를 발급받습니다.

### 2. 환경변수 설정 (개발용)

개발 환경에서 테스트할 때는 `.env` 파일을 생성하고 다음 내용을 입력합니다:

```env
# URL 인코딩된 API 키 (브라우저에서 사용)
ENCODING_API_KEY="your_url_encoded_api_key_here"

# 디코딩된 API 키 (일반 사용)
DECODING_API_KEY="your_decoded_api_key_here"
```

**참고:** API endpoint는 자동으로 설정되므로 별도 설정이 필요 없습니다.



## 사용 예시

### Claude Desktop에서 사용

```
사업장명으로 검색:
"삼성전자"라는 이름이 포함된 사업장을 검색해줘

지역별 검색:
서울특별시 강남구에 있는 사업장들을 찾아줘

상세정보 조회:
식별번호 12345인 사업장의 상세정보를 보여줘

기간별 현황:
식별번호 12345 사업장의 2025년 1월 취득/상실 현황을 알려줘
```

### Python에서 직접 사용

```python
import asyncio
from mcp_nps_business_enrollment.api_client import NPSAPIClient

async def main():
    async with NPSAPIClient() as client:
        # 사업장 검색
        result = await client.search_business(
            wkpl_nm="삼성전자",
            num_of_rows=5
        )
        print(f"Found {result['total_count']} businesses")
        
        # 상세정보 조회
        if result['items']:
            seq = result['items'][0]['seq']
            detail = await client.get_business_detail(seq=seq)
            print(f"Detail: {detail}")

asyncio.run(main())
```

## 테스트

```bash
# 테스트 실행
uv run python tests/test_api.py

# pytest 사용
uv run pytest tests/
```

## API 제한사항

- 공공데이터포털 API 일일 호출 제한이 있을 수 있습니다
- 3인 이상 법인사업장 정보만 제공됩니다
- 매월 15일 이후 데이터가 갱신됩니다
- 사업자등록번호는 앞 6자리만 제공 (뒤 4자리는 마스킹)

## 알려진 한계점 및 이슈

### 1. 시계열 데이터 조회 불가
- **문제**: 한 회사의 여러 달 임직원 변동 추이를 한 번에 조회할 수 없음
- **원인**: API에서 `seq`는 사업장 고유번호가 아닌 월별 데이터 식별번호
  - 동일 회사도 매월 다른 seq를 가짐 (예: 스페이스와이 202506월 seq=6500466, 202505월 seq=5919804)
- **현재 해결방법**: 각 월별로 개별 검색 후 seq를 찾아 조회해야 함

### 2. 대기업 본사 조회 어려움
- **문제**: 삼성전자 같은 대기업 본사가 검색되지 않음 (협력업체만 1,600개+ 검색됨)
- **가능한 원인**:
  - 대기업은 지역별/사업부별로 별도 사업장 등록
  - API에 등록된 정식 명칭이 다를 수 있음
  - 일부 대기업 데이터는 제공하지 않을 가능성

### 3. 사업자등록번호 검색 한계
- **문제**: 사업자등록번호만으로는 특정 회사를 찾을 수 없음
- **원인**: API는 앞 6자리만 제공하며, 동일한 앞 6자리를 가진 회사가 수백 개 존재
- **예시**: 436860으로 검색 시 725개 회사 검색됨
- **해결방법**: 회사명 + 사업자등록번호 조합으로 검색

### 4. 데이터 제공 범위
- 최근 1년치 데이터만 제공 (2018.7.2부터 적용)
- 현재 데이터는 특정 월(예: 202506)까지만 제공되며, 이후 월은 조회 불가

### 5. API 응답 제한
- **한 번에 조회 가능한 최대 개수**: 100개
- **테스트 결과**: 100개까지는 정상, 150개 이상 요청 시 CLIENT_ERROR 발생
- **개선사항**: 검색 결과를 더 많이 보기 위해 `num_of_rows` 기본값을 10에서 100으로 변경
  - 이전: 회사명 검색 시 10개만 표시 → 여러 회사 중 원하는 회사 찾기 어려움
  - 현재: 100개 표시 → 더 많은 검색 결과를 한 번에 확인 가능
- **추가 데이터 필요 시**: 페이지네이션 활용 (pageNo 파라미터 사용)

## 향후 개선 계획 (TODO)

### 데이터베이스 기반 MCP 서버 구축
- [ ] [공공데이터포털 CSV 파일](https://www.data.go.kr/data/15083277/fileData.do)을 활용한 완전한 데이터베이스 구축
  - 월별 CSV 파일 전체 다운로드 및 파싱
  - SQLite/PostgreSQL 등 로컬 DB에 데이터 저장
  - 사업장별 고유 ID 생성으로 시계열 추적 가능
  - API 제한 없는 빠른 조회 성능
  - 과거 전체 기간 데이터 분석 가능

## 기여하기

프로젝트에 기여하고 싶으시다면 Pull Request를 보내주세요!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 라이센스

MIT License - 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 문의

문제가 있거나 제안사항이 있으시면 [Issues](https://github.com/yourusername/mcp-nps-business-enrollment/issues)에 등록해주세요.

## 참고자료

- [국민연금공단 OpenAPI 활용가이드](https://www.data.go.kr/data/3046071/openapi.do)
- [MCP (Model Context Protocol)](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)