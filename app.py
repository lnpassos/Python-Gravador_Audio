import customtkinter
import pyaudio
import wave

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

janela = customtkinter.CTk()
janela.geometry('500x300')

header = customtkinter.CTkLabel(janela, text="Gravador de Áudio", text_color='white')
header.pack(padx=10, pady=10)

gravando_label = None

def iniciar_gravacao():
    global gravando_label
    if not gravando_label:
        gravando_label = customtkinter.CTkLabel(janela, text="Gravando...", text_color='lightblue')
        gravando_label.pack(padx=10, pady=10)

        global frames
        frames = []

        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=pyaudio.paInt32,
            channels=1,
            rate=44000,
            input=True,
            frames_per_buffer=1024
        )

        def gravar_audio():
            try:
                while True:
                    bloco = stream.read(1024)
                    frames.append(bloco)
            except KeyboardInterrupt:
                pass

        import threading
        gravacao_thread = threading.Thread(target=gravar_audio)
        gravacao_thread.start()

def finalizar_gravacao():
    global gravando_label
    if gravando_label:
        gravando_label.destroy()

        sucesso_label = customtkinter.CTkLabel(janela, text="Gravação realizada com sucesso!", text_color='lightgreen')
        sucesso_label.pack(padx=10, pady=10)

        global frames
        if frames:
            arquivo_audio = wave.open('gravacao.wav', 'wb')
            arquivo_audio.setnchannels(1)
            arquivo_audio.setframerate(44000)
            arquivo_audio.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt32))
            arquivo_audio.writeframes(b''.join(frames))
            arquivo_audio.close()

        janela.after(1000, janela.destroy)

iniciaGravacao = customtkinter.CTkButton(janela, text='GRAVAR', command=iniciar_gravacao)
iniciaGravacao.pack(padx=10, pady=10)

finalizaGravacao = customtkinter.CTkButton(janela, text='FINALIZAR GRAVAÇÃO', command=finalizar_gravacao)
finalizaGravacao.pack(padx=10, pady=10)

janela.mainloop()
