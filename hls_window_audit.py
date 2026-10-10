"""Offline audit of a deliberately bounded HLS media-playlist pair."""
import argparse, decimal, hashlib, json, pathlib

def parse(text):
    if len(text.encode()) > 2*1024*1024: raise ValueError("playlist exceeds 2 MiB")
    lines=text.lstrip("\ufeff").splitlines()
    if not lines or lines[0] != "#EXTM3U": raise ValueError("missing EXTM3U")
    seq=disc=0; target=None; duration=None; segments=[]; seen=set(); ended=False; discontinuity_seen=False
    for number,line in enumerate(lines[1:],2):
        line=line.strip()
        if not line: continue
        if ended: raise ValueError("content after ENDLIST")
        if line.startswith("#EXTINF:"):
            if duration is not None: raise ValueError("duration without URI")
            raw=line.split(":",1)[1].split(",",1)[0]
            duration=decimal.Decimal(raw)
            if not duration.is_finite() or duration<=0: raise ValueError("invalid segment duration")
        elif line=="#EXT-X-DISCONTINUITY":
            if duration is not None: raise ValueError("discontinuity between EXTINF and URI")
            disc+=1; discontinuity_seen=True
        elif line=="#EXT-X-ENDLIST":
            if duration is not None: raise ValueError("duration without URI")
            ended=True
        elif line.startswith("#EXT-X-"):
            key,sep,value=line.partition(":")
            if key not in {"#EXT-X-MEDIA-SEQUENCE","#EXT-X-DISCONTINUITY-SEQUENCE","#EXT-X-TARGETDURATION","#EXT-X-VERSION"} or not sep:
                raise ValueError("unsupported media tag at line "+str(number))
            if key in seen or segments or duration is not None: raise ValueError("duplicate or late header")
            seen.add(key)
            if not value.isascii() or not value.isdigit(): raise ValueError("invalid integer header")
            n=int(value)
            if n>2**63-1: raise ValueError("header exceeds integer bound")
            if key=="#EXT-X-MEDIA-SEQUENCE": seq=n
            elif key=="#EXT-X-DISCONTINUITY-SEQUENCE":
                if discontinuity_seen: raise ValueError("discontinuity sequence after discontinuity tag")
                disc=n
            elif key=="#EXT-X-TARGETDURATION":
                if n==0: raise ValueError("target must be positive")
                target=n
        elif line.startswith("#"):
            if line.startswith("#EXT"): raise ValueError("unsupported EXT tag")
        else:
            if duration is None: raise ValueError("URI without EXTINF")
            if any(c.isspace() for c in line): raise ValueError("URI contains whitespace")
            segments.append({"sequence":seq+len(segments),"discontinuity":disc,"duration":str(duration.normalize()),"uri_sha256":hashlib.sha256(line.encode()).hexdigest()})
            duration=None
            if len(segments)>10000: raise ValueError("more than 10000 segments")
    if duration is not None or not segments or target is None: raise ValueError("incomplete media playlist")
    return {"target":target,"ended":ended,"segments":segments}

def audit(before,after):
    a,b=parse(before),parse(after);findings=[]
    for label,p in [("before",a),("after",b)]:
        for s in p["segments"]:
            rounded=int(decimal.Decimal(s["duration"]).quantize(decimal.Decimal(1),rounding=decimal.ROUND_HALF_UP))
            if rounded>p["target"]: findings.append({"code":"target-duration","snapshot":label,"sequence":s["sequence"]})
    old={s["sequence"]:s for s in a["segments"]};new={s["sequence"]:s for s in b["segments"]}
    overlap=sorted(old.keys()&new.keys())
    for n in overlap:
        for key in ["discontinuity","duration","uri_sha256"]:
            if old[n][key]!=new[n][key]: findings.append({"code":"changed-segment","sequence":n,"field":key})
    if min(new)<min(old): findings.append({"code":"sequence-regression"})
    if min(new)>max(old)+1: findings.append({"code":"unobserved-gap","missing":min(new)-max(old)-1})
    if a["target"]!=b["target"]: findings.append({"code":"target-changed"})
    if a["ended"] and a!=b: findings.append({"code":"ended-playlist-changed"})
    return {"ok":not findings,"overlap_count":len(overlap),"findings":findings,"before":a,"after":b}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("before");p.add_argument("after");args=p.parse_args()
    try:
        r=audit(pathlib.Path(args.before).read_text(encoding="utf-8"),pathlib.Path(args.after).read_text(encoding="utf-8"));print(json.dumps(r));return 0 if r["ok"] else 1
    except (ValueError,OSError,decimal.InvalidOperation) as e: print(json.dumps({"error":str(e)}));return 2
if __name__=="__main__":raise SystemExit(main())
