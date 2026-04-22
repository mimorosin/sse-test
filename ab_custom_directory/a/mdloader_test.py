"""
테스트 전용: MDLLoader.cpp의 MDLLoaderTest 네임스페이스와 대응하는 취약점/패치 헬퍼.

C 64비트 size_t 곱 오버플로를 (a * b) & MASK 로 모델링합니다.
"""

from __future__ import annotations

# 패치 함수(alloc_array_patched 등) 주석 해제 시: from typing import Optional, Tuple

# 64비트 부호 없는 size_t
_SIZE_MASK = (1 << 64) - 1
# C SIZE_MAX (일반적인 64비트 size_t)
SIZE_MAX = _SIZE_MASK


def _as_size_t(x: int) -> int:
    return int(x) & _SIZE_MASK


def _mul_size_t(count: int, elem_size: int) -> int:
    """C에서 size_t끼리 곱한 뒤 잘리는 결과."""
    return _as_size_t(_as_size_t(count) * _as_size_t(elem_size))


def copy_bytes_vulnerable(
    dst: bytearray,
    dst_capacity: int,
    src: bytes,
    length: int,
) -> None:
    """
    CWE-787 스타일: dst_capacity를 무시하고 length만큼 복사.

    dst는 길이가 dst_capacity와 같다고 가정하는 것이 C API와 동일합니다.
    length가 버퍼 길이를 넘기면 memoryview 대입으로 예외가 날 수 있습니다(UB에 대응).
    """
    _ = dst_capacity
    if dst is None or src is None:
        return
    n = int(length)
    mv = memoryview(dst)
    mv[:n] = src[:n]


# def copy_bytes_patched(
#     dst: bytearray,
#     dst_capacity: int,
#     src: bytes,
#     length: int,
# ) -> Tuple[bool, int]:
#     """
#     len > dst_capacity 이면 실패. 성공 시 복사한 바이트 수 반환.
#     반환: (성공 여부, 복사된 바이트 수)
#     """
#     if dst is None or src is None:
#         return False, 0
#     n = int(length)
#     cap = int(dst_capacity)
#     if n > cap:
#         return False, 0
#     mv = memoryview(dst)
#     mv[:n] = src[:n]
#     return True, n


def alloc_array_vulnerable(count: int, elem_size: int) -> bytearray:
    """
    CWE-190 스타일: count * elem_size 가 size_t에서 오버플로하면 작은 크기로 할당될 수 있음.
    """
    bytes_total = _mul_size_t(count, elem_size)
    return bytearray(bytes_total)


# def alloc_array_patched(
#     count: int,
#     elem_size: int,
# ) -> Tuple[Optional[bytearray], bool]:
#     """
#     오버플로 및 (0, *) / (*, 0) 거부.
#     반환: (버퍼 또는 None, 성공 여부)
#     """
#     c = _as_size_t(count)
#     e = _as_size_t(elem_size)
#     if c == 0 or e == 0:
#         return None, False
#     # 곱하기 전에 검사 (패치 버전은 래핑 전에 실패)
#     if c > SIZE_MAX // e:
#         return None, False
#     bytes_total = c * e
#     return bytearray(bytes_total), True


# C++ 심볼 이름과 대응 (외부 도구/문서 문자열 매칭용 별칭)
MDLLoader_TestCopyBytes_Vulnerable = copy_bytes_vulnerable
# MDLLoader_TestCopyBytes_Patched = copy_bytes_patched
MDLLoader_TestAllocArray_Vulnerable = alloc_array_vulnerable
# MDLLoader_TestAllocArray_Patched = alloc_array_patched


if __name__ == "__main__":
    # 간단 동작 확인
    buf = bytearray(4)
    try:
        copy_bytes_vulnerable(buf, 4, b"ABCDEF", 6)
        print("vulnerable dst after overshoot:", buf)
    except Exception as ex:
        print("vulnerable overshoot (expected error):", type(ex).__name__, ex)

    # buf2 = bytearray(4)
    # ok, n = copy_bytes_patched(buf2, 4, b"ABCDEF", 6)
    # print("patched overshoot:", ok, n, buf2)

    # 오버플로 예: 큰 수 * 큰 수 -> 래핑된 작은 할당
    huge = (1 << 63) + 100
    w = alloc_array_vulnerable(huge, huge)
    print("vulnerable alloc len (wrapped):", len(w))

    # arr, ok2 = alloc_array_patched(huge, huge)
    # print("patched alloc:", ok2, len(arr) if arr else None)
