import requests,re
import pandas as pd
import matplotlib.pyplot as plt
import os

def main():
    url='https://www.worldometers.info/world-population/population-by-country/'
#    print('scraping population...')
    page=requests.get(url)
    df = pd.read_html(page.text)[0]
    df.columns.values[1]='Country'
    df.columns.values[2]='Population'
    df.to_csv('pop.csv')
#    print('pop.csv was created')

#    print('downloading owid-co2-data.csv file')
    import subprocess as sp
    if(os.path.isfile('owid-co2-data.csv')):
        os.remove('owid-co2-data.csv')
#    sp.call("wget https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv",shell=True)
    p=pd.read_csv('https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv')
    year=p['year'][len(p)-1]

#    print('countries file was read...')
#    d=open('countries').read().strip()
#    print('scoring the following ',len(d),' countries...')
    country = 'Germany,Australia,Iceland,South Korea,India,Brazil,France,New Zealand,Taiwan,Sweden,Japan,United States,Canada,United Kingdom,Israel'
    d=country.split(',')
    print(d)

    dd=pd.DataFrame(
    {
      "country": d,
      "co2": range(len(d)),
      "population": range(len(d)),
      "sumco2": range(len(d)),
    })

    pp=pd.read_csv('pop.csv')
#    print('calculating scores of countries\n')
#    print('score is created in result.csv')
#    print('year is ',year)

    for i in d:
        x = p[p['country'] == i]
        h = x[x['year'] == year]
        dd.loc[dd.country==i,'co2']=float(h['co2'])
        dd.loc[dd.country==i,'population']=float(pp.loc[pp.Country==i,'Population'])
        dd.loc[dd.country==i,'sumco2']=float(dd.loc[dd.country==i,'co2']*dd.loc[dd.country==i,'population'])
      
    dd=dd.sort_values(by=['population'], ascending=False)
    dd.to_csv('result.csv',index=False)
    dd=pd.read_csv('result.csv',index_col=0)

    fig, ax1 = plt.subplots(1,1,figsize=(10,8))
    ax2 = ax1.twinx()
    ax1.bar(dd.index,dd["population"],color="lightblue",label="population")
    ax2.plot(dd["sumco2"],linestyle="solid",color="k",marker="^",label="sumco2")
    ax1.set_ylim(100000,1400000000)
    ax2.set_ylim(100000000,4000000000000)
    handler1, label1 = ax1.get_legend_handles_labels()
    handler2, label2 = ax2.get_legend_handles_labels()
    ax1.legend(handler1+handler2,label1+label2,borderaxespad=0)
    ax1.grid(True)
    ax1.set_xticklabels(dd.index, rotation=45, ha='right')
    plt.savefig("../results/results.png")
    plt.show()

if __name__ == "__main__":
  main()
