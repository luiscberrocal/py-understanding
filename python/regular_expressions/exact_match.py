import re
from typing import List


def find_remote_branches(branches: List[str], branch_type: str) -> List[str]:
    """Parse through a list of branches. """
    found_branches = []
    regexp = re.compile(r"origin/(?P<branch_type>[a-z]+)/(?P<branch>.+)")
    for branch in branches:
        match = regexp.match(branch.strip())
        if match is not None:
            if match.group('branch_type') == branch_type:
                found_branches.append(f'{branch_type}/{match.group("branch")}')

    return found_branches


if __name__ == '__main__':
    """

    """
    origin_branches = ['origin/HEAD -> origin/develop', 'origin/develop', 'origin/feature/1093_cluster_upgrade',
                       'origin/feature/OP-176_Upgrade_SSL_libs', 'origin/feature/WWW-10_eliminating_landing_pages',
                       'origin/feature/WWW-3_Update_django_and_pillow',
                       'origin/feature/add_endpoint_to_resend_transactions ',
                       '  origin/feature/get_deployment_working', 'origin/feature/s55_fix_wu_integration_k8s_deployment',
                       'origin/master', ]

    brs = find_remote_branches(origin_branches, branch_type='feature')
    for br in brs:
        print(f'{br}')