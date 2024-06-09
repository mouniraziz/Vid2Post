from langchain_google_genai import GoogleGenerativeAI
import streamlit as st
from langchain.globals import set_llm_cache
from langchain.cache import InMemoryCache

@st.cache_resource 
def load_model(api):
    return GoogleGenerativeAI(model="gemini-pro", google_api_key=api, temperature=0.0)

def produce(api):
    llm = load_model(api)
    with open('./files/transcript.txt', 'r', encoding="utf8") as file:
        data = file.read().rstrip()
    file.close()
    set_llm_cache(InMemoryCache())
    #if(len(data)>4500):
    #    data = llm("Summerize this transcript into 4500 characters, this is the transcript: -"+data+"- avoid making up information that are not in the transcript.'")
    article = llm.invoke("""Hello, today I'd like you to assume the role of an expert in article writing, specializing in creating highly viral and engaging articles and blog posts from a video transcript. You will be writing an article today.
    Transcript: -"""+data+"""-
    The subject of the article is: from the provided transcript.
    The target audience for the article: you decide which audience according to the transcript.
    Goal:
    Write an engaging and in-depth article on the subject provided, using natural language that resonates strongly with my target audience. Ensure this article sounds like it is written by a human.
    Guidelines & Presentation:
    - Please create an article that is no less than 2000 tokens in length and don't exceed your max token response.
    - Please organize my content with relevant H1, H2, and H3 tags and has an engaging title.
    Additional Instructions:
    - The article writing style should be engaging and informative, striking a balance between relaying complex ideas and maintaining reader interest.
    - Writing techniques should include the use of anecdotes or personal experiences to establish context and make the information relatable to the reader.
    - The article structure should be organized with clear headings and subheadings, which guide the reader through the content and make it easy to follow.
    - The article should utilize research and data to support its claims, presenting findings from studies and experiments to substantiate the main points being made.
    - The underlying intent of the article should be evident from the beginning, creating a consistent theme throughout.
    - The article should incorporate quotes and insights from experts to lend credibility to the discussion.
    - The article should incorporate real-life examples to illustrate the points being made.
    - The article should address potential counterarguments or alternative perspectives, acknowledging the limitations or nuances of the main argument.
    - The article should end with a thought-provoking or forward-looking conclusion, inviting the reader to consider the implications of the research or potential solutions to the problems discussed.
    - The article should be written in a clear, concise, and accessible language to ensure that a wide range of readers can understand and engage with the content. Be simple, straightforward and ensure the article is easy to read, follow, and understand.
    - Use storytelling and narrative techniques to create a compelling and relatable story that conveys your main points.
    - Employ vivid and evocative language to paint a mental picture for the reader and immerse them in the topic.
    - Use comparisons and figurative language to simplify complex ideas and make them more relatable.
    - Use words and phrases that link ideas and guide the reader smoothly from one point to the next.
    - Use active voice whenever possible in order to make your writing more dynamic and engaging.
    Constraints:
    - Avoid long, dense paragraphs: Break up your content into shorter paragraphs to improve readability and make it easier for readers to digest the information.
    - Avoid overly complex language: Don't use complicated or obscure words when simpler alternatives will suffice.
    - Avoid overuse of jargon: While some technical terms may be necessary, avoid excessive use of industry-specific language that may be confusing or alienating to readers who are not familiar with the topic.
    Additional Guidelines
    Approach the subject with a comprehensive understanding, considering historical, practical, and diverse perspectives. Begin with a concise overview, then elaborate on key points. Outline your approach before diving in, ensuring depth beyond surface-level observations. Align with recognized research standards. Reflect on past implications, current status, and future projections of the topic. Weigh contrasting viewpoints, factor in hypothetical scenarios, and challenge your conclusions with counter-arguments. Progressively refine your analysis, cross-reference with related domains, and continuously probe deeper. Discuss potential outcomes and their likelihood. Your response should be layered, detailed, and balanced, achieving a holistic exploration of the subject.
    Thank you!""")

    tweet= llm.invoke("""Assume the role of a social media manager. Formulate at least 20 from this transcript:  -"""+data+"""-.  the respond should be in the following for [these are the proposed tweets:] [tweets in form of bullet points, with returning to a new line at the end of each tweet]. avoid exceeding the your response's character limits. """)
    generated_output = "## Blog Article 📰"+"""\n"""+article+"""\n"""+"## Tweets 🐤"+"""\n"""+tweet
    clean_generated_output = llm.invoke("""remove emojis from this text: """+generated_output+""". do not change any word and keep the same strecture of it""")
    return article, tweet, clean_generated_output

    
