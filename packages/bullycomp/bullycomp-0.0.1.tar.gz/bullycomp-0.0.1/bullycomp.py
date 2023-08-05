
import pandas as pd
import numpy as np
import sys
from time import sleep
import subprocess as sp

sp.call("wget https://raw.githubusercontent.com/DaichiKitazawa/bully/main/kisode-ta_tokyo.csv",shell=True)
sp.call("cat kisode-ta_tokyo.csv",shell=True)
data=pd.read_csv("kisode-ta_tokyo.csv", encoding="shift-jis")
data.fillna(0,inplace=True)
# data = data.rename(columns={'H２３（件）': 'H23', 'H２４（件）': 'H24', 'H２５（件）': 'H25', 'H２６（件）': 'H26', 'H２７（件）': 'H27'}, index={0:'elementary school', 2:'junior high school', 4:'high school', 6:'special needs school', 8:'total'})
# data = data.drop('年度', axis=1)
# data.drop([1, 3, 5, 7, 9], inplace=True)
sp.call("rm kisode-ta_tokyo.csv",shell=True)

class main():
    def main(self, year, c_year, school):
        self.year = year
        self.c_year = c_year
        self.school = school
        
        if school == 'e_school':
            school_num = 0
        elif school == 'jh_school':
            school_num = 1
        elif school == 'h_school':
            school_num = 2
        elif school == 'sn_school':
            school_num = 3
        elif school == 's_total':
            school_num = 4
            
        hikaku = data[year][school_num] - data[c_year][school_num]
        if hikaku > 0:
            print(school,'について、',year, 'は', c_year, 'よりも', hikaku, '件多いです。')
        else:
            hikaku = hikaku * -1
            print(school,'について、',year, 'は', c_year, 'よりも', hikaku, '件少ないです。')
            
if len(sys.argv)==1:
    print('知りたい年度を入力してください。')
    sys.exit()
if len(sys.argv)==2:
    if sys.argv[1] in data.columns:
        year=str(sys.argv[1])
    else:
        print('データにない年度です。')
        sys.exit()
        
if len(sys.argv)==3:
    if sys.argv[1] in data.columns:
        year=str(sys.argv[1])
        if sys.argv[2] in data.columns:
            c_year=str(sys.argv[2])
        else:
            print('データにない年度です。')
            sys.exit()
    else:
        print('データにない年度です。')
        sys.exit()

if len(sys.argv)==4:
    if sys.argv[1] in data.columns:
        year=str(sys.argv[1])
        if sys.argv[2] in data.columns:
            c_year=str(sys.argv[2])
            if sys.argv[3] in data['school'].values:
                school=str(sys.argv[3])
            else:
                print('データがありません。(学年の指定にはシングルクォーテーションを用いてください)')
                sys.exit()
        else:
            print('データにない年度です。')
            sys.exit()
    else:
        print('データにない年度です。')
        sys.exit()
m=main()  
m.main(year=year,c_year=c_year,school=school)

