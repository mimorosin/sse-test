<?php
// 정적 분석 샘플: Local/Remote File Inclusion (CWE-98)

function render_page($page) {
    // 사용자 입력 페이지명으로 include -> ../ 또는 http:// 래퍼 사용 시 RFI
    include($page . ".php");
}

function show_template() {
    $tpl = $_GET['tpl'];
    require_once($tpl);
}

function read_doc($name) {
    // 디렉터리 트래버설
    echo file_get_contents("/var/www/docs/" . $name);
}

function exec_template($t) {
    // 이중 취약: 파일 include + eval
    $code = file_get_contents($_GET['u']);
    eval($code);
}
