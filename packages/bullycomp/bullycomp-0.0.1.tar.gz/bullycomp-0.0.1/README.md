# bully
bullycompはkisode-ta_tokyo.csvを使って各都市のいじめ件数の認知度を比較する簡単なPythonプログラムです。

# kisode-ta_tokyo
bullycomp は 件数を比較するために kisode-ta_tokyo.csv を必要とします。

# how to install
$ pip install bully_comparsion

# how to run bully_comparsion
"year" には知りたい年度を入れます。
ex)H23,H24,H25...
"c_year" には比較したい年度を入れます。
ex)H23,H24,H25...
"school" には対象となる学年を入れます。
ex)e_school,jh_school,h_school...
$ bullycomp year c_year school
→
$ bullycomp H23 H24 h_school
year="H23",c_year="H24", school="h_school"

$ bullycomp H26 H23 sn_school
year="H26",c_year="H23", school="jh_school"
