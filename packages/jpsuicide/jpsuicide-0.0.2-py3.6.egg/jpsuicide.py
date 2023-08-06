import matplotlib.pyplot as plt
import japanize_matplotlib
import sys
import pandas as pd
import tabula

# pdfを読み込み,該当ページの表をDataFrameに変換
pdf_h23 = tabula.read_pdf("https://www.npa.go.jp/safetylife/seianki/jisatsu/H23/H23_jisatunojoukyou_02.pdf", 
                    lattice=True, pages='8')
df_h23 = pd.DataFrame(pdf_h23[0])
# 都道府県名と自殺者数のみ抽出
df_h23 = df_h23.iloc[:,:2].drop(index=0)
# カラム名変更(自殺者数→データ集計年)
df_h23 = df_h23.rename(columns={'自殺者数': 2011})
# カンマ区切りの文字列を数字に変換
df_h23[2011] = df_h23[2011].str.replace(',', '').astype(int)

pdf_h24 = tabula.read_pdf("https://www.npa.go.jp/safetylife/seianki/jisatsu/H24/H24_jisatunojoukyou_02.pdf", 
                    lattice=True, pages='8')
df_h24 = pd.DataFrame(pdf_h24[0])
df_h24 = df_h24.iloc[:,:2].drop(index=0)
df_h24 = df_h24.rename(columns={'自殺者数': 2012})
df_h24[2012] = df_h24[2012].str.replace(',', '').astype(int)

pdf_h25 = tabula.read_pdf("https://www.npa.go.jp/safetylife/seianki/jisatsu/H25/H25_jisatunojoukyou_01.pdf", 
                    lattice=True, pages='12')
df_h25 = pd.DataFrame(pdf_h25[0])
df_h25 = df_h25.iloc[:,:2].drop(index=0)
df_h25 = df_h25.rename(columns={'自殺者数': 2013})
df_h25[2013] = df_h25[2013].str.replace(',', '').astype(int)

pdf_h26 = tabula.read_pdf("https://www.npa.go.jp/safetylife/seianki/jisatsu/H26/H26_jisatunojoukyou_01.pdf", 
                    lattice=True, pages='12')
df_h26 = pd.DataFrame(pdf_h26[0])
df_h26 = df_h26.iloc[:,:2].drop(index=0)
df_h26 = df_h26.rename(columns={'自殺者数': 2014})
df_h26[2014] = df_h26[2014].str.replace(',', '').astype(int)

pdf_h27 = tabula.read_pdf("https://www.npa.go.jp/safetylife/seianki/jisatsu/H27/H27_jisatunojoukyou_01.pdf", 
                    lattice=True, pages='12')
df_h27 = pd.DataFrame(pdf_h27[0])
df_h27 = df_h27.iloc[:,:2].drop(index=0)
df_h27 = df_h27.rename(columns={'自殺者数': 2015})
df_h27[2015] = df_h27[2015].str.replace(',', '').astype(int)

pdf_h28 = tabula.read_pdf("https://www.npa.go.jp/safetylife/seianki/jisatsu/H28/H28_jisatunojoukyou_01.pdf", 
                    lattice=True, pages='32')
df_h28 = pd.DataFrame(pdf_h28[0])
df_h28 = df_h28.iloc[:,:2].drop(index=0)
df_h28 = df_h28.rename(columns={'自殺者数': 2016})
df_h28[2016] = df_h28[2016].str.replace(',', '').astype(int)

pdf_h29 = tabula.read_pdf("https://www.npa.go.jp/safetylife/seianki/jisatsu/H29/H29_jisatsunojoukyou_01.pdf", 
                    lattice=True, pages='32')
df_h29 = pd.DataFrame(pdf_h29[0])
df_h29 = df_h29.iloc[:,:2].drop(index=0)
df_h29 = df_h29.rename(columns={'自殺者数': 2017})
df_h29[2017] = df_h29[2017].str.replace(',', '').astype(int)

pdf_h30 = tabula.read_pdf("https://www.npa.go.jp/safetylife/seianki/jisatsu/H30/H30_jisatunojoukyou.pdf", 
                    lattice=True, pages='31')
df_h30 = pd.DataFrame(pdf_h30[0])
df_h30 = df_h30.iloc[:,:2].drop(index=0)
df_h30 = df_h30.rename(columns={'自殺者数': 2018})
df_h30[2018] = df_h30[2018].str.replace(',', '').astype(int)

