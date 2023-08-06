import logging
import os
import re
from os import mkdir, path
from pathlib import Path
from github import Github

DATA_PATH = os.path.join(str(Path.home()), '.kolibri')

GITHUB_TOKEN="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"
GITHUB_REPO_NAME="mbenhaddou/kolibri-data"
MODEL_CARD_NAME = "model_card.json"

Path(DATA_PATH).mkdir(exist_ok=True, parents=True)


# [entity_text](entity_type(:entity_synonym)?)
ent_regex = re.compile(r'\[(?P<entity_text>[^\]]+)'
                       r'\]\((?P<entity>[^:)]*?)'
                       r'(?:\:(?P<text>[^)]+))?\)')

RELATIVE_ERROR = 10000
DEFAULT_SERVER_PORT = 5005
DEFAULT_SEED=4231
EMBEDDING_SIZE = 100
WORD2VEC_WORKERS = 4
MIN_WORD_COUNT = 5
WORD2VEC_CONTEXT = 5
TARGET_RANKING_LENGTH = 10
LOGS_DIR = path.join(DATA_PATH, 'logs')
LOG_NAME = 'kolibri'
LOG_FILE = path.join(LOGS_DIR, LOG_NAME + '.log')
LOG_LEVEL = logging.DEBUG

MINIMUM_COMPATIBLE_VERSION = "0.0.1"

DEFAULT_NLU_FALLBACK_THRESHOLD = 0.0

DEFAULT_CORE_FALLBACK_THRESHOLD = 0.0

DEFAULT_REQUEST_TIMEOUT = 60 * 5  # 5 minutes

DEFAULT_SERVER_FORMAT = "http://localhost:{}"

DEFAULT_SERVER_URL = DEFAULT_SERVER_FORMAT.format(DEFAULT_SERVER_PORT)


DOCUMENT_TEXT_MAX_LENGTH = 255

DOCUMENT_LABEL_MAX_LENGTH = 32

# The maximum length_train of characters that the name of a tag can contain
TAG_NAME_MAX_LENGTH = 50

DIRS = [DATA_PATH, LOGS_DIR]

for d in DIRS:
    if not path.exists(d):
        mkdir(d)



try:
    Resources_sha
except NameError:
    Resources_sha={}
path_i=Path(".")
path=path_i
try:
    _repo=Github(GITHUB_TOKEN).get_repo(GITHUB_REPO_NAME)
    __branch=_repo.get_branch("main").commit
except:
    _repo=None
    __branch=None
    pass





def traverse(node, path = [], paths = []):

    if hasattr(node, "path"):
        path.append(node.path)
    if hasattr(node, "type") and node.type == "blob":
        data=dict(node.raw_data)
        data['path']='/'.join(path)
        data['url']="https://raw.githubusercontent.com/mbenhaddou/kolibri-data/main/{}".format(data['path'])
        Resources_sha['/'.join(path[1:])]=data

        path.pop()
    else:
        for child in _repo.get_git_tree(node.sha).tree:
            traverse(child, path, paths)
        if path:
            path.pop()

p=[]
if __branch is not None:
    print('getting resources')
    for child in _repo.get_git_tree(__branch.sha).tree:
        if child.path=="data":
            traverse(child, p, Resources_sha)





