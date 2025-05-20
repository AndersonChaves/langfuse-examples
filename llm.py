import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()  

def invoke(user_prompt: str):
    try:
        azure_api_key = os.environ["AZURE_OPENAI_API_KEY"]
        azure_endpoint_url = os.environ["AZURE_OPENAI_ENDPOINT"]
        azure_deployment = os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]
        api_version = os.environ["OPENAI_API_VERSION"]
    except KeyError as e:
        print(f"Erro: Variável de ambiente não encontrada: {e}")
        print("Certifique-se de definir AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT_NAME e OPENAI_API_VERSION.")
        raise e

    client = AzureOpenAI(
        api_key=azure_api_key,
        azure_endpoint=azure_endpoint_url,
        api_version=api_version
    )

    modelo_deployment_azure = azure_deployment

    try:
        completion = client.chat.completions.create(
            model=modelo_deployment_azure,
            messages=[
                {"role": "system", "content": "You are a helpful assistent."},
                {"role": "user", "content": user_prompt}
            ]
        )

        response = completion.choices[0].message.content
        return response

    except Exception as e:
        print(f"\nOcorreu um erro ao chamar a API do Azure OpenAI: {e}")
        print("Verifique se:")
        print(f"- O endpoint '{azure_endpoint_url}' está correto e acessível.")
        print(f"- A chave da API é válida para este endpoint.")
        print(f"- O nome da implantação '{modelo_deployment_azure}' existe e está ativo.")
        print(f"- A versão da API '{api_version}' é suportada pela sua implantação/endpoint.")
        print("- Você tem permissões de rede/firewall para acessar o endpoint.")