# Hand Tracking

## :books: Descrição ##
Módulo para detecção de mãos utilizando [OpenCv](https://pypi.org/project/opencv-python/) e [Medipipe](https://mediapipe.dev/).

## Como utilizar

```powershell
pip install -U git+https://github.com/AllanCapistrano/hand-tracking.git
```

### Testar o projeto
1. Clone este repositório;
2. Instale as dependências de execução e testes do projeto:
   ```powershell
   pip install -r requirements.txt
   pip install -r test-requirements.txt
   ```
4. Crie um arquivo com as varáveis de ambiente, e modifique-o caso necessário:
   ```powershell
   cp .env.example .env
   ```
6. Execute o projeto
   ```powershell
   # Linux/macOS
   python3 tests/main.py

   # Windows
   py tests/main.py
   ```

## :pushpin: Autores ##
- Allan Capistrano: [Github](https://github.com/AllanCapistrano) - [Linkedin](https://www.linkedin.com/in/allancapistrano/) - [E-mail](https://mail.google.com/mail/u/0/?view=cm&fs=1&tf=1&source=mailto&to=asantos@ecomp.uefs.br)
- João Erick Barbosa: [Github](https://github.com/JoaoErick) - [Linkedin](https://www.linkedin.com/in/joão-erick-barbosa-9050801b0/) - [E-mail](https://mail.google.com/mail/u/0/?view=cm&fs=1&tf=1&source=mailto&to=jsilva@ecomp.uefs.br)

------------

## :balance_scale: Licença ##
[GPL 3.0 License](./LICENSE)
