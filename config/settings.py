class WeChatConf:
    CORPID = "wx02f71fb3dea46c16"
    CORPSECRET = "r4OGerF_p4UrIN6QERCefJRxzpI0SquNG5gHCxGxcOM"
    TOUSER = ""
    TOPARTY = "1"
    TOTAG = ""
    AGENTID = "1"

#开发环境
class DevelopmentConfig(WeChatConf):
    pass

APP_ENV = DevelopmentConfig
