# Labrador 사용자 정의 함수(스니펫) — 매칭 테스트 픽스처

해당 TC 실행용 픽스처:

> `review > 정책 > 정책 반영 검증 > 사용자 정의 함수`
> "사용자 정의 함수 등록 후 신규 분석에서 해당 함수가 사용자 정의 이슈로 탐지된다"

## 구성

```
사용자정의-함수/
├── README.md                    # 본 문서
├── vulnerable-function.java     # /group/policy/snippet 모달 "취약 함수" 입력용 코드
├── patched-function.java        # /group/policy/snippet 모달 "패치 함수" 입력용 코드
└── target-project/              # 분석 대상 모의 프로젝트
    └── src/main/java/com/labradorfixture/
        ├── VulnerableUserDao.java  # 취약 함수가 포함된 소스 (매칭 예상)
        └── SafeProductDao.java     # 대조군 (PreparedStatement 사용, 매칭 안 됨)
```

## 등록 시 모달 입력값

| 필드 | 값 |
|------|-----|
| **취약점 ID** | `CUSTOM-VULN-LABFIX-SQLI-001` (자유 입력 가능) |
| **위험도 (UVSS)** | `높음` |
| **언어** | `Java` |
| **취약 함수** | `vulnerable-function.java` 파일 내용 전체 붙여넣기 |
| **패치 함수** | `patched-function.java` 파일 내용 전체 붙여넣기 (선택) |
| **설명** | `SQL Injection in findUserByName (Labrador QA fixture)` |

## 매칭 설계

- **매칭 예상**: `VulnerableUserDao.findUserByName(String)` — 등록한 취약 함수 스니펫과 동일한 문자열 연결 기반 SELECT 패턴
- **매칭 안 됨 (대조군)**: `SafeProductDao.findProductByName(String)` — 구조는 유사하지만 `PreparedStatement + setString` 사용. 패치 함수와 유사해 매칭되지 않아야 정상
- **매칭 안 됨**: `VulnerableUserDao.countUsers()` — 같은 클래스 내 다른 메서드이므로 영향 없음

> Labrador의 스니펫 매칭은 함수 본문의 AST/토큰 구조를 비교한다(파일 단위 해시가 아님).
> 따라서 target 소스의 주변 클래스/import/포맷팅은 자유롭게 유지해도 된다.

## 사용 절차

1. **target-project 등록 / 소스 포함**
   - `target-project/` 를 Labrador 분석 대상 프로젝트로 등록하거나,
   - 기존 target 프로젝트 소스 트리에 `VulnerableUserDao.java`·`SafeProductDao.java` 를 복사한다.
2. **기준 분석 회차 확보**
   - "사용자정의 포함여부" **해제** 상태로 1회 분석하여 baseline (사용자 정의 함수 매칭 0건).
3. **스니펫 등록**
   - `/group/policy/snippet` 진입 → "함수 추가하기" 클릭.
   - 위 표대로 위험도/언어/취약 함수/(선택) 패치 함수/설명 입력 → "추가하기".
   - 정책 목록에 `CUSTOM-VULN-LABFIX-SQLI-001` 행 추가 확인.
4. **재분석**
   - target 프로젝트를 "사용자정의 포함여부" **체크** 상태로 재분석.
5. **검증**
   - 분석요약 > "사용자 정의 이슈" 카드의 **함수** 카운트가 직전 회차 대비 증가.
   - `사용자 정의 이슈 > 사용자정의 함수` 페이지에 `CUSTOM-VULN-LABFIX-SQLI-001` 행 노출, 파일 `VulnerableUserDao.java` / 함수 `findUserByName` / 해당 라인 정보 표시.
   - `SafeProductDao.findProductByName` 은 목록에 나타나지 않아야 함(대조군 기대).

## 주의

- 함수 이름·시그니처보다 **본문의 구조**가 매칭의 핵심이므로, 취약 함수 코드의 SELECT/문자열 연결/Statement 사용 부분을 임의로 리팩터링하지 않는다.
- 실제 오픈소스와 충돌 방지: `lab_fixture_users`, `LABRADOR_FIXTURE_*` 시그니처를 유지한다.
- 반복 실행 시 "함수 삭제 → 재등록" 절차를 반복할 수 있다. 정책 ID는 자유 입력이므로 변경해도 된다.
