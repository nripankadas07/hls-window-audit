import json,pathlib,subprocess,sys,tempfile
ROOT=pathlib.Path(__file__).resolve().parent
with tempfile.TemporaryDirectory() as tmp:
    for case in json.loads((ROOT/"smoke.json").read_text()):
        args=[str(ROOT/x) if (ROOT/x).is_file() else str(pathlib.Path(tmp)/x) for x in case["args"]]
        r=subprocess.run([sys.executable,str(ROOT/"hls_window_audit.py"),*args],capture_output=True,text=True)
        assert r.returncode==case["exit"],r.stdout+r.stderr
        result=json.loads(r.stdout)
        for k,v in case.get("expect",{}).items():assert result[k]==v,result
        print(json.dumps({"exit":r.returncode,"result":result}))
