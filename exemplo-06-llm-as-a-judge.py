from langfuse import Langfuse
import llm, os

# Langfuse setup
langfuse = Langfuse(
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

# Criar uma trace para agrupar as interações
trace = langfuse.trace(name="meu-exemplo", user_id="user-123")
span = trace.span(name="exemplo-llm-as-a-judge")

# Chamada à OpenAI
input = "Me fale sobre o langfuse. Seja sucinto."
answer = llm.invoke(input + "fim.")
ground_truth = "O Langfuse é uma ferramenta de observabilidade para aplicações que" \
               "utilizam modelos de linguagem (LLMs). " \
               "Ele permite rastrear, monitorar e analisar interações com LLMs," \
               "ajudando a depurar fluxos de conversação," \
               " medir desempenho e otimizar o uso de APIs de IA, " \
               "como OpenAI e Azure OpenAI."  

# Também pode adicionar inputs e outros metadados
print(answer)
metadata = {"tarefa": "responder pergunta", 
            "query": "Me fale sobre o tecgraf.",
            "generation": answer,
            "ground_truth": ground_truth},

# Início de uma observação (span) para a chamada do modelo
span = trace.update(name="exemplo-llm-as-a-judge",
                  input=input,
                  output=answer,
                  metadata=metadata)
langfuse.flush()
print("Chamada ao langfuse realizada.")