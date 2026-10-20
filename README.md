# Transcritor de Áudio

Aplicação desktop desenvolvida em Python para converter arquivos de áudio em texto em português, utilizando reconhecimento de fala com inteligência artificial executada localmente.

**Desenvolvido por Erik Goulart**  
Versão 1.0

## Funcionalidades

- Transcrição de áudio em português.
- Processamento local com Faster-Whisper.
- Interface gráfica com tema escuro.
- Barra de progresso durante a transcrição.
- Exibição gradual do texto reconhecido.
- Cópia do texto para a área de transferência.
- Suporte a arquivos MP3, WAV, M4A, OGG, FLAC, AAC, WMA e MP4.
- Processamento em segundo plano para manter a interface responsiva.

## Tecnologias utilizadas

- Python 3.13
- CustomTkinter
- Faster-Whisper
- Modelo Whisper Small
- PyInstaller para geração do executável Windows

## Requisitos

- Windows 10 ou 11, 64 bits.
- Python 3.13.
- Aproximadamente 1 GB de espaço livre, conforme a documentação do projeto.
- Conexão com a internet na primeira execução para baixar o modelo de transcrição.

## Instalação

Clone o repositório:

```bash
git clone https://github.com/SEU-USUARIO/transcritor-de-audio.git
cd transcritor-de-audio
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Execute o programa:

```bash
python transcrever.py
```

## Como utilizar

1. Abra o programa.
2. Clique em **Escolher áudio**.
3. Selecione o arquivo que deseja transcrever.
4. Clique em **Transcrever**.
5. Acompanhe o progresso e visualize o texto gerado.
6. Clique em **Copiar** para utilizar a transcrição.

## Funcionamento

A aplicação utiliza o Faster-Whisper com o modelo Small, configurado para processamento em CPU com precisão numérica INT8 e idioma português.

O processamento é executado em uma thread separada, enquanto uma fila de mensagens comunica o progresso e os resultados à interface gráfica.

Após o download inicial do modelo, a transcrição pode ser executada sem conexão com a internet.

## Geração do executável

O projeto prevê a utilização do PyInstaller para gerar uma versão executável para Windows. Consulte a documentação do projeto para obter os procedimentos de compilação e distribuição.

## Licença

A licença de distribuição deste projeto ainda precisa ser definida.