pdf_r1 = tabula.read_pdf("https://www.npa.go.jp/safetylife/seianki/jisatsu/R02/R01_jisatuno_joukyou.pdf", 
                    lattice=True, pages='30')
df_r1 = pd.DataFrame(pdf_r1[0])
df_r1 = df_r1.iloc[:,:2].drop(index=0)
df_r1 = df_r1.rename(columns={'自殺者数': 2019})
df_r1[2019] = df_r1[2019].str.replace(',', '').astype(int)

pdf_r2 = tabula.read_pdf("https://www.npa.go.jp/safetylife/seianki/jisatsu/R03/R02_jisatuno_joukyou.pdf", 
                    lattice=True, pages='30')
df_r2 = pd.DataFrame(pdf_r2[0])
df_r2 = df_r2.iloc[:,:2].drop(index=0)
df_r2 = df_r2.rename(columns={'自殺者数': 2020})
df_r2[2020] = df_r2[2020].str.replace(',', '').astype(int)

pdf_r3 = tabula.read_pdf("https://www.npa.go.jp/safetylife/seianki/jisatsu/R04/R3jisatsunojoukyou.pdf", 
                    lattice=True, pages='30')
df_r3 = pd.DataFrame(pdf_r3[0])
df_r3 = df_r3.iloc[:,:2].drop(index=0)
df_r3 = df_r3.rename(columns={'自殺者数': 2021})
df_r3[2021] = df_r3[2021].str.replace(',', '').astype(int)

## データが追加されたらアップデート
# pdf = tabula.read_pdf("xxxx", 
#                     lattice=True, pages='xx')
# df = pd.DataFrame(pdf[0])
# df = df.iloc[:,:2].drop(index=0)
# df = df.rename(columns={'自殺者数': '20xx'})
# df[20xx] = df[20xx].str.replace(',', '').astype(int)

# 各年のデータを結合
df = pd.merge(df_h23, df_h24, on='都道府県名')
df = pd.merge(df, df_h25, on='都道府県名')
df = pd.merge(df, df_h26, on='都道府県名')
df = pd.merge(df, df_h27, on='都道府県名')
df = pd.merge(df, df_h28, on='都道府県名')
df = pd.merge(df, df_h29, on='都道府県名')
df = pd.merge(df, df_h30, on='都道府県名')
df = pd.merge(df, df_r1, on='都道府県名')
df = pd.merge(df, df_r2, on='都道府県名')
df = pd.merge(df, df_r3, on='都道府県名')
# df.to_csv('sample.csv')


size=0
prefecture=[]
for i in df.都道府県名:
    prefecture.append(i)
    size=size+1

print(len(prefecture),': ',prefecture)
no=len(sys.argv)-1

# x軸用の年取得
x=[]
for i in range(2011,2022):
    x.append(i)

# 入力された都道府県のデータを格納
pft=[]
for i in range(no):
    if sys.argv[i+1] in prefecture:
        pft.append(df.loc[df.都道府県名==sys.argv[i+1]])
    else: 
        print('correct the name of ',sys.argv[i+1])

# 入力された都道府県の各年のデータを格納
prfet=[]
for j in range(len(pft)):
    for i in range(2011,2022):
        prfet.append(int(pft[j][i]))

if len(pft)==1:
    plt.plot(x,prfet,'k-',label=sys.argv[1])
if len(pft)==2:
    plt.plot(x,prfet[0:11],'k-',label=sys.argv[1])
    plt.plot(x,prfet[11:22],'k--',label=sys.argv[2])
if len(pft)==3:
    plt.plot(x,prfet[0:11],'k-',label=sys.argv[1])
    plt.plot(x,prfet[11:22],'k--',label=sys.argv[2])
    plt.plot(x,prfet[22:33],'k:',label=sys.argv[3])
if len(pft)==4:
    plt.plot(x,prfet[0:11],'k-',label=sys.argv[1])
    plt.plot(x,prfet[11:22],'k--',label=sys.argv[2])
    plt.plot(x,prfet[22:33],'k:',label=sys.argv[3])
    plt.plot(x,prfet[33:44],'k-.',label=sys.argv[4])

def main():
    plt.legend()
    plt.savefig('result.png')
    plt.show()