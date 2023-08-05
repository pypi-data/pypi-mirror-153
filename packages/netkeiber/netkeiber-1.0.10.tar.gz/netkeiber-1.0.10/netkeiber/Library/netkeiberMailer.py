import LibHanger.Library.uwLogger as Logger
import LibHanger.Library.uwUtil as uwUtil
from LibHanger.Library.uwMail import uwMail
from LibHanger.Models.recset import recset
from netkeiber.Models.trn_race_id import trn_race_id
from netkeiber.Models.trn_race_info import trn_race_info

class netkeiberMailer():
    
    """
    netkeiber - メールクラス
    """
    
    class nkMessage():
        
        """
        メッセージクラス
        """
        
        def __init__(self):
            
            """
            コンストラクタ
            """
            
            self.mail_from = ''
            """ 送信元メールアドレス """

            self.mail_to = ''
            """ 送信先メールアドレス """
            
            self.subject = []
            """ 件名 """
            
            self.bodyText = []
            """ 本文 """
    
    class nkMessageTemplate():
        
        """
        メール定型文クラス
        """
        
        class mailMessage():
            
            """
            メール定型文
            """
            
            subjectTemplate = '[netkeiber] proc:{0} result:{1}'
            """ 件名テンプレート 
            {0}:処理内容
            {1}:処理結果(success/warning/error)
            """
            
            diskFreeInfo = 'diskfree: {0}%'
            """ 空きディスク容量 
            {0}:空きディスク容量(%)
            """
            
            importDataCal = 'year:{0} \n race_id_count:{1} \n scraping_count:{2}'
            """ 取込データカレンダー情報 
            {0}:取得年
            {1}:取得race_id件数
            {2}:スクレイピング回数
            """
            
            importDataInfoHeaderH = 'race_id,racecourse_id,race_no,race_nm,scraping_count,get_time,result'
            importDataInfoHeaderL = '--------------------------------------------------------------------'
            importDataInfoDetailD = '{0[0]};{0[1]};{0[2]}R;{0[3]};{0[4]};{0[5]};{0[6]}'
            """ 取込データ情報 
            {0}:レースID
            {1}:競馬場ID
            {2}:レース番号
            {3}:レース名
            {4}:スクレイピング回数
            {5}:取得に要した時間
            {6}:処理結果
            """
            
    def __init__(self, __um:uwMail):
        
        """
        コンストラクタ
        """

        # uwMailクラスインスタンス取得
        self.um = __um
    
    def sendMail(self, msg:nkMessage):
        
        """
        メール送信
        """
        
        try:
            # メール送信
            subject = '\n'.join(msg.subject)
            bodyText = '\n'.join(msg.bodyText)
            self.um.sendMail(msg.mail_from, msg.mail_to, subject, bodyText)
        except Exception as e:
            print(str(e))
            Logger.logging.error(e)

    def getSubject(self, proc, result)->list:
        
        msgLine = []
        msgLine.append(self.nkMessageTemplate.mailMessage.subjectTemplate.format(proc,result))
        return msgLine
    
    def addMessageDiskfree(self, msgLine:list):

        # 空きディスク容量取得
        diskFree = uwUtil.dskFree

        msgLine.append('====================================================')
        msgLine.append(self.nkMessageTemplate.mailMessage.diskFreeInfo.format(str(diskFree)))
        msgLine.append('====================================================')
    
    def getBodyTextByRaceIdGetter(self, year, race_id_count, scrapingCount)->list:
        
        msgLine = []
        # 取得メッセージ
        msgLine.append(self.nkMessageTemplate.mailMessage.importDataCal.format(str(year),str(race_id_count),str(scrapingCount)))
        # ディスク空き容量
        self.addMessageDiskfree(msgLine)
        return msgLine
    
    def getBodyTextByRaceInfoGetter(self, msgLine)->list:

        # ディスク空き容量
        self.addMessageDiskfree(msgLine)
        
        return msgLine
    