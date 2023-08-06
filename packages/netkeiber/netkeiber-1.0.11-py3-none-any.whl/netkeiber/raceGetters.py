import os
import sys
import time
import LibHanger.Library.uwGetter as Getter
import LibHanger.Library.uwLogger as Logger
import LibHanger.Library.uwMath as uwMath
import netkeiber.Library.netkeiberConfiger as hc
from LibHanger.Library.DataAccess.uwPostgres import uwPostgreSQL
from LibHanger.Library.uwDeclare import uwDeclare as en
from LibHanger.Library.uwMail import uwMail
from LibHanger.Library.uwExport import JsonExporter
from LibHanger.Library.uwImport import JsonImporter
from LibHanger.Models.recset import recset
from LibHanger.Models.saWhere import saWhere
from LibHanger.Models.saOrderBy import saOrderBy
from netkeiber.Library.netkeiberGlobals import *
from netkeiber.Library.netkeiberDeclare import netkeiberDeclare as nd
from netkeiber.Models.trn_race_id import trn_race_id
from netkeiber.Models.trn_race_info import trn_race_info
from netkeiber.Getter.trn_race_id import getter_trn_race_id
from netkeiber.Getter.get_RaceData import getter_RaceData
from netkeiber.Register.register_RaceData import register_RaceData
from netkeiber.Library.netkeiberMailer import netkeiberMailer

def getAllRaceId(filePath, fromYear = 2021, toYear = 2007):
    
    """
    レースID取得メソッド(2008年～2021年)

    Parameters
    ----------
    filePath : str
        呼び出し元ファイルのパス
    fromYear : int
        取得年From
    toYear : int
        取得年To
    """

    # 共通設定
    hc.netkeiberConfiger(gv, filePath, 'config')
    
    # year.jsonファイル名定義
    yearJsonFileName = 'year.json'

    # year.jsonを格納するフォルダ名定義
    yearJsonDirName = 'json'
    
    # year.jsonの出力先ディレクトリチェック
    yearJsonDir = os.path.dirname(filePath)
    yearJsonDir = os.path.join(yearJsonDir, 'json')
    if not os.path.exists(yearJsonDir):
        os.mkdir(yearJsonDir)

    # 取込済年dict初期化
    yearDict = dict()
    
    # importer,exporterクラスインスタンス
    je = JsonExporter(filePath)
    ji = JsonImporter(filePath)

    # スクレイピング回数累計初期化
    scountCumu = 0

    # 2021->2008までループしてtrn_race_idを生成
    for year in range(fromYear, toYear, -1):
    
        # 取込済の年取得
        yearJsonFilePath = os.path.join(yearJsonDir, yearJsonFileName)
        if (os.path.exists(yearJsonFilePath)):
            yearDict = ji.convertToDict(yearJsonDirName, yearJsonFileName)
        
        # 対象年がyearDictに存在するか
        if str(year) in yearDict:
            continue
        
        # trn_race_id取得
        scount, getResult = getRaceId(filePath, year)
        scountCumu += scount
        
        # 成功したらyear.jsonに出力
        if getResult:
            try:
                yearDict[str(year)] = scount
                je.putJsonFile(yearJsonDirName, yearJsonFileName, yearDict)
            except Exception as e:
                Logger.logging.error(str(e))
                Logger.logging.error('Output of year.json failed. The Process is terminated.')
                sys.exit()
                
        # スクレイピング回数上限値チェック(超過時はループを抜ける)
        if scountCumu > gv.netkeiberConfig.LimitsScrapingCount:
            Logger.logging.warning('Scraping count exceeded.')
            break
        
