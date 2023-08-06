from gevent import monkey; monkey.patch_all()
from time import sleep
import os
import pathlib
import json
import threading

import requests
import websocket
import gevent


API_VERSION = 'v1'

def _check_for_error(r):
    if not r.ok:
        print(json.dumps(json.loads(r.text), indent=4))
    r.raise_for_status()


class _Base:
    def __init__(self, token, host):
        self.token = token
        self.host = host

    def _get_route(self):
        return f'{self.host}/{API_VERSION}'

    def _get_headers(self):
        return {'Authorization': f'Bearer {self.token}'}

    def _make_request(self, method, url, params=None, files=None, list=False):
        if method == 'POST':
            r = requests.post(
                f'{self._get_route()}{url}',
                headers=self._get_headers(),
                json=params,
                files=files
            )
        elif method == 'GET':
            r = requests.get(
                f'{self._get_route()}{url}',
                headers=self._get_headers(),
                params=params
            )
        elif method == 'DELETE':
            r = requests.delete(
                f'{self._get_route()}{url}',
                headers=self._get_headers()
            )

        _check_for_error(r)

        if r.content:
            if list:
                return r.json()['data']
            else:
                return r.json()


class _Project(_Base):
    def __init__(self, token, host, key, ws):
        super().__init__(token, host)
        self.key = key
        self.ws = ws
        self.on_complete_callback = None

    def get_info(self):
        return self._make_request('GET', f'/projects/{self.key}')

    def update_rounds(self, rounds):
        return self._make_request('POST', f'/projects/{self.key}', params={'rounds': rounds})

    def update_schedule(self, schedule):
        return self._make_request('POST', f'/projects/{self.key}', params={'schedule': schedule})

    def update_paused(self, paused):
        return self._make_request('POST', f'/projects/{self.key}', params={'paused': paused})

    def update_auto_increment(self, auto_increment):
        return self._make_request('POST', f'/projects/{self.key}', params={'autoIncrement': auto_increment})

    def update_optimizer_params(self, optimizer_params):
        return self._make_request('POST', f'/projects/{self.key}', params={'optimizerParams': optimizer_params})

    def delete_project(self):
        return self._make_request('DELETE', f'/projects/{self.key}')

    def add_contributor(self, email, role='member'):
        return self._make_request('POST', f'/projects/{self.key}/contributors', params={'email': email, 'role': role})

    def delete_contributor(self, email):
        return self._make_request('DELETE', f'/projects/{self.key}/contributors', params={'email': email})

    def get_next_schedule(self):
        return self._make_request('GET', f'/projects/{self.key}/schedule')

    def increment_round(self):
        return self._make_request('POST', f'/projects/{self.key}/increment')

    def get_rounds(self):
        return self._make_request('GET', f'/projects/{self.key}/rounds', list=True)

    def get_round(self, round):
        return self._make_request('GET', f'/projects/{self.key}/rounds/{round}')

    def get_stats(self, round=None, datasource_key=None):
        params = {}
        if round is not None:
            params['round'] = round
        if datasource_key is not None:
            params['datasource'] = datasource_key
        return self._make_request('GET', f'/projects/{self.key}/stats', params, list=True)

    def get_stats_avg(self):
        return self._make_request('GET', f'/projects/{self.key}/stats/avg')

    def get_submissions(self, datasource_key=None, round=None, owned=None):
        params = {}
        if round is not None:
            params['round'] = round
        if datasource_key is not None:
            params['datasource'] = datasource_key
        if owned is not None:
            params['owned'] = owned
        return self._make_request('GET', f'/projects/{self.key}/submissions', params, list=True)

    def upload_optimizer(self, path):
        with open(path, 'rb') as f:
            self._make_request('POST', f'/projects/{self.key}/optimizers', files={'optimizer': f})

    def report_stats(self, scores, num_samples, round, datasource_key):
        return self._make_request('POST', f'/projects/{self.key}/stats', params={
            'round': round,
            'scores': scores,
            'numPoints': num_samples,
            'datasource': datasource_key
        })

    def push_model(self, path, datasource_key, params=None):
        if params is not None:
            self._make_request('POST', f'/projects/{self.key}/models/{datasource_key}/params', params=params)

        if datasource_key is None:
            url = f'/projects/{self.key}/models'
        else:
            url = f'/projects/{self.key}/models/{datasource_key}'
        with open(path, 'rb') as f:
            self._make_request('POST', url, files={'modelfile': f})

    def pull_model(self, filepath, datasource_key=None, round=None, throw_error=False):
        params = {}
        if round is not None:
            params['round'] = round

        if datasource_key is None:
            url = f'{self._get_route()}/projects/{self.key}/models'
        else:
            url = f'{self._get_route()}/projects/{self.key}/models/{datasource_key}'
        r = requests.get(url, headers=self._get_headers(), params=params)
        _check_for_error(r)

        directory = os.path.dirname(filepath)
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)

        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)

    def add_datasource_and_trainer(self, datasource_key, trainer_key):
        return self._make_request('POST', '/bridges', params={'projectKey': self.key, 'datasourceKey': datasource_key, 'trainerKey': trainer_key})


