import subprocess
from glob import glob

BC_files = glob("../datasets_mtx/BC/*")
SSSP_files = glob("../datasets_mtx/SSSP/*")
kcore_files = glob("../datasets_mtx/kcore/*")

for i in range(5):
    for f in BC_files:
        r = subprocess.run(["./bc", "-m", f], bufsize=-1, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"BC ; file: {f} ; r code: {r.returncode} ; out: {r.stdout.decode('utf-8')}")

    for f in SSSP_files:
        r = subprocess.run(["./sssp", "-m", f], bufsize=-1, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"SSSP ; file: {f} ; r code: {r.returncode} ; out: {r.stdout.decode('utf-8')}")

    for f in kcore_files:
        r = subprocess.run(["./kcore", f], bufsize=-1, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"kcore ; file: {f} ; r code: {r.returncode} ; out: {r.stdout.decode('utf-8')}")