def getRaceId(filePath, year):
    
    """
    レースID取得メソッド(年単位)

    Parameters
    ----------
    filePath : str
        呼び出し元ファイルのパス
    year : int
        取得年
    """

    # 共通設定
    hc.netkeiberConfiger(gv, filePath, 'config')

    # レースID情報取得クラスインスタンス
    getTrnRaceId = getter_trn_race_id()

    # uwPostgreSQL
    psgr_trid = uwPostgreSQL(gv.config) # trn_race_id用

    # 開始ログ
    Logger.logging.info('>> Started the process of trn_race_id. year={0}'.format(str(year)))

    # レースID情報取得
    scountCumu = 0
    for month in range(1,13,1):
        Logger.logging.info('>>>> Started getTrnRaceId.getData. Month={0}'.format(str(month)))
        getTrnRaceId.getData(year=year, month=month)
        scountCumu = getTrnRaceId.scrapingCount
        Logger.logging.info('<<<< Finished getTrnRaceId.getData. Month={0} ScrapingCount={1}'.format(str(month),str(getTrnRaceId.scrapingCount)))
        if scountCumu > gv.netkeiberConfig.LimitsScrapingCount:
            return scountCumu, False

    # レコードセット退避
    rsRaceId = getTrnRaceId.rsRaceId
    
    # reg
    regRaceData = register_RaceData(psgr_trid)
    regRaceData.appendRecsetList(rsRaceId)

    # 処理結果初期化
    procResult = nd.getterResult.success

    # update
    Logger.logging.info('>>>> Started trn_race_id regist database')
    result = regRaceData.execUpdate()
    if result:
        Logger.logging.info('<<<< ◎trn_race_id Regist Success Count={0}'.format(str(rsRaceId.recordCount)))
    else:
        Logger.logging.info('<<<< ☓trn_race_id Regist Failed')
        procResult = nd.getterResult.error

    # 終了ログ
    Logger.logging.info('<< trn_race_id acquisition process has been completed. year={0} result={1}'.format(str(year), procResult))

    # メールインスタンス
    um = uwMail(gv.config.MailConfig.Host, 
                gv.config.MailConfig.SmtpPort, 
                gv.config.MailConfig.User, 
                gv.config.MailConfig.Password)

    # netkeiber - mail
    nkm = netkeiberMailer(um)

    # netkeiber - mailMsg
    mmsg = nkm.nkMessage()

    # mailMessage
    mmsg.mail_from = gv.netkeiberConfig.netkeibaMailConfig.mail_from
    mmsg.mail_to = gv.netkeiberConfig.netkeibaMailConfig.mail_to
    mmsg.subject = nkm.getSubject('trn_race_id acquisition process has been completed. year=[{0}]'.format(str(year)),procResult.name)
    mmsg.bodyText = nkm.getBodyTextByRaceIdGetter(year, rsRaceId.recordCount, scountCumu)
    # mailsend
    nkm.sendMail(mmsg)
    
    # スクレイピング回数累計を返す
    return scountCumu, True

