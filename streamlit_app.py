#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import numpy as np
from surprise import BaselineOnly
from surprise import Reader
from surprise import Dataset

#initialize variables
reading_no_zero_df = pd.read_csv('./data/reading_no_zero.csv')
combined_all_info_df = pd.read_csv('./data/combined_all_info_df_clean.csv')
combined_df = pd.DataFrame([],columns = ['user','item','rating'])
non_adult_genres = ['Drama','Action','Comedy','Sci-Fi','Girls Love','Avant Garde','Horror','Supernatural','Fantasy','Adventure','Romance','Gourmet','Ecchi','Sports','Boys Love','Mystery','Slice of Life','Suspense']
all_genres = ['Drama','Action','Comedy','Sci-Fi','Girls Love','Avant Garde','Horror','Supernatural','Fantasy','Adventure','Romance','Gourmet','Ecchi','Sports','Boys Love','Mystery','Slice of Life','Suspense', 'Hentai','Erotica']

#no adult recommendations by default
adult_recommendations = 'no'

#set cache function for model so it does not re-fit when user inputs remain the same
@st.cache
def Recommend():
    with st.spinner('Loading...'):
        reader = Reader(rating_scale=(1, 10))
        data = Dataset.load_from_df(combined_df[['user', 'item', 'rating']], reader)
        algo = BaselineOnly()
        trainset = data.build_full_trainset()
        algo.fit(trainset)
        recommend_list = []
        user_titles = combined_df[combined_df['user'] == 'streamlit_user']['item'].unique()
        no_user_titles = []
        for title in combined_df['item'].unique():
            if title not in user_titles:
                no_user_titles.append(title)
        for title in no_user_titles:
            title_compatibility = []
            prediction = algo.predict(uid= 'streamlit_user', iid=title)
            title_compatibility.append(prediction.iid)
            title_compatibility.append(prediction.est)
            recommend_list.append(title_compatibility)
        recommend_df = pd.DataFrame(recommend_list, columns = ['Title', 'Compatibility'])
        return recommend_df.sort_values('Compatibility',ascending = False)
        


# In[2]:


st.title('This is my manga recommender')
st.write("By Bryan Soh [GitHub](https://github.com/bryansoh/)")
st.markdown("[Source code](https://github.com/bryansoh/mangarecommender) | Model from [Scikit-Surprise](https://surprise.readthedocs.io/en/stable/)")
st.text("")
st.text("")

agree = st.checkbox('You are above the age of 18 and wish to see adult recommendations as well')
genres_to_use = non_adult_genres

#change variables when user wants to see adult recommendations
if agree:
    genres_to_use = all_genres
    adult_recommendations = 'yes'
        
yes_genres = st.multiselect('Choose the genres you want to see in your recommendations', options = genres_to_use)
    
with st.form("my_form"):

    user_mangas = st.multiselect('Select any number of your favorite manga titles', options = combined_all_info_df['combined_title'].unique())
    
    #add user's favorite manga titles to dataframe and fit model only upon click of recommend button
    submitted = st.form_submit_button("Recommend")
    if submitted:
    
        user_rating_list = []
        for item in user_mangas:
            manga_rating = []
            manga_rating.append('streamlit_user')
            manga_rating.append(str(combined_all_info_df.loc[combined_all_info_df['combined_title'] == item,['title']].values[0])[2:-2])
            manga_rating.append(10)
            user_rating_list.append(manga_rating)

        user_rating_df = pd.DataFrame(user_rating_list, columns = ['user','item','rating'])


        # In[3]:

        combined_df = pd.concat(objs = [reading_no_zero_df, user_rating_df])

       
        Recommend()

# In[ ]:


#once model generates recommendations, merge recommended titles with dataframe containing all information to pull relevant info to display
        st.header('Recommendations')

        recommendations_details_df = pd.merge(left = combined_all_info_df, right = Recommend(), left_on = 'title', right_on = 'Title', how = 'right')
        
#remove adult titles from recommendations by default                
        if adult_recommendations == 'no':
            recommendations_details_df = recommendations_details_df[(recommendations_details_df['Hentai'] == 0) & (recommendations_details_df['Erotica'] == 0)]
        
        new_features = ['title']
        
        for genre in yes_genres:
            new_features.append(genre)
        
        recommendations_details_df = recommendations_details_df[new_features]
        
        recommendations_details_df['sum'] = recommendations_details_df.sum(axis = 1)
        
        recommendations_details_df = recommendations_details_df[recommendations_details_df['sum'] != 0]
        
        recommendations_details_df = pd.merge(left = combined_all_info_df, right = recommendations_details_df, on = 'title', how = 'right')
        
       
        col1, col2, col3 = st.columns(3)

        with col1:
            st.header('#1')
            st.image(f"{recommendations_details_df.iloc[0]['image']}", caption = recommendations_details_df.iloc[0]['title'])

            with st.expander("See Summary"):
                link = f"[MAL Link]({recommendations_details_df.iloc[0]['url']})"
                st.markdown(link,unsafe_allow_html=True)
                st.write(f"{recommendations_details_df.iloc[0]['synopsis']}")

        with col2:
            st.header('#2')
            st.image(f"{recommendations_details_df.iloc[1]['image']}", caption = recommendations_details_df.iloc[1]['title'])
            with st.expander("See Summary"):
                link = f"[MAL Link]({recommendations_details_df.iloc[1]['url']})"
                st.markdown(link,unsafe_allow_html=True)
                st.write(f"{recommendations_details_df.iloc[1]['synopsis']}")

        with col3:
            st.header('#3')
            st.image(f"{recommendations_details_df.iloc[2]['image']}", caption = recommendations_details_df.iloc[2]['title'])
            with st.expander("See Summary"):
                link = f"[MAL Link]({recommendations_details_df.iloc[2]['url']})"
                st.markdown(link,unsafe_allow_html=True)
                st.write(f"{recommendations_details_df.iloc[2]['synopsis']}")

        col4, col5, col6 = st.columns(3)

        with col4:
            st.header('#4')
            st.image(f"{recommendations_details_df.iloc[3]['image']}", caption = recommendations_details_df.iloc[3]['title'])
            with st.expander("See Summary"):
                link = f"[MAL Link]({recommendations_details_df.iloc[3]['url']})"
                st.markdown(link,unsafe_allow_html=True)
                st.write(f"{recommendations_details_df.iloc[3]['synopsis']}")

        with col5:
            st.header('#5')
            st.image(f"{recommendations_details_df.iloc[4]['image']}", caption = recommendations_details_df.iloc[4]['title'])
            with st.expander("See Summary"):
                link = f"[MAL Link]({recommendations_details_df.iloc[4]['url']})"
                st.markdown(link,unsafe_allow_html=True)
                st.write(f"{recommendations_details_df.iloc[4]['synopsis']}")

        with col6:
            st.header('#6')
            st.image(f"{recommendations_details_df.iloc[5]['image']}", caption = recommendations_details_df.iloc[5]['title'])
            with st.expander("See Summary"):
                link = f"[MAL Link]({recommendations_details_df.iloc[5]['url']})"
                st.markdown(link,unsafe_allow_html=True)
                st.write(f"{recommendations_details_df.iloc[5]['synopsis']}")


