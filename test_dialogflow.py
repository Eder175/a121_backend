from google.cloud import dialogflow

def test_dialogflow_connection():
    try:
        # Cria uma sessão para o Dialogflow
        session_client = dialogflow.SessionsClient()
        print("Conexão com o Dialogflow bem-sucedida!")
    except Exception as e:
        print(f"Erro ao conectar ao Dialogflow: {e}")

if __name__ == "__main__":
    test_dialogflow_connection()
