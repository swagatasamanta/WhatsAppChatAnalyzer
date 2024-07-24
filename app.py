
import streamlit as st
import matplotlib.pyplot as plt 
import seaborn as sns 
import preprocessor, helper

st.sidebar.title('WhatsApp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue() # Get in txt format
    data = bytes_data.decode("utf-8") # Convert the entire chat(Raw data) into string and store it into a var   
    # st.text(data)
    df = preprocessor.preprocess(data)
    
    # st.dataframe(df)
    
    # -------------------Analysis starts from here--------------------
    # Fetch unique users and show then in a dropdown menu
    
    user_list = df['user'].unique().tolist()
    
    user_list.remove('group_Notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)
    
    if st.sidebar.button("Show Analysis"): 
        
        num_messages, num_words, num_media_shared, num_links_shared = helper.fetch_stats(selected_user, df)
        
        st.title("Top Statistics")
        
        col_1, col_2, col_3, col_4 = st.columns(4)
        
        with col_1:   
            st.header("Total Messages")
            st.title(num_messages)
        with col_2:
            st.header("Total Words")
            st.title(num_words)
        with col_3:
            st.header("Media Shared")
            st.title(num_media_shared)
        with col_4:
            st.header("Links Shared")
            st.title(num_links_shared)
            
        # -------------- Monthly Timeline --------------
        st.title("Monthly Timeline")
        m_timeline = helper.monthly_timeline(selected_user, df)
        
        fig, ax = plt.subplots()
        
        ax.plot(m_timeline['time'], m_timeline['message'], color="green")
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)
        
        # -------------- Daily   Timeline --------------
        st.title("Daily Timeline")
        d_timeline = helper.daily_timeline(selected_user, df)
        
        fig, ax = plt.subplots()
        
        ax.plot(d_timeline['only_date'], d_timeline['message'], color="green")
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)
            
        
        # ----------------- Activity Map ------------------    
            
        st.title("Activity Map")    
        col_1, col_2 = st.columns(2)
        
        with col_1:
            st.header("Most Busy Day")
            busy_day = helper.weekly_activity_map(selected_user, df)
            
            fig, ax = plt.subplots()
            
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation = 'vertical')

            st.pyplot(fig)
        with col_2:
            st.header("Most Busy Month")
            busy_month = helper.monthly_activity_map(selected_user, df)
            
            fig, ax = plt.subplots()
            
            ax.bar(busy_month.index, busy_month.values, color="orange")
            plt.xticks(rotation = 'vertical')

            st.pyplot(fig)
            
        # ----------- Activity HeatMap ---------------
        st.title("Weekly Activity HeatMap")
        
        user_heatmap = helper.activity_heapmap(selected_user, df) 
        
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        
        st.pyplot(fig)
            
        # --------------  Finding the busiest user in the group (Group Level) ---------
        if selected_user == "Overall": # Over allpicable in group level
            st.title("Most Busy Users")
            
            # Return the users, sorted in desc order based on number of messages they did in the group
            x, new_df= helper.most_busy_users(df); 
            
            fig, ax = plt.subplots()
            
            col_1, col_2 = st.columns(2)
            
            with col_1:
                ax.bar(x.index, x.values, color='green')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            
            with col_2:
                st.dataframe(new_df)

                
        # ---------------------- Generate WordCloud ------------------
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
 
        # ---------------------- Most common words ----------------------
        most_common_df = helper.most_common_words(selected_user, df)
        # st.dataframe(most_common_df)
        
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1]) # barh for horizontal
        
        plt.xticks(rotation = 'vertical')
        
        st.title("Most Common Words")
        st.pyplot(fig)
        
         
        # ---------------- Emoji Analysis -------------- 
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")
        
        col_1, col_2 = st.columns(2)
        
        with col_1:
            st.dataframe(emoji_df)
        with col_2:
            fig, ax = plt.subplots()    
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            # ax.bar(emoji_df[0].head(10), emoji_df[1].head(10))

            st.pyplot(fig)
    
    