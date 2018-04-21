
# coding: utf-8

# ### Ülkelere ilişkin kişi başı gayri safi yurt içi hasıla verilerini alın:
# Birleşmiş Milletler İnsani Gelişmişlik Raporları (Human Deveoplemen Reports) sitesinde, farklı boyutlar altında çeşitli göstergeleri içeren, ülkelerin 1990-2015 yılları arasındaki İnsani Gelişmişlik Verileri (http://hdr.undp.org/en/data) bulunmaktadır. Bu verilerden "Income/composition of resources" boyutu altında yer alan, "Gross domestic product (GDP) per capita" (kişi başı gayri safi yurt içi hasıla) göstergesine ilişkin verileri indirin ("Gross domestic product (GDP) per capita (2011 PPP $).csv"). Bu dosyadan verileri yükleyin ve bir DataFrame oluşturun.
# 
# ### Veri Temizleme&Düzenleme:
# ```
# 1- Kodlamayı, ISO-8859-1 olarak ayarlayın (read_csv fonksiyonu içindeki encoding parametresi ile)
# 2- Dosyanın ilk satırını atlayın
# 3- Son satırı silin
# 4- Boş sütunları (bütün değerleri 'NaN' olan sütunları) silin
# 5- Herhangi bir verisi boş ('NaN') olan ülkeleri silin
# 6- Country sütununda bulunan değerlerin sonundaki ekstra boşlukları silin
# 7- Country sütunundaki ülke isimlerinin bazılarını aşağıdaki şekilde yeniden adlandırın:
#     'Korea (Republic of)':'South Korea',
#     'Venezuela (Bolivarian Republic of)':'Venezuela',
#     'The former Yugoslav Republic of Macedonia':'Macedonia',
#     'Hong Kong, China (SAR)':'Hong Kong'
# ```

# In[127]:


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
gdp = pd.read_csv('gdp.csv', 'encoding=ISO-8859-1',skiprows=1,engine='python',delimiter=',')
gdp = gdp[:-1]
#gdp


# In[128]:


gdp = gdp.dropna(axis=1,how='all')
gdp = gdp.dropna(axis=0,how='any')
gdp


# In[129]:


print(len(gdp.iloc[1].Country))
#gdp['Country'] = gdp['Country'].str.strip()
gdp.Country = gdp.Country.apply(lambda text: text.strip())
print(len(gdp.iloc[1].Country))


# In[130]:


print(gdp.loc[180].Country)
mapping = {'Korea (Republic of)':'South Korea',
    'Venezuela (Bolivarian Republic of)':'Venezuela',
    'The former Yugoslav Republic of Macedonia':'Macedonia',
    'Hong Kong, China (SAR)':'Hong Kong'}
gdp.Country.replace(mapping,inplace=True)
print(gdp.loc[180].Country)


# ### Ülkelere ilişkin coğrafi verileri alın:
# Geonames veri tabanından ülkelere ilişkin coğrafi verileri içeren dosyadan (http://download.geonames.org/export/dump/countryInfo.txt) verileri yükleyin ve başka bir DataFrame daha oluşturun.
# 
# ### Veri Temizleme&Düzenleme:
# ```
# 1- Dosyanın ilk 50 satırını atlayın
# 2- Son satırı silin
# 3- '#ISO' sütununun ismini 'CountryCode' olarak değiştirin
# 4- 'ISO3', 'ISO-Numeric', 'fips', 'EquivalentFipsCode', 'Postal Code Format', 'Postal Code Regex' ve 'geonameid' sütunlarını silin
# 5- Kıta (Continent) değeri boş ('NaN') olan ülkelerin kıta değerini 'NA' (North America) olarak değiştirin
# ```

# In[131]:


data = pd.read_csv('countryInfo.txt', skiprows=50,sep="\t")
data = data[:-1]
data


# In[132]:


mapping = {'#ISO':"CountryCode"}
data.rename(columns=mapping,inplace=True)
data.head()


# In[133]:


toRemove = ['ISO3', 'ISO-Numeric', 'fips', 'EquivalentFipsCode', 'Postal Code Format', 'Postal Code Regex' , 'geonameid']
data.drop(toRemove, inplace=True, axis=1)
data


# In[134]:


print(data.Continent.isnull().sum())
data.Continent = data.Continent.fillna(value="NA")
print(data.Continent.isnull().sum())
data.head()


