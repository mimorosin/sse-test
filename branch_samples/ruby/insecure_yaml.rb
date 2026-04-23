# 정적 분석 샘플: Unsafe Deserialization via YAML.load (CWE-502)

require "yaml"

def load_config(text)
  # YAML.load 는 임의 객체 복원 허용 -> RCE
  YAML.load(text)
end

def load_profile(path)
  YAML.load_file(path)
end

def parse_marshal(blob)
  Marshal.load(blob)
end
