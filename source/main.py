import os
import subprocess

from pathlib import Path

from tkinter import *
from tkinter import ttk
from tkinter import font


BASE_DIR = Path(__file__).resolve(strict=True).parent
RCLONE = BASE_DIR / 'rclone/rclone.exe'

# subprocess.run([RCLONE, 'ls'], shell=True)


class Application(Frame):

    def __init__(self, master=None):
        super().__init__(master)

        self.master = master

        self.window_settings()
        self.grid()
        self.create_widgets()


    def create_widgets(self):
        jFont = font.Font(family="맑은 고딕", size=12)

        self.config_button = Button(self, text="구글 드라이브 등록", font =jFont, command=lambda:self.config_btn('new'))

        self.url_input_entry = Entry(self, font=jFont, width=40)
        self.video_list = Listbox(self, font=jFont, width=40)

        self.lookup_button = Button(self, text="조회", font=jFont, command=lambda:self.button_cmd('lookup', self.url_input_entry.get()))
        self.download_button = Button(self, text="다운로드", font=jFont, command=lambda:self.button_cmd('download', self.url_input_entry.get()))
        self.download_prg_bar = ttk.Progressbar(self, length=400, mode='determinate')


        '''
            layout settings
        '''
        self.config_button.grid(row=0, padx=2, pady=2)
        self.url_input_entry.grid(row=1, column=0, padx=2, pady=2)
        self.video_list.grid(row=1, column=1, padx=2, pady=2)
        self.download_button.grid(row=2, column=0, padx=2, pady=2)
        self.lookup_button.grid(row=2, column=1, padx=2, pady=2)
        self.download_prg_bar.grid(row=3, padx=2, pady=2)


        return
    

    def window_settings(self):
        self.master.title("GDRIVE RCLONE")
        self.master.geometry("800x400+0+0")
        self.master.iconbitmap(BASE_DIR / 'static/images/unluckystrike_logo_clear.ico')

        return


    def config_new_window(self):
        self.config_window = Toplevel(self)
        self.config_window.title("CONFIG")
        self.config_window.geometry("800x400+0+0")
        self.config_window.iconbitmap(BASE_DIR / 'static/images/unluckystrike_logo_clear.ico')

        self.config_window.grid()


        self.drive_name_label = Label(self.config_window, text="드라이브 이름")
        self.drive_name_entry = Entry(self.config_window, width=40)
        self.api_id_label = Label(self.config_window, text="API ID")
        self.api_pw_label = Label(self.config_window, text="API PW")
        self.api_id_entry = Entry(self.config_window, width=40)
        self.api_pw_entry = Entry(self.config_window, width=40)
        self.enrollment_btn = Button(self.config_window, text="등록", command=lambda:self.config_btn('enrollment'))
        


        self.drive_name_label.grid(row=0, column=0)
        self.drive_name_entry.grid(row=0, column=1)
        self.api_id_label.grid(row=1, column=0)
        self.api_id_entry.grid(row=1, column=1)
        self.api_pw_label.grid(row=2, column=0)
        self.api_pw_entry.grid(row=2, column=1)
        self.enrollment_btn.grid(row=3, column=3)




    def config_btn(self, value):
        self.new_drive = 'n'
        self.drive_name = ''
        self.drive_code = 'drive'
        self.api_id = ''
        self.api_pw = ''


        if value == 'new':
            self.config_new_window()
        elif value == 'enrollment':
            self.drive_name = self.drive_name_entry.get()
            self.api_id = self.api_id_entry.get()
            self.api_pw = self.api_pw_entry.get()

            key_pair = '[\'' + self.api_id.rstrip() + '\' ' + '\'' + self.api_pw.rstrip() + '\']'
            print(self.api_id)
            print(key_pair)

            subprocess.run([RCLONE, 'config', 'create', self.drive_name, self.drive_code, key_pair, 'false'], shell=True)


    def button_cmd(self, value, url):
        yt = YouTube(url, on_progress_callback=self.progressbar_cmd)

        if value == 'download':
            selection = self.video_list.get(self.video_list.curselection())
            selection = selection.split(' ')
            print(selection)
            pre_itag = selection[1].split('=')
            pre_itag = pre_itag[1].split('"')
            itag = int(pre_itag[1])
            print(itag)
            #d_stream = yt.streams.first()
            d_stream = yt.streams.get_by_itag(itag)
            d_stream.download(BASE_DIR / 'download')
        elif value == 'lookup':
            l_stream = yt.streams

            # video list box init
            self.video_list.delete(0, END)

            for idx, stream in enumerate(l_stream.all()):
                self.video_list.insert(END, str(stream))

            self.video_list.update()
        else:
            return

        return

    
    def progressbar_cmd(self, stream, chunk, bytes_remaining):
        size = stream.filesize
        progress = (float(abs(bytes_remaining - size) / size)) * float(100)
        self.download_prg_bar['value'] = progress
        self.download_prg_bar.update()

        return


def main():
    root = Tk()
    app = Application(master=root)
    app.mainloop()


if __name__ == '__main__':
    main()