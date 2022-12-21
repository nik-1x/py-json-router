from threading import Thread
import asyncio
import random


class REP:

    def __init__(self):
        self._methods = {}

    def register(self, name, required_parameters):
        def decorator(func):
            self._methods[name] = {
                'func': func,
                'rp': required_parameters,
                'template': {
                    'name': name,
                    'args': {arg: random.choice("abcdefghijklmnopqrstuvwxyz") for arg in required_parameters}
                }
            }

        return decorator

    def rep_wrapper(self, data: dict):
        if 'name' in list(data.keys()) and 'args' in list(data.keys()):
            name = data['name']
            args: dict = data['args']
            if name in list(self._methods.keys()):
                execution = self._methods[name]
                func_ = execution['func']
                rprm_ = execution['rp']
                params_filled = True
                for rprm in rprm_:
                    if rprm not in list(args.keys()):
                        params_filled = False
                if params_filled:
                    return asyncio.run(func_(args))
                else:
                    return {'error': 'required params not filled'}
            else:
                return {'error': 'unknown function'}
        else:
            return {'error': 'invalid data'}

    def execute(self, data_):
        response = self.rep_wrapper(data_)
        return response
