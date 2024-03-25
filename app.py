import streamlit as st
import os
from groq import Groq
import random


def chat_with_groq(client,promptx,prompt,model):
    """
    This function sends a chat message to the Groq API and returns the content of the response.
    It takes three parameters: the Groq client, the chat prompt, and the model to use for the chat.
    """
    
    completion = client.chat.completions.create(
    model=model,
    messages=[{"role": "system", "content": promptx }, {"role": "user", "content": prompt } ]
    )
  
    return completion.choices[0].message.content


def get_conversational_history(user_question_history,chatbot_answer_history,conversational_memory_length):
    """
    This function generates a full prompt for the chatbot based on the history of the conversation.
    It takes three parameters: the history of user questions, the history of chatbot answers, and the length of the conversational memory.

    Parameters:
    user_question_history (list): The history of user questions.
    chatbot_answer_history (list): The history of chatbot answers.
    conversational_memory_length (int): The length of the conversational memory.

    Returns:
    str: The full prompt for the chatbot.
    """

    base_prompt = '''
    Hello! I'm your friendly Groq chatbot. Provided by Raul Perez Development Studio. I have multiple personnalities with expertise kowledge to answer any of your questions, provide information, or just chat. I'm also super fast! Let's start our conversation!
    '''
    user_question_history = user_question_history[conversational_memory_length * -1:]
    chatbot_answer_history = chatbot_answer_history[conversational_memory_length * -1:]
    if len(chatbot_answer_history) > 0:
        conversational_history = '''
        As a recap, here is the current conversation:
            
        ''' + "\n".join(f"Human: {q}\nAI: {a}" for q, a in zip(user_question_history, chatbot_answer_history))

        full_prompt = base_prompt + conversational_history + '''
            Human: {user_question}
            AI:
        '''.format(user_question = user_question_history[-1])
    else:
        full_prompt = base_prompt + '''
            Human: {user_question}
            AI:
        '''.format(user_question = user_question_history[-1])
    
    return full_prompt


def get_random_prompt(file_path):
    """
    This function reads a file of prompts and returns a random prompt.
    """

    with open(file_path, 'r') as f:
        prompts = f.readlines()
    return random.choice(prompts).strip()


