import csv
import hashlib
import math
import shutil
import sys
import pathlib
import logging
import argparse
from typing import Dict
from os import listdir, scandir
from os.path import join, exists, isfile, getsize
from paramiko import SSHClient
from scp import SCPClient
from ablean.components.util.logger import Logger
from ablean.components.config.lean_config_manager import LeanConfigManager

HASH_FILE = 'data_hash.csv'


def _get_file_hash(local_file: str):
    md5_object = hashlib.md5()
    block_size = 64 * md5_object.block_size
    with open(local_file, 'rb') as f:
        chunk = f.read(block_size)
        while chunk:
            md5_object.update(chunk)
            chunk = f.read(block_size)
    return md5_object.hexdigest()


def _scantree(path):
    """Recursively yield DirEntry objects for given directory."""
    for entry in scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield from _scantree(entry.path)  # see below for Python 2.x
        else:
            yield entry


def _convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


class DataManager:
    def __init__(
        self,
        lean_config_manager: LeanConfigManager,
        logger: Logger,
    ):
        self.lean_config_manager = lean_config_manager
        self.logger = logger
        self.progress = None
        self.progress_task =None
        self._load_config()

    def _load_data_hash(self, filename: str = HASH_FILE):
        filename = join(self.data_path, filename)
        if exists(filename):
            with open(filename, mode='r') as infile:
                reader = csv.reader(infile)
                return {rows[0]: rows[1] for rows in reader}
        else:
            return {}

    def _scp_get(self, scp: SCPClient, remote_path: str, local_path: str):
        if self.progress is not None:
            self.progress.stop()
        self.progress = self.logger.progress()
        self.progress_task = self.progress.add_task(remote_path)
        try:
            scp.get(remote_path, local_path)
        except KeyboardInterrupt as e:
            if self.progress is not None:
                self.progress.stop()
            raise e
        pass

    def _scp_download_file(
        self,
        scp: SCPClient,
        remote_file: str,
        local_file: str,
        hash: str = None,
    ):
        remote_file = f"{self.remote_path}/{remote_file}".replace('//', '/')
        local_file = f"{self.remote_path}/{local_file}".replace('//', '/')
        if not exists(local_file):
            local_path = pathlib.Path(local_file).parent.resolve()
            local_path.mkdir(parents=True, exist_ok=True)
        elif _get_file_hash(local_file) == hash:
            self.logger.info(f'{local_file} is OK!')
            return

        if hash is None:
            self._scp_get(scp, remote_file, local_file)
        else:
            temp_file = f"{self.data_path}/{hash}.tmp".replace('//', '/')
            self._scp_get(scp, remote_file, temp_file)
            shutil.move(temp_file, local_file)

    def _load_data_hash(self, filename: str = HASH_FILE):
        filename = join(self.data_path, filename)
        if exists(filename):
            with open(filename, mode='r') as f:
                reader = csv.reader(f)
                return {rows[0]: rows[1] for rows in reader}
        else:
            return {}

    def _init_data_hash(self, hash_table: Dict):
        for path in ['option', 'future', 'crypto']:
            path = join(self.data_path, path)
            if not exists(path):
                continue
            for item in _scantree(path):
                if not item.path.endswith(".zip"):
                    continue
                self._update_file_hash(item.path, hash_table)
                self.logger.info(f"init {item.path} hash")

    def _get_file_key(self, local_file: str):
        return local_file[len(self.data_path) :].replace('\\', '/')

    def _update_file_hash(self, local_file: str, hash_table: Dict):
        md5 = _get_file_hash(local_file)
        key = self._get_file_key(local_file)
        hash_table[key] = md5
        pass

    def _save_data_hash(self, hash_table: Dict):
        filename = join(self.data_path, HASH_FILE)
        with open(filename, mode='w') as outfile:
            for k, v in hash_table.items():
                outfile.write(f"{k},{v}\n")

    def _on_data(self, filename: str, size: int, send: int):
        if size >= send:
            send_size = _convert_size(send)
            file_size = _convert_size(size) + ' ' * 5
            desc = f'{send_size}/{file_size}'
            self.progress.update(
                self.progress_task,
                completed=(send / float(size) * 100),
                description=desc,
            )

    def _load_config(self):
        config = self.lean_config_manager.get_lean_config()
        self.data_path = config["data-folder"]
        self.remote_path = config["remote-data-folder"]
        self.ssh_host = config["ssh-host"]
        self.ssh_port = config["ssh-port"]
        self.ssh_user = config["ssh-user"]
        self.ssh_password = config["ssh-pwd"]
        self.update_second_data = config["update-second-data"]

    def update_data(self, update_second_data=False, force_update=False):        
        self._load_config()
        self.logger.info(f"update data from {self.ssh_host}")
        local_hash = self._load_data_hash()
        if force_update or len(local_hash) == 0:
            self._init_data_hash(local_hash)
            self._save_data_hash(local_hash)

        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.connect(
            self.ssh_host,
            port=self.ssh_port,
            username=self.ssh_user,
            password=self.ssh_password,
            compress=True,
        )
        scp = SCPClient(ssh.get_transport(), progress=self._on_data)
        self._scp_download_file(scp, HASH_FILE, f'server_{HASH_FILE}')
        remote_hash = self._load_data_hash(f'server_{HASH_FILE}')
        update_second_data = update_second_data or self.update_second_data
        for k, v in remote_hash.items():
            if k in local_hash and v == local_hash[k]:
                continue
            if 'second' in k and not update_second_data:
                continue

            self.logger.info(f"download: {k}")
            self._scp_download_file(scp, k, k, v)
            local_hash[k] = v
        self._save_data_hash(local_hash)
