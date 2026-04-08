import pandas as pd
import re
from tabulate import tabulate
import time

def clean_fatal(val):
    val = str(val).strip().upper()
    if val == 'Y': return 1
    if val in ['N', 'N ', ' N']: return 0
    return None

def clean_age(val):
    val = str(val).lower()
    if 'teen' in val: return 15
    nums = re.findall(r'\d+', val)
    if nums: return int(nums[0])
    return None

def loadFile(url):
    print("Connecting to database and fetching latest records...")
    df = pd.read_excel(url)
    time.sleep(1)
    print("\nWohoo, Data is fetched successfully !!")

    df['Is_Fatal'] = df['Fatal Y/N'].apply(clean_fatal)
    df['Age_Clean'] = df['Age'].apply(clean_age)
    df['Country'] = df['Country'].str.strip().str.upper()

    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df = df[(df['Year'] >= 1900) & (df['Year'] <= 2025)].copy()

    cols_to_drop = ['Unnamed: 22','Unnamed: 21','original order','Case Number',
                    'Case Number.1', 'href','href formula','pdf']
    df = df.drop(columns=cols_to_drop, errors='ignore')
    return df

def conclude(df):
    print("\n" + "="*70)
    print("       GLOBAL SHARK ATTACK RISK ANALYSIS: EXECUTIVE SUMMARY       ")
    print("="*80)
    time.sleep(1)

    # Global Metrics
    print(f"OVERALL MARKET SCOPE:")
    print(f"- Total Validated Incidents: {len(df):,}")
    print(f"- Global Avg. Fatality Rate: {df['Is_Fatal'].mean():.2%}")
    print("-" * 80)
    time.sleep(1)

    # Top 10 Countries
    print("\n[TABLE 1] REGIONAL RISK: TOP 10 COUNTRIES")
    country_counts = df['Country'].value_counts().head(10).reset_index()
    country_counts.columns = ['Country', 'Incident Count']
    print(tabulate(country_counts, headers='keys', tablefmt='fancy_grid', showindex=False))
    time.sleep(1)

    # Top 10 Activities
    print("\n[TABLE 2] ACTIVITY RISK PROFILE")
    activity_analysis = df.groupby('Activity')['Is_Fatal'].agg(['count', 'mean'])
    activity_analysis = activity_analysis.sort_values(by='count', ascending=False).head(10).reset_index()
    activity_analysis.columns = ['Activity', 'Volume', 'Fatality Rate']
    activity_analysis['Fatality Rate'] = activity_analysis['Fatality Rate'].map(lambda x: f"{x:.2%}")
    print(tabulate(activity_analysis, headers='keys', tablefmt='fancy_grid', showindex=False))