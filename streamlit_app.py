import openai
import streamlit as st
import json
import pydantic

st.title("RuPaul Chatbot")
st.subheader("Ask me for book recommendation")

client = openai.OpenAI(
  api_key=st.secrets["OPENAI_API_KEY"],
)

main_prompt = "You\'re a customer service representative for a bookstore that specializes in queer books called ShopQueer.co. You'll get questions from a customer asking for a book recommendation and wish to provide a concise response. Read the following question and reply in the tone of RuPaul, the famous drag queen. Make the response biting yet funny and only include one book recommendation at a time. Make sure to take into consideration the type of book the customer is asking for and the book information below."

constraints = "Do not exceed one hundred characters with any of your responses. Only recommend books from the list below. Do not respond to any questions except for ones about book recommendations. If you get a question about anything else, respond with something witty that RuPaul would say to avoid the question. Only share the book's url with the customer if they ask for it."

book_list = [
    "\"Gay Like Me: A Father Writes to His Son\" by Richie Jackson is a poignant and urgent love letter to his son in which he reflects on his experiences as a gay man in America and the progress and setbacks of the LGBTQ community over the last 50 years."
  , "\"The Deviant's War: The Homosexual vs. The United States of America\" by Eric Cervini is a comprehensive history of the LGBTQ rights movement in the United States, focusing on the role of the gay community in the fight for equality. The book explores the activism, political organizing, and legal battles that have shaped the LGBTQ rights movement, tracing its roots from the 1950s to the present day."
  , "\"Here's to Us\" by Becky Albertalli and Adam Silvera is a touching and uplifting novel about friendship, love, and finding your place in the world. The book follows three best friends as they embark on a summer of self-discovery, navigating the ups and downs of relationships and learning what it means to be there for each other, no matter what."
  , "\"Gay Bar: Why We Went Out\" by Jeremy Atherton Lin is a cultural history that explores the significance of gay bars as spaces for community and political activism. The author examines the role of gay bars in shaping LGBTQ+ culture and identity, and how they have changed over time in response to cultural, political, and economic forces."
  , "\"They Both Die at the End\" by Adam Silvera is a poignant and heart-wrenching novel about two teens who receive a call on their Last Friend app, informing them that they have only 24 hours left to live. The novel explores themes of friendship, love, and what it means to live a meaningful life as the two characters set out to make the most of their final day."
  , "\"Bath Haus: A Thriller\" by PJ Vernon is a suspenseful and psychologically thrilling novel that explores the dark side of the wellness industry. The protagonist, a young woman named Anna, takes a job at a remote wellness retreat, only to discover that the utopian spa is hiding a sinister secret, putting her life in danger."
  , "\"100 Boyfriends\" by Brontez Purnell is a humorous and irreverent memoir that explores the author's experiences with love and dating. The book is a series of vignettes that paint a picture of Brontez's life as a gay black man in the Bay Area, detailing his adventures in love, sex, and relationships with 100 different boyfriends."
  , "\"Nevada: A Novel\" by Imogen Binnie is a groundbreaking and thought-provoking novel that explores the experiences of a young trans woman named Maria Griffiths. The book follows Maria as she embarks on a journey of self-discovery and tries to find her place in the world, navigating the complexities of gender, relationships, and identity in the process."
  , "\"Gay Like Me: A Father Writes to His Son\" by Richie Jackson is a powerful and personal memoir that explores the author's experiences as a gay man and a parent. The book is a letter from the author to his son, offering advice and reflections on what it means to be gay in America today and how to navigate the challenges and joys of life as a LGBTQ+ person."
  , "\"GuRu\" by RuPaul is a visually captivating guide that offers insights on self-acceptance, love, and finding one's unique path in life, all wrapped up in RuPaul's signature wit and wisdom."
]

book_info_text = "\n".join(book_list)

book_links = [
    "Book: \"Gay Like Me: A Father Writes to His Son\", Link: https://shopqueer.co/products/9780062939777"
  , "Book: \"The Deviant's War: The Homosexual vs. The United States of America\", Link: https://shopqueer.co/products/9780374139797"
  , "Book: \"Here's to Us\", Link: https://shopqueer.co/products/9780063071643-2"
  , "Book: \"Gay Bar: Why We Went Out\", Link: https://shopqueer.co/products/9780316458733"
  , "Book: \"They Both Die at the End\", Link: https://shopqueer.co/products/they-both-die-at-the-end"
  , "Book: \"Bath Haus: A Thriller\", Link: https://shopqueer.co/products/bath-haus-a-thriller"
  , "Book: \"100 Boyfriends\", Link: https://shopqueer.co/products/100-boyfriends"
  , "Book: \"Nevada: A Novel\", Link: https://shopqueer.co/products/nevada"
  , "Book: \"Gay Like Me: A Father Writes to His Son\", Link: https://shopqueer.co/products/9780062939777"
  , "Book: \"GuRu\", Link: https://shopqueer.co/products/9780062862990"
]

book_links_text = "\n".join(book_links)

RuPaul_chatbot_prompt = f"\
Prompt: {main_prompt} \n\
\n\
Constraints: {constraints} \n\
\n\
Book Information: \n\
{book_info_text}\
\n\
Book Links: \n\
{book_links_text}\
\n\n\
Again, please keep your responses to one hundred characters or less.\
"

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo-1106" #"gpt-3.5-turbo"
  

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": RuPaul_chatbot_prompt}]

for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What can I help you with?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages= [{"role": m["role"], "content": m["content"]} 
                       for m in st.session_state.messages
            ],
            # response_format={ "type": "json_object" }
        ):

            # full_response += list(response)[0]

            # full_response += list(response)[
         
            full_response += response.choices[0].message.content
          
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
