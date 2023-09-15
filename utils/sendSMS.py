import json
import random

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.sms.v20210111 import sms_client, models
from django_redis import get_redis_connection


# 获取随机数
def captcha():
    captcha = ''
    for i in range(4):
        now_number = str(random.randint(0, 9))
        captcha += now_number
    return captcha


class TencentSMS(object):
    # 初始化数据
    def __init__(self):
        self.secretId = "AKIDmJbcNwTG1UkkTxv2A0ZppZ2GsEJ8CVIp"
        self.secretKey = "Q5UhhF7pHY5MNHwNXQ8h38yZv31MSJtE"
        self.SmsSdkAppId = "1400541834"
        self.SignName = "零五零五"
        self.TemplateId = "1031891"

    def send_sms(self, mobile):
        try:
            # 实例化一个认证对象，入参需要传入腾讯云账户secretId，secretKey,此处还需注意密钥对的保密
            # 密钥可前往https://console.cloud.tencent.com/cam/capi网站进行获取
            cred = credential.Credential(self.secretId, self.secretKey)
            # 实例化一个http选项，可选的，没有特殊需求可以跳过
            httpProfile = HttpProfile()
            httpProfile.endpoint = "sms.tencentcloudapi.com"
            # 生成随机6位数
            sms_code = captcha()
            # 实例化一个client选项，可选的，没有特殊需求可以跳过
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            # 实例化要请求产品的client对象,clientProfile是可选的
            client = sms_client.SmsClient(cred, "ap-guangzhou", clientProfile)

            # 实例化一个请求对象,每个接口都会对应一个request对象
            req = models.SendSmsRequest()
            params = {
                "PhoneNumberSet": mobile,
                "SmsSdkAppId": self.SmsSdkAppId,
                "SignName": self.SignName,
                "TemplateId": self.TemplateId,
                "TemplateParamSet": [sms_code]
            }

            # 把请求数据格式序列化
            req.from_json_string(json.dumps(params))

            # 返回的resp是一个SendSmsResponse的实例，与请求对象对应
            # resp = client.SendSms(req)
            # 输出json格式的字符串回包
            # print(resp.to_json_string())

            # 把验证码保存在Redis中
            conn = get_redis_connection("default")
            # ex=30 是30秒的过期时间
            conn.set("sms_code", sms_code, ex=30)
            conn.set("mobile", mobile[0], ex=30)
            # 打印获取Redis中保存的验证码
            print('生成的验证码', conn.get("sms_code"), '手机号', conn.get("mobile"))

        except TencentCloudSDKException as err:
            print(err)


# 测试功能
if __name__ == "__main__":
    tencentSMS = TencentSMS()
    tencentSMS.send_sms(["15575694746"])
