import openai
import streamlit as st
from streamlit_chat import message

# Setting page title and header
st.set_page_config(page_title="RuPaul Chatbot - Book Recommendations", page_icon=":robot_face:")

# Swt API key
openai.api_key = st.secrets['api_secret']

prompt = "You\'re a customer service representative for a bookstore that specializes in queer books called ShopQueer.co. You'll get questions from a customer asking for a book recommendation and wish to provide a concise response. Read the following question and reply in the tone of RuPaul, the famous drag queen. Make the response biting yet funny and only include one book recommendation at a time. Make sure to take into consideration the type of book the customer is asking for and the book information below."

constraints = "Do not exceed one hundred characters with any of your responses. Only recommend books from the list below. Do not respond to any questions except for ones about book recommendations. If you get a question about anything else, respond with something witty that RuPaul would say to avoid the question. Only share the book's url with the customer if they ask for it."

book_list = [
    "\"The Deviant's War: The Homosexual vs. The United States of America\" by Eric Cervini is a comprehensive history of the LGBTQ rights movement in the United States, focusing on the role of the gay community in the fight for equality. The book explores the activism, political organizing, and legal battles that have shaped the LGBTQ rights movement, tracing its roots from the 1950s to the present day."
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
    "Book: \"The Deviant's War: The Homosexual vs. The United States of America\", Link: https://shopqueer.co/products/9780374139797"
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
Prompt: {prompt} \n\
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

# Initialise session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": RuPaul_chatbot_prompt}
    ]
if 'model_name' not in st.session_state:
    st.session_state['model_name'] = []
if 'cost' not in st.session_state:
    st.session_state['cost'] = []
if 'total_tokens' not in st.session_state:
    st.session_state['total_tokens'] = []
if 'total_cost' not in st.session_state:
    st.session_state['total_cost'] = 0.0

# Sidebar - let user choose model, show total cost of current conversation, and let user clear the current conversation
st.sidebar.title("Clear Chat")
clear_button = st.sidebar.button("Clear Conversation", key="clear")

# Map model names to OpenAI model IDs
model = "gpt-3.5-turbo"
# model = "gpt-4"



# reset everything
if clear_button:
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state['messages'] = [
        {"role": "system", "content": RuPaul_chatbot_prompt}
    ]
    st.session_state['number_tokens'] = []
    st.session_state['model_name'] = []
    st.session_state['cost'] = []
    st.session_state['total_cost'] = 0.0
    st.session_state['total_tokens'] = []
    counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")


# generate a response
def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": prompt})

    completion = openai.ChatCompletion.create(
        model=model,
        messages=st.session_state['messages']
    )
    response = completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": response})

    # print(st.session_state['messages'])
    total_tokens = completion.usage.total_tokens
    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens
    return response, total_tokens, prompt_tokens, completion_tokens


# container for chat history
response_container = st.container()
# container for text box
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        output, total_tokens, prompt_tokens, completion_tokens = generate_response(user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
        st.session_state['model_name'].append(model_name)
        st.session_state['total_tokens'].append(total_tokens)

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
