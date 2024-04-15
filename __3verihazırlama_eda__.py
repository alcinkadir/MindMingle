#######################################################################################################################
#                                                                                                                     #
#                                                                                                                     #
#                                                                                                                     #
#                                                                                                                     #
#                                                                                                                     #
#                                                                                                                     #
#                                                                                                                     #
#######################################################################################################################




#######################################################################################################################
#                                                                                                                     #
#                                         VERİ DOĞRULAMA / ÖN İŞLEME                                                  #
#                             Gelişmiş Fonksiyonel Keşifçi Veri Analizi (AF-EDA)                                      #
#                                                                                                                     #
# Tüm değişkenleri sağlanan kriterlere göre doğrulamış ve gerektiğinde analize hazır                                  #
# veriler elde etmek için temizleme görevlerini yerine getirme aşaması.                                               #
# - Genel Resim                                                                                                       #
# - Kategorik Değişken Analizi (Analysis of Categorical Variables)                                                    #
# - Sayısal Değişken Analizi (Analysis of Numerical Variables)                                                        #
# - Hedef Değişken Analizi (Analysis of Target Variable)                                                              #
# - Korelasyon Analizi (Analysis of Correlation)                                                                      #
#######################################################################################################################

# - Genel Resim
from __1lib__ import *
from __2funct__ import *

pandas_ince_ayar()

df = pd.read_csv('mental_health_sampled.csv')
df.head()
#kopya oluşturma
df_ = df.copy()
df_.head()

check_df(df)

# Nümerik ve Kategorik değişken yakalanması
cat_cols, cat_but_col, num_col= grab_col_names(df)  # num_cols çıkarıldı sayısal sütün olmadığından hata veriyor.

cat_cols

# - Kategorik Değişken Analizi
for col in cat_cols:
    cat_summary(df, col)

# - Hedef Değişken Analizi
for col in cat_cols:
    grouped_df = df.groupby(["Mood_Swings", col]).size().unstack(fill_value=0)
    print(grouped_df)
    print("\n")

# - Korelasyon Analizi ve Korelasyonların gösterilmesi
df_encoded = pd.get_dummies(df[cat_cols])
corr = df_encoded.corr()

# Korelasyonların gösterilmesi
sns.set(rc={'figure.figsize': (12, 12)})
sns.heatmap(corr, cmap="RdBu")
plt.show()

df.head()
df_.head()

#######################################################################################################################
#                                                                                                                     #
#                                         VERİ GÖRSELLEŞTİRME                                                         #
#                                                                                                                     #
# En az tek değişken veya daha fazla değişken içeren  bir görselleştirme oluşturulmuştur.                             #
# (örn. kolerasyon analizi, histogram, çubuk grafik, tek kutu grafiği dağılım grafiği,                                #
# dolu çubuk grafik, çoklu kutu grafikleri)                                                                           #
# Sunulan bulguları destekleyen görselleştirmeler kullanmıştır.                                                       #
#######################################################################################################################


# Kategorik değişkenlerin dağılımı (Bar grafik)
for col in cat_cols:
    plt.figure(figsize=(10, 6))
    sns.countplot(x=col, data=df)
    plt.title(f"{col} Dağılımı")
    plt.xlabel(col)
    plt.ylabel("Frekans")
    plt.xticks(rotation=45)
    plt.show()


# Korelasyon analizi görselleştirmesi (Kategori kesişimlerini gösteren ısı haritası)
cross_tab = pd.crosstab(df[cat_cols[0]], df[cat_cols[1]])
plt.figure(figsize=(10, 6))
sns.heatmap(cross_tab, annot=True, cmap="YlGnBu")
plt.title(f"{cat_cols[0]} ve {cat_cols[1]} İlişkisi")
plt.xlabel(cat_cols[1])
plt.ylabel(cat_cols[0])
plt.show()

# Çapraz analiz görselleştirmesi (örneğin, cinsiyet ve yaş arasındaki ilişki)
plt.figure(figsize=(10, 6))
sns.countplot(x="Gender", hue="Mood_Swings", data=df)
plt.title("Cinsiyet ve Mental Dalgalanma Arasındaki İlişki")
plt.xlabel("Cinsiyet")
plt.ylabel("Frekans")
plt.show()

