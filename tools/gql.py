"""Tiny wrapper: run Admin GraphQL through `shopify store execute` and return the data dict."""
import json, os, subprocess, tempfile

STORE = "t6ngcu-uh.myshopify.com"


def gql(query, variables=None, mutation=None):
    with tempfile.TemporaryDirectory() as d:
        qf = os.path.join(d, "q.graphql"); open(qf, "w", encoding="utf-8").write(query)
        cmd = ["shopify", "store", "execute", "-s", STORE, "-j", "--query-file", qf]
        if variables is not None:
            vf = os.path.join(d, "v.json"); json.dump(variables, open(vf, "w", encoding="utf-8"))
            cmd += ["--variable-file", vf]
        if mutation if mutation is not None else query.lstrip().startswith("mutation"):
            cmd.append("--allow-mutations")
        of = os.path.join(d, "out.json"); cmd += ["--output-file", of]
        out = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", shell=(os.name == "nt"))
        if os.path.exists(of) and os.path.getsize(of):
            obj = json.load(open(of, encoding="utf-8"))
            data = obj.get("data", obj)
            for v in (data or {}).values():
                if isinstance(v, dict) and v.get("userErrors"):
                    raise RuntimeError(json.dumps(v["userErrors"]))
            return data
    lines = [l for l in (out.stdout + "\n" + out.stderr).splitlines() if l.strip().startswith("{")]
    for l in reversed(lines):
        obj = json.loads(l)
        if obj.get("type") == "progress":
            continue
        if "error" in obj:
            raise RuntimeError(obj["error"].get("tryMessage") or obj["error"])
        data = obj.get("data", obj)
        # surface userErrors
        for v in (data or {}).values():
            if isinstance(v, dict) and v.get("userErrors"):
                raise RuntimeError(json.dumps(v["userErrors"]))
        return data
    raise RuntimeError(out.stdout[-2000:] + out.stderr[-2000:])


if __name__ == "__main__":
    import sys
    print(json.dumps(gql(sys.argv[1]), indent=1))
