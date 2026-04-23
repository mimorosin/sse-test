# 정적 분석 샘플: Timing Attack (CWE-208) + 평문 비교

def valid_token?(given, expected)
  # == 비교는 짧은 쪽에서 조기 반환 -> 타이밍 공격 가능
  given == expected
end

def verify_api_key(input)
  stored = "api_key_1234567890abcdef"
  input == stored
end
