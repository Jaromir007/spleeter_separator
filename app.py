import os
import tkinter as tk
from tkinter import ttk, filedialog
from threading import Thread
from audio_separator import AudioSeparator
import webbrowser
from PIL import Image, ImageTk


class App:
    def __init__(self, root):
        self.start_icon = None
        self.audio_icon = None
        self.folder_icon = None
        self.file_label = None
        self.status_label = None
        self.configuration_combobox = None
        self.root = root
        self.root.title('Spleeter separator')
        self.root.geometry('600x300')
        self.create_widgets()
        self.output_folder = 'out'
        self.set_window_icon('icons/spleeter_icon.png')

    def set_window_icon(self, icon_path):
        icon_image = Image.open(icon_path)
        icon_photo = ImageTk.PhotoImage(icon_image)
        self.root.iconphoto(False, icon_photo)

    def create_widgets(self):
        # style
        style = ttk.Style(self.root)
        style.theme_use('clam')

        def load_icon(path, size=(28, 28)):
            image = Image.open(path)
            image = image.resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(image)

        # Add icons
        self.folder_icon = load_icon('icons/folder_icon.png')
        self.audio_icon = load_icon('icons/audio_icon.png')
        self.start_icon = load_icon('icons/start_icon.png')

        # selected file path
        self.file_label = tk.Label(self.root, text='', width=70)
        self.file_label.pack(pady=5)

        # select an audio file
        select_button = tk.Button(self.root, text='Select Audio File', image=self.audio_icon, compound=tk.LEFT,
                                  command=self.select_audio_file, padx=10, pady=5)
        select_button.pack(pady=5)

        # output folder
        output_button = tk.Button(self.root, text='Select Output Folder', image=self.folder_icon, compound=tk.LEFT,
                                  command=self.select_output_folder, padx=10, pady=5)
        output_button.pack(pady=5)

        # start the separation process
        start_button = tk.Button(self.root, text='Start Separation', image=self.start_icon, compound=tk.LEFT,
                                 command=self.start_separation, padx=10, pady=5)
        start_button.pack(pady=5)

        # status of the operation
        self.status_label = tk.Label(self.root, text='')
        self.status_label.pack(pady=5)

        self.configuration_combobox = ttk.Combobox(self.root,
                                                   values=['2 stems', '4 stems', '5 stems'], state='readonly', width=67)
        self.configuration_combobox.pack(pady=5)
        self.configuration_combobox.set('2 stems')

    def select_output_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_folder = folder_path
            self.status_label.config(text=f'Output folder selected: {folder_path}')

    def start_separation(self):
        audio_file = self.file_label.cget("text")
        configuration = self.configuration_combobox.get()
        if audio_file:
            self.status_label.config(text='Separating, please wait...')
            # Pass the configuration to the thread
            Thread(target=self.separate_audio_thread, args=(audio_file, configuration)).start()
        else:
            self.status_label.config(text='Please select an audio file first.')

    def separate_audio_thread(self, audio_file, configuration):
        config_map = {'2 stems': 'spleeter:2stems', '4 stems': 'spleeter:4stems', '5 stems': 'spleeter:5stems'}
        separator = AudioSeparator(configuration=config_map[configuration])
        success, message = separator.separate(audio_file, self.output_folder)
        if success:
            # Replace the text with a link to the output folder
            self.status_label.config(text='Completed successfully! Click here to open',
                                     fg='blue', cursor='hand2')
            self.status_label.bind("<Button-1>", lambda e: self.open_output_folder())
        else:
            self.status_label.config(text=message)

    def open_output_folder(self):
        audio_file_base_name = os.path.splitext(os.path.basename(self.file_label.cget("text")))[0]
        spleeter_subfolder_path = os.path.join(self.output_folder, audio_file_base_name)
        webbrowser.open(os.path.realpath(spleeter_subfolder_path))

    def select_audio_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3")])
        if file_path:
            self.file_label.config(text=file_path)
            self.status_label.config(text='')