# ### Verilerinizi birleştirin:
# Ülke adı ('Country') sütunlarının kesişimini kullanarak bu iki veri kümesini birleştirin ve 'Country' sütununu index olarak beirleyin.

# In[135]:


merged = pd.merge(data,gdp,on='Country',how='inner')
merged.set_index(merged['Country'],inplace =True)
merged


# 
# Ülkelerin, 1990-2015 yıllarını kapsayan 'GDP ortalama' değerlerini bulun ve veri setine yeni bir sütun olarak ekleyin.

# In[136]:


years = ['1990', '1995', '2000', '2005', '2010', '2011', '2012', '2013', '2014', '2015']
merged['GDP_ortalama'] = merged[years].mean(axis=1)
merged


# Ülkelerin GDP ortalamalarını gösteren bir histogram (hist) çizin.

# In[137]:


merged.GDP_ortalama.hist()


# GDP ortalaması en yüksek ilk 10 ülkeyi gösteren bir sütun (bar) grafik çizin.

# In[138]:


merged.GDP_ortalama.sort_values(ascending=False).head(10).plot(kind='bar')


# 
# Her ülkenin kişi başına düşen yüzey alanını hesaplayınız ve kişi başına düşen yüzey alanı en küçük olan ilk 20 ülkeyi gösteren bir sütun grafik çizin.

# In[139]:


merged['KBDYA'] = merged['Area(in sq km)'] /merged['Population']
merged.KBDYA.sort_values().head(20).plot(kind='bar')


# 
# Kıtalara göre 'GDP ortalama' değerlerini gösteren bir sütun grafik çizin.

# In[140]:


merged.groupby('Continent').GDP_ortalama.mean().plot(kind='bar')


# Kıtalara göre toplam nüfus ve toplam alan dağılımlarını gösteren pasta (pie) grafikleri içeren bir şekil (figure) çizin. 

# In[141]:


fig = plt.figure(figsize=(15,15))
p1 = fig.add_subplot(2,2,1)
merged.groupby('Continent').Population.sum().plot(kind='pie')
p2 = fig.add_subplot(2,2,2)
merged.groupby('Continent')["Area(in sq km)"].sum().plot(kind='pie')
plt.show()


# 
# Veri setinden Türkiye'nin komşularını bulun, bu ülkelerin ve Türkiye'nin GDP ortalamalarını gösteren bir sütun grafik çizin.

# In[142]:


neighbours = merged.loc['Turkey'].neighbours.split(',')
neighbours.append('TR')
merged.loc[merged['CountryCode'].isin(neighbours)].GDP_ortalama.plot(kind='bar')


#  
# Her ülke için o ülkenin komşu ülkelerinin ortalama GDP değerlerinin ortalamasını hesaplayarak yeni bir seri oluşturunuz (eğer bir ülkenin komuşusu yoksa kendi GDP ortalamasını alınız) ve komşuları ile en fazla ortalama GDP farkı olan ilk 20 ülkeyi listeleyin.

# In[143]:


NeighboursGDP = pd.Series()
for country, row in merged.iterrows():
    if pd.isnull(row.neighbours):
        neighbourss = [row.CountryCode]
    else :
        neighbourss = row.neighbours.split(',')
        #NeighboursGDP[country] = neighbourss
    avg = merged.loc[merged['CountryCode'].isin(neighbourss)].GDP_ortalama.mean()
    if np.isnan(avg):
        NeighboursGDP[country] =row.GDP_ortalama
    else:
        NeighboursGDP[country] = avg
NeighboursGDP


# In[144]:


GDPDiff = pd.Series()
for country,row in merged.iterrows():
    diff = row.GDP_ortalama - NeighboursGDP[country]
    diff = round(diff, 1)
    GDPDiff[country] = [abs(diff),'+'] if diff >0 else [abs(diff),'-']
GDPDiff


# In[145]:


GDPDiff.sort_values(ascending=False).head(20)


# 
# Ülkelerin yüzey ölçümü ile nüfusları arasındaki ilişkiyi gösteren bir dağılım (scatter) grafiği çizin. Baloncuklara ülke isimlerini ekleyin.

# In[146]:


ax = merged.plot(x='Area(in sq km)',y='Population', kind='scatter',s=2000,alpha=0.75, figsize=[16,6])
for i, txt in enumerate(merged.index):
    ax.annotate(txt, [merged['Area(in sq km)'][i], merged['Population'][i]], ha='center')


