import subprocess as sp
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl
import sys,os
import matplotlib.animation as animation

#popunimation countryname 

def delete_rows(fromText,countryname):
	sep = ","
	prev_country=""
	with open(fromText) as oldfile,open('newfile.csv', 'w') as newfile:
		
		for line in oldfile:
			csv=line.split(sep)
			if prev_country != csv[1]:
				print("" + csv[1])
				prev_country = csv[1]
			if 'Location' in line:
				newfile.write(line)
				continue
			if countryname == csv[1]:
				newfile.write(line)


countryname=sys.argv[1]

print(countryname)

#get data
if not os.path.exists('./WPP2019_PopulationByAgeSex_Medium.csv'):
	print("downloading")
	sp.call("wget https://population.un.org/wpp/Download/Files/1_Indicators%20\(Standard\)/CSV_FILES/WPP2019_PopulationByAgeSex_Medium.csv",shell=True)

delete_rows('WPP2019_PopulationByAgeSex_Medium.csv',countryname)
data = pd.read_csv('newfile.csv')
data.to_excel('worldpopulation.xlsx')

dataframe=pd.read_excel('worldpopulation.xlsx')


ims=[]

#fig = plt.figure()

fig,ax = plt.subplots()

for year in range(1950,2101):

	year_data=dataframe.loc[dataframe.Time == int(year)]

	dataa=[]
	x=[]
	for age in year_data["AgeGrpStart"]:
		x.append(age)
	for pop in year_data["PopTotal"]:
		dataa.append(pop)

	im = ax.plot(x,dataa,"black")
	title = ax.text(0.5, 1.01, '{}:{}'.format(countryname,year),
                     ha='center', va='bottom',
                     transform=ax.transAxes, fontsize='large')
	ims.append(im + [title])

#plt.legend()
#plt.savefig("result_population.png")

ani = animation.ArtistAnimation(fig,ims,interval=200)
ani.save("animation.gif")
plt.show()
