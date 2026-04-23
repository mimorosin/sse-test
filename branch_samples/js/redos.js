// 정적 분석 샘플: ReDoS (CWE-1333)

const EMAIL_RE = /^([a-zA-Z0-9]+)+@([a-zA-Z0-9]+)+\.[a-z]{2,}$/;

function isEmail(s) {
  return EMAIL_RE.test(s);
}

const NESTED_QUANT = /^(a+)+$/;
function looksLikeA(s) {
  return NESTED_QUANT.test(s);
}

function stripTags(html) {
  // 탐욕적 + 역추적으로 ReDoS
  return html.replace(/<(.|\n)*?>/g, "");
}

module.exports = { isEmail, looksLikeA, stripTags };
