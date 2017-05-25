from hashlib import sha1
import hmac
import base64
import datetime
import time
import os

def getToken():
	# 七牛 密钥
	AK = os.environ.get('AK') or 'UkIkqJcV3DvInPK0zXsHaZBD6UYjLGaRGzLybY7J' #access key
	SK = os.environ.get('SK') or 'WfyHKYFtijCvX03i6pTUjqwUeFjwUM2CYy5jXZuT' #secret key
	dl = int(time.mktime(datetime.datetime.now().timetuple()))+21600
	s = '{"scope":"blog-pic","deadline":%s}'%(dl,) #BUCKET填自己存储空间bucket的名字
	s = base64.urlsafe_b64encode(bytes(s,'utf-8'))
	sign = hmac.new(b'SK',s,sha1).digest()
	sign = base64.urlsafe_b64encode(sign)
	token = AK + ':' + str(sign) + ':' + str(s)
	return token
