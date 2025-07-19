import gradio as gr
import requests

def responder(mensagem):
    # aqui você chama a API do seu SaaS
    r = requests.post("SUA_URL_DA_API", json={"prompt": mensagem})
    return r.json().get("response", "Erro ou sem resposta")

iface = gr.Interface(fn=responder, inputs="text", outputs="text")
iface.launch()
