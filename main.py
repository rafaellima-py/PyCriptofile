import customtkinter as ctk
from pathlib import Path
from PIL import Image
from tkinter.filedialog import askdirectory
import pyAesCrypt
from time import sleep

# Importando icones
lock_icone = ctk.CTkImage(Image.open('_icones/lock.png'), size=(50,50))
unlock_icone = ctk.CTkImage(Image.open('_icones/unlock.png'), size=(50,50))
cript_icone = ctk.CTkImage(Image.open('_icones/criptografar.png'), size=(50,50))
senha_icone = ctk.CTkImage(Image.open('_icones/senha.png'), size=(50,50))
arquivo_icone =ctk.CTkImage(Image.open('_icones/arquivo.png'), size=(50,50))
logo_icone =ctk.CTkImage(Image.open('_icones/logo.png'), size=(300,300))

            #Funções 
file_g = ''                                   # váriáveis globais
senha_g = ''
buffersize = ''

def c_select_file():
    global file_g
    file = askdirectory()
    print(file)
    c_mensagem.set(f'Diretório selecionado: {file}')
    file_g = file

def d_select_file():
    global file_g
    dfile = askdirectory()
    print(dfile)
    d_mensagem.set(f'Diretório selecionado: {dfile}')
    file_g = dfile


#            CRIPTOGRAFIA  / DESCRIPTOGRAFIA           #
def criptografia():
    senha = c_input_senha.get()
    print(senha)
    if senha == '':
        c_erro.set('')
        c_erro.set('Você não digitou uma senha')
        c_sucesso.set('')
        return
    if file_g == '':
        c_erro.set('')
        c_erro.set('Você não informou um diretório')
        c_sucesso.set('')
        return
    else:
        c_sucesso.set('Em andamento. Talvez isso demore um pouco')
        criptografar_label.after(1000)
        
        def criptografar_arquivos():
            dir = Path(file_g)
            pasta = dir.glob('**/*')
            for arquivo in pasta:
                if arquivo.is_file():
                    pyAesCrypt.encryptFile(infile=f'{arquivo}', outfile=f'{arquivo.absolute()}.pct', passw=senha, bufferSize=1024*1024)
                    arquivo.unlink()
        c_sucesso.set('Em andamento. Talvez isso demore um pouco')
        criptografar_arquivos()
        c_erro.set('')
        c_sucesso.set('Sucesso')
        c_progresso.place_forget()
        
 




def descriptografia():
    senha = d_input_senha.get()
    if senha == '':
        d_erro.set('')
        d_erro.set('Você não digitou uma senha')
        d_sucesso.set('')
        return
    if file_g == '':
        d_erro.set('')
        d_erro.set('Você não informou um diretório')
        d_sucesso.set('')
        return
    
    else:
        d_sucesso.set('Em andamento. Talvez isso demore um pouco')
        sleep(1)
        dir = Path(file_g)
        pasta = dir.glob('**/*.pct')
    
        for arquivo in  pasta:
            if arquivo.is_file():
                original = arquivo.with_suffix('')
                
                try:
                    pyAesCrypt.decryptFile(str(arquivo), str(original), passw=senha, bufferSize=1024*1024)
                    if '.pct' in arquivo.name:
                        arquivo.unlink()
                except ValueError:
                    d_erro.set('A senha está incorreta')
                    return
     
        d_erro.set('')
        d_sucesso.set('Sucesso')
    
    print('A função continua')
  

#       CONFIGURAR TRANSIÇÃO DO MENU
def transicao_criptografar():
    descriptografar_label.place_forget()
    criptografar_label.place(y=0, x=210)

def transicao_desciptografar():
    criptografar_label.place_forget()
    descriptografar_label.place(y=0, x=210)

def transicao_bruteforce():
    criptografar_label.place_forget()
    descriptografar_label.place_forget()
    bruteforce_label.place(y=0, x=210)



ctk.set_appearance_mode('dark')
app = ctk.CTk()
app.geometry('800x500')
app.resizable(False, False)
app.iconbitmap('_icones/icon.ico')
app.title('PyCryptoFile')




menu_frame = ctk.CTkFrame(app, 200,600).place(rely=0.0, relx=0.0)
lock_bt = ctk.CTkButton(menu_frame, width=210, height=50, image=lock_icone,command=transicao_criptografar)
lock_bt.configure( text='  CRIPTOGRAFAR  ',font=('Pacifico', 13),fg_color='transparent',hover_color='#191919')
lock_bt.place(y=190-60, x=-10)

