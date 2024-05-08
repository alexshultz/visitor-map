# gunicorn_config.py
command = '/opt/homebrew/Caskroom/miniconda/base/envs/visitor-map/bin/gunicorn'
pythonpath = '/Users/alex/Library/Mobile Documents/com~apple~CloudDocs/scripts/visitor-map'  # This should be the directory containing 'src'
bind = '0.0.0.0:8000'
workers = 4
worker_tmp_dir = '/tmp'
