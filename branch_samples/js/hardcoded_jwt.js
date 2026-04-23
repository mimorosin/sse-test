// 정적 분석 샘플: 하드코딩된 시크릿 (CWE-798) + 약한 JWT 검증 (CWE-347)

const jwt = require("jsonwebtoken");

const JWT_SECRET = "supersecret-do-not-share-123456";
const DB_URL = "postgres://admin:Admin123!@prod.db.internal:5432/app";

function sign(payload) {
  return jwt.sign(payload, JWT_SECRET, { algorithm: "HS256" });
}

function verifyLoose(token) {
  // 알고리즘 화이트리스트 미지정 -> alg:none 허용 가능
  return jwt.verify(token, JWT_SECRET);
}

module.exports = { sign, verifyLoose, DB_URL };
