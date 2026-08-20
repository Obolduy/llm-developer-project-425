import os

os.environ.setdefault("YDB_ENDPOINT", "grpcs://localhost:2135")
os.environ.setdefault("YDB_DATABASE", "/local/test")
os.environ.setdefault("YC_FOLDER_ID", "test-folder")