unlock_bt = ctk.CTkButton(menu_frame, width=202, height=50, image=unlock_icone,command=transicao_desciptografar)
unlock_bt.configure( text='DESCRIPTOGRAFAR',font=('Pacifico', 13),fg_color='transparent',hover_color='#191919')
unlock_bt.place(y=190, x=-2)

brutef_bt = ctk.CTkButton(menu_frame, width=210, height=50, image=senha_icone,command=transicao_bruteforce)
brutef_bt.configure( text='  BRUTEFORCE   ',font=('Pacifico', 14),fg_color='transparent',hover_color='#191919')
brutef_bt.place(y=250, x=-10)

criptografar_label = ctk.CTkFrame(app, 590,600)
criptografar_label.place_forget()
descriptografar_label = ctk.CTkFrame(app, 590,600)
descriptografar_label.place_forget()


descriptografar_label.place(y=0, x=210)
# Construção do frame criptofrafia
c_img_logo = ctk.CTkLabel(criptografar_label, width=200,height=200, image=logo_icone,text='')
c_img_logo.place(y=0, x=100)


bt_selec_file = ctk.CTkButton(criptografar_label,text='Selecione a pasta', image=arquivo_icone,command=c_select_file)
bt_selec_file.configure(fg_color='transparent',hover_color='gray', font=('',15),)
bt_selec_file.place(y=200+50, x=10)

c_input_senha = ctk.CTkEntry(criptografar_label,
placeholder_text='Insira uma senha segura', width=320, show='*', font=('',15))
c_input_senha.place(y=215+50, x=210)


bt_criptografar = ctk.CTkButton(criptografar_label,text='Criptografar', image=cript_icone, command=criptografia)
bt_criptografar.configure(fg_color='transparent',hover_color='gray', font=('',15))
bt_criptografar.place(y=270+50, x=200)




#Construção do frame descriptografia 
d_img_logo = ctk.CTkLabel(descriptografar_label, width=200,height=200, image=logo_icone,text='')
d_img_logo.place(y=0, x=100)


bt_selec_file = ctk.CTkButton(descriptografar_label,text='Selecione a pasta', image=arquivo_icone,command=d_select_file)
bt_selec_file.configure(fg_color='transparent',hover_color='gray', font=('',15))
bt_selec_file.place(y=200+50, x=10)

d_input_senha = ctk.CTkEntry(descriptografar_label,
placeholder_text='Insira a senha da pasta', width=320, show='*', font=('',15))
d_input_senha.place(y=215+50, x=210)


bt_criptografar = ctk.CTkButton(descriptografar_label,text='Descriptografar', image=cript_icone, command=descriptografia)
bt_criptografar.configure(fg_color='transparent',hover_color='gray', font=('',15))
bt_criptografar.place(y=270+50, x=200)

    # Exibindo mensagens e erros criptografia
c_sucesso = ctk.StringVar()
c_sucesso_t= ctk.CTkLabel(criptografar_label, textvariable=c_sucesso, font=('',15),text_color='green')
c_sucesso_t.place(y=420, x=215)

c_mensagem = ctk.StringVar()
c_mensagem_t= ctk.CTkLabel(criptografar_label, textvariable=c_mensagem, font=('',10))
c_mensagem_t.place(y=450, x=15)

c_erro = ctk.StringVar()
c_erro_t = ctk.CTkLabel(criptografar_label, textvariable=c_erro, font=('',15),text_color='red')
c_erro_t.place(y=400, x=215)

# Mensagens e erros descriptofrafia
    
d_sucesso = ctk.StringVar()
d_sucesso_t= ctk.CTkLabel(descriptografar_label, textvariable=d_sucesso, font=('',15),text_color='green')
d_sucesso_t.place(y=420, x=215)

d_mensagem = ctk.StringVar()
d_mensagem_t= ctk.CTkLabel(descriptografar_label, textvariable=d_mensagem, font=('',10), )
d_mensagem_t.place(y=450, x=15)

d_erro = ctk.StringVar()
d_erro_t= ctk.CTkLabel(descriptografar_label, textvariable=d_erro, font=('',15),text_color='red')
d_erro_t.place(y=400, x=215)

## Barras de progresso
c_progresso = ctk.CTkProgressBar(criptografar_label, width=500, progress_color='#191919')
c_progresso.place_forget()
d_progresso = ctk.CTkProgressBar(descriptografar_label, width=500, progress_color='#191919')
d_progresso.place_forget()
app.mainloop()

# Frame BruteForce
bruteforce_label = ctk.CTkFrame(app,590,600)
