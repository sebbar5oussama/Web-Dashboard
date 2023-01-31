import streamlit as st
import plotly.express as px
import pandas as pd
st.set_page_config(page_title="DE-TRACA", page_icon=":bar_chart:", layout="wide")
df = pd.read_excel(io=r'C:\\Users\PC\Desktop\Project\projet expertise.xlsm',
                engine='openpyxl',
                sheet_name='Sortie')
df_11 = pd.read_excel(io=r'C:\\Users\PC\Desktop\projet expertise.xlsm',
                engine='openpyxl',
                sheet_name='lot')                 
st.sidebar.header("Please filter here:")
product= st.sidebar.multiselect(
    "select the Product :",
    options=df["type_produit"].unique(),
    default=df["type_produit"].unique()
)
number= st.sidebar.multiselect(
    "select the N° lot :",
    options=df["Nlot"].unique(),
    default=df["Nlot"].unique()
)
provenance= st.sidebar.multiselect(
    "select the provenance :",
    options=df_11["provenance"].unique(),
    default=df_11["provenance"].unique()
)
df_selection = df.query("type_produit== @product & Nlot==@number")
df_1=df_11.query("provenance==@provenance")
st.title(":bar_chart: Product Dashboard")
st.markdown("##")
Nb=int(df_selection["id_sortie"].count())
Qte_max=int(df_selection["quantité"].max())
Taille_Max=int(df_11["taille"].max())
#Star_rating=":star:" * int(round(Total_defect/10,0))
left_column, middle_column, right_column=st.columns(3)
with left_column:
    st.subheader("Nombre des produits sorties:")
    st.subheader(Nb)
with middle_column:
    st.subheader("Quantité maximale: ")
    st.subheader(Qte_max)
with right_column:
    st.subheader("Taille maximale: ")
    st.subheader(Taille_Max)
st.markdown("---")
occurence_product=(
    df_selection.groupby(by=["type_produit"]).sum()[["quantité"]].sort_values("quantité")
)
occurence_type=(
    df_1.groupby(by=["provenance"]).sum()[["taille"]].sort_values("taille")
)
tot=int(df_selection["quantité"].sum())
tit=int(df_1["taille"].sum())
values=df_selection["quantité"]/tot
names=df_selection["type_produit"]
values_1=df_1["taille"]/tit
names_1=df_1["provenance"]
fig_bar= px.bar(
    occurence_product,
    x=occurence_product.index,
    y="quantité",
    orientation="v",
    title="<b>Total Qte per Product<b>",
    color_discrete_sequence=["#0083B8"]*len(occurence_product),
    template="plotly_white",
)
fig_bar.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)
fig_pie=px.pie(df,values=values,names=names,title="Poucentage des produits")
fig_pie.update_traces(textposition='inside',textinfo='percent+label')
fig_pie.update_layout(title_font_size=42)
df_2=df_1.drop(columns="provenance")
dfu=df_selection.drop(columns="type_produit")
left_column, right_column=st.columns(2)
left_column.plotly_chart(fig_bar,use_container_width=True)
with right_column:
    st.plotly_chart(figure_or_data=fig_pie)
st.line_chart(df_2,y="taille")
fig_pie_1=px.pie(df_1,values=values_1,names=names_1,title="Pourcentage selon les povenances")
fig_pie_1.update_traces(textposition='inside',textinfo='percent+label')
fig_pie_1.update_layout(title_font_size=42)
left_column, right_column=st.columns(2)
with left_column:
    st.plotly_chart(figure_or_data=fig_pie_1)
with right_column:
    st.line_chart(dfu,y="quantité")