def getRaceData(filePath, year, race_id = '*', open_id = '*'):
    
    """
    レースデータ取得メソッド(年単位)

    Parameters
    ----------
    filePath : str
        呼び出し元ファイルのパス
    year : int
        取得年
    race_id : str
        レースID
    open_id : str
        開催ID
    """

    # 共通設定
    hc.netkeiberConfiger(gv, filePath, 'config')
    
    # メールインスタンス
    um = uwMail(gv.config.MailConfig.Host, 
                gv.config.MailConfig.SmtpPort, 
                gv.config.MailConfig.User, 
                gv.config.MailConfig.Password)

    # uwPostgreSQL
    psgr_trid = uwPostgreSQL(gv.config) # trn_race_id用
    psgr_grad = uwPostgreSQL(gv.config) # getter用
    psgr_regt = uwPostgreSQL(gv.config) # register用

    # netkeiber - mail
    nkm = netkeiberMailer(um)

    # netkeiber - mailMsg
    mmsg = nkm.nkMessage()
    
    # 開始ログ
    Logger.logging.info('>> Started get trn_race_id. year={0}'.format(str(year)))

    # where
    ts = saWhere()
    if year >= 2008 and race_id == '*' and open_id == '*':
        w = ts.and_(trn_race_id.race_id >= str(year) + '00000000').and_(trn_race_id.race_id <= str(year) + '99999999')
        w = w.and_(trn_race_id.get_status == 0)
    elif year < 2007 and race_id == '*' and open_id == '*':
        print('year is invalid.')
        sys.exit()
    elif race_id != '*':
        w = ts.and_(trn_race_id.race_id == race_id)
        w = w.and_(trn_race_id.get_status == 0)
    elif open_id != '*':
        w = ts.and_(trn_race_id.open_id == open_id)
        w = w.and_(trn_race_id.get_status == 0)
    else:
        print('args is invalid.')
        sys.exit()

    # order by
    ob = saOrderBy()
    s = ob.asc_(trn_race_id.race_id)
    
    # 更新用レコードセット用意
    psgr_trid.openSession(True)
    rsRaceId = recset[trn_race_id](trn_race_id)
    rsRaceId.setDA(psgr_trid)
    rsRaceId.filter(w, s)

    # 終了ログ
    Logger.logging.info('<< Finished get trn_race_id. year={0}'.format(str(year)))
        
    # レースデータ取得クラスインスタンス
    getRaceData = getter_RaceData(psgr_grad)

    # 開始ログ
    Logger.logging.info('>> Started the process of acquiring race data. year={0}'.format(str(year)))

    # trn_race_idループ
    msgLine = []
    while rsRaceId.eof() == False:
        
        # 処理時間計測 - 開始
        start = time.perf_counter()
        
        # レースデータ取得:パラメーター設定
        getRaceData.horseResultRead = False # 競走馬成績は取得しない
        getRaceData.openInfoRead = False # 開催情報は取得しない
        race_id = rsRaceId.fields(trn_race_id.race_id.key).value
        racecourse_id = rsRaceId.fields(trn_race_id.racecourse_id.key).value
        open_id = rsRaceId.fields(trn_race_id.open_id.key).value

        # 処理結果初期化
        procResult = nd.getterResult.success
        
        # 開始ログ
        Logger.logging.info('>>>> □===== Started get race_id={0} ====='.format(race_id))

        # レースデータ取得
        getRaceData.init_recset()
        getRaceData.getData(race_id=race_id, racecourse_id=racecourse_id)

        # レコードセット退避
        rsRaceResult = getRaceData.raceResult.rsRaceResult
        rsRaceInfo = getRaceData.raceResult.rsRaceInfo
        rsMstHorse = getRaceData.raceResult.rsMstHourse
        rsMstJockey = getRaceData.raceResult.rsMstJockey
        rsMstTrainer = getRaceData.raceResult.rsMstTrainer
        rsMstHowner = getRaceData.raceResult.rsMstHowner
        rsHorseResult = getRaceData.horseResult.rsHorseResult
        rsOpenInfo = getRaceData.openInfo.rsOpenInfo
        rsRefundInfo = getRaceData.refundInfo.rsRefundInfo
        rsRaceIdLog = getRaceData.raceIdLog.rsLogRaceId

        # レースNo,レース名退避
        race_no = ''
        race_nm = ''
        if getRaceData.hasError == False:
            race_no = rsRaceInfo.fields(trn_race_info.race_no.key).value
            race_nm = rsRaceInfo.fields(trn_race_info.race_nm.key).value

        # rsRaceIdLog - setDA
        rsRaceIdLog.setDA(psgr_regt)

        # エラー有無判定
        if getRaceData.hasError == True:

            # 終了ログ
            Logger.logging.info('<<< ■===== Finished get race_id={0} (getter_RaceData is terminated with an error) ====='.format(race_id))
            
            # レースIDログ登録
            upResult = rsRaceIdLog.upsert()
            if upResult.result == en.resultRegister.success:
                Logger.logging.warning('<<<< ◎log_race_id registration process Succeeded. [Error]')
            elif upResult.result == en.resultRegister.failure:
                Logger.logging.error('<<<< ☓log_race_id registration process failed.')
            procResult = nd.getterResult.error
        else:
            
            # DB更新対象セット
            regRaceData = register_RaceData(psgr_regt, race_id)
            regRaceData.appendRecsetList(rsRaceResult)
            regRaceData.appendRecsetList(rsRaceInfo)
            regRaceData.appendRecsetList(rsMstHorse)
            regRaceData.appendRecsetList(rsMstJockey)
            regRaceData.appendRecsetList(rsMstTrainer)
            regRaceData.appendRecsetList(rsMstHowner)
            regRaceData.appendRecsetList(rsHorseResult)
            regRaceData.appendRecsetList(rsOpenInfo)
            regRaceData.appendRecsetList(rsRefundInfo)

            # 開始ログ
            Logger.logging.info('>>>> □===== Started race data registration process race_id={0} ====='.format(race_id))

            # update
            result = regRaceData.execUpdate()

            # 終了ログ
            Logger.logging.info('<<<< □===== Finished race data registration process race_id={0} ====='.format(race_id))

            if result == en.resultRegister.success:
                Logger.logging.info('<<<< ◎Race data registration process Succeeded.')
            elif result == en.resultRegister.failure:
                Logger.logging.error('<<<< ☓Race data registration process Failed.')
                procResult = nd.getterResult.error

            # 処理時間 - 取得
            procTime = time.perf_counter() - start

            # 開始ログ
            Logger.logging.info('>>>> □===== Started trn_race_id registration process race_id={0} ====='.format(race_id))

            # スクレイピング回数、データ取得時間セット
            rsRaceId.editRow()
            rsRaceId.fields(trn_race_id.scraping_count.key).value = getRaceData.scrapingCount
            rsRaceId.fields(trn_race_id.get_time.key).value = uwMath.round(procTime, uwMath.fraction.round)
            rsRaceId.fields(trn_race_id.get_status.key).value = nd.getStatus.acquired.value
            rsRaceId.fields(trn_race_id.updinfo.key).value = Getter.getNow(Getter.datetimeFormat.updinfo)

            # レースID情報登録
            riResult = rsRaceId.upsert()

            # 終了ログ
            Logger.logging.info('<<<< □===== Finished trn_race_id registration process race_id={0} ====='.format(race_id))

            if riResult.result == en.resultRegister.success:
                Logger.logging.info('<<<< ◎trn_race_id registration process Succeeded.')
            elif riResult.result == en.resultRegister.failure:
                Logger.logging.error('<<<< ☓trn_race_id registration process Failed.')
                procResult = nd.getterResult.warning

            # 開始ログ
            Logger.logging.info('>>>> □===== Started log_race_id registration process race_id={0} ====='.format(race_id))
            
            # レースIDログ登録
            rsRaceIdLog = regRaceData.raceIdLog.rsLogRaceId
            rsRaceIdLog.setDA(psgr_regt)
            upResult = rsRaceIdLog.upsert()
            
            # 終了ログ
            Logger.logging.info('<<<< □===== Finished log_race_id registration process race_id={0} ====='.format(race_id))
            
            if upResult.result == en.resultRegister.success:
                Logger.logging.info('◎log_race_id registration process Succeeded.')
            elif upResult.result == en.resultRegister.failure:
                Logger.logging.error('☓log_race_id registration process Failed.')
                procResult = nd.getterResult.warning

            # 終了ログ
            if procResult == nd.getterResult.success:
                Logger.logging.info('>>> □===== Finished get race_id={0} ====='.format(race_id))
            else:
                Logger.logging.warning('>>> ■===== Finished get race_id={0} (An error has occured)====='.format(race_id))
        
        # msgLine追加
        AddMailMessage(nkm, msgLine, rsRaceId, race_no, race_nm, procResult)
        
        # open_idが変わったらメール送信
        if rsRaceId.nexteof() == True or \
           rsRaceId.fields(trn_race_id.open_id.key).nextvalue != open_id:

            # mailMessage
            mmsg.mail_from = gv.netkeiberConfig.netkeibaMailConfig.mail_from
            mmsg.mail_to = gv.netkeiberConfig.netkeibaMailConfig.mail_to
            mmsg.subject = nkm.getSubject('race data acquisition process has been completed. open_id={0}'.format(open_id), procResult.name)
            mmsg.bodyText = nkm.getBodyTextByRaceInfoGetter(msgLine)
            # mailsend
            nkm.sendMail(mmsg)
            # msgLine初期化
            msgLine = []
    
    # 終了ログ
    Logger.logging.info('<< Race data acquisition process has been completed. year={0}'.format(str(year)))

    # psgr_trid - close
    psgr_trid.closeSession()
    
