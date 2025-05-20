from langfuse import Langfuse
import llm
import os

from dotenv import load_dotenv
load_dotenv()

langfuse = Langfuse(
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

# Criar uma trace para agrupar as interações
trace = langfuse.trace(name="meu-exemplo", user_id="user-123")

# Chamada à OpenAI
query = "Me fale sobre o langfuse. Seja sucinto. "
answer = llm.invoke(query)

# Registrando uma observação (span) para a chamada do modelo
metadata = {"metadados": "qualquer metadado da observação pode vir aqui"}
span = trace.span(name="chamada-simples-llm", metadata=metadata,
                  output=answer, input=query)

# Fazendo uma nova chamada
query = "Me fale sobre a história das LLMs."
answer = llm.invoke(query)
span = trace.span(name="outra-chamada-llm", input=query, output=answer)
print(answer)

metadata = {"metadados": "qualquer metadado do trace pode vir aqui"}
trace.update(input=query,
             output=answer,
             metadata=metadata)

langfuse.flush()
print("Chamada ao langfuse realizada.")
