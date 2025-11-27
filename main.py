import pandas as pd
import numpy as np

url = 'https://s3-eu-west-1.amazonaws.com/shanebucket/downloads/uk-500.csv'
df_origin = pd.read_csv(url)

#1. Імпорт та первинне дослідження
# print(df.head())
# print(df.info())
# print(df.describe())
# df.isna().sum()
# print(df.duplicated().sum())

#2. Очищення даних
COLUMNS_TO_DROP = []
df = df_origin.copy([col for col in COLUMNS_TO_DROP if col in df.columns])
if COLUMNS_TO_DROP:
    df = df.drop()
df["email"] = df['email'].str.strip().str.lower()
df["web"] = df['web'].str.strip().str.lower()
####################
def clean_phone(x):
    if pd.isna(x):
        return np.nan
    s = str(x)
    s = s.strip()
    plus = ''
    plus = "+" if s.startswith("+") else ""
    digits = "".join(ch for ch in s if ch.isdigit())
    if digits == "":
       return np.nan
    return plus + digits
####################
df['phone1'] = df['phone1'].astype(str).str.replace(r'\D+', '', regex=True)
df['phone2'] = df['phone2'].astype(str).str.replace(r'\D+', '', regex=True)
# .astype(str) - Перетворює кожне значення в колонці на строку (текст).Цей крок гарантує, що колонка точно текстова.
# .str - Це "строковий аксесор" pandas.
# \D означає «не-цифра»
# + означає «один або більше разів»
# '' — заміни їх на нічого (видали)
# regex=True - шукай по патерну, а не по буквальному тексту
# r'' raw string = сирий рядок."\n" — це новий рядок r"\n" — це буквально символи \ і n
# df['phone'] = df['phone'].astype(str).str.strip().str.replace("(","").str.replace(")","").str.replace(" ","").str.replace("-","").str.replace("+","").str.replace(".","") #мій варіант

# str.replace() — для рядкових операцій поелементно
# Series.replace() — для заміни конкретних значень у всій колонці
cols_to_standart = ["first_name","last_name", "city",'county']
for col in cols_to_standart:
    df[col] = df[col].astype(str).str.strip().str.title()
df['company_name'] = df['company_name'].astype(str).str.strip()
df['postal'].astype(str).str.strip()
df['email'] = df['email'].astype(str).str.lower().str.strip()
df['email'] = df['email'].astype(str).str.strip()
df['address'] = df['address'].astype(str).str.title().str.replace(r'\s+', ' ', regex=True)
def standartize_text(s):
    if pd.isna(s):
        return np.nan
    if not isinstance(s,str):
        s = str(s)
        s = (' ').join(s.split())
    return s
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].apply(standartize_text)

# Дивимось, чи є у нас назви колонок, які нам потрібні. Досліджуємо, які є
possible_email_col = [c for c in df.columns if 'email' in c.lower()]
possible_web_col = [c for c in df.columns if ('web' in c.lower()) or ('url' in c.lower())]
possible_phone_col = [c for c in df.columns if 'phone' in c.lower()]
for col in possible_phone_col:
   df[col].apply(clean_phone)
# print(possible_email_col)
# print(possible_web_col)
# print(possible_phone_col)
for col in possible_email_col:
    df[col] = df[col].str.lower()
for col in possible_web_col:
    df[col] = df[col].str.lower()
for col in possible_phone_col:
    df[col] = df[col].str.lower()


### **3. Створення нових колонок (Feature Engineering)**
df['full_name'] = df['first_name'] + " " + df['last_name']
# print(df['address'])
df['email_domain'] = df['email'].astype(str).str.split("@").str[-1]
# print(df['email_domain'])
df['city_length'] = df['city'].astype(str).str.len()
# print(df['city_length'])
df['is_gmail'] = df['email'].astype(str).str.contains('gmail.com')
# print(df_origin['is_gmail'])

### **4. Фільтрація даних**
gmail_users = df.loc[df['is_gmail'] == True]
# print(df.describe(include=[object]).T)
llc_ltd_users = df.loc[(df['company_name'].str.contains('Ltd')) | (df['company_name'].str.contains('LLC'))]
# print(llc_ltd_users)
london_users = df.loc[df['city'] == 'London']
complex_name_comps = df.loc[df['company_name'].str.split().str.len() >=4]
# print(complex_name_comps)

### **5. Позиційна вибірка (iloc)**
subset = df.iloc[0:11, 2:6]
# print(subset)
every_tenth = df.iloc[::10]
# print(every_tenth)
random_five = df.sample(5)
# random_five = df.sample(5, random_state=42)-фіксуємо цю вибірку
# print(random_five)

### **6. Групування та статистика**
top_cities = df['city'].value_counts()
# print(df.groupby("city")["full_name"].count())
agg_by_sity = df.groupby('city').agg(
    people_count = ('first_name', 'count'),
    uniq_dom = ('email_domain','nunique')).sort_values('people_count', ascending=False).head(10)
# print(agg_by_sity)
top_domains = df['email_domain'].value_counts()
# print(df['email_domain'].value_counts())
# df['email_domain'].value_counts() повертає Series, де індекс — це унікальні значення колонки email_domain, а значення — скільки разів кожне зустрічається.
# quantity = df['email_domain'].value_counts()
# uniquie_domains = []
# for domain,num in quantity.items():
#     if num == 1:
#        uniquie_domains.append(domain)
# print(len(uniquie_domains))

### **7. Експорт результатів**
df.to_csv("uk500_clean.csv",index=True)
gmail_users.to_csv("gmail_users.csv",index=True)
with pd.ExcelWriter("stats.xlsx") as writer:
    top_cities.to_excel(writer, sheet_name="Top Cities")
    top_domains.to_excel(writer, sheet_name="Top Domains")