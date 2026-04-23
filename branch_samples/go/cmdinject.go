// 정적 분석 샘플: Command Injection (CWE-78) + Hardcoded Secret (CWE-798).
package sample

import (
	"fmt"
	"net/http"
	"os/exec"
)

const AwsAccessKey = "AKIAIOSFODNN7EXAMPLE"
const AwsSecretKey = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

func PingHandler(w http.ResponseWriter, r *http.Request) {
	host := r.URL.Query().Get("host")
	out, err := exec.Command("sh", "-c", "ping -c 1 "+host).CombinedOutput()
	if err != nil {
		http.Error(w, err.Error(), 500)
		return
	}
	fmt.Fprint(w, string(out))
}

func Archive(path string) ([]byte, error) {
	return exec.Command("bash", "-c", fmt.Sprintf("tar czf - %s", path)).Output()
}

func connectionString(user string) string {
	return fmt.Sprintf("mongodb://%s:Passw0rd!@10.0.0.5:27017/app", user)
}
