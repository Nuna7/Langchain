from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import random
import math
import os
from config import HUGGINGFACE_API_KEY


os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACE_API_KEY
repo_id = "google/flan-t5-xxl"

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=30)
def create_transcript(video_url: str):
    loader = YoutubeLoader.from_youtube_url(video_url)
    transcript = loader.load()

    docs = text_splitter.split_documents(transcript)
    return transcript,docs

def get_chunk_from_transcript(docs, chunk_no):
    chunk = docs[chunk_no]
    return chunk


def get_response_from_query(docs):

    llm = HuggingFaceHub(repo_id=repo_id, model_kwargs={"temperature": 0.5})

    prompt = PromptTemplate(input_variables=['docs'],template="""        
        'Task' : Please make questions by searching the relevant information which would test whether the user understand the video 
        from the following video transcript: {docs}
        
        Only use the factual information from the transcript should to use to make the question.

        Make sure the question are not too concise but self explanatory. 
        
        'Important' : Viewers must be able to understand the question without reading the transcript
        """)
    
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    response = llm_chain.run(docs=docs,verbose=True)
    response = response.replace("\n", "")
    return response

def generate_question(youtube_link):
    try:
        transcript,docs = create_transcript(youtube_link)

        chunks = []
        step = math.ceil(len(docs)/20)

        for i in range(0,len(docs),step):
            chunk = get_chunk_from_transcript(docs,i)
            chunks.append(chunk)

        questions = []
        i = 0
        for chunk in chunks:
            i+=1
            question = get_response_from_query(chunk)
            questions.append(question)
    except Exception:
        questions = 'Error'
    return questions

        
