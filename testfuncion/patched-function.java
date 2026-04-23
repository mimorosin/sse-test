public ResultSet findUserByName(String name) throws SQLException {
    String query = "SELECT id, name, email, role FROM lab_fixture_users WHERE name = ?";
    PreparedStatement stmt = this.connection.prepareStatement(query);
    stmt.setString(1, name);
    ResultSet rs = stmt.executeQuery();
    return rs;
}
