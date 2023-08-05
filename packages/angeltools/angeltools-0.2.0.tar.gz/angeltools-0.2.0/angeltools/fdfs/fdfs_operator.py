import os.path

import redis_lock
from angeltools.StrTool import FileLock
from redis import Redis

from angeltools.fdfs.fdfs_client.client import Fdfs_client, get_tracker_conf

from angeltools.fdfs import FASTFDS_CONFIG_FILE


class Fdfs:
    def __init__(self, config: str = None, lock_client: Redis = None, lock_name=None):
        self.lock_name = lock_name if lock_name else 'FdfsLock'
        self.lock_client = lock_client
        self.config = config
        self.lock = self.__lock()
        self.conf = self.__conf()
        self.client = Fdfs_client(self.conf)

    def __conf(self):
        conf_file = self.config if self.config else FASTFDS_CONFIG_FILE
        if not os.path.exists(conf_file):
            raise ValueError(f"Fdfs config file not exists! {conf_file}")
        conf = get_tracker_conf(conf_file)
        return conf

    def __lock(self):
        if self.lock_client:
            lock = redis_lock.Lock(self.lock_client, self.lock_name, expire=10)
        else:
            lock = FileLock(self.lock_name, timeout=10)
        return lock

    def upload(self, file_string, decode=False, print_out=True):
        try:
            if isinstance(file_string, str):
                file_string = file_string.encode()
            with self.lock:
                save_res = self.client.upload_by_buffer(file_string)
            fid = save_res.get("Remote file_id")
            if print_out:
                group_name = save_res.get("Group name").decode('utf-8')
                upload_status = True if 'success' in save_res.get("Status") else False
                file_size = save_res.get("Uploaded size") or 0
                upload_ip = save_res.get("Storage IP").decode('utf-8')
                print(f"file uploaded: \n        [ {upload_ip} ] [ {upload_status} ] id: {fid.decode('utf-8')} ({file_size}); group_name: {group_name} ")
        except Exception as UE:
            print(f"error in upload file: {UE}")
            return False
        return fid if not decode else fid.decode('utf-8')

    def get(self, remote_file_id, decode=False):
        file_content = b''
        if remote_file_id:
            if isinstance(remote_file_id, str):
                remote_file_id = remote_file_id.encode()
            try:
                with self.lock:
                    res_dic = self.client.download_to_buffer(remote_file_id)
                file_content = res_dic.get('Content')
            except Exception as GE:
                print(f"error in getting fdfs file: {GE}")
        return file_content if not decode else file_content.decode('utf-8')

    def delete(self, remote_file_id):
        """
        res
            'Delete file successed.', remote_file_id, storage_ip
        """
        del_sta = False
        try:
            if isinstance(remote_file_id, str):
                remote_file_id = remote_file_id.encode()
            with self.lock:
                del_sta_str, del_fid, storage_ip = self.client.delete_file(remote_file_id)
            del_sta = True if 'success' in del_sta_str else False
        except Exception as DE:
            print(f"error in deleting file {remote_file_id}: {DE}")
        return del_sta

    def __del__(self):
        pass


if __name__ == '__main__':
    fdfs = Fdfs(config='fdfs.env')

    # with open('../../requirements.txt', 'rb') as rf:
    #     file = rf.read()
    # up_res = fdfs.upload(file_string=file)
    # print(f"fid: {up_res}")

    fc = fdfs.get('group1/M00/00/09/CsABR2JiHnSARlJ7AAAArH5GiRY3348186', decode=True)
    print(fc[:500] + '...')

    # dl = fdfs.delete('group1/M00/00/09/CsABR2JiHFCAB5ZtAAAArH5GiRY5310310')
    # print(dl)


