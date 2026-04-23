// 정적 분석 샘플: Unsafe Deserialization (CWE-502)
package sample;

import java.io.ByteArrayInputStream;
import java.io.ObjectInputStream;
import java.util.Base64;

public class UnsafeDeserialize {
    public static Object loadFromBase64(String b64) throws Exception {
        byte[] raw = Base64.getDecoder().decode(b64);
        try (ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(raw))) {
            return ois.readObject();
        }
    }

    public static Object loadFromBytes(byte[] raw) throws Exception {
        ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(raw));
        return ois.readObject();
    }
}
