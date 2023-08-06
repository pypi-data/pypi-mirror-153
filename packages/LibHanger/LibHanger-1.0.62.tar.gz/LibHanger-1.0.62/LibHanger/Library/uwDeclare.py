from enum import Enum

class uwDeclare():
    
    """
    各種定義
    """
    
    class result(Enum):
        
        """
        処理結果
        """
        
        success = 0
        """ 成功 """
        
        warning = 1
        """ 警告 """
        
        critical = 2
        """ 致命的エラー """
        
    class resultRegister(Enum):
        
        """
        登録処理結果
        """
        
        success = 0
        """ 成功 """
        
        failure = 1
        """ 失敗 """
        
    class logFileNameSuffix(Enum):
        
        """
        ログファイル名サフィックス
        """
        
        suffixNone = 0
        """ サフィックス無し"""

        yyyyMMddhhmmss = 1
        """ yyyyMMddhhmmss(日時) """

        yyyyMMddhhmm = 2
        """ yyyyMMddhhmm(日時+秒抜き) """
        
        yyyyMMdd = 3
        """ yyyyMMdd(日付のみ+西暦4桁) """
        
        yyMMdd = 4
        """ yyMMdd(日付のみ+西暦下2桁) """
        
        MMdd = 5
        """ MMdd(日付のみ+月日) """
        
        @classmethod
        def value_of(cls, target_value):
            for e in uwDeclare.logFileNameSuffix:
                if e.value == target_value:
                    return e.name
            raise ValueError('{} is not a valid logFileNameSuffix value.'.format(target_value))
