import base64
import json
import requests


def fetchFromGithub(repo_url="https://api.github.com/repos/<USER>/<REPO>/contents/<PATH>/<TO>/<FILE>.json", ghtoken="<YOUR PAT OR OAUTH ghtoken>", ref="branch or commit or tag"):
    headers = {
        "Authorization": f"token {ghtoken}",
        "Accept": "application/vnd.github.v4+raw"
    }
    response = requests.get(repo_url, headers=headers, params={'ref': ref},)

    if response and response.status_code == 200:
        binary_content = base64.b64decode(response.json()["content"])
        content = binary_content.decode("utf-8")
        return content
    else:
        raise Exception("Unable to download "+repo_url+": "+response)