def AddMailMessage(nkm:netkeiberMailer, msgLine:list, rsRaceId:recset[trn_race_id], race_no, race_nm, procResult:nd.getterResult):
    
    """
    メール本文追加
    
    Parameters
    ----------
    nkm : netkeiberMailer
        netkeiberMailerインスタンス
    msgLine : list
        メッセージリスト
    rsRaceId : recset
        trn_race_id - recset
    race_no : str
        レース番号
    race_nm : str
        レース名
    procResult : getterResult
        処理結果
    """
    
    # メッセージヘッダ部挿入
    if len(msgLine) == 0:
        msgLine.append(nkm.nkMessageTemplate.mailMessage.importDataInfoHeaderH)
        msgLine.append(nkm.nkMessageTemplate.mailMessage.importDataInfoHeaderL)
    
    # msgArgs追加
    msgArgs = []
    msgArgs.append(rsRaceId.fields(trn_race_id.race_id.key).value)
    msgArgs.append(rsRaceId.fields(trn_race_id.racecourse_id.key).value)
    msgArgs.append(race_no)
    msgArgs.append(race_nm)
    msgArgs.append(rsRaceId.fields(trn_race_id.scraping_count.key).value)
    msgArgs.append(rsRaceId.fields(trn_race_id.get_time.key).value)
    msgArgs.append(procResult.name)
    # msgLine追加
    msgLine.append(nkm.nkMessageTemplate.mailMessage.importDataInfoDetailD.format(msgArgs))
