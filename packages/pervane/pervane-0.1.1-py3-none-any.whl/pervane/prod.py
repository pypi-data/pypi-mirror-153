"""
This is the actual main from the published cli tool.

`pervane --dir=.` calls this and then run is being called.
"""
#from pervane import serve
from pervane import run as serve
import multiprocessing
import gunicorn.app.base
import subprocess
from pervane import run_create_admin


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def main(as_module=False):
  print(f'running in mode: {serve.args.mode}')
  if serve.args.mode == 'serve':
    options = {
        'bind': '%s:%s' % (serve.args.host, serve.args.port),
        'workers': number_of_workers(),
    }
    StandaloneApplication(serve.app, options).run()
  elif serve.args.mode == 'init':
    import os
    os.environ['FLASK_APP'] = 'pervane.run_create_admin'
    subprocess.call(['flask', 'fab', 'create-admin'])
    # run_create_admin.main()
  else:
    print('unknown mode')


if __name__ == '__main__':
  serve.cli_main()
