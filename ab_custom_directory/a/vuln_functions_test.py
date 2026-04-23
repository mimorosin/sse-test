"""
테스트 전용: 함수 단위 취약점 예시 모음.

각 함수는 흔히 발생하는 Python 수준의 취약점을 재현합니다.
실제 서비스 코드가 아닌 정적 분석/보안 교육 및 SSE 파이프라인 테스트용입니다.
"""

from __future__ import annotations

import hashlib
import os
import pickle
import random
import sqlite3
import subprocess
import xml.etree.ElementTree as ET

# -----------------------------------------------------------------------------
# CWE-78: OS Command Injection
# -----------------------------------------------------------------------------
def ping_host_vulnerable(host: str) -> int:
    """
    사용자 입력 host를 쉘에 그대로 전달. `127.0.0.1; rm -rf /` 같은 주입 가능.
    """
    return os.system("ping -c 1 " + host)


def run_shell_vulnerable(user_cmd: str) -> bytes:
    """shell=True + 사용자 입력 연결 -> 임의 명령 실행."""
    return subprocess.check_output("echo result: " + user_cmd, shell=True)


# -----------------------------------------------------------------------------
# CWE-89: SQL Injection
# -----------------------------------------------------------------------------
def find_user_vulnerable(conn: sqlite3.Connection, username: str):
    """f-string으로 쿼리 조립 -> `' OR 1=1 --` 등으로 우회 가능."""
    cur = conn.cursor()
    cur.execute(f"SELECT id, name FROM users WHERE name = '{username}'")
    return cur.fetchall()


# -----------------------------------------------------------------------------
# CWE-94: Code Injection via eval/exec
# -----------------------------------------------------------------------------
def calc_expression_vulnerable(expr: str):
    """eval에 사용자 입력을 그대로 전달 -> 임의 코드 실행."""
    return eval(expr)


def run_user_script_vulnerable(script: str) -> None:
    """exec로 문자열 실행 -> 모듈 import 포함 임의 코드 실행."""
    exec(script)


# -----------------------------------------------------------------------------
# CWE-22: Path Traversal
# -----------------------------------------------------------------------------
def read_user_file_vulnerable(base_dir: str, filename: str) -> bytes:
    """
    filename 검증 없이 결합 -> `../../etc/passwd` 같은 경로 탈출 가능.
    """
    path = os.path.join(base_dir, filename)
    with open(path, "rb") as f:
        return f.read()


# -----------------------------------------------------------------------------
# CWE-502: Unsafe Deserialization
# -----------------------------------------------------------------------------
def load_session_vulnerable(blob: bytes):
    """신뢰할 수 없는 입력을 pickle.loads -> __reduce__ 통한 RCE."""
    return pickle.loads(blob)


# -----------------------------------------------------------------------------
# CWE-611: XML External Entity (XXE)
# -----------------------------------------------------------------------------
def parse_xml_vulnerable(xml_text: str):
    """
    ElementTree 기본 파서는 외부 엔티티 확장을 제한하긴 하지만,
    외부 DTD/엔티티가 허용되는 환경/파서 치환 시 XXE 노출 가능.
    """
    return ET.fromstring(xml_text)


# -----------------------------------------------------------------------------
# CWE-798: Hardcoded Credentials
# -----------------------------------------------------------------------------
def get_admin_token_vulnerable() -> str:
    """하드코딩된 비밀키 -> 저장소 유출 시 그대로 노출."""
    API_TOKEN = "sk-live-HARDCODED-1234567890ABCDEF"  # noqa: S105
    return API_TOKEN


# -----------------------------------------------------------------------------
# CWE-327: Weak Cryptographic Hash
# -----------------------------------------------------------------------------
def hash_password_vulnerable(password: str) -> str:
    """MD5 사용 + salt 없음 -> 레인보우 테이블/충돌 공격."""
    return hashlib.md5(password.encode()).hexdigest()


# -----------------------------------------------------------------------------
# CWE-330: Insecure Randomness
# -----------------------------------------------------------------------------
def generate_reset_token_vulnerable(length: int = 16) -> str:
    """random 모듈은 예측 가능 -> 토큰/세션에 부적합(secrets 사용해야 함)."""
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
    return "".join(random.choice(alphabet) for _ in range(length))


# -----------------------------------------------------------------------------
# CWE-918: Server-Side Request Forgery (SSRF)
# -----------------------------------------------------------------------------
def fetch_url_vulnerable(url: str) -> bytes:
    """
    사용자 제공 URL을 검증 없이 요청 -> 내부망(169.254.169.254 등) 접근 가능.
    urllib는 file:// 스킴도 허용하여 로컬 파일 읽기 위험.
    """
    from urllib.request import urlopen

    with urlopen(url) as resp:  # noqa: S310
        return resp.read()


# -----------------------------------------------------------------------------
# 외부 매칭용 별칭 (C++/다른 언어 심볼 스타일과의 교차참조)
# -----------------------------------------------------------------------------
VulnTest_CommandInjection = ping_host_vulnerable
VulnTest_ShellInjection = run_shell_vulnerable
VulnTest_SQLInjection = find_user_vulnerable
VulnTest_EvalInjection = calc_expression_vulnerable
VulnTest_ExecInjection = run_user_script_vulnerable
VulnTest_PathTraversal = read_user_file_vulnerable
VulnTest_UnsafeDeserialize = load_session_vulnerable
VulnTest_XXE = parse_xml_vulnerable
VulnTest_HardcodedSecret = get_admin_token_vulnerable
VulnTest_WeakHash = hash_password_vulnerable
VulnTest_WeakRandom = generate_reset_token_vulnerable
VulnTest_SSRF = fetch_url_vulnerable


if __name__ == "__main__":
    # 간단 동작 확인 (실제 공격 수행 X, 각 함수가 임포트/호출 가능함만 확인)
    print("weak hash:", hash_password_vulnerable("hello"))
    print("weak token:", generate_reset_token_vulnerable(8))
    print("hardcoded:", get_admin_token_vulnerable())
