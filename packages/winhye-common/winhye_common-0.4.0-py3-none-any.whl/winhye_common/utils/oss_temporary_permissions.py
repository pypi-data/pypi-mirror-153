import logging

from Tea.core import TeaCore

from alibabacloud_sts20150401.client import Client as Sts20150401Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_sts20150401 import models as sts_20150401_models
from alibabacloud_tea_util.client import Client as UtilClient

from winhye_common.winhye_logger import logging as logging

logger = logging.getLogger()


class OssTemporaryPermissions:
    def __init__(self, endpoint, access_key_id, access_key_secret, role_arn, role_session_name, duration_seconds=3600):
        self.endpoint = endpoint  # 访问的域名
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.role_arn = role_arn  # 角色Arn
        self.role_session_name = role_session_name  # 角色Arn名称
        self.duration_seconds = duration_seconds  # SecurityToken过期时间

    def create_client(self):
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        :param end_point:
        """
        config = open_api_models.Config(
            # 您的AccessKey ID,
            access_key_id=self.access_key_id,
            # 您的AccessKey Secret,
            access_key_secret=self.access_key_secret
        )
        # 访问的域名
        config.endpoint = self.endpoint
        return Sts20150401Client(config)

    def get_security_token(self):
        retry_count = 0
        while True:
            try:
                retry_count += 1
                client = self.create_client()
                assume_role_request = sts_20150401_models.AssumeRoleRequest()
                assume_role_request.duration_seconds = self.duration_seconds
                assume_role_request.role_arn = self.role_arn
                assume_role_request.role_session_name = self.role_session_name
                resp = client.assume_role(assume_role_request)
                return UtilClient.to_jsonstring(TeaCore.to_map(resp))
            except Exception as e:
                if retry_count >= 3:
                    logger.error(e)
                    raise Exception("oss_temporary_permissions has error")


if __name__ == '__main__':
    tok = OssTemporaryPermissions(
        'sts.cn-shenzhen.aliyuncs.com',
        'LTAI5t7p1eu71D42w6rQgRVe',
        'vBwcJofSyQUqm1GCBah5mIfOy8oDzx',
        'acs:ram::1153626070681379:role/ramoss',
        'RamOss',
        3600
    )
    aa = tok.get_security_token()
    print(aa)
    # '''
    #     oss_temporary_permissions.endpoint = sts.cn-shenzhen.aliyuncs.com
    #     oss_temporary_permissions.access_key_id = LTAI5t7p1eu71D42w6rQgRVe
    #     oss_temporary_permissions.access_key_secret = vBwcJofSyQUqm1GCBah5mIfOy8oDzx
    #     oss_temporary_permissions.role_arn = acs:ram::1153626070681379:role/ramoss
    #     oss_temporary_permissions.role_session_name = RamOss
    #     oss_temporary_permissions.bucket_name = winhye-kaifa
    #     oss_temporary_permissions.duration_seconds = 3600
    # '''
