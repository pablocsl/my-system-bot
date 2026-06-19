import subprocess
from collections import Counter

def ssh_failures(last_lines=2000):
    try:
        cmd = f"journalctl -u ssh --no-pager -n {last_lines} | grep 'Failed password' || true"

        result = subprocess.check_output(cmd, shell=True, text=True)

        lines = [l for l in result.split("\n") if l.strip()]

        ips = []
        for l in lines:
            if "from" in l:
                try:
                    ips.append(l.split("from")[1].split()[0])
                except:
                    pass

        top = Counter(ips).most_common(5)

        return {
            "total": len(ips),
            "ips": top
        }

    except Exception as e:
        return {"error": str(e)}
