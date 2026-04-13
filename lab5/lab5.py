import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.set_page_config(page_title="VHI Analysis", layout="wide")

@st.cache_data
def load_and_clean_data(folder_path):
    all_data = []
    noaa_indices = {1:"Cherkasy", 2:"Chernihiv", 3:"Chernivtsi", 4:"Crimea", 5:"Dnipropetrovsk", 6:"Donetsk", 7:"Ivano-Frankivsk", 8:"Kharkiv", 9:"Kherson", 10:"Khmelnytskyy", 11:"Kyiv", 12:"Kyiv City", 13:"Kirovohrad", 14:"Luhansk", 15:"Lviv", 16:"Mykolayiv", 17:"Odessa", 18:"Poltava", 19:"Rivne", 20:"Sevastopol", 21:"Sumy", 22:"Ternopil", 23:"Transcarpathia", 24:"Vinnytsya", 25:"Volyn", 26:"Zaporizhzhya", 27:"Zhytomyr"}
    ua_alphabet_map = {"Vinnytsya": "Вінницька", "Volyn": "Волинська", "Dnipropetrovsk": "Дніпропетровська", "Donetsk": "Донецька", "Zhytomyr": "Житомирська", "Transcarpathia": "Закарпатська", "Zaporizhzhya": "Запорізька", "Ivano-Frankivsk": "Івано-Франківська", "Kyiv City": "Київ", "Kyiv": "Київська", "Kirovohrad": "Кіровоградська", "Crimea": "Крим", "Luhansk": "Луганська", "Lviv": "Львівська", "Mykolayiv": "Миколаївська", "Odessa": "Одеська", "Poltava": "Полтавська", "Rivne": "Рівненська", "Sevastopol": "Севастополь", "Sumy": "Сумська", "Ternopil": "Тернопільська", "Kharkiv": "Харківська", "Kherson": "Херсонська", "Khmelnytskyy": "Хмельницька", "Cherkasy": "Черкаська", "Chernivtsi": "Чернівецька", "Chernihiv": "Чернігівська"}

    if not os.path.exists(folder_path): return pd.DataFrame()
    
    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    for file in files:
        old_id = int(file.split('_')[2])
        headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
        df_temp = pd.read_csv(os.path.join(folder_path, file), skiprows=2, names=headers).drop(columns=['empty']).dropna()
        df_temp['Year'] = pd.to_numeric(df_temp['Year'].astype(str).str.extract('(\d+)', expand=False)).astype(int)
        df_temp[['Week','VCI','TCI','VHI']] = df_temp[['Week','VCI','TCI','VHI']].apply(pd.to_numeric)
        
        eng_name = noaa_indices.get(old_id)
        df_temp['Province_Name'] = ua_alphabet_map.get(eng_name)
        all_data.append(df_temp)
    
    return pd.concat(all_data, ignore_index=True)

df = load_and_clean_data("vhi_data")
prv_list = sorted(df['Province_Name'].unique())
min_y, max_y = int(df['Year'].min()), int(df['Year'].max())

if 'yrs' not in st.session_state:
    st.session_state.idx = "VCI"
    st.session_state.prv = prv_list[0]
    st.session_state.wks = (1, 52)
    st.session_state.yrs = (min_y, max_y)
    st.session_state.sort_asc = False
    st.session_state.sort_desc = False

def handle_asc():
    if st.session_state.sort_asc:
        st.session_state.sort_desc = False

def handle_desc():
    if st.session_state.sort_desc:
        st.session_state.sort_asc = False

def reset_filters_callback():
    st.session_state.idx = "VCI"
    st.session_state.prv = prv_list[0]
    st.session_state.wks = (1, 52)
    st.session_state.yrs = (min_y, max_y)
    st.session_state.sort_asc = False
    st.session_state.sort_desc = False

