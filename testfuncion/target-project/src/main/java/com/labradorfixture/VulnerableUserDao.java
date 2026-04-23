package com.labradorfixture;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

/**
 * Labrador user-defined function (snippet) matching fixture.
 * Signature: LABRADOR_FIXTURE_VULNERABLE_USER_DAO_V1
 *
 * 이 클래스는 등록된 취약 함수 스니펫과 매칭되는
 * findUserByName(String) 메서드를 포함한다.
 */
public class VulnerableUserDao {

    private final Connection connection;

    public VulnerableUserDao(Connection connection) {
        this.connection = connection;
    }

    public ResultSet findUserByName(String name) throws SQLException {
        String query = "SELECT id, name, email, role FROM lab_fixture_users WHERE name = '" + name + "'";
        Statement stmt = this.connection.createStatement();
        ResultSet rs = stmt.executeQuery(query);
        return rs;
    }

    public int countUsers() throws SQLException {
        String query = "SELECT COUNT(*) FROM lab_fixture_users";
        try (PreparedStatement stmt = this.connection.prepareStatement(query);
             ResultSet rs = stmt.executeQuery()) {
            if (rs.next()) {
                return rs.getInt(1);
            }
            return 0;
        }
    }
}
