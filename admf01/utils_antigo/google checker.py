import google.generativeai as genai
import os

# Certifique-se de que sua GOOGLE_API_KEY está definida como variável de ambiente
GOOGLE_API_KEY = "AIzaSyAxDYI7fsQqVs8TqrOxk26E4h1RV-wwBJs"
genai.configure(api_key=GOOGLE_API_KEY)

print("Tentando listar modelos disponíveis...")
try:
    for m in genai.list_models():
        # Filtra apenas modelos que suportam generateContent ou são do tipo TEXT
        # O generateContent é o método para gerar texto
        if "generateContent" in m.supported_generation_methods or m.name.startswith("models/gemini") or m.name.startswith("models/text"):
            print(f"Nome do Modelo: {m.name}, Métodos Suportados: {m.supported_generation_methods}")
except Exception as e:
    print(f"Erro ao listar modelos: {e}")