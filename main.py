import csv
import requests
from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib import dates as mpldates
import numpy as np

timelst, timeindex, bidenchances, trumpchances, votesharetrump, trump_lo, trump_hi, votesharebiden, biden_lo, biden_hi, biden_ev, biden_ev_hi, \
biden_ev_lo, trump_ev, trump_ev_hi, trump_ev_lo = [[] for x in range(16)]

with requests.Session() as s:
    dwl_csv = s.get('https://projects.fivethirtyeight.com/2020-general-data/presidential_national_toplines_2020.csv')
    dwl_csv = dwl_csv.content.decode('utf-8').splitlines()
    csv_dr = csv.DictReader(dwl_csv)
    for row in csv_dr:
        time = datetime.strptime(row['modeldate'], '%m/%d/%Y')
        timeindex.append(row['modeldate'])
        timelst.append(time)
        bidenchances.append(float(row['ecwin_chal']))
        trumpchances.append(float(row['ecwin_inc']))
        votesharebiden.append(float(row['national_voteshare_chal']))
        biden_lo.append(float(row['national_voteshare_chal_lo']))
        biden_hi.append(float(row['national_voteshare_chal_hi']))
        votesharetrump.append(float(row['national_voteshare_inc']))
        trump_lo.append(float(row['national_voteshare_inc_lo']))
        trump_hi.append(float(row['national_voteshare_inc_hi']))
        biden_ev.append(float(row['ev_chal']))
        biden_ev_lo.append(float(row['ev_chal_lo']))
        biden_ev_hi.append(float(row['ev_chal_hi']))
        trump_ev.append(float(row['ev_inc']))
        trump_ev_lo.append(float(row['ev_inc_lo']))
        trump_ev_hi.append(float(row['ev_inc_hi']))

myFmt = mpldates.DateFormatter('%d/%m')
timelst = mpldates.date2num(timelst)
last_day_recorded = mpldates.num2date(timelst[0]).strftime('%d-%m')


# plt.style.use('fivethirtyeight')
colorbiden = 'blue'
colortrump = 'orange'
columnwidth = 0.5
alpha_mor = 0.4
alpha_fil = 0.1

bidenline1 = {'linestyle': 'solid', 'marker': None, 'color': colorbiden}
bidenline2 = {'linestyle': 'solid', 'marker': None, 'color': colorbiden, 'alpha': alpha_mor}
trumpline1 = {'linestyle': 'solid', 'marker': None, 'color': colortrump}
trumpline2 = {'linestyle': 'solid', 'marker': None, 'color': colortrump, 'alpha': alpha_mor}

fig = plt.figure()
ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,3)
ax3 = fig.add_subplot(2,2,(2,4))
ax1.set_title('Popular votes (%) \nElector votes (total)', loc='left')
ax1.plot_date(timelst, votesharebiden, **bidenline1)
ax1.plot_date(timelst, votesharetrump, **trumpline1)
ax1.plot_date(timelst, biden_lo, **bidenline2)
ax1.plot_date(timelst, trump_lo, **trumpline2)
ax1.plot_date(timelst, biden_hi, **bidenline2)
ax1.plot_date(timelst, trump_hi, **trumpline2)
ax1.fill_between(timelst, biden_hi, biden_lo, color=colorbiden, alpha=alpha_fil)
ax1.fill_between(timelst, trump_hi, trump_lo, color=colortrump, alpha=alpha_fil)
ax1.minorticks_on()
ax1.grid(axis='y', linewidth=0.7, which='major')
ax1.grid(axis='y', linewidth=0.3, which='minor')
plt.gcf().autofmt_xdate()
ax1.axis(ymin=min(biden_lo+trump_lo)*0.9, ymax=max(biden_hi+trump_hi)*1.1)
ax1.legend(['Biden', 'Trump', 'margin of error', 'margin of error'], loc=2)
ax2.plot_date(timelst, biden_ev, **bidenline1)
ax2.plot_date(timelst, biden_ev_lo, **bidenline2)
ax2.plot_date(timelst, biden_ev_hi, **bidenline2)
ax2.plot_date(timelst, trump_ev, **trumpline1)
ax2.plot_date(timelst, trump_ev_lo, **trumpline2)
ax2.plot_date(timelst, trump_ev_hi, **trumpline2)
ax2.fill_between(timelst, biden_ev_hi, biden_ev_lo, color=colorbiden, alpha=alpha_fil)
ax2.fill_between(timelst, trump_ev_hi, trump_ev_lo, color=colortrump, alpha=alpha_fil)
ax2.minorticks_on()
ax2.grid(axis='y', linewidth=0.7, which='major')
ax2.grid(axis='y', linewidth=0.3, which='minor')
plt.gcf().autofmt_xdate()
ax2.axis(ymin=min(biden_ev_lo+trump_ev_lo)*0.9, ymax=max(biden_ev_hi+trump_ev_hi)*1.1)
ax2.xaxis.set_major_formatter(myFmt)
ax3.set_title('Chances of winning', loc='left')
ax3.plot_date(timelst, bidenchances, **bidenline1)
ax3.plot_date(timelst, trumpchances, **trumpline1)
ax3.minorticks_on()
ax3.grid(axis='y', linewidth=0.7, which='major')
ax3.grid(axis='y', linewidth=0.3, which='minor')
ax3.axis(ymin=0, ymax=1)
ax3.xaxis.set_major_formatter(myFmt)
# ax3.text(timelst[0], 0.5, f'last day recorded = {last_day_recorded}')
plt.xticks(np.arange(min(timelst), max(timelst)+1, 7))
ax3.legend(['Biden', 'Trump'], loc=2)
plt.subplots_adjust(hspace=0)
plt.gcf().autofmt_xdate()
mng = plt.get_current_fig_manager()
plt.show()




# plt.tight_layout()


# plt.xlabel(timeindex)
# plt.tight_layout()

# print(timeindex)
# print(bidenchances)
# print(votesharebiden)

# date_format = mpldates.DateFormatter('%d-%m')
# ax1.gca().xaxis.set_major_formatter(date_format)
