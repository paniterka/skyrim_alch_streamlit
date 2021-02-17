import streamlit as st
import pandas as pd
import numpy as np

def return_common_effects(list_of_ings, df): 
    common_effects = df.query('Ingredient in @list_of_ings')['Effect'].value_counts()
    return common_effects[common_effects>0]

def return_common_ingredients(list_of_effs, df): 
    common_effects = df.query('Effect in @list_of_effs')['Ingredient'].value_counts()
    return common_effects[common_effects>1]

def return_ingredients(list_of_effs, df): 
    common_effects = df.query('Effect in @list_of_effs')
    return common_effects    

st.title("Skyrim Alchemy Helper")


# ======= LOAD DATA 
DATA_DIR = './'
ingdf2 = pd.read_csv(DATA_DIR+'ingdf_long_encoded.csv')
ingdf1 = pd.read_csv(DATA_DIR+'ingdf_wide_encoded.csv')
effects_df = pd.read_csv(DATA_DIR+'effects.csv')
ing_en_pl = pd.read_csv(DATA_DIR+'ing_en_pl.csv')
eff_en_pl = pd.read_csv(DATA_DIR+'eff_en_pl.csv')


def replace_ing(series,lang):
    return series.replace(dict(ing_en_pl[['Ing_ID','Ing_'+lang]].values))

def replace_eff(series,lang):
    try:
        tmp = series.replace(dict(eff_en_pl[['Effect_ID','Effect_'+lang]].values))
    except: 
        tmp = series.replace(dict(effects_df[['Effect_ID','Effect']].values))
    return tmp

# ======= PICK LANGUAGE 
lang = st.radio('Pick language', options=['PL', 'EN'])
st.write(lang)

ingdf1['Ingredient'] = replace_ing(ingdf1['Ingredient'],lang)
ingdf2['Ingredient'] = replace_ing(ingdf2['Ingredient'],lang)

for tmp in [x for x in ingdf1.columns if x.endswith('Effect')]:
    ingdf1[tmp] = replace_eff(ingdf1[tmp],lang)
ingdf2['Effect'] = replace_eff(ingdf2['Effect'],lang)

ingdf1 = ingdf1.sort_values(by="Ingredient")
ingdf2 = ingdf2.sort_values(by="Ingredient")

if st.checkbox('Show translations'):
    st.subheader('Ingredients')
    st.write(ing_en_pl)
    st.subheader('Effects')
    st.write(eff_en_pl)



# ==================== 
st.header('Pick one ingredient to find out its properties')

ingredients_unique = ingdf2['Ingredient'].unique()

sel_ing = st.selectbox('Select an ingredient', ingredients_unique)
st.write(ingdf1.query('Ingredient == @sel_ing').T)


# ==================== 
st.header('Pick multiple ingredients to find out their shared effects')

# ingredients_unique = ingdf2['Ingredient'].unique()

sel_ings = st.multiselect('Select ingredients', ingredients_unique)
shared_effs = return_common_effects(sel_ings, ingdf2)

st.subheader('Shared effects')
st.write(shared_effs[shared_effs>1])

st.subheader('Singular effects')
st.write(shared_effs[shared_effs==1])


# ==================== 
st.header('Pick an effect to see the ingredients')

effects_unique = ingdf2['Effect'].unique()
effects_unique.sort()
sel_effs = st.selectbox('Select an effect', effects_unique)
st.subheader('Ingredients exhibiting this effect')
st.write(return_ingredients(sel_effs, ingdf2))


# ==================== 
st.header('Find effect combinations')

effects_unique = ingdf2['Effect'].unique()
effects_unique.sort()
sel_effs2 = st.multiselect('Select effects', effects_unique)
st.subheader('Ingredients exhibiting all these effects')
st.write(return_common_ingredients(sel_effs2, ingdf2))
st.subheader('Complementary ingredients')
for eff in sel_effs2: 
    st.write(return_ingredients([eff], ingdf2))
