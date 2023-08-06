"""
PDS Validate Wrapper

Tool that downloads PDS Validate Tool and executes based upon
input arguments.
"""
import github3

def get_latest_release(token, org, repo, github_object=None):
    if not github_object:
        github_object = github3.login(token=token)

    repo = github_object.repository(org, repo)
    return repo.latest_release()
