
<h1 align="center">AttendAI</h1>
<h2>O que é? 🤔</h2>
O <b>AttendAI</b> é um projeto desenvolvido para a aula de aprendizado de máquina com uma proposta simples: agilizar o processo de checagem da presença de alunos utilizando inteligência artificial.

---

<h2>👩🏾‍💻Nosso time</h2>

<table align="center">
  <tr >
      <td align="center"><a href="https://github.com/ericksantos12"><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/16109127?v=4" width="100px;" alt=""/><br /><sub><b>Erick Santos</b></sub></a><br />🎨💻</td>
      <td align="center"><a href="https://github.com/GabrielleCGNeves"><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/88461057?v=4" width="100px;" alt=""/><br /><sub><b>Gabrielle C G Neves</b></sub></a><br />🎨💻📖</td>
      <td align="center"><a href="https://github.com/Gabstxr"><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/98724979?v=4" width="100px;" alt=""/><br /><sub><b>Giovanna Gabrielle</b></sub><br />💻</td>
  <tr>
<table>

<h2>🎨 Layout</h2>

<div>
    <a href="https://www.figma.com/design/GkfV9cgirecKD0okncoYvH/FacialRecognition?node-id=8-121&t=J89kOo3TcobaLbvF-1"><img src="https://img.shields.io/badge/ver_mais-F24E1E?style=for-the-badge&logo=figma&logoColor=white"></a>
</div>

<h3>📱 Mobile</h3>

<div align="center"> 
<img src = "https://files.catbox.moe/twdu5a.png" height="400em">
<img src = "https://files.catbox.moe/oc9f86.png" height="400em">
<img src = "https://files.catbox.moe/bv8s9j.png" height="400em">
</div>

<h3>💻 Web</h3>
<div align="center">
    <img src = "https://files.catbox.moe/93r8vo.png" width="350em">
    <img src = "https://files.catbox.moe/qmqfs8.png" width="350em">
</div>

<h3>👩🏾‍💻 Tecnologias</h3>

<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" width="50"/>
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/react/react-original.svg" width="50"/>
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/flask/flask-original.svg" width="50"/>
          

<h3>🏁 Como Utilizar</h3>

- Tenha o Python instalado em sua máquina
- Tenha o Node LTS instalado
- Clone o repositório

#### API:
Para executar a API, acesse a pasta `facial-api` e execute os seguintes comandos:
```bash
# Instale as dependências
pip install -r requirements.txt

# Execute o projeto
flask --app api/routes.py run -h 0.0.0.0
```
OBS: Você pode adicionar a flag `--debug` para que a API recarregue automaticamente a cada alteração no código.

Para treinar a API, acesse a rota `/train`, para que ela carregue o modelo com as imagens da pasta `images`. Caso você não tenha uma ferramenta para fazer requisições HTTP, você pode utilizar o próprio powershell do windows executando os seguintes comandos juntos:

```powershell
$uri = "http://127.0.0.1:5000/train"
$response = Invoke-RestMethod -Uri $uri -Method Post
$response | ConvertTo-Json -Depth 4
```

#### Frontend:
Para executar o frontend, acesse a pasta `facial-project` e execute os seguintes comandos:
```bash
# Instale as dependências
npm install

# Execute o projeto
npm run dev
```
