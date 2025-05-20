from langfuse import Langfuse
import llm
from langfuse.decorators import observe
from dotenv import load_dotenv

load_dotenv()  

@observe()
def story():
    print("Perguntando a IA")
    answer = llm.invoke("Me fale sobre o langfuse. Seja sucinto. ")
    print(f"Resposta: {answer}")

@observe()
def main():
    return story()

if __name__ == "__main__":
    main()