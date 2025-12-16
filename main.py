import pandas as pd
import numpy as np

url = 'https://s3-eu-west-1.amazonaws.com/shanebucket/downloads/uk-500.csv'
df_origin = pd.read_csv(url)

#1. Import and primary research

print(df_origin.head())
print(df_origin.info())
print(df_origin.describe())
df_origin.isna().sum()
print(df_origin.duplicated().sum())

#2. Data cleaning

COLUMNS_TO_DROP = []
df = df_origin.copy([col for col in COLUMNS_TO_DROP if col in df.columns])

if COLUMNS_TO_DROP:
    df = df.drop()
df["email"] = df['email'].str.strip().str.lower()
df["web"] = df['web'].str.strip().str.lower()

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

df['phone1'] = df['phone1'].astype(str).str.replace(r'\D+', '', regex=True)
df['phone2'] = df['phone2'].astype(str).str.replace(r'\D+', '', regex=True)

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

possible_email_col = [c for c in df.columns if 'email' in c.lower()]
possible_web_col = [c for c in df.columns if ('web' in c.lower()) or ('url' in c.lower())]
possible_phone_col = [c for c in df.columns if 'phone' in c.lower()]
for col in possible_phone_col:
   df[col].apply(clean_phone)

for col in possible_email_col:
    df[col] = df[col].str.lower()
for col in possible_web_col:
    df[col] = df[col].str.lower()
for col in possible_phone_col:
    df[col] = df[col].str.lower()


# 3.Creating new columns (Feature Engineering)

df['full_name'] = df['first_name'] + " " + df['last_name']
print(df['address'])
df['email_domain'] = df['email'].astype(str).str.split("@").str[-1]
print(df['email_domain'])
df['city_length'] = df['city'].astype(str).str.len()
print(df['city_length'])
df['is_gmail'] = df['email'].astype(str).str.contains('gmail.com')
print(df_origin['is_gmail'])

# 4. Data filtering

gmail_users = df.loc[df['is_gmail'] == True]
print(df.describe(include=[object]).T)
llc_ltd_users = df.loc[(df['company_name'].str.contains('Ltd')) | (df['company_name'].str.contains('LLC'))]
print(llc_ltd_users)
london_users = df.loc[df['city'] == 'London']
complex_name_comps = df.loc[df['company_name'].str.split().str.len() >=4]
print(complex_name_comps)

# 5. Positional sampling(iloc)

subset = df.iloc[0:11, 2:6]
print(subset)
every_tenth = df.iloc[::10]
print(every_tenth)
random_five = df.sample(5)


# 6. Grouping and statistics

top_cities = df['city'].value_counts()
print(df.groupby("city")["full_name"].count())
agg_by_sity = df.groupby('city').agg(
    people_count = ('first_name', 'count'),
    uniq_dom = ('email_domain','nunique')).sort_values('people_count', ascending=False).head(10)
print(agg_by_sity)
top_domains = df['email_domain'].value_counts()
print(df['email_domain'].value_counts())

# 7. Export results

df.to_csv("uk500_clean.csv",index=True)
gmail_users.to_csv("gmail_users.csv",index=True)
with pd.ExcelWriter("stats.xlsx") as writer:
    top_cities.to_excel(writer, sheet_name="Top Cities")
    top_domains.to_excel(writer, sheet_name="Top Domains")