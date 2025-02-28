import tkinter
import customtkinter
import pygame
from PIL import Image
from threading import Thread, Event
import time
import random

# Initialize Pygame Mixer
pygame.mixer.init()

class MusicPlayer:
    def __init__(self):
        self.root = customtkinter.CTk()
        self.root.title('Music Player')
        self.root.geometry('450x600')
        # State management
        self.is_paused = True
        self.is_repeating = False
        self.is_shuffled = False
        self.volume = 1.0
        self.is_seeking = False
        # Song lists
        self.list_of_songs = ['music/DNA.mp3', 'music/hey now.mp3', 'music/PRIDE.mp3', 'music/Wesley Theory.mp3']
        self.list_of_covers = ['img/DAMN.jpg', 'img/GNX.png', 'img/DAMN.jpg', 'img/TPAB.png']
        self.current_song_index = 0
        # Load icons once
        self.icons = {
            'play': customtkinter.CTkImage(Image.open("icons/play.png"), size=(20, 20)),
            'pause': customtkinter.CTkImage(Image.open("icons/pause.png"), size=(20, 20)),
            'skip_next': customtkinter.CTkImage(Image.open("icons/skip_next.png"), size=(20, 20)),
            'skip_prev': customtkinter.CTkImage(Image.open("icons/skip_prev.png"), size=(20, 20)),
            'shuffle_on': customtkinter.CTkImage(Image.open("icons/shuffle_on.png"), size=(20, 20)),
            'shuffle_off': customtkinter.CTkImage(Image.open("icons/shuffle_off.png"), size=(20, 20)),
            'repeat_on': customtkinter.CTkImage(Image.open("icons/repeat_on.png"), size=(20, 20)),
            'repeat_off': customtkinter.CTkImage(Image.open("icons/repeat_off.png"), size=(20, 20))
        }
        # Define methods before they're used
        self.setup_ui()

    def setup_ui(self):
        # Progress Slider
        self.progress_frame = customtkinter.CTkFrame(self.root, fg_color="transparent")
        self.progress_frame.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)
        self.progress_slider = customtkinter.CTkSlider(
            self.progress_frame,
            from_=0,
            to=100,
            command=self.seek,
            width=250,
            height=4,
            progress_color='#1DB954',
            button_color='#1DB954',
            button_hover_color='#1DB954'
        )
        self.progress_slider.set(0)
        self.progress_slider.pack(side="left", padx=5)

        # Control Buttons
        self.controls_frame = customtkinter.CTkFrame(self.root, fg_color="transparent")
        self.controls_frame.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
        
        # Shuffle Button moved to left side
        self.shuffle_button = customtkinter.CTkButton(
            self.controls_frame,
            image=self.icons['shuffle_off'],
            text="",
            width=35,
            height=35,
            corner_radius=20,
            fg_color="transparent",
            hover_color="gray30",
            command=self.toggle_shuffle
        )
        self.shuffle_button.pack(side="left", padx=5)

        skip_prev_button = customtkinter.CTkButton(
            self.controls_frame,
            image=self.icons['skip_prev'],
            text="",
            width=35,
            height=35,
            corner_radius=20,
            fg_color="transparent",
            hover_color="gray30",
            command=self.skip_backward
        )
        skip_prev_button.pack(side="left", padx=5)

        self.play_pause_button = customtkinter.CTkButton(
            self.controls_frame,
            image=self.icons['play'],
            text="",
            width=35,
            height=35,
            corner_radius=20,
            fg_color="transparent",
            hover_color="gray30",
            command=self.play_music
        )
        self.play_pause_button.pack(side="left", padx=5)

        skip_next_button = customtkinter.CTkButton(
            self.controls_frame,
            image=self.icons['skip_next'],
            text="",
            width=35,
            height=35,
            corner_radius=20,
            fg_color="transparent",
            hover_color="gray30",
            command=self.skip_forward
        )
        skip_next_button.pack(side="left", padx=5)

        self.repeat_button = customtkinter.CTkButton(
            self.controls_frame,
            image=self.icons['repeat_off'],
            text="",
            width=35,
            height=35,
            corner_radius=20,
            fg_color="transparent",
            hover_color="gray30",
            command=self.toggle_repeat
        )
        self.repeat_button.pack(side="left", padx=5)

        # Volume Slider
        self.volume_frame = customtkinter.CTkFrame(self.root, fg_color="transparent")
        self.volume_frame.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)
        volume_label = customtkinter.CTkLabel(
            self.volume_frame,
            text="Volume",
            font=('Poppins', 10),
            text_color='white'
        )
        volume_label.pack(side="left", padx=5)
        self.volume_slider = customtkinter.CTkSlider(
            self.volume_frame,
            from_=0,
            to=1,
            command=self.set_volume,
            width=150,
            height=4,
            progress_color='#1DB954',
            button_color='#1DB954',
            button_hover_color='#1DB954'
        )
        self.volume_slider.set(self.volume)
        self.volume_slider.pack(side="left", padx=5)
        self.initialize_player()

    def toggle_shuffle(self):
        self.is_shuffled = not self.is_shuffled
        self.shuffle_button.configure(image=(
            self.icons['shuffle_on'] if self.is_shuffled
            else self.icons['shuffle_off']
        ))

    def toggle_repeat(self):
        self.is_repeating = not self.is_repeating
        self.repeat_button.configure(image=(
            self.icons['repeat_on'] if self.is_repeating
            else self.icons['repeat_off']
        ))

    def set_volume(self, value):
        self.volume = float(value)
        pygame.mixer.music.set_volume(self.volume)

    def initialize_player(self):
        self.get_album_cover(self.list_of_songs[self.current_song_index], self.current_song_index)
        pygame.mixer.music.set_volume(self.volume)

    def get_album_cover(self, song_name, n):
        try:
            if hasattr(self, 'song_name_label') and self.song_name_label:
                self.song_name_label.destroy()
            if hasattr(self, 'album_cover_label') and self.album_cover_label:
                self.album_cover_label.destroy()
            img1 = Image.open(self.list_of_covers[n])
            img2 = img1.resize((250, 250))
            load = customtkinter.CTkImage(img2, size=(250, 250))
            self.album_cover_label = customtkinter.CTkLabel(
                self.root,
                image=load,
                text=""
            )
            self.album_cover_label.image = load
            self.album_cover_label.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)
            stripped_string = song_name[6:-4]  # Remove 'music/' and '.mp3'
            self.song_name_label = customtkinter.CTkLabel(
                self.root,
                text=stripped_string,
                font=('Poppins', 16, 'bold'),
                text_color='white'
            )
            self.song_name_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        except Exception as e:
            print(f"Error loading cover: {e}")

    def reset_progress(self):
        """Reset progress bar"""
        self.progress_slider.set(0)

    def skip_forward(self):
        """Skip to next song in playlist"""
        self.current_song_index = (self.current_song_index + 1) % len(self.list_of_songs)
        self.reset_progress()
        pygame.mixer.music.stop()
        self.play_music()

    def skip_backward(self):
        """Skip to previous song in playlist"""
        self.current_song_index = (self.current_song_index - 1) % len(self.list_of_songs)
        self.reset_progress()
        pygame.mixer.music.stop()
        self.play_music()

    def seek(self, value):
        try:
            self.is_seeking = True
            song_length = pygame.mixer.Sound(f'{self.list_of_songs[self.current_song_index]}').get_length()
            seek_time = (float(value) / 100) * song_length
            pygame.mixer.music.set_pos(seek_time)
        except Exception as e:
            print(f"Error seeking: {e}")
            self.reset_progress()
        self.is_seeking = False

    def progress(self):
        """Handle song progress tracking"""
        try:
            song_length = pygame.mixer.Sound(f'{self.list_of_songs[self.current_song_index]}').get_length()
            
            while pygame.mixer.music.get_busy() or self.is_paused:
                if not self.is_seeking:
                    current_time = pygame.mixer.music.get_pos() / 1000
                    
                    if current_time <= 0 and not self.is_paused:
                        if self.is_repeating:
                            self.reset_progress()
                            pygame.mixer.music.stop()
                            self.play_music()
                        else:
                            self.skip_forward()
                
                    if current_time > 0:
                        self.progress_slider.set(current_time / song_length * 100)
            
                time.sleep(0.1)
        
        except Exception as e:
            print(f"Error in progress tracking: {e}")
            self.reset_progress()

    def play_music(self):
        """Handle play/pause functionality"""
        try:
            if not pygame.mixer.music.get_busy():
                song_name = self.list_of_songs[self.current_song_index]
                pygame.mixer.music.load(song_name)
                pygame.mixer.music.play()
                self.get_album_cover(song_name, self.current_song_index)
                Thread(target=self.progress).start()
                self.play_pause_button.configure(image=self.icons['pause'])  # Set pause icon immediately
            else:
                if self.is_paused:
                    pygame.mixer.music.unpause()
                    self.play_pause_button.configure(image=self.icons['pause'])
                else:
                    pygame.mixer.music.pause()
                    self.play_pause_button.configure(image=self.icons['play'])
        
            self.is_paused = not self.is_paused
        
        except Exception as e:
            print(f"Error playing music: {e}")
            self.is_paused = False

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    player = MusicPlayer()
    player.run()