# 정적 분석 샘플: Open Redirect (CWE-601)

class SessionsController
  def login_redirect(params, response)
    # next 파라미터를 검증 없이 Location으로 반환
    response["Location"] = params[:next]
    response.status = 302
  end

  def logout(params, response)
    target = params[:return_to] || "/"
    response["Location"] = target
    response.status = 302
  end
end
