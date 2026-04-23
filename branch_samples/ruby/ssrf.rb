# 정적 분석 샘플: SSRF (CWE-918)

require "net/http"
require "uri"

def fetch_preview(url)
  # 사용자 입력 URL을 그대로 요청 -> 내부망(169.254.169.254 등) 접근 가능
  uri = URI.parse(url)
  Net::HTTP.get_response(uri).body
end

def proxy(params)
  uri = URI(params[:target])
  req = Net::HTTP::Get.new(uri)
  Net::HTTP.start(uri.host, uri.port) { |http| http.request(req).body }
end
