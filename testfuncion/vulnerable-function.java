public ResultSet findUserByName(String name) throws SQLException {
    String query = "SELECT id, name, email, role FROM lab_fixture_users WHERE name = '" + name + "'";
    Statement stmt = this.connection.createStatement();
    ResultSet rs = stmt.executeQuery(query);
    return rs;
}