def main():
    """
    This function is the main entry point of the application. It sets up the Groq client, the Streamlit interface, and handles the chat interaction.
    """
    
    # Initialize Groq client
     # Get Groq API key
    groq_api_key = "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"

    client = Groq(
        # This is the default and can be omitted
        api_key=groq_api_key
        
    )

    # Display the Groq logo
    spacer, col = st.columns([5, 1])  
    with col:  
        st.image('groqcloud_darkmode.png')

    # The title and greeting message of the Streamlit application
    st.title("Chat with Groq!")
    st.write("Hello! I'm your friendly Artificial Intelligence. Provided by Raul Perez Development Studio. Select one of my personalities with expertise kowledge to answer any of your questions, provide information, or just chat. I'm also super fast! Let's start our conversation!")

    # Add customization options to the sidebar
    st.sidebar.title('Customization')

    # additional_context = st.sidebar.text_input('Enter additional summarization context for the LLM here (i.e. write it in spanish):')
    
    model = st.sidebar.selectbox(
        'Choose a model',
        ['mixtral-8x7b-32768', 'llama2-70b-4096', 'gemma-7b-it' ]
    )
    conversational_memory_length = st.sidebar.slider('Conversational memory length:', 1, 10, value = 5)


     # Add customization options to Select system prompts in the sidebar
    promptx = st.sidebar.selectbox(
    'Choose a Personality',
    [
        'You are chaty pirate named Raul.       Feel free to write in Argentinean Spanish, or site Tango lines.',
        'You are a professional lawyer.         From Los Angeles, named Julian Andre. When drafting legal contracts, ensure that all clauses are written in clear, unambiguous language. Use standardized legal terminology and reference relevant laws and regulations where appropriate. Follow the specified contract structure, including sections for definitions, terms and conditions, and signature fields.',
        'You are a certified personal fitness.  Assistant Coach named Sam. Your goal is to help clients achieve their health and fitness objectives through personalized workout plans, nutrition advice, and ongoing support. When interacting with clients, use a friendly and encouraging tone, and provide clear, actionable guidance based on their specific goals, fitness level, and preferences. Please respond to user inquiries in a friendly and empathetic manner. Use positive motivational language. Always site some inspirational questions that enhance their motivation.',
        'You are male Poet named Raul Jose.     born in argentina, When generating stories or poems, feel free to use figurative language, such as metaphors, similes, and personification, to make your writing more vivid and engaging. Draw upon a wide range of literary techniques, such as foreshadowing, symbolism, and irony, to create depth and layers of meaning in your work. Feel free to write in Argentinean Spanish, or site Tango lines.',
        'I want you to act as an academician.   You will be responsible for researching a topic of your choice and presenting the findings in a paper or article form. Your task is to identify reliable sources, organize the material in a well-structured way and document it accurately with citations. My first suggestion request is “I need help writing an article on modern trends in renewable energy generation targeting college students aged 18-25.',
        'I want you to act as a journalist.     You will report on breaking news, write feature stories and opinion pieces, develop research techniques for verifying information and uncovering sources, adhere to journalistic ethics, and deliver accurate reporting using your own distinct style. My first suggestion request is “I need help writing an article about the political corruption in major cities around the world.',
        'I want you to act as a French tutor.   Provide a detailed lesson plan for teaching a beginner french class, including vocabulary, grammar points, and cultural context. feel free to write all in french and english to explain the student ',
        'I want you to act as a film director.  Write a 200-word pitch for a new sci-fi movie, including a brief synopsis, target audience, and the unique elements that set it apart from other films in the genre.',
        'I want you to act as a DJ David Guetta.  Pierre David Guetta is a French DJ and record producer. Provide a step-by-step guide on how to create a seamless mix of electronic dance music tracks, including beatmatching, phrasing, and transitioning techniques.',
        'I want you to act as Perplexity.       Generate a comprehensive and informative answer (but no more than 80 words) for a given question solely based on the provided web Search Results (URL and Summary). You must only use information from the provided search results. Use an unbiased and journalistic tone. Use this current date and time: Wednesday, December 07,202222:50:56 UTC. Combine search results together into a coherent answer. Do not repeat text. Cite search results using [${number}] notation. Only cite the most relevant results that answer the question accurately. If different results refer to different entities with the same name, write separate answers for each entity. ',
        'I want you to act as a Linux terminal. I will type commands and you will reply with what the terminal should show. I want you to only reply with the terminal output inside one unique code block, and nothing else. Do not write explanations. Do not type commands unless I instruct you to do so. '
    ]
    )


    # The user is prompted to ask a question. The default value is a random prompt from the 'starter_prompt.txt' file.
    # user_question = st.text_input("Ask a question:",value=get_random_prompt('starter_prompt.txt'))
    user_question = st.text_input("Ask a question:")
    
    # If there is no user question history in the session state, an empty list is initialized.
    if 'user_question_history' not in st.session_state:
        st.session_state['user_question_history'] = []

    # If there is no chatbot answer history in the session state, an empty list is initialized.
    if 'chatbot_answer_history' not in st.session_state:
        st.session_state['chatbot_answer_history'] = []

    # If the user has asked a question,
    if user_question:
        # The question is added to the user question history.
        st.session_state['user_question_history'].append(user_question)

        # The full prompt for the chatbot is generated based on the conversational history.
        conversational_history_question = get_conversational_history(st.session_state['user_question_history'],st.session_state['chatbot_answer_history'],conversational_memory_length)
        
        # The chatbot's answer is generated by sending the full prompt to the Groq API.
        llm_answer = chat_with_groq(client,promptx,conversational_history_question,model)
        
        # The chatbot's answer is added to the chatbot answer history.
        st.session_state['chatbot_answer_history'].append(llm_answer)
        
        # The chatbot's answer is displayed.
        st.write("Chatbot:", llm_answer)

if __name__ == "__main__":
    main()







##random_prompt = get_random_prompt('starter_prompt.txt')
##print(random_prompt)