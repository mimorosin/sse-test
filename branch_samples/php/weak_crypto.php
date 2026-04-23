<?php
// 정적 분석 샘플: Weak Crypto (CWE-327) - DES + ECB + 하드코딩 키

function encrypt_token($plaintext) {
    $key = "12345678"; // 하드코딩된 약한 키
    return openssl_encrypt($plaintext, "DES-ECB", $key, OPENSSL_RAW_DATA);
}

function decrypt_token($cipher) {
    $key = "12345678";
    return openssl_decrypt($cipher, "DES-ECB", $key, OPENSSL_RAW_DATA);
}

function hash_password($password) {
    return md5($password); // CWE-327
}

function sign($data) {
    $secret = "secret";
    return sha1($secret . $data); // length-extension 취약 구성
}
