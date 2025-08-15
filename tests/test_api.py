"""Tests for NPS API client."""

import os
import asyncio
import pytest
from dotenv import load_dotenv
from mcp_nps_business_enrollment.api_client import NPSAPIClient

# 환경변수 로드
load_dotenv()


@pytest.mark.asyncio
async def test_search_business():
    """Test business search functionality."""
    async with NPSAPIClient() as client:
        # 삼성전자로 테스트
        result = await client.search_business(
            wkpl_nm="삼성전자",
            num_of_rows=5
        )
        
        assert 'items' in result
        assert 'total_count' in result
        assert 'page_no' in result
        assert 'num_of_rows' in result
        
        print(f"Found {result['total_count']} businesses")
        if result['items']:
            print(f"First business: {result['items'][0]}")


@pytest.mark.asyncio
async def test_search_business_by_region():
    """Test business search by region."""
    async with NPSAPIClient() as client:
        # 서울특별시(11) 강남구(680) 테스트
        result = await client.search_business(
            ldong_addr_mgpl_dg_cd="11",
            ldong_addr_mgpl_sggu_cd="11680",
            num_of_rows=3
        )
        
        assert 'items' in result
        print(f"Found {result['total_count']} businesses in Gangnam")


@pytest.mark.asyncio
async def test_get_business_detail():
    """Test getting business details."""
    async with NPSAPIClient() as client:
        # 먼저 사업장 검색
        search_result = await client.search_business(
            wkpl_nm="삼성전자",
            num_of_rows=1
        )
        
        if search_result['items'] and search_result['items'][0].get('seq'):
            seq = search_result['items'][0]['seq']
            
            # 상세정보 조회
            detail_result = await client.get_business_detail(seq=seq)
            
            assert 'items' in detail_result
            if detail_result['items']:
                detail = detail_result['items'][0]
                print(f"Business detail: {detail}")
                
                # 추가 필드 확인
                assert any(key in detail for key in ['wkpl_nm', 'bzowr_rgst_no'])


@pytest.mark.asyncio
async def test_get_period_status():
    """Test getting period status."""
    async with NPSAPIClient() as client:
        # 먼저 사업장 검색
        search_result = await client.search_business(
            wkpl_nm="삼성전자",
            num_of_rows=1
        )
        
        if search_result['items'] and search_result['items'][0].get('seq'):
            seq = search_result['items'][0]['seq']
            
            # 기간별 현황 조회
            status_result = await client.get_period_status(
                seq=seq,
                data_crt_ym="202501"
            )
            
            assert 'items' in status_result
            if status_result['items']:
                status = status_result['items'][0]
                print(f"Period status: {status}")


def run_tests():
    """Run all tests."""
    asyncio.run(test_search_business())
    asyncio.run(test_search_business_by_region())
    asyncio.run(test_get_business_detail())
    asyncio.run(test_get_period_status())


if __name__ == "__main__":
    # 간단한 테스트 실행
    run_tests()