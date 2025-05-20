from langfuse.callback import CallbackHandler
from langchain.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain.schema.runnable import RunnableLambda
from langchain.schema.output_parser import StrOutputParser

from langfuse import Langfuse
from dotenv import load_dotenv
import os

load_dotenv()

langfuse = Langfuse(
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

# Defina os prompts para cada etapa
prompt1 = ChatPromptTemplate.from_template("Qual é a capital de {país}?")
prompt2 = ChatPromptTemplate.from_template("Quantos habitantes tem {cidade}?")

chat = AzureChatOpenAI(
    temperature=0
)

# Defina os parsers de saída
parser = StrOutputParser()

# Defina as etapas como funções
def etapa1(inputs):
    return prompt1.format_messages(**inputs)

def etapa2(inputs):
    return prompt2.format_messages(**inputs)

# Crie as cadeias para cada etapa
chain1 = RunnableLambda(etapa1) | chat | parser
chain2 = RunnableLambda(etapa2) | chat | parser

langfuse_handler = CallbackHandler(
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

# Execute as cadeias com o handler do Langfuse
resposta1 = chain1.invoke({"país": "França"}, 
                          config={"callbacks": [langfuse_handler], 
                                  "metadata": {"model": "gpt-4o"}})

resposta2 = chain2.invoke({"cidade": resposta1}, 
                          config={"callbacks": [langfuse_handler], 
                                  "metadata": {"model": "gpt-4o"}})

print("Resposta 1:", resposta1)
print("Resposta 2:", resposta2)
#langfuse_handler.shutdown()
langfuse.flush()