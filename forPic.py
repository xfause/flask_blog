from hashlib import sha1
import hmac
import base64
import datetime
import time
import os

def getToken():
	# 七牛 密钥
	AK = os.environ.get('AK') or '' #access key
	SK = os.environ.get('SK') or '' #secret key
	d1 = int(time.mktime(datetime.datetime.now().timetuple()))+21600
	s = '{"scope":"BUCKET","deadline":%s}'%(dl,) #BUCKET填自己存储空间bucket的名字
	s = base64.urlsafe_b64encode(s)
	sign = hmac.new(SK,s,sha1).digest()
	sign = base64.urlsafe_b64encode(sign)
	token = AK + ':' + sign + ':' + s
	return token
