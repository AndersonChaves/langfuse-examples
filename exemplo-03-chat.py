from langfuse import Langfuse
from datetime import datetime
import llm
import os

from dotenv import load_dotenv
load_dotenv()

langfuse = Langfuse(
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

# Gera um trace_id único para a conversa
trace = langfuse.trace(
    name="exemplo-rastreamento-conversa",
    user_id="user_123",
    metadata={"session_type": "demo"},
)

trace_id = trace.id

# Simulando mensagens do usuário e respostas da LLM
messages= [
    "Oi, pode me ajudar com informações sobre Langfuse?",
    "E como ele funciona com LangChain? Seja sucinto. ",
    "Pode me dar um resumo em forma de tabela?"
]

ground_truth = [
    "Langfuse é um framework.",
    "Ele se integra ao langchain.",
    "Não."
]

chat_history = ""
for i, message in enumerate(messages):
  chat_history += "User: " + message
  print(f"Enviando mensagem {i} para LLM")
  start_request = datetime.now()
  llm_answer = llm.invoke(chat_history)
  print("LLM Answer: ", llm_answer)
  chat_history += "System: " + llm_answer
  end_request = datetime.now()
  
  print(f"Registrando interação mensagem {i} para LLM")
  trace.span(
              name=f"user_message_{i}",
              input=message,
              output=llm_answer,
              metadata={"message_id": i,
                        "query": message,
                        "generation": llm_answer,
                        "ground_truth": ground_truth[i]},
              start_time=start_request,
              end_time=end_request,
  )
langfuse.flush()
