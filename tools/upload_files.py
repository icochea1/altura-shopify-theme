"""Upload images to Shopify Files (staged upload -> fileCreate). Keeps media/uploaded.json {filename: {id, url}}.
Usage: python upload_files.py <file> [<file> ...]
"""
import json, mimetypes, os, sys, time, urllib.request, uuid
from gql import gql

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "..", "media", "uploaded.json")
db = json.load(open(DB)) if os.path.exists(DB) else {}

STAGE = """mutation($input:[StagedUploadInput!]!){ stagedUploadsCreate(input:$input){ stagedTargets{ url resourceUrl parameters{ name value } } userErrors{ field message } } }"""
CREATE = """mutation($files:[FileCreateInput!]!){ fileCreate(files:$files){ files{ id fileStatus } userErrors{ field message } } }"""
STATUS = """query($ids:[ID!]!){ nodes(ids:$ids){ ... on MediaImage { id fileStatus image { url } } } }"""


def multipart(url, params, path):
    b = uuid.uuid4().hex
    body = b""
    for p in params:
        body += f"--{b}\r\nContent-Disposition: form-data; name=\"{p['name']}\"\r\n\r\n{p['value']}\r\n".encode()
    body += f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{os.path.basename(path)}\"\r\nContent-Type: {mimetypes.guess_type(path)[0]}\r\n\r\n".encode()
    body += open(path, "rb").read() + f"\r\n--{b}--\r\n".encode()
    req = urllib.request.Request(url, body, {"Content-Type": f"multipart/form-data; boundary={b}"})
    urllib.request.urlopen(req).read()


def upload(paths):
    paths = [p for p in paths if os.path.basename(p) not in db]
    for i in range(0, len(paths), 10):
        chunk = paths[i:i + 10]
        inp = [{"filename": os.path.basename(p), "mimeType": mimetypes.guess_type(p)[0], "httpMethod": "POST", "resource": "IMAGE",
                "fileSize": str(os.path.getsize(p))} for p in chunk]
        targets = gql(STAGE, {"input": inp})["stagedUploadsCreate"]["stagedTargets"]
        for p, t in zip(chunk, targets):
            multipart(t["url"], t["parameters"], p)
        files = [{"originalSource": t["resourceUrl"], "contentType": "IMAGE", "filename": os.path.basename(p),
                  "alt": os.path.splitext(os.path.basename(p))[0].replace("altura-", "").replace("-", " ")} for p, t in zip(chunk, targets)]
        created = gql(CREATE, {"files": files})["fileCreate"]["files"]
        ids = [c["id"] for c in created]
        for _ in range(40):
            nodes = gql(STATUS, {"ids": ids})["nodes"]
            if all(n and n["fileStatus"] in ("READY", "FAILED") for n in nodes):
                break
            time.sleep(3)
        for p, n in zip(chunk, nodes):
            db[os.path.basename(p)] = {"id": n["id"], "url": (n.get("image") or {}).get("url"), "status": n["fileStatus"]}
            print(os.path.basename(p), n["fileStatus"], flush=True)
        json.dump(db, open(DB, "w"), indent=1)


if __name__ == "__main__":
    upload(sys.argv[1:])
