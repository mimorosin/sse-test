// 정적 분석 샘플: XSS (CWE-79)
const express = require("express");
const app = express();

app.get("/hello", (req, res) => {
  // 사용자 입력을 그대로 HTML에 삽입 -> Reflected XSS
  res.send("<h1>Hello " + req.query.name + "</h1>");
});

app.get("/profile", (req, res) => {
  const html = `<div>bio: ${req.query.bio}</div>`;
  res.type("html").send(html);
});

function renderComment(comment) {
  // DOM XSS (클라이언트 스니펫 가정)
  document.getElementById("c").innerHTML = comment;
}

module.exports = { app, renderComment };