st.sidebar.header("Фільтри")
st.sidebar.selectbox("Показник", ["VCI", "TCI", "VHI"], key="idx")
st.sidebar.selectbox("Основна область", prv_list, key="prv")
st.sidebar.slider("Тижні", 1, 52, key="wks")
st.sidebar.slider("Роки", min_y, max_y, key="yrs")
st.sidebar.subheader("Сортування")
st.sidebar.checkbox("За зростанням", key="sort_asc", on_change=handle_asc)
st.sidebar.checkbox("За спаданням", key="sort_desc", on_change=handle_desc)

st.sidebar.button("Скинути фільтри", on_click=reset_filters_callback)

def get_filtered_data(p_name):
    if not isinstance(st.session_state.yrs, (list, tuple)):
        return pd.DataFrame()
        
    return df[(df['Province_Name'] == p_name) & 
              (df['Year'].between(st.session_state.yrs[0], st.session_state.yrs[1])) & 
              (df['Week'].between(st.session_state.wks[0], st.session_state.wks[1]))].sort_values(['Year','Week'])

main_df = get_filtered_data(st.session_state.prv)

tab1, tab2, tab3 = st.tabs(["Таблиця", "Графік динаміки", "Порівняльна діаграма"])

with tab1:
    if not main_df.empty:
        st.subheader(f"Дані для області: {st.session_state.prv}")
        
        display_df = main_df[['Year', 'Week', st.session_state.idx]].copy()
        
        if st.session_state.sort_asc:
            display_df = display_df.sort_values(st.session_state.idx, ascending=True)
        elif st.session_state.sort_desc:
            display_df = display_df.sort_values(st.session_state.idx, ascending=False)
            
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("Дані за вказаний період відсутні.")

with tab2:
    if not main_df.empty:
        st.subheader(f"Динаміка {st.session_state.idx} ({st.session_state.yrs[0]}-{st.session_state.yrs[1]})")
        
        chart_df = main_df.copy()
        chart_df['Time'] = chart_df['Year'] + (chart_df['Week'] / 52)
        
        fig_ts = px.line(
            chart_df, 
            x='Time', 
            y=st.session_state.idx,
            custom_data=['Year', 'Week']
        )

        fig_ts.update_traces(
            line_color='green', 
            line_width=1.5,
            hovertemplate="Рік: %{customdata[0]}<br>Тиждень: %{customdata[1]}<br>Значення: %{y:.2f}<extra></extra>"
        )
        
        fig_ts.update_layout(
            xaxis_rangeslider_visible=False,
            hovermode="x unified",
            margin=dict(t=10, b=10, l=0, r=0),
            height=450,
            yaxis_title=st.session_state.idx,
            xaxis_title="Рік",
            xaxis=dict(tickformat="d")
        )

        st.plotly_chart(fig_ts, use_container_width=True)
    else:
        st.info("Дані за вказаний період відсутні.")
with tab3:
    st.subheader(f"Середній {st.session_state.idx} по всіх областях")
    
    averages = []
    for p in prv_list:
        p_df = get_filtered_data(p)
        if not p_df.empty:
            p_avg = p_df[st.session_state.idx].mean()
            averages.append({'Область': p, 'Значення': round(p_avg, 2)})
    
    if averages:
        res_df = pd.DataFrame(averages)
        
        if st.session_state.sort_asc:
            res_df = res_df.sort_values('Значення', ascending=True)
        elif st.session_state.sort_desc:
            res_df = res_df.sort_values('Значення', ascending=False)
        else:
            res_df = res_df.sort_values('Значення', ascending=False)
        
        fig_plotly = px.bar(
            res_df, 
            x='Область', 
            y='Значення',
            color='Область',
            color_discrete_map={p: 'red' if p == st.session_state.prv else 'skyblue' for p in prv_list},
            labels={'Значення': f'Середній {st.session_state.idx}'},
            hover_data={'Область': True, 'Значення': True}
        )
        
        fig_plotly.update_layout(showlegend=False, xaxis_tickangle=-90)
        st.plotly_chart(fig_plotly, use_container_width=True)
    else:
        st.warning("Неможливо розрахувати середні значення для обраного періоду.")