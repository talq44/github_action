import sys
import urllib.request
import json

owner = "bejewel-amondz"  # 레포지토리 소유자 이름
repo = "amondz-user-ios"  # 레포지토리 이름
related_pr_title = "### Related PRs"

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
            body = pr_data['body']
            base_branch = pr_data['base']['ref']
            return body, base_branch
    except urllib.error.HTTPError as e:
        print(f"Failed to fetch PR data: {e.code}")
        return None, None
    
def get_related_prs_html_urls(pr_number, base_branch, github_token):
    base_url = "https://api.github.com"
    prs_url = f"{base_url}/repos/{owner}/{repo}/pulls"
    params = {"base": base_branch}
    headers = {"Authorization": f"token {github_token}"}
    
    # PR 목록 가져오기
    req = urllib.request.Request(f"{prs_url}?base={base_branch}&state=all", headers=headers)
    with urllib.request.urlopen(req) as response:
        prs_data = json.loads(response.read().decode("utf-8"))

    # 같은 base 브랜치로 PR한 목록의 html_url 가져오기
    html_urls = [pr["html_url"] for pr in prs_data]
    filtered_urls = [url for url in html_urls if f"{pr_number}" not in url]
    formatted_urls = ["- " + url for url in filtered_urls]

    return formatted_urls

def update_pr_body(pr_number, github_token, beforeBody, html_urls):

    # 문자열 내에 'o' 문자가 있는지 확인
    if f"{related_pr_title}" in beforeBody:
        print(f"{related_pr_title} 기존 관련된 PR목록이 있어, 종료합니다.")
        return
    else:
        print(f"{related_pr_title} 기존 관련된 PR목록이 없어, 로직을 계속합니다.")

    base_url = "https://api.github.com"
    pr_url = f"{base_url}/repos/{owner}/{repo}/pulls/{pr_number}"

    # PR body에 html_urls 추가하기
    body = beforeBody
    updated_body = f"{body}\n\n{related_pr_title}\n" + "\n".join(html_urls)

    # PR body 업데이트
    patch_data = {"body": updated_body}
    req = urllib.request.Request(pr_url, data=json.dumps(patch_data).encode("utf-8"), headers={"Authorization": f"token {github_token}"}, method="PATCH")
    with urllib.request.urlopen(req) as response:
        if response.code == 200:
            print(f"PR {pr_number}의 body 정보가 성공적으로 업데이트되었습니다.")
        else:
            print(f"PR {pr_number}의 body 정보 업데이트에 실패했습니다. 상태 코드: {response.code}")


pr_number = ""
github_token = ""

# 명령행 인수에서 값을 받음
if len(sys.argv) > 1:
    
    pr_number = sys.argv[1]
    github_token = sys.argv[2]
    print("값이 성공적으로 들어왔습니다.")
else:
    print("비정상적인 주입이 되어 로직이 동작하지 않습니다.")

# 해당 PR의 정보 가져오기
body, base_branch = get_pr_info(pr_number, github_token)

# 같은 base 브랜치로 PR한 목록의 HTML URL 가져오기
html_urls = get_related_prs_html_urls(pr_number ,base_branch, github_token)

# PR body 정보 업데이트하기
update_pr_body(pr_number, github_token, body, html_urls)
