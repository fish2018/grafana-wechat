# _*_ coding:utf-8 _*_
from flask import Flask,request,jsonify,current_app
from utils import WeChat

app = Flask(__name__)
app.config.from_object('config.APP_ENV')


@app.route('/')
@app.route('/wechat',methods=['POST','GET'])
def send_wechat():
    toparty = request.args.get('toparty')
    req = request.json
    # from utils.wechat import testdata
    # req = testdata
    try:
        res,token,expires_in = WeChat.send_card(req,toparty=toparty)
    except Exception as e:
        print(e)
        pass
    return jsonify({"msg":req})

if __name__ == '__main__':
    app.run()