# 
# İnsani gelişmişlik indeksi en yüksek 20 ülkenin, insani gelişmişlik indeksi ile ortalama GDP değerleri arasındaki ilişkiyi gösteren bir dağılım (scatter) grafiği çizin. Baloncukların büyüklüklerini, ortalama GDP değeriyle orantılayın. Baloncuklara ülke isimlerini ekleyin. Baloncukları kıtalara göre renklendirin.

# In[147]:


merged['HDI Rank (2015)']=pd.to_numeric(merged['HDI Rank (2015)'])
top20 = merged.sort_values(by=['HDI Rank (2015)']).head(20)
top20


# In[148]:


colors = np.where(top20.Continent=='AS','r','b')
colors = np.where(top20.Continent=='NA','g',colors)
colors = np.where(top20.Continent=='EU','y',colors)
colors = np.where(top20.Continent=='SA','c',colors)
colors = np.where(top20.Continent=='OC','m',colors)
colors = np.where(top20.Continent=='AF','k',colors)
colors


# In[149]:


ax = top20.plot(x='HDI Rank (2015)',y='GDP_ortalama',s=top20['GDP_ortalama']/15, kind='scatter',alpha=0.75, figsize=[16,10],c=colors)
for i, txt in enumerate(top20.index):
    ax.annotate(txt, [top20['HDI Rank (2015)'][i], top20['GDP_ortalama'][i]], ha='center')


# 
# 1990 yılı ile 2015 yılı arasındaki GDP değeri değişimi en yüksek olan 15 ülkenin (1) 1990 ve 2015 GDP değerlerini, (2) fark  değerlerini gösteren sütun grafiklerini içeren bir şekil (figure) çizin.

# In[150]:


top15 = pd.Series()
for country, row in merged.iterrows():
    top15[country] = abs(row['2015'] - row['1990'])
top15 = top15.sort_values(ascending=False).head(15)
#top15.plot(kind='bar')


# In[151]:


raw_data = {'Country': merged['Country'],
        '1990': merged['1990'],
        '2015': merged['2015']}
ndf= pd.DataFrame(raw_data, columns = ['Country','1990', '2015'])
ndf15 = ndf[ndf.Country.isin(top15.index)]
#ndf15.plot(kind='bar')


# In[152]:


fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16,6))

ndf15.plot(ax=axes[0],kind='bar')
top15.plot(ax=axes[1],kind='bar')


# 
# Güney Amerika ('SA') ülkelerinin 1990'dan 2015'e kadar olan GDP değişimlerini yıllara göre gösteren bir çizgi (line) grafik çizin.  

# In[153]:


SA = merged[merged['Continent'] == 'SA']
SA = SA.drop(SA.columns[0:13], axis=1)
SAD = SA.drop(SA.columns[10:12], axis=1)
for index, row in SAD.iterrows():
    plt.plot(row, linewidth=3)


# In[154]:


SAD = SAD.transpose()
SAD


# In[155]:


SAD.plot(figsize=(16,6))
plt.show()


# 
# Dünya'da en çok sayıda ülkede konuşulan ilk 10 dili (bir dilin ülkelere göre yerelleşmiş türlerini, aynı dil olarak kabul edin) ve konuşuldukları ülke sayılarını gösteren bir sütun grafik çizin.

# In[156]:


merged.Languages


# In[157]:


LangFreq = {}
for country, row in merged.iterrows():
    langs = row.Languages.split(',')
    editedLangs=[]
    for item in langs:
        if "-"  in item: 
            newItem = item.split('-')
            editedLangs.append(newItem[0])
        else:
            editedLangs.append(item)
    for lang in editedLangs:
        if lang not in LangFreq:
             LangFreq[lang] = 1
        else:
            LangFreq[lang] += 1
LangFreq


# In[158]:


LangFreqD = pd.DataFrame( LangFreq, index=["Counts"] )
LangFreqD


# In[159]:


temp = LangFreqD.transpose()
top10 = temp.sort_values(by='Counts',ascending=False).head(10)
top10


# In[160]:


ax = top10.plot(kind='bar',figsize=(16,6))
for p in ax.patches: 
    ax.annotate(np.round(p.get_height(),decimals=2), (p.get_x()+p.get_width()/2., p.get_height()), ha='center', va='center', xytext=(0, 5), textcoords='offset points')

