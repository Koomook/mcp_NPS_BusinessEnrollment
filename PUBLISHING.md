# PyPI 배포 가이드

## 사전 준비

### 1. PyPI 계정 생성
- [PyPI](https://pypi.org/account/register/) 계정 생성
- [Test PyPI](https://test.pypi.org/account/register/) 계정 생성 (테스트용)

### 2. API 토큰 생성
1. PyPI 로그인 후 Account Settings
2. "API tokens" 섹션에서 "Add API token" 클릭
3. 토큰 이름 입력 및 scope 설정
4. 생성된 토큰 안전하게 보관

### 3. 필요 패키지 설치
```bash
pip install build twine
```

## 패키지 빌드

### 1. 버전 확인 및 업데이트
`pyproject.toml`에서 버전 확인:
```toml
version = "0.1.0"  # 필요시 업데이트
```

### 2. 빌드 실행
```bash
# 이전 빌드 파일 제거
rm -rf dist/ build/ *.egg-info

# 패키지 빌드
python -m build
```

빌드 후 `dist/` 폴더에 다음 파일들이 생성됩니다:
- `mcp_nps_business_enrollment-0.1.0.tar.gz` (소스 배포)
- `mcp_nps_business_enrollment-0.1.0-py3-none-any.whl` (휠 파일)

## Test PyPI에 업로드 (권장)

### 1. Test PyPI에 업로드
```bash
python -m twine upload --repository testpypi dist/*
```

### 2. 테스트 설치
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ mcp-nps-business-enrollment
```

## 실제 PyPI에 업로드

### 1. PyPI에 업로드
```bash
python -m twine upload dist/*
```

또는 API 토큰 사용:
```bash
python -m twine upload dist/* -u __token__ -p pypi-YOUR_API_TOKEN_HERE
```

### 2. 설치 확인
```bash
pip install mcp-nps-business-enrollment
```

## 자동화된 배포 (GitHub Actions)

`.github/workflows/publish.yml` 파일 생성:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: python -m build
    
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

GitHub Secrets에 `PYPI_API_TOKEN` 추가 필요

## 버전 관리

### Semantic Versioning 사용
- MAJOR.MINOR.PATCH (예: 1.0.0)
- MAJOR: 호환되지 않는 API 변경
- MINOR: 하위 호환성 있는 기능 추가
- PATCH: 하위 호환성 있는 버그 수정

### 버전 업데이트 시
1. `pyproject.toml`의 `version` 업데이트
2. `src/mcp_nps_business_enrollment/__init__.py`의 `__version__` 업데이트
3. Git 태그 생성:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

## 체크리스트

배포 전 확인사항:
- [ ] 모든 테스트 통과
- [ ] README.md 업데이트
- [ ] 버전 번호 업데이트
- [ ] CHANGELOG 업데이트 (있는 경우)
- [ ] 라이센스 파일 확인
- [ ] 의존성 버전 확인
- [ ] Python 버전 호환성 확인

## 문제 해결

### 인증 오류
- API 토큰이 올바른지 확인
- 토큰 권한이 충분한지 확인

### 패키지 이름 충돌
- PyPI에서 패키지 이름 검색하여 중복 확인
- 필요시 패키지 이름 변경

### 빌드 오류
- `pyproject.toml` 문법 확인
- 필수 파일들이 모두 있는지 확인
- Python 버전 호환성 확인