#######################################################################################################################
#                                                                                                                     #
#                                         ÖZELLİK MÜHENDİSLİĞİ                                                        #
#                                                                                                                     #
#  Yeni değişkenler türetildi. Özellikleri belirlendi ve Önemli noktalar dahilinde değişkenler üzerinden çalışmalar   #
#  gerçekleştirildi.                                                                                                  #
#                                                                                                                     #
#######################################################################################################################

#Growing_Stress ve Changes_Habits arasındaki etkileşim.
def create_stress_response_feature(row):
    if row['Growing_Stress'] == 'Yes' and row['Changes_Habits'] in ['Yes', 'Maybe']:
        return 'High'
    elif row['Growing_Stress'] == 'Maybe' or row['Changes_Habits'] == 'Maybe':
        return 'Medium'
    else:
        return 'Low'

df['Stress_Response'] = df.apply(create_stress_response_feature, axis=1)



#Stres ve Serbest Meslek Etkileşimi:
def growing_stress_self_employed_interaction(row):
    if row['Growing_Stress'] == 'Yes' and row['self_employed'] in ['Yes', 'No']:
        return 'YSDZS'
    elif row['Growing_Stress'] == 'No' and row['self_employed'] in ['Yes', 'No']:
        return 'DSYZS'
    else:
        return 'Other'


df['Stress_Employed'] = df.apply(growing_stress_self_employed_interaction, axis=1)


# Sosyal zayıflık ile Başa çıkma mücadeleleri etkileşimi
def create_social_coping_interaction(row):
    if row['Social_Weakness'] == 'Yes' and row['Coping_Struggles'] == 'Yes':
        return 'Çift Yük'
    elif row['Social_Weakness'] == 'Yes':
        return 'Sosyallik Zayıf'
    elif row['Coping_Struggles'] == 'Yes':
        return 'Mücadele Eden'
    else:
        return 'Normal'


df['Social_Coping_Interaction'] = df.apply(create_social_coping_interaction, axis=1)



#Stres ve Çalışma İlgisi Etkileşimi
def create_stress_work_interaction(row):
    if row['Growing_Stress'] == 'Yes' and row['Work_Interest'] == 'Yes':
        return 'High_Stress_High_Interest'
    elif row['Growing_Stress'] == 'Yes' and row['Work_Interest'] == 'No':
        return 'High_Stress_Low_Interest'
    elif row['Growing_Stress'] == 'No' and row['Work_Interest'] == 'Yes':
        return 'Low_Stress_High_Interest'
    else:
        return 'Low_Stress_Low_Interest'

df['Stress_Work_Interaction'] = df.apply(create_stress_work_interaction, axis=1)


#  Meslek Gruplarına Göre Yeni Değişken
def group_occupation(row):
    if row['Occupation'] in ['Corporate', 'Business']:
        return 'Professional'
    elif row['Occupation'] == 'Student':
        return 'Student'
    else:
        return 'Other'

df['Occupation_Group'] = df.apply(group_occupation, axis=1)

#  Days_Indoors Değişkenini Kategorilere Ayırma
def categorize_days_indoors(value):
    if value == 'Go out Every day':
        return 'None'
    elif value == '15-30 days':
        return 'Medium'
    elif value == '31-60 days':
        return 'High'
    else:
        return 'Very High'

df['Indoor_Duration'] = df['Days_Indoors'].apply(categorize_days_indoors)

# Segmentasyon analizi yapalım
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Social_Weakness', y='Stress_Response', hue='Coping_Struggles', data=df, palette='viridis')
plt.title('Sosyal Zayıflık ve Stres Yanıtı İlişkisi')
plt.xlabel('Sosyal Zayıflık')
plt.ylabel('Stres Yanıtı')
plt.legend(title='Başa Çıkma Mücadelesi', loc='upper right')
plt.show()

# Zaman Serisi Analizi, eğilimleri ve desenleri belirleyelim. Gün İçinde Kapalı Alanlarda Geçirilen Zaman
plt.figure(figsize=(10, 6))
sns.lineplot(x='Days_Indoors', y='Stress_Response', data=df, ci=None)
plt.title('Gün İçinde Kapalı Alanlarda Geçirilen Zamanın Stres Yanıtı Üzerindeki Etkisi')
plt.xlabel('Gün İçinde Kapalı Alanlarda Geçirilen Zaman')
plt.ylabel('Stres Yanıtı')
plt.show()

df.head()
df.shape
check_df(df)