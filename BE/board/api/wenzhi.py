import requests
import random
import time
import hmac
import hashlib
import binascii
from urllib.parse import urlencode

class Wenzhi:
    def __init__(self, param, method="POST"):
        self.param = param
        '''
           in_param_list:
             region: &eg: 'gz'
             secretId:
             secretKey:
             action: &eg: 'TextSentiment'
             action-param: ""
        '''
        self.domain = "https://wenzhi.api.qcloud.com/v2/index.php"
        self.method = method
    def _build_param(self):
        def __build_signature(params):
            srcStr = self.method + self.domain[8:] + '?' + "&".join(k.replace("_",".") + "=" + str(params[k]) for k in sorted(params.keys()))
            hashed = hmac.new(self.param['SecretKey'].encode('utf-8'), srcStr.encode('utf-8'), hashlib.sha1)
            return binascii.b2a_base64(hashed.digest())[:-1].decode('utf-8')
        timestamp = int(time.time())
        nonce = random.randint(0, 999999)
        build_param = {
            "Action": self.param['Action'],
            "Nonce": nonce,
            "Region": self.param['Region'],
            "SecretId": self.param['SecretId'],
            "Timestamp": timestamp,
        }
        for param_key in self.param['action-param']:
            build_param[param_key] = self.param['action-param'][param_key]
        build_param["Signature"] = __build_signature(build_param)
        return build_param
    def send(self):
        req = requests.post(self.domain, data=self._build_param(), timeout=100, verify=False)
        return req

if __name__ == "__main__":
    action_param = {
        'title': u'挑战杯',
        'content': u'各学院团委、作品团队：深圳大学2017年“挑战杯”大学生课外学术科技作品竞赛终审决赛将于12月17日（周日）下午在西丽校区举行。现将相关事宜通知如下：一、评审说明校内竞赛终审决赛采取分学科书面评审、现场问辩、会审3种方式进行。1.书面评审校团委已经将 作品材料报送给评审专家对作品进行书面评审，每组评审有5位校外专家。2.现场问辩现场问辩将于12月17日（周日）下午在西丽校区体 育馆西侧走廊举行，具体作品编号见附件1。（1）问辩由展板展示和评委提问两个环节组成，各参赛团队现场展板展示，评委自由提问。（2）参赛作品团队可以自行准备作品文本、PPT、视频等辅助说明物品、宣传品，在现场分发给评委（PPT展示、视频需自带笔记本电脑 ）。（3）作品编号与展位编号一致，现场按照编号即可找到展位。3.会审会审将采用现场评选的方式进行。各小组评审结束后，评委将 按照评审作品的类别被分为三组：①自然科学类学术论文、②哲学社会科学类（含哲学、经济、社会、法律、教育、管理）社会调查报告和学术论文、③科技发明制作。评委将根据作品书面评审和现场问辩评选出各作品的最终成绩。二、奖项设置本次比赛设立特等奖、一等奖、二等奖、三等奖。奖项产生方式：根据专家会审综合考量，分别评选出特等奖、一等奖、二等奖作品（评选结果将于一周后公布，届时请留意公文通）。其余作品将由学院团委评选出三等奖作品。三、展位及展板1.问辩展位提供1.6m长的桌子1张、展板1个，电源正在沟通（需了解整体用电负荷），可以携带其他辅助评审的物品。2.展板已经交付供应商制作，未接到通知的即是规格符合要求，不需修改。3.现场提供热水，参赛同学可以携带杯子取饮。4.科技发明制作类需将实物带至问辩现场（如果实物实在很大，不方便携带，需通过视频演示）。5.需要使用电源的作品，请在12月14日（周四）14:00前扫描下方二维码或点击链接https://www.wjx.top/jq/19250810.aspx登 记信息，优先提供科技发明制作类作品用电。四、现场问辩1.每件作品最多可以派2名作者参加现场问辩。2.地点：西丽校区体育馆（靠 近学生宿舍、西丽校区西门惟品门）。3.时间安排：13:30前，各作品参赛同学到签到处签到，领取参赛证，布置展位。13:50前，评委在会审室签到完毕。14:15前，评委评审说明会议。14:15-16:00，评审说明会议结束，由工作人员带至负责展区，现场问辩开始。16:00， 评委会审。问辩开始和结束具体以当天评委评审工作所需为准。4.未在签到时间前到的作品视作弃权。5.评委会佩戴评审证，不得攀认关系，不得索要评委联系方式，如有发现影响评委公正评审的行为，将做严肃处理。6.现场问辩结束后，请收拾好各自物品，清理干净展位，展板将继续用于作品展览。五、交通方式各作品参赛同学可以利用导航软件，地点定位为“深圳大学西丽校区西门”或“深圳大学西丽校区惟品门（西门）”，即可搜索到合适的前往路线。六、作品展览本次终审决赛的作品将在西丽校区体育馆展览一周（12月17日—23日），欢迎同学们到场学习交流。七、其他1.如有特殊需要，可以致电或者邮件与工作人员联系。2.请各学院团委及时将通知传达相关团队，做好相应准备。3.问辩现场如有问题，请及时与签到咨询处工作人员联系。特此通知。咨询电话:黄老师，电话：0755-86089545，邮箱：huangyj@szu.edu.cn。附件1：深圳大学2017年“挑战杯”大学生课外学术科技作品竞赛作品编号共青团深圳大学委员会2017年12月13 日',
    }
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.path.append("../")
    from board.config import wenzhi_info
    param = {
        'Region': 'sz',
        'SecretId': wenzhi_info['SecretId'],
        'SecretKey': wenzhi_info['SecretKey'],
        'Action': 'TextClassify',
        'action-param': action_param
    }
    w = Wenzhi(param)
    res = w.send()
    print (res.json())