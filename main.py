import os
import requests
import threading

ip = int(input("How many times do you want to commit? \n"))
autoPush = input("Auto git push when committed? (y/n) \n")
createPR = input("Create pull requests? (y/n) \n")
autoApprove = input("Automatically approve pull requests? (y/n) \n")

for i in range(ip):
    os.system(f'git commit --allow-empty -m "Commit {i + 1} of {ip}"')

print("Committed " + str(ip) + " times")

if autoPush == "y":
    os.system('git push')

if createPR == "y":
    base_branch = input("Enter the base branch for the pull request: ")
    pr_title = input("Enter the title for the pull request: ")
    pr_body = input("Enter the description for the pull request: ")

    github_token = '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'
    repo_owner = 'Comicly69'
    repo_name = 'dotfiles'

    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    def create_and_approve_pr(commit_number):
        pr_branch = f'feature/commit-{commit_number + 1}'
        os.system(f'git checkout -b {pr_branch}')
        os.system(f'git push -u origin {pr_branch}')

        # Create the pull request using GitHub REST API
        data = {
            'title': pr_title,
            'body': pr_body,
            'head': pr_branch,
            'base': base_branch
        }

        response = requests.post(f'https://api.github.com/repos/{repo_owner}/{repo_name}/pulls', json=data, headers=headers)

        if response.status_code == 201:
            pr_data = response.json()
            pr_number = pr_data['number']
            print(f"Pull request {commit_number + 1} created successfully! PR number: {pr_number}")

            if autoApprove == "y":
                # Automatically approve the pull request using GitHub REST API
                approval_data = {
                    'event': 'APPROVE'
                }

                approval_response = requests.post(f'https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}/reviews', json=approval_data, headers=headers)

                if approval_response.status_code == 200:
                    print(f"Pull request {pr_number} approved!")
                else:
                    print(f"Failed to approve pull request {pr_number}. Error: {approval_response.text}")
        else:
            print(f"Failed to create pull request {commit_number + 1}. Error: {response.text}")

    threads = []
    for i in range(ip):
        t = threading.Thread(target=create_and_approve_pr, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
