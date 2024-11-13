import os
import re
from pathlib import Path
import numpy as np
import soundfile as sf
from f5_tts.model import DiT, UNetT
from f5_tts.infer.utils_infer import (
    load_vocoder,
    load_model,
    preprocess_ref_audio_text,
    infer_process,
    remove_silence_for_generated_wav,
)
from flask import Flask, request, send_file
from flask_ngrok import run_with_ngrok
import google.generativeai as genai

genai.configure(api_key='')
model = genai.GenerativeModel('gemini-1.5-pro-latest')
chat = model.start_chat(history=[])

# Descrevendo para o modelo seu modo de operação
response = chat.send_message('''Você é um assistente virtual chamado Ricardo Kauer com uma funcionalidade para acender uma lâmpada. Sempre que você receber um prompt com qualquer texto relacionado a acender a luz, responda apenas 'Acender.', e mais nenhuma outra palavra. Caso contrário, responda de acordo com as duas regras a seguir.
                             :Nunca gere listas em suas respostas.
                             :Suas respostas devem ser de no máximo 2 frases.''')
print(response.text)  # puramente por debug

app = Flask(__name__)
run_with_ngrok(app)  # Start ngrok when app is run

# Global model and vocoder variables
vocoder = None
ema_model = None
mel_spec_type = "vocos"  # Define the mel_spec_type globally

def initialize_model(model_name="F5-TTS", ckpt_file=None, vocab_file=""):
    """
    Initializes and loads the TTS model and vocoder for the specified model.
    """
    global vocoder, ema_model, mel_spec_type

    # Load the vocoder if it hasn't been loaded
    if vocoder is None:
        vocoder = load_vocoder(vocoder_name=mel_spec_type)

    # Model loading only once
    if ema_model is None:
        if model_name == "F5-TTS":
            model_cls = DiT
            model_cfg = dict(dim=1024, depth=22, heads=16, ff_mult=2, text_dim=512, conv_layers=4)
            if not ckpt_file:
                ckpt_file = 'model_last_467k_sf.pt'  # Update path as needed
        elif model_name == "E2-TTS":
            model_cls = UNetT
            model_cfg = dict(dim=1024, depth=24, heads=16, ff_mult=4)
            if not ckpt_file:
                ckpt_file = "path/to/E2-TTS/model_checkpoint.safetensors"  # Update path as needed

        # Corrected call to load_model
        ema_model = load_model(
            model_cls,
            model_cfg,
            ckpt_file,
            mel_spec_type=mel_spec_type,  # Pass mel_spec_type here
            vocab_file=vocab_file
        )

def mytts(text, output_dir="output", model_name="F5-TTS", speed=1.0, remove_silence=True):
    """
    Converts text to speech and saves the audio file to the output directory.
    """
    global mel_spec_type
    # Ensure the model and vocoder are initialized
    initialize_model(model_name=model_name)

    # Configure output path
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    wave_path = Path(output_dir) / "generated_audio.wav"

    # Placeholder reference audio and text (adjust paths as needed)
    ref_audio = "sounds/RicardoCut.wav"
    ref_text = "A introdução do VAR, árbitro de vídeo, no futebol, trouxe consigo uma série de mudanças no modo como o esporte é vivenciado e celebrado. Embora a tecnologia tenha sido implementada com o objetivo de trazer decisões mais justas e precisas..."

    # Process reference for each use
    main_voice = {"ref_audio": ref_audio, "ref_text": ref_text}
    main_voice["ref_audio"], main_voice["ref_text"] = preprocess_ref_audio_text(
        main_voice["ref_audio"], main_voice["ref_text"]
    )

    # Split text based on voice tags if present
    generated_audio_segments = []
    reg1 = r"(?=\[\w+\])"
    chunks = re.split(reg1, text)
    reg2 = r"\[(\w+)\]"
    for chunk in chunks:
        match = re.match(reg2, chunk)
        voice = "main" if not match else match[1]
        chunk_text = re.sub(reg2, "", chunk).strip()
        audio, final_sample_rate, _ = infer_process(
            main_voice["ref_audio"],
            main_voice["ref_text"],
            chunk_text,
            ema_model,
            vocoder,
            speed=speed,
            mel_spec_type=mel_spec_type  # Pass mel_spec_type here
        )
        generated_audio_segments.append(audio)

    # Concatenate audio segments and save
    final_wave = np.concatenate(generated_audio_segments)
    with open(wave_path, "wb") as f:
        sf.write(f.name, final_wave, final_sample_rate)
        if remove_silence:
            remove_silence_for_generated_wav(f.name)

    print(f"Generated audio: {wave_path}")
    return str(wave_path)

os.environ['NGROK_AUTHTOKEN'] = ''

def run(text):
    response = chat.send_message(text)
    print(response.text)
    audio_file = mytts(response.text)
    return audio_file

app = Flask(__name__)

@app.route('/output.mp3', methods=['GET'])
def get_mp3():
    # Extract 'text' from the query parameters
    text = request.args.get('text')

    if not text:
        return "Missing 'text' parameter", 400

    # Call the run(text) function to generate the mp3 file
    print("Received text:", text)
    audio_file = run(text)
    # audio_file="/content/drive/MyDrive/TelecomVozes/arquivo1.mp3"
    print("Generated audio file:", audio_file)
    # Send the generated mp3 file as a response
    if os.path.exists(audio_file):
        return send_file(audio_file, mimetype='audio/mpeg')
    else:
        return "Audio file not found", 404

import ngrok
listener = ngrok.forward("localhost:5000", authtoken_from_env=True, domain="kid-relative-polecat.ngrok-free.app")

if __name__ == "__main__":
    app.run(port=5000)
