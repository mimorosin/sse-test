# 정적 분석 샘플: Mass Assignment (CWE-915)

class UsersController
  def update(params, current_user)
    # permit/strong parameters 미사용 -> role, is_admin 등 임의 수정 가능
    current_user.update(params[:user])
  end

  def create(params)
    User.create(params[:user])
  end
end
