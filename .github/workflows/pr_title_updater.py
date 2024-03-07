import sys
import urllib.request
import json

owner = "bejewel-amondz"  # 레포지토리 소유자 이름
repo = "amondz-user-ios"  # 레포지토리 이름

# PR 정보 요청 후, title, base_brach, head_branch 를 돌려줍니다.
# https://docs.github.com/en/rest/pulls/pulls#get-a-pull-request
def get_pr_info(pr_number, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req) as response:
            pr_data = json.loads(response.read().decode())
            title = pr_data['title']
            base_branch = pr_data['base']['ref']
            head_brach = pr_data['head']['ref']
            return title, base_branch, head_brach
    except urllib.error.HTTPError as e:
        print(f"Failed to fetch PR data: {e.code}")
        return None, None, None

# PR의 title을 업데이트 합니다.
# https://docs.github.com/en/rest/pulls/pulls#get-a-pull-request
def update_pr_body(pr_number, github_token, title):

    base_url = "https://api.github.com"
    pr_url = f"{base_url}/repos/{owner}/{repo}/pulls/{pr_number}"

    # PR title 업데이트
    patch_data = {"title": title}
    req = urllib.request.Request(pr_url, data=json.dumps(patch_data).encode("utf-8"), headers={"Authorization": f"token {github_token}"}, method="PATCH")
    with urllib.request.urlopen(req) as response:
        if response.code == 200:
            print(f"PR {pr_number}의 body 정보가 성공적으로 업데이트되었습니다.")
        else:
            print(f"PR {pr_number}의 body 정보 업데이트에 실패했습니다. 상태 코드: {response.code}")

def convert_title(title):
    title = "title"

pr_number = ""
github_token = ""

# 명령행 인수에서 값을 받음
if len(sys.argv) > 1:
    # 첫 번째 요소(sys.argv[0])는 스크립트의 경로입니다. 따라서 실제 값은 두 번째 요소부터 시작합니다.
    pr_number = sys.argv[1]
    github_token = sys.argv[2]
    print("값이 성공적으로 들어왔습니다.")
else:
    print("비정상적인 주입이 되어 로직이 동작하지 않습니다.")

# 해당 PR의 정보 가져오기
title = get_pr_info(pr_number, github_token)

# PR body 정보 업데이트하기
update_pr_body(pr_number, github_token, title)
