import pandas as pd
import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
from collections import Counter

st.sidebar.title('WhatsApp Chat Analyzer')


# def analyze_chat(df):
#     st.write("Analyzing chat data...")
#     # Example analysis: Display the number of messages per user
#     user_message_count = df['Name'].value_counts()
#     st.bar_chart(user_message_count, height=500)
#
#     # Display the number of messages over time
#     df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour', 'minute']])
#     messages_per_day = df.groupby(df['datetime'].dt.date).size()
#     st.line_chart(messages_per_day)


uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8').splitlines()

    # Print data for debugging
    # st.write("Data before preprocessing:")
    # st.write(data)

    # Process the data using the preprocess function
    df = preprocessor.preprocess(data)

    # Display the dataframe
    # st.dataframe(df)

    # # Pass the DataFrame to the analysis function
    # analyze_chat(df)
    user_list=df['Name'].unique().tolist()
    # user_list.remove('group')
    user_list.insert(0,'overall')
    selected_user=st.sidebar.selectbox('show anakyis wrt to ',user_list)
    if st.sidebar.button('show analysis'):
        nums_messages,num_words,num_files,num_links=helper.fetch_stats(selected_user,df)
        st.title('Top Statistics')
        col1,col2,col3,col4= st.columns(4)
        with col1:
            st.header('Total Messages')
            st.title(nums_messages)
        with col2:
            st.header('Total words')
            st.title(num_words)
        with col3:
            st.header('Media Shared')
            st.title(num_files)
        with col4:
            st.header('Links Shared')
            st.title(num_links)





        st.title('MONTHLY TIMELINE')
        monthly_timeline_df = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(monthly_timeline_df['time'], monthly_timeline_df['Message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)



        st.title('DAILY TIMELINE')
        daily_timeline_df = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline_df['date'], daily_timeline_df['Message'], color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        st.title('ACTIVITY MAP')

        col1,col2=st.columns(2)
        with col1:
            st.title('MOST BUSY DAY')
            daily_active_df = helper.daily_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(daily_active_df['day_name'], daily_active_df['Message'], color='blue')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.title('MOST BUSY MONTH')
            monthly_active_df=helper.monthly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(monthly_active_df['month_name'], monthly_active_df['Message'], color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)








    #   finding the busiest users in the group (Group level)
        if selected_user=='overall':
            st.title('Most Busy Users')
            x,n_df=helper.most_busy_users(df)
            fig,ax=plt.subplots()

            col1,col2=st.columns(2)
            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(n_df)
        st.title('Word Cloud')
        df_wc=helper.word_cloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
#       most common words
        most_common_df=helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title('Most Common Words')
        st.pyplot(fig)

#         analysing emoji
        emojis = helper.extract_emojis(selected_user,df)
        emojis_df=pd.DataFrame(Counter(emojis).most_common(5))
        st.title('EMOGIS ANALYSIS')
        cols1,cols2=st.columns(2)

        with cols1:
            st.dataframe(emojis_df)
        with cols2:
            fig, ax = plt.subplots()
            ax.pie(emojis_df[1],labels=emojis_df[0],autopct='%0.2f')
            st.pyplot(fig)













