import speech_recognition as sr

def ouvir_e_armazenar():
    # Inicializa o reconhecedor
    reconhecedor = sr.Recognizer()

    # Usa o microfone como fonte de áudio
    with sr.Microphone() as fonte:
        print("Ouvindo...")
        reconhecedor.adjust_for_ambient_noise(fonte)  # Ajusta para o ruído ambiente
        audio = reconhecedor.listen(fonte)  # Ouve a entrada do microfone

    try:
        # Reconhece o discurso usando a API do Google Web Speech
        texto = reconhecedor.recognize_google(audio, language='pt-BR')
        return texto
    except sr.UnknownValueError:
        print("Desculpe, não entendi o que você disse.")
    except sr.RequestError as e:
        print(f"Não foi possível solicitar os resultados; {e}")

if __name__ == "__main__":
    entrada_do_usuario = ouvir_e_armazenar()
    if entrada_do_usuario == None:
        print("deu none")
    print("Você disse:", entrada_do_usuario)