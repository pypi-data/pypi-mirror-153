import json
import time
from os import path

from git import Repo


def createRelease(app, path_project: str, release_version: str, doc_id: int):
    # generate release:
    # verify ssh access
    # stash all
    # change to develop
    # pull
    # create release branche
    # update Version and commit
    # push
    # create PR

    repo = Repo.init(path_project)
    branch_name = f'release/{release_version}'
    project_bb_name = repo.remote().url.split(':')[1][:-4]
    app.log.info('---')
    app.log.info(project_bb_name)
    app.log.info(f'release/{release_version}')
    repo.git.stash('save')
    repo.heads.develop.checkout()
    repo.remote().pull()
    commit_feature = repo.head.commit.tree
    commit_origin_dev = repo.commit("origin/master")
    new_files = []
    deleted_files = []
    modified_files = []

    # Comparing 
    diff_index = commit_origin_dev.diff(commit_feature)

    # Collection all new files
    for file in diff_index.iter_change_type('A'):
        new_files.append(file)

    # Collection all deleted files
    for file in diff_index.iter_change_type('D'):
        deleted_files.append(file)

    # Collection all modified files
    for file in diff_index.iter_change_type('M'):
        modified_files.append(file)
    if len(new_files) + len(deleted_files) + len(modified_files) == 0:
        app.log.info('No change for this release')
        return None
    # else:
        # print(new_files[0].a_path)
    repo.git.checkout('HEAD', b=f'release/{release_version}')
    try:
        with open(path.join(path_project, 'package.json'), 'r') as f:
            data = json.load(f)
            data['version'] = release_version
        app.log.info(f'update {path.join(path_project, "package.json")}')
        with open(path.join(path_project, 'package.json'), 'w') as f:
            f.write(json.dumps(data, indent=2))
        repo.git.add(update=True)
        repo.index.commit(f'push Version {release_version}')
    except BaseException as e:
        print(e)
        pass
    data = repo.git.push()
    app.log.info(f'update version {release_version} for project {project_bb_name}')
    app.db.update({'version': release_version}, doc_ids=[doc_id])

    return f'https://bitbucket.org/{project_bb_name}/pull-requests/new?source={branch_name}&t=1'
