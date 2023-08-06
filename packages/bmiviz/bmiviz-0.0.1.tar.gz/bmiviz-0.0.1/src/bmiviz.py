import subprocess as sp
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import sys

filename='NCD_RisC_Lancet_2017_BMI_age_standardised_country.csv'

if not os.path.isfile(filename):
    #sp.call('wget https://ncdrisc.org/downloads/bmi/adult_country/'+filename, shell=True)
    sp.call('wget https://ncdrisc.org/downloads/bmi/'+filename, shell=True)
else:
    #print('csv file ('+filename+') already exists.')
    print('csv file already exists.')

df=pd.read_csv(filename, encoding = "shift-jis")
#print(df)
c_list = df.drop_duplicates(subset=['Country/Region/World'])['Country/Region/World'].values.tolist()
#print(c_list)
#print(type(c_list))

if len(sys.argv) >= 3:
    print('too many arguments.')
    sys.exit()
elif (len(sys.argv) == 1) or (sys.argv[1] not in c_list):
    print('country name must be chosen from the list')
    print(c_list)
    print(str(len(c_list)) + ' countries')
    sys.exit()
else:
    country = sys.argv[1]

#filename='NCD_RisC_Lancet_2017_BMI_age_standardised_'+country+'.csv'

dfc=df[df['Country/Region/World']==country]
#print(dfc)
dfc=dfc.filter(items=['Country/Region/World','Sex','Year', 'Mean BMI',
    'Mean BMI lower 95%% uncertainty interval',
    'Mean BMI upper 95%% uncertainty interval',
    'Prevalence of BMI>=30 kg/mｲ (obesity)',
    'Prevalence of BMI<18.5 kg/mｲ (underweight)',
    'Prevalence of BMI 18.5 kg/mｲ to <20 kg/mｲ',
    'Prevalence of BMI 20 kg/mｲ to <25 kg/mｲ',
    'Prevalence of BMI 25 kg/mｲ to <30 kg/mｲ',
    'Prevalence of BMI 30 kg/mｲ to <35 kg/mｲ',
    'Prevalence of BMI 35 kg/mｲ to <40 kg/mｲ',
    'Prevalence of BMI >=40 kg/mｲ(morbid obesity)'
    ])
#print(dfc)
dfc=dfc.rename(columns={'Country/Region/World':'Country',
    'Mean BMI lower 95%% uncertainty interval':'lower 95 %%',
    'Mean BMI upper 95%% uncertainty interval':'upper 95 %%',
    'Prevalence of BMI>=30 kg/mｲ (obesity)':'30-- (obesity)',
    'Prevalence of BMI<18.5 kg/mｲ (underweight)': '--18.5 (underweight)', 
    'Prevalence of BMI 18.5 kg/mｲ to <20 kg/mｲ': '18.5--20',
    'Prevalence of BMI 20 kg/mｲ to <25 kg/mｲ':'20--25',
    'Prevalence of BMI 25 kg/mｲ to <30 kg/mｲ':'25--30',
    'Prevalence of BMI 30 kg/mｲ to <35 kg/mｲ':'30--35 (obesity)',
    'Prevalence of BMI 35 kg/mｲ to <40 kg/mｲ':'35--40 (severe obesity)',
    'Prevalence of BMI >=40 kg/mｲ(morbid obesity)':'40-- (morbid obesity)'
    })
#print(dfc)

maxy=max(dfc['Year'])
miny=min(dfc['Year'])
print(maxy,miny)

dfcm=dfc[dfc['Sex']=='Men']
dfcw=dfc[dfc['Sex']=='Women']
print(dfcm)
print(dfcw)

fig, ax = plt.subplots(2,1)
## 折れ線グラフを作る ##
ax[0].set_title('Mean BMI by Year (upside), BMI Distribution in '+str(maxy)+' (downside)')
#ax[0].xlabel('year')
#ax[0].ylabel('Mean BMI')
ax[0].plot(dfcm['Year'],dfcm['Mean BMI'], 'b-')
ax[0].plot(dfcw['Year'],dfcw['Mean BMI'], 'r-')
bp1 = mpatches.Patch(color='Blue', label=country+' (Men)')
rp1 = mpatches.Patch(color='red', label=country+' (Women)')
ax[0].legend(handles=[bp1, rp1])

## making horizontal bar chart ##
c_names = ['--18.5 (underweight)', '18.5--20', '20--25', '25--30', '30--35 (obesity)', '35--40 (severe obesity)', '40-- (morbid obesity)']

for cname in c_names:
    dfcm[cname]=dfcm[cname]*100
    dfcm[cname] = dfcm[cname].round(1)
    dfcw[cname]=dfcw[cname]*100
    dfcw[cname] = dfcw[cname].round(1)
print(dfcm)

linem = dfcm.query('Year == '+str(maxy)).index[0]
linew = dfcw.query('Year == '+str(maxy)).index[0]
results = {
    country+' (M)':[dfcm.loc[linem, cn] for cn in c_names],
    country+' (W)':[dfcw.loc[linew, cn] for cn in c_names]}
print(results)
#fig, ax[1] = survey(results, c_names)

labels = list(results.keys())
data = np.array(list(results.values()))
data_cum = data.cumsum(axis=1)
category_colors = plt.colormaps['RdYlGn'](np.linspace(0.15, 0.85, data.shape[1]))

#fig, ax = plt.subplots(figsize=(9.2, 5))
ax[1].invert_yaxis()
ax[1].xaxis.set_visible(False)
ax[1].set_xlim(0, np.sum(data, axis=1).max())

for i, (colname, color) in enumerate(zip(c_names, category_colors)):
    widths = data[:, i]
    starts = data_cum[:, i] - widths
    rects = ax[1].barh(labels, widths, left=starts, height=0.5,
                    label=colname, color=color)

    r, g, b, _ = color
    text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
    ax[1].bar_label(rects, label_type='center', color=text_color)
ax[1].legend(ncol=len(c_names), bbox_to_anchor=(0, 1),
            loc='lower left', fontsize='small')
ax[1].set_title(' ')

fig.savefig(country +".png")
plt.show()

