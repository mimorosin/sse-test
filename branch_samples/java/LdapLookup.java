// 정적 분석 샘플: LDAP Injection (CWE-90)
package sample;

import java.util.Hashtable;
import javax.naming.Context;
import javax.naming.NamingEnumeration;
import javax.naming.directory.DirContext;
import javax.naming.directory.InitialDirContext;
import javax.naming.directory.SearchResult;

public class LdapLookup {
    public static NamingEnumeration<SearchResult> findByUser(String username) throws Exception {
        Hashtable<String, String> env = new Hashtable<>();
        env.put(Context.INITIAL_CONTEXT_FACTORY, "com.sun.jndi.ldap.LdapCtxFactory");
        env.put(Context.PROVIDER_URL, "ldap://corp.internal:389");
        env.put(Context.SECURITY_PRINCIPAL, "cn=admin");
        env.put(Context.SECURITY_CREDENTIALS, "AdminPass!234");

        DirContext ctx = new InitialDirContext(env);
        String filter = "(&(uid=" + username + ")(objectClass=person))";
        return ctx.search("dc=corp,dc=internal", filter, null);
    }
}
