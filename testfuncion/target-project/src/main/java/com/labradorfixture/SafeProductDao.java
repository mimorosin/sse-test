package com.labradorfixture;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

/**
 * Labrador user-defined function (snippet) NEGATIVE fixture.
 * Signature: LABRADOR_FIXTURE_SAFE_PRODUCT_DAO_V1
 *
 * 구조는 VulnerableUserDao와 비슷하지만 PreparedStatement를 사용하므로
 * 등록된 취약 함수 스니펫과 매칭되지 않아야 한다(대조군).
 */
public class SafeProductDao {

    private final Connection connection;

    public SafeProductDao(Connection connection) {
        this.connection = connection;
    }

    public ResultSet findProductByName(String name) throws SQLException {
        String query = "SELECT id, name, price FROM lab_fixture_products WHERE name = ?";
        PreparedStatement stmt = this.connection.prepareStatement(query);
        stmt.setString(1, name);
        ResultSet rs = stmt.executeQuery();
        return rs;
    }
}
