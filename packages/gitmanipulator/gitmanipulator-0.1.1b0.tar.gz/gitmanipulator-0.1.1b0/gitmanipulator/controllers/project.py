import json
import webbrowser
from concurrent.futures import ThreadPoolExecutor, as_completed
from os import path
from cement import Controller, ex
from tqdm import tqdm

from gitmanipulator.service.gitManager import createRelease


class Project(Controller):
    class Meta:
        label = 'project'
        stacked_type = 'nested'
        stacked_on = 'base'

    @ex(help='list projects')
    def list(self):
        data = {}
        data['projects'] = self.app.db.all()
        lstP = [d['project'] for d in data['projects']]
        lstV = [d['version'] for d in data['projects']]
        data['maxP'] = len(max(lstP, key=len, default=''))
        data['maxV'] = len(max(lstV, key=len, default=''))
        self.app.render(data, 'projects.jinja2')

    @ex(help='add one or many projects',
        arguments=[
            (['project_paths'],
             dict(action='store', nargs='*', help='project path'))
        ], )
    def add(self):
        project_paths = self.app.pargs.project_paths
        for project_path in project_paths:
            if path.exists(project_path) == False:
                self.app.log.error(f'bad path : "{project_path}"')
                continue
            if not path.exists(path.join(project_path, '.git')):
                self.app.log.error(f'bad git folder : "{path.join(project_path, ".git")}"')
                continue
            project_path = path.abspath(project_path)
            version = '0.0.0'
            try:
                with open(path.join(project_path, 'package.json'), 'r') as f:
                    data = json.load(f)
                    version = data['version']
            except BaseException as e:
                self.app.log.info(f'package.json not found "{path.join(project_path, "package.json")}"')
                pass
            self.app.log.info('adding project: %s' % project_path)
            project = {
                'path': project_path,
                'version': version,
                'project': path.basename(project_path)
            }
            self.app.db.insert(project)

    @ex(help='delete a project',
        arguments=[
            (['project_id'],
             {'help': 'project database id',
              'action': 'store'}),
        ], )
    def delete(self):
        id = int(self.app.pargs.project_id)
        self.app.log.info('deleting project id: %s' % id)
        self.app.db.remove(doc_ids=[id])

    @ex(
        help='update an existing project',
        arguments=[
            (['item_id'],
             {'help': 'project database id',
              'action': 'store'}),
            (['--version'],
             {'help': 'project version',
              'action': 'store',
              'dest': 'version'}),
        ],
    )
    def update(self):
        id = int(self.app.pargs.item_id)
        version = self.app.pargs.version

        item = {
            'version': version,
        }

        self.app.db.update(item, doc_ids=[id])

    @ex(help='delete all projects')
    def dropall(self):
        self.app.log.info('deleting all projects')
        self.app.db.truncate()

    @ex(help='create release for all projects')
    def release(self):
        all_projects = self.app.db.all()
        processes = []
        with ThreadPoolExecutor(max_workers=len(all_projects)) as executor:
            for project in all_projects:
                maj = int(project['version'].split('.')[0])
                min = int(project['version'].split('.')[1]) + 1
                new_version = f'{maj}.{min}.0'
                processes.append(executor.submit(createRelease, self.app, project['path'], new_version, project.doc_id))

        for task in tqdm(as_completed(processes)):
            url = task.result()
            if url is None:
                continue
            print(url)
            webbrowser.open(url, new=2)

    @ex(help='fetch all projects')
    def fetch(self):
        pass
