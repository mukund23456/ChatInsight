# import streamlit as st
# import preprocess,helper
# import matplotlib.pyplot as plt
# import seaborn as sns
# import numpy as np
# st.sidebar.title("Chat Insight")

# uploaded_file = st.sidebar.file_uploader("Choose a file")
# if uploaded_file is not None:
#     bytes_data = uploaded_file.getvalue()
#     data = bytes_data.decode("utf-8")
#     df = preprocess.preprocess(data)
#     st.dataframe(df)

#     user_list = df['user'].unique().tolist()
#     user_list.remove('group_notification')
#     user_list.sort()
#     user_list.insert(0,"Overall")

#     selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

#     if st.sidebar.button("Show Analysis"):

#         num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
#         st.title("Top Statistics")
#         col1, col2, col3, col4 = st.columns(4)

#         with col1:
#             st.header("Total Messages")
#             st.title(num_messages)
#         with col2:
#             st.header("Total Words")
#             st.title(words)
#         with col3:
#             st.header("Media Shared")
#             st.title(num_media_messages)
#         with col4:
#             st.header("Links Shared")
#             st.title(num_links)

#         most_common_df = helper.most_common_words(selected_user,df)

#         fig,ax = plt.subplots()

#         ax.barh(most_common_df[0],most_common_df[1])
#         plt.xticks(rotation='vertical')

#         st.title('Most common words')
#         st.pyplot(fig)

#     st.title("Monthly Timeline")
#     timeline = helper.monthly_timeline(selected_user,df)
#     fig,ax = plt.subplots()
#     ax.plot(timeline['time'], timeline['message'],color='green')
#     plt.xticks(rotation='vertical')
#     plt.tight_layout()
#     st.pyplot(fig)


   
# # ### Most Busy Month 
# #     st.title("Most Busy Month")
# #     month_list=timeline['year'].unique().tolist()
# #     option = st.selectbox(
# #     'Choose Year ',month_list,key="month_list")
# #     p=helper.solve(timeline,option)
# #     timeline=helper.help_most_busy_month(selected_user,df)
# #     fig,ax=plt.subplots()
# #     keys = [key for key in p.keys()]
# #     values = [value for value in p.values()]
# #     ax.bar(keys, [value[0] if len(value) == 1 else 0 for value in values],
# #        width=0.5,color='r')
# #     plt.xticks(rotation='vertical')
# #     st.pyplot(fig)



# # ### Most Busy Day 
# #     st.title("Most Busy Day")
# #     col11, col22 = st.columns(2)
# #     with col11:
#     year_list=timeline['year'].unique().tolist()
# #         year = st.selectbox(
# #         'Choose Year ',year_list,key="year_list")
# #     with col22:
# #         k=['January','February','March','April','May','June','July','August','September','October','November','December']
# #         month= st.selectbox(
# #         'Choose Month ',k,key="m_list")
    
#     # b=helper.solve2(df,year,month)
#     # print(b)
#     # fig,ax=plt.subplots()
#     # keys = [key for key in b.keys()]
#     # values = [value for value in b.values()]
#     # ax.bar(keys, [value[0] if len(value) == 1 else 0 for value in values],
#     #    width=0.5,color='b')
#     # plt.xticks(rotation='vertical')
#     # st.pyplot(fig)


#     #stacked bar graph implementation 
#     month_dict=dict()
#     #print(year_list)
#     k=['January','February','March','April','May','June','July','August','September','October','November','December']
#     temp=timeline.sort_values(by=['month_num','year'])
#     # print(temp)
#     month_dict=helper.solve(temp,year_list)
#     print(month_dict)
    
#     months = list(month_dict.keys())
#     message_counts = []
#     for month_data in month_dict.values():
#         message_counts.append(list(month_data.values()))
#     new_dict = {}
#     for month, year_data in month_dict.items():
#         for year, message_count in year_data.items():
#             if month not in new_dict.keys():
#                 new_dict[month] = []
#             new_dict[month].append((message_count))
#     print(new_dict)
#     fig, ax = plt.subplots()
#     width=0.5
#     bottom=np.zeros(5)
#     print('\n')
#     for k, weight_count in new_dict.items():
#         for i in range(1,5):
#             bottom[i]=bottom[i-1]+weight_count[i-1]
#         p = ax.bar(k, weight_count, width, label=k, bottom=bottom)
#         print(k,weight_count,bottom)
#     ax.legend()
#     print('\n')
#     plt.xticks(rotation='vertical')
#     st.pyplot(fig)
import streamlit as st
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D  # Importing the 3D toolkit
import preprocess
import helper
import seaborn as sns
import html
import re

# Set the page layout to wide
st.set_page_config(layout="wide")

# Add custom CSS to center the tabs
st.markdown(
    """
    <style>
        .st-cg {
            max-width: 1600px;
            margin: auto;
        }

        #tabs-bui3-tabpanel-5 img {width:75% !important; margin:auto !important;]}
        #tabs-bui3-tabpanel-3 img {width:75% !important; margin:auto !important;]}
        #tabs-bui3-tabpanel-2 img {width:75% !important; margin:auto !important;]}

        .st-emotion-cache-12w0qpk.e1f1d6gn1 {
            width: 400px; /* Adjust the width as needed */
            height: 300px; /* Make it a square for a circle effect */
            border-radius: 50%; /* Make it a circle */
            background-color: #3498db; /* Set your desired background color */
        }

        .st-emotion-cache-10trblm.e1nzilvr1 {
            padding: 25px; /* Adjust the value according to your preference */
        }

        .element-container.st-emotion-cache-1e5lw08.e1f1d6gn2 {
            margin-top: 10px; /* Adjust the value according to your preference */
        }
        
    </style>
    """,
    unsafe_allow_html=True,
)