class _Datasource(_Base):
    def __init__(self, dfl, key):
        super().__init__(dfl.token, dfl.host)
        self.dfl = dfl
        self.key = key
        self.trainers = {}

    def add_trainer(self, key, train_callback, test_callback, description=None, model_path=None):
        params = {'key': key}
        if description is not None:
            params['description'] = description
        self._make_request('POST', f'/datasources/{self.key}/trainers', params=params)
        self.trainers[key] = {
            'train': train_callback,
            'test': test_callback,
        }

        if model_path is not None:
            self.trainers[key]['model_path'] = model_path

        for p in self.dfl.project_participants:
            project_key = p['project_key']
            datasource_key = p['datasource_key']
            info = self._make_request('GET', f'/projects/{project_key}')
            threads_key = get_threads_key(project_key, datasource_key)
            self.dfl.on_round_threads[threads_key] = gevent.spawn(self.dfl.train_and_test_callback, datasource_key, info)


class DynamoFL(_Base):
    def __init__(self, token, host='https://api.dynamofl.com', metadata=None):
        super().__init__(token, host)

        self.wshost = self.host.replace('http', 'ws', 1)
        self.project_callbacks = {}
        self.on_round_threads = {}
        # self.projects = {}
        self.project_participants = []
        self.datasources = {}
        self.instance_id = None
        self.metadata = metadata

        self.ws = websocket.WebSocketApp(
            self.wshost,
            on_open=self._on_open,
            on_message=self._on_message,
            on_close=self._on_close,
            on_error=self._on_error
        )

        t = threading.Thread(target=self.ws.run_forever)
        t.setDaemon(False)
        t.start()

    def _on_open(self, ws):
        self.ws.send('{ "action": "auth", "token": "' + self.token + '" }')

    def _on_message(self, ws, res):
        j = json.loads(res)
        if j['event'] == 'client-info':
            self.instance_id = j['data']['id']

        if j['event'] == 'new-project':
            project_key = j['data']['projectKey']
            datasource_key = j['data']['datasourceKey']
            trainer_key = j['data']['trainerKey']

            # self.projects[project_key] = {
            #     'datasource_key': datasource_key,
            #     'trainer_key': trainer_key
            # }

            self.project_participants.append({
                'project_key': project_key,
                'datasource_key': datasource_key,
                'trainer_key': trainer_key
            })

            info = self._make_request('GET', f'/projects/{project_key}')
            threads_key = get_threads_key(project_key, datasource_key)
            self.on_round_threads[threads_key] = gevent.spawn(self.train_and_test_callback, datasource_key, info)


        if 'data' in j and 'project' in j['data'] and 'key' in j['data']['project']:
            project_key = j['data']['project']['key']
        if j['event'] == 'project-complete':
            for p in self.project_participants:
                threads_key = get_threads_key(project_key, p['datasource_key'])
                if threads_key in self.on_round_threads:
                    self.on_round_threads[threads_key].kill()
                if project_key == p['project_key']:
                    self.on_round_threads[threads_key] = gevent.spawn(self.train_and_test_and_end_callback, p['datasource_key'], j['data']['project'])

                    # del self.projects[project_key]
            # if not len(self.project_participants):
            #     self.ws.close()
            #     return


        elif j['event'] == 'round-complete':
            for p in self.project_participants:
                threads_key = get_threads_key(project_key, p['datasource_key'])
                if threads_key in self.on_round_threads:
                    self.on_round_threads[threads_key].kill()
                if project_key == p['project_key']:
                    self.on_round_threads[threads_key] = gevent.spawn(self.train_and_test_callback, p['datasource_key'], j['data']['project'])


        elif j['event'] == 'round-error':
            for p in self.project_participants:
                threads_key = get_threads_key(project_key, p['datasource_key'])
                if threads_key in self.on_round_threads:
                    print('Federation error occured:\n  ' + j['data']['errorMessage'])

    def _on_close(self, ws, close_status_code, close_msg):
        print('Connection closed')

    def _on_error(self, ws, error):
        print('Connection error:')
        print(error)

    def train_and_test_callback(self, datasource_key, project_info):
        project = _Project(self.token, self.host, project_info['key'], self.ws)

        # on some project round completed
        # get appropriate train, test methods
        for p in self.project_participants:
            if project_info['key'] == p['project_key'] and datasource_key == p['datasource_key']:
                trainer_key = p['trainer_key']
                break
        train = self.datasources[datasource_key].trainers[trainer_key]['train']
        test = self.datasources[datasource_key].trainers[trainer_key]['test']
        model_path = 'models'
        if 'model_path' in self.datasources[datasource_key].trainers[trainer_key]:
            model_path = self.datasources[datasource_key].trainers[trainer_key]['model_path']

        current_round = project_info['currentRound']
        if project_info['isComplete']:
            current_round += 1
        ext = project_info['modelType']
        prev_round = current_round - 1
        federated_model_path = get_federated_path(model_path, ext, datasource_key, prev_round)

        # Pull
        print(f'>>> Waiting to download round ({prev_round}) federated model...')
        project.pull_model(federated_model_path, round=prev_round)

        # Test
        if test == None:
            return
        # if check_stats(current_round, datasource_key):
        #     print(f'>>> Already uploaded round ({current_round}) stats.')
        else:
            print(f'>>> Running validation on round ({prev_round}) federated model...')
            scores, num_samples = test(datasource_key, federated_model_path, project_info)
            print(scores)
            print(f'>>> Uploading scores...')
            project.report_stats(scores, num_samples, prev_round, datasource_key)
            print('Done.')
            print()

        # Push
        if not project_info['isComplete']:
            new_model_path = get_trained_path(model_path, ext, datasource_key, current_round)

            print('>>> Training weights on local model...')
            train(datasource_key, federated_model_path, new_model_path, project_info)

            print(f'>>> Uploading round ({current_round}) trained model...')
            project.push_model(new_model_path, datasource_key)
            print('Done.')
            print()

    def train_and_test_and_end_callback(self, datasource_key, project_info):
        self.train_and_test_callback(datasource_key, project_info)
        self.project_participants = list(filter(lambda x : x['project_key'] != project_info['key'], self.project_participants))


    # creates a new datasource in the api
    def attach_datasource(self, key, name=None, metadata=None):

        while not self.instance_id:
            sleep(0.1)

        params = { 'key': key, 'instanceId': self.instance_id }
        if name is not None:
            params['name'] = name
        if self.metadata is not None:
            params['metadata'] = self.metadata
        if metadata is not None:
            params['metadata'] = metadata

        found_datasources = self._make_request('GET', '/datasources', params={'key': key}, list=True)
        if len(found_datasources):
            self._make_request('POST', f'/datasources/{key}', params=params)
        else:
            self._make_request('POST', '/datasources', params=params)

        # get current projects of newly attached datasource
        j = self._make_request('GET', '/bridges', params={'datasourceKey': key})
        for i in j['data']:
            self.project_participants.append({
                'project_key': i['projectKey'],
                'datasource_key': i['datasourceKey'],
                'trainer_key': i['trainerKey']
            })

        ds = _Datasource(self, key)
        self.datasources[key] = ds
        return ds

    def delete_datasource(self, key):
        return self._make_request('DELETE', f'/datasources/{key}')

    def get_user(self):
        return self._make_request('GET', '/user')

    def create_project(self, base_model_path, params):
        j = self._make_request('POST', '/projects', params=params)

        project = _Project(self.token, self.host, j['key'], self.ws)
        project.push_model(base_model_path, None)

        return project

    def get_project(self, project_key):
        j = self._make_request('GET', f'/projects/{project_key}')
        return _Project(self.token, self.host, j['key'], self.ws)

    def get_projects(self):
        return self._make_request('GET', '/projects', list=True)



def get_trained_path(base, ext, ds, round):
    return f'{base}/trained_model_{ds}_{round}.{ext}'
def get_federated_path(base, ext, ds, round):
    return f'{base}/federated_model_{ds}_{round}.{ext}'


def get_threads_key(project_key, datasource_key):
    return project_key + '.' + datasource_key