class GetBourseOnline:
    def __init__(self):
        pass
    def Get(self):
        import  pandas as pd
        import time
        import os
        import requests
        start_time = time.time()
        self.url='http://members.tsetmc.com/tsev2/excel/MarketWatchPlus.aspx?d=0'
        r = requests.get(self.url)
        open('temp.xls', 'wb').write(r.content)
        df = pd.read_excel('temp.xls')
        os.remove('.\\temp.xls')
        Mylist=df.T.values.tolist()
        self.Get_Time=Mylist[0][0]
        dictionary=dict()
        columns=['Symbol','Name','Number','Volume','Value','Yesterday','First','Last-Amount','Last-Change','Last-Percent','LastPR-Amount','LastPR-Percent','Min','Max','EPS','P/E','Buy-Number','Buy-Volume','Buy-Price','Sale-Price','Sale-Volume','Sale-Number']
        for i in range(0,len(columns)):
            dictionary[columns[i]]=Mylist[i][2:]
        self.Pd_Output=pd.DataFrame(dictionary)
        self.Time_long=time.time()-start_time