Dashboard, Searchword, Timelines, ActivityMap, BusyUsers, WordAnalysis, EmojiAnalysis= st.tabs(["🖥️Dashboard", "🔎Search word", "📈Timelines", "⌚Activity Map", "🤳Busy Users", "🔣Word Analysis", "😄Emoji Analysis"])

st.sidebar.title("Chat-Insights")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")  # bit stream to string
    df = preprocess.preprocess(data)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    with Dashboard:
        # Code for the Statistics tab
        st.title("Top Figures")
        # Rest of your Statistics tab code...
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)
        font_size_px = "30px"

        with col1:
            st.markdown(f"<h1 style='font-size: {font_size_px}; text-align: center; color: blue; text-decoration: underline;'>Total Messages</h1>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='font-size: {font_size_px}; text-align: center; color: white;'>{num_messages}</h2>", unsafe_allow_html=True)

        with col2:
            st.markdown(f"<h1 style='font-size: {font_size_px}; text-align: center; color: blue; text-decoration: underline;'>Total Words</h1>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='font-size: {font_size_px}; text-align: center; color: white;'>{words}</h2>", unsafe_allow_html=True)

        with col3:
            st.markdown(f"<h1 style='font-size: {font_size_px}; text-align: center; color: blue; text-decoration: underline;'>Total Media Shared</h1>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='font-size: {font_size_px}; text-align: center; color: white;'>{num_media_messages}</h2>", unsafe_allow_html=True)

        with col4:
            st.markdown(f"<h1 style='font-size: {font_size_px}; text-align: center; color: blue; text-decoration: underline;'>Total Links Shared</h1>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='font-size: {font_size_px}; text-align: center; color: white;'>{num_links}</h2>", unsafe_allow_html=True)



    with Searchword:
        # Code for the Search tab
        st.title('Search messages with a word')
        # Create a text input for search
        search_term = st.text_input("Enter search term:")
        # Display the search term
        if search_term != "":
            st.write("Here are the messages with the searched word:")

            for s in range(df.shape[0]):
                if search_term in df['message'][s]:
                    escaped_search_term = html.escape(search_term)
                    # Use a regular expression to replace non-alphanumeric characters with underscores
                    valid_tag_name = re.sub(r'\W', '_', df['message'][s])

                    # Check if the resulting tag name is not empty and is valid
                    if valid_tag_name:
                        escaped_message = html.escape(df['message'][s])
                        highlighted_message = escaped_message.replace(escaped_search_term, f'<mark style="background-color:lightgrey">{escaped_search_term}</mark>')
                        with st.container():
                            st.markdown(f'<div style="background-color:#008000; padding:20px; border-radius:15px; border:5px solid black"><b>{df["date"][s]}</b><br>{highlighted_message}</div>', unsafe_allow_html=True)
                    else:
                        # Handle the case where the tag name is not valid
                        print(f"Invalid tag name for message: {df['message'][s]}")


    with Timelines:
        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()

        plt.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()

        plt.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


    with ActivityMap:
        # Activity Map
        st.title('Activity Map')
        
        # Use a single column layout
        col1 = st.columns(1)[0]
        
        with col1:
            st.title("Most Busy Day")
            col11, col22 = st.columns(2)
            with col11:
                year_list=timeline['year'].unique().tolist()
                year = st.selectbox(
                'Choose Year ',year_list,key="year_list")
            with col22:
                k=['January','February','March','April','May','June','July','August','September','October','November','December']
                month= st.selectbox(
                'Choose Month ',k,key="m_list")

            b=helper.solve2(df,year,month,selected_user)
            print(b)
            fig,ax=plt.subplots()
            keys = [key for key in b.keys()]
            values = [value for value in b.values()]
            ax.bar(keys, [value[0] if len(value) == 1 else 0 for value in values],
               width=0.5,color='b')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
            st.title("Most Busy Month")
            month_list = helper.monthly_timeline(selected_user, df)['year'].unique().tolist()
            option = st.selectbox('Choose Year ', month_list)
            p = helper.solve(helper.monthly_timeline(selected_user, df), option)
            fig, ax = plt.subplots(figsize=(6, 4))  # Adjust the figsize as needed
            keys = [key for key in p.keys()]
            values = [value for value in p.values()]
            ax.bar(keys, [value[0] if len(value) == 1 else 0 for value in values], width=0.5, color='r')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        

            st.title("Weekly Activity Map")
            user_heatmap = helper.activity_heatmap(selected_user, df)
            fig, ax = plt.subplots(figsize=(6, 4))  # Adjust the figsize as needed
            ax = sns.heatmap(user_heatmap)
            st.pyplot(fig)



    with BusyUsers:
        # finding the busiest user in the group
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
        
            with col1:
                ax.pie(x.values, labels=x.index, autopct='%1.1f%%', colors=['red', 'blue', 'green','yellow','grey'])  # Customize colors as needed
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        else:
            st.text("Oops! Go & check overall analysis for this...")
        

    with WordAnalysis:
        # WordCloud
        st.title('WordCloud')
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        plt.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_df = helper.most_common_words(selected_user, df)
        # st.dataframe(most_common_df);
        fig, ax = plt.subplots()

        ax.barh(most_common_df[0], most_common_df[1],color='purple')
        plt.xticks(rotation='vertical')

        st.title('Most Common Words')
        st.pyplot(fig)
        # st.dataframe(most_common_df)

    with EmojiAnalysis:
        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            plt.rcParams['font.family'] = 'Segoe UI Emoji'
            ax.pie(emoji_df[1].head(5), labels=emoji_df[0].head(5), autopct="%0.2f")
            st.pyplot(fig)

else:
    st.title("WELCOME TO THE CHAT ANALYSER-VISUALIZER....")
    
   

    
    
    
   
    

    
 


