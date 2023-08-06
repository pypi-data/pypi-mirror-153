import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate

class uwMail():
    
    """
    メール送受信クラス
    """
    
    def __init__(self, host, smtpPort, user, password):
        
        """
        コンストラクタ

        Parameters
        ----------
        host : str
            ホスト名
        smtpPort : str
            送信ポート番号
        user : str
            ユーザーアカウント
        password : str
            ユーザーパスワード
        """
        
        # ホスト、ポート番号
        self.host = host
        self.smtpPort = smtpPort
        
        # ユーザー、パスワード
        self.user = user
        self.password = password
    
    def sendMail(self, mail_from, mail_to, subject, bodyText):

        """
        メール送信
        
        Parameters
        ----------
        mail_from : str
            送信元メールアドレス
        mail_from : str
            送信先メールアドレス
        subject : str
            件名
        bodyText : str
            メール本文
        """

        # stmpオブジェクト
        self.smtp = smtplib.SMTP(self.host, self.smtpPort)
        
        # 暗号化通信開始
        self.smtp.starttls()
        
        # ログイン
        self.smtp.login(self.user, self.password)
        
        # メッセージオブジェクト
        msg = MIMEText(bodyText)
        msg['Subject'] = subject
        msg['From'] = mail_from
        msg['To'] = mail_to
        msg['Date'] = formatdate(localtime=True)
        
        # 送信
        self.smtp.sendmail(mail_from, mail_to, msg.as_string())
        
        # 切断
        self.smtp.quit()
        