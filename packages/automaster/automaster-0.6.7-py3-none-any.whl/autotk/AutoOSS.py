import configparser
import tkinter as tk
from tkinter import ttk
import oss2

class RemoteConfig(object):
    def __init__(self, access_id, access_key, bucket_name):
        raise "Close OSS"  # 暂时关闭OSS,Download未接入,后续未调试完毕
        """验证权限"""
        self.auth = oss2.Auth(access_id, access_key)
        self.endpoint = 'https://oss-cn-shenzhen.aliyuncs.com'
        self.bucket = oss2.Bucket(self.auth, self.endpoint, bucket_name=bucket_name)

    def get_bucket_list(self):
        """列举当前endpoint下所有的bucket_name"""
        service = oss2.Service(self.auth, self.endpoint)
        bucket_list = [b.name for b in oss2.BucketIterator(service)]
        return bucket_list

    def get_all_file(self, dirstr):
        """获取指定前缀下所有文件"""
        listfiles=[]
        for obj in oss2.ObjectIterator(self.bucket):
            obj_str=obj.key
            if not dirstr==obj_str:
                listfiles.append(obj_str)
        return listfiles
    def ossfile_dict_conf(self, ossfile,sub=None):
        ini_byte=self.read_ossfile(ossfile)
        cf = configparser.ConfigParser()
        d={}
        if ini_byte:
            cf = configparser.ConfigParser()
            cf.read_string(ini_byte.decode())
            d = dict(cf._sections)
            for k in d:
                d[k] = dict(d[k])
            if (sub): return d[sub]
        return d,cf
    def read_ossfile(self, path):
        try:
            file_info = self.bucket.get_object(path).read()
            return file_info
        except Exception as e:
            print('[read_ossfile]文件不存在',e)
            return None

    def download_file(self, path, save_path):
        result = self.bucket.get_object_to_file(path, save_path)
        if result.status == 200:
            print('下载完成')

    def upload_file(self, path, local_path):
        print(self.bucket.object_exists(path))
        result = self.bucket.put_object_from_file(path, local_path)
        if result.status == 200:
            print('上传完成')
            return True
        return False
    def diff_oss_conf(self,osspath,local,showfunc=None):
        d1,_cf1=self.ossfile_dict_conf(osspath)
        if(isinstance(local,dict)):  # 支持缓存的字典
            d2=local
        else:
            cf = configparser.ConfigParser()
            cf.read(local)
            d2 = dict(cf._sections)
        same_key=d1.keys() & d2
        for s in same_key:
            diff = d1[s].keys() & d2[s]
            diff_vals = [(k, d1[s][k], d2[s][k]) for k in diff if d1[s][k] != d2[s][k]]
            if(diff_vals):
                if showfunc:showfunc(s,diff_vals,"same")
            rm_keys=d1[s].keys() - d2[s].keys()
            add_keys=d2[s].keys() - d1[s].keys()
            if rm_keys:
                _r_list=[]
                for r in rm_keys:
                    _r=(r,d1[s][r],"")
                    _r_list.append(_r)
                if showfunc:showfunc(s,_r_list,"add")
            if add_keys:
                _a_list = []
                for a in add_keys:
                    _a = (a, "",d2[s][a])
                    _a_list.append(_a)
                if showfunc: showfunc(s, _a_list, "del")
        rm_secs = d1.keys() - d2.keys()
        add_secs = d2.keys() - d1.keys()
        if rm_secs:
            for rr in rm_secs:
                rr_list = []
                for r in d1[rr]:
                    rr_list.append((r,d1[rr][r],""))
                if showfunc:showfunc(rr,rr_list,"add")
        if add_secs:
            for aa in add_secs:
                aa_list = []
                for a in d2[aa]:
                    aa_list.append((a,"",d2[aa][a]))
                if showfunc:showfunc(aa,aa_list,"del")
        return d1
if __name__ == '__main__':
    access_id = 'LTAI5tQWvrvbxNW7BufbpsPL'
    access_key = 'pQ58Moes1OsZlcstfivbgYpjntS7UP'
    bucket_name = 'sei-pms-bin'
    co = ConnectOss(access_id, access_key, bucket_name)
    lsfiles=co.get_all_file("Auto_FactoryLite/")
    # print(lsfiles)
    # for f in lsfiles:
    #     co.diff_oss_conf(f,"./config.ini",print)

    # co.upload_file('Auto_FactoryLite/测试配置.ini',"./config.ini")
    setdict={"oss_files":lsfiles,"func_diff":co.diff_oss_conf,"local":"./config1.ini",}
    ret_dict={"Result":False}
    root=tk.Frame()
    root.wait_window(DiffTreeBox(root,setting=setdict,result=ret_dict))
    print(ret_dict)