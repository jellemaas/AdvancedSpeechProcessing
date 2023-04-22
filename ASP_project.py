from pydub.generators import Sine
import os
import fnmatch
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import glob
import shutil
from resemble import Resemble
import requests
import numpy as np
import librosa
from pydub import AudioSegment
from pydub.effects import speedup
import pretty_midi
import warnings
import noisereduce as nr

KEY = 'INSERT YOUR RESEMBLE AI API KEY'
my_voice_uuid = "FIND YOUR VOICE UUID"

#gives you all the speech
def Lyrics_all():


    Resemble.api_key(KEY)

    page = 1
    page_size = 10

    response = Resemble.v2.projects.all(page, page_size)
    projects = response['items']
    project_uuid = projects[0]['uuid']

    response = Resemble.v2.clips.all(project_uuid, page, page_size)
    clips = response['items']
    url_data_download = clips[0]['audio_src']



    url = url_data_download
    response = requests.get(url)

    # save the audio file to disk
    with open('lyrics.wav', 'wb') as f:
        f.write(response.content)

    print("Resemble.ai API call succesfull, and generated speech is saved as lyrics.wav")

#Lyrics_all()

#if you only want a part of the speech on the website
def Lyrics_loose():



    Resemble.api_key(KEY)

    page = 1
    page_size = 10

    response = Resemble.v2.projects.all(page, page_size)
    projects = response['items']
    project_uuid = projects[0]['uuid']

    response = Resemble.v2.clips.all(project_uuid, page, page_size)
    clips = response['items']
    url_data_download = clips[0]['audio_src']



    url = url_data_download
    response = requests.get(url)

    # save the audio file to disk
    with open('lyrics_loose.wav', 'wb') as f:
        f.write(response.content)

    input_file = "lyrics_loose.wav"  # or .wav
    audio = AudioSegment.from_wav(input_file)  # Use .from_wav for a WAV file

    #split at the time you want to cut it off
    split_time = 96000  # Time in milliseconds, e.g., 10000 ms = 10 seconds

    first_part, second_part = audio[:split_time], audio[split_time:]

    output_file = "lyrics_loose.wav"  # or .mp3
    second_part.export(output_file, format="wav")

    print("Resemble.ai API call succesfull, and generated speech is saved as lyrics_loose.wav")

#Lyrics_loose()

#splits the audio to 15 seconds for the step
def split_audio(input_file, chunk_length_ms=15000):
    audio = AudioSegment.from_wav(input_file)
    audio_length_ms = len(audio)
    output_dir = os.path.dirname(input_file)

    for i in range(0, audio_length_ms, chunk_length_ms):
        chunk = audio[i:i+chunk_length_ms]
        output_file = os.path.join(output_dir, f'chunk_{i//1000}-{(i+chunk_length_ms)//1000}.wav')
        chunk.export(output_file, format="wav")
        print(f'Saved chunk: {output_file}')


#split_audio('lyrics_loose.wav')



def Seleniumtwopointo(file_path,filename):

    driver = webdriver.Chrome()
    chrome_options = Options()
    download_location = r"DOWNLOAD LOCATION"
    prefs = {
        "download.default_directory": download_location,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
    }
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://sites.research.google/tonetransfer")

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "intro__button--text") and contains(@class, "intro__vignette-controls__skip") and text()="Skip intro"]'))).click()

    # More specific CSS selector for the button
    specific_css_selector = '#react-root .intro .intro__landing .intro__buttons .intro__button--primary'
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, specific_css_selector))).click()

    time.sleep(1)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.controls__item__text[data-id="record"]'))).click()

    time.sleep(1)


    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (
        By.CSS_SELECTOR, '.footer-container.footer-container--show-recorder [for="recorder__upload"]'))).click()
    # File upload
    print(file_path)
    file_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
    file_input.send_keys(file_path)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '.MuiButtonBase-root.button.button--primary.recorder__button'))).click()

    # Wait 30 seconds
    time.sleep(30)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.cookie-bar__content .MuiButtonBase-root[tabindex="0"]'))).click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-id="trumpet"]'))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                '.MuiButtonBase-root.player__controls__config[aria-label="Fine tune how your transformation sounds"]'))).click()

    time.sleep(30)

    decrease_output_mix_button = driver.find_element(By.CSS_SELECTOR,
                                                     '.MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeSmall.MuiIconButton-edgeStart[aria-label="Decrease output mix"]')
    for _ in range(12):
        decrease_output_mix_button.click()
        time.sleep(0.5)  # Add a small delay between clicks to avoid potential issues

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                '.MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeSmall.MuiIconButton-edgeStart[aria-label="Decrease loudness"]'))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                '.MuiButtonBase-root.MuiIconButton-root.MuiIconButton-colorInherit[aria-label="close"]'))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                '.MuiButtonBase-root.player__controls__download[aria-label="Download recording and transformations"]'))).click()
    time.sleep(1)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '.download-btn[aria-label="Download trumpet transformation"]'))).click()

    # Change this to the folder where your files are located
    folder_path = r"SELECTPATH"

    # Find the latest file in the folder
    list_of_files = glob.glob(folder_path + "/*")
    latest_file = max(list_of_files, key=os.path.getctime)

    # Set new file name and file type (e.g., new_file_type can be '.txt', '.jpg', etc.)
    integers_string = ''.join(char for char in filename if char.isdigit())
    new_file_name = "ddsp" + integers_string
    new_file_type = ".wav"

    # Rename the file and change its file type
    new_file_path = os.path.join(folder_path, new_file_name + new_file_type)
    shutil.move(latest_file, new_file_path)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                '.MuiButtonBase-root.MuiIconButton-root.MuiIconButton-colorInherit[aria-label="close"]'))).click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                '.MuiButtonBase-root.controls__delete-recording[aria-label="Delete this recording and start new"]'))).click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                                '//button[contains(@class, "MuiButtonBase-root") and contains(@class, "dialog__btn") and text()="Delete"]'))).click()

    driver.quit()
    print("We have done it!")

def Selenium_Operator():
    file_pattern = "chunk_*.wav"
    for filename in os.listdir():
        if fnmatch.fnmatch(filename, file_pattern):
            print(f"Processing file: {filename}")
            file_path = r"SELECTPATH\{}".format(filename)
            Seleniumtwopointo(file_path=file_path,filename=filename)

#Selenium_Operator()

#This function connects all files from the previous step back together
def connect():
    file_pattern = "ddsp*.wav"
    concat_ddsp = 0
    for filename in os.listdir():
        if fnmatch.fnmatch(filename, file_pattern):
            if concat_ddsp == 0:
                concat_ddsp = AudioSegment.from_wav(filename)
            else:
                concat_ddsp = concat_ddsp + AudioSegment.from_wav(filename)
    concat_ddsp.export("concatenated_ddsp.wav", format="wav")

    file_pattern = "chunk_*.wav"
    concat_chunks = 0
    for filename in os.listdir():
        if fnmatch.fnmatch(filename, file_pattern):
            if concat_chunks == 0:
                concat_chunks = AudioSegment.from_wav(filename)
            else:
                concat_chunks = concat_chunks + AudioSegment.from_wav(filename)

    concat_chunks.export("concatenated_chunks.wav", format="wav")

    # Load the two audio segments
    segment2 = AudioSegment.from_wav("concatenated_ddsp.wav")
    segment1 = AudioSegment.from_wav("concatenated_chunks.wav")

    # Reduce the volume of segment2 by 6 dB
    segment2_low_volume = segment2 - 12

    # Overlay the low-volume segment2 onto segment1 using the gain_during_overlay parameter
    synchronized = segment1.overlay(segment2_low_volume, gain_during_overlay=-1)

    # Export the synchronized audio to a new file
    synchronized.export("synchronized.wav", format="wav")

connect()



# Load audio file
audio = AudioSegment.from_file("synchronized.wav", format="wav")

# Speed up audio
audio = speedup(audio, playback_speed=1.15)  # Change this value to adjust the speed (1.2 for a bit faster)

# Convert audio to NumPy array
samples = np.array(audio.get_array_of_samples()).astype(np.float32) / (2**15)

# If the audio is stereo, convert it to mono
if audio.channels == 2:
    samples = librosa.to_mono(samples.reshape(-1, 2).T)

# Adjust the pitch
pitch_shift_n_semitones = -0.7  # Change this value to adjust the pitch (minus is lowering pitch, plus is higher pitch)
samples_shifted = librosa.effects.pitch_shift(samples, sr=audio.frame_rate, n_steps=pitch_shift_n_semitones)

# Convert back to pydub AudioSegment
samples_shifted = (samples_shifted * (2**15)).astype(np.int16)
shifted_audio = AudioSegment(
    samples_shifted.tobytes(),
    frame_rate=audio.frame_rate,
    sample_width=samples_shifted.dtype.itemsize,
    channels=1
)

# Export audio
shifted_audio.export("song_without_drum.mp3", format="mp3")

print("Speech to singing voice succesful and is saved as song_without_drum.mp3")


warnings.filterwarnings("ignore", category=RuntimeWarning)


# Convert to wav file and have all drum sounds to your disposal
bass_drum_path = 'bass_drum.mp3'
bass_drum_dst = "bass_drum.wav"
sound = AudioSegment.from_mp3(bass_drum_path)
sound.export(bass_drum_dst, format="wav")


bass_drum_path = 'drum_hat1.mp3'
bass_drum_dst = "drum_hat1.wav"
sound = AudioSegment.from_mp3(bass_drum_path)
sound.export(bass_drum_dst, format="wav")

bass_drum_path = 'drum_hat2.mp3'
bass_drum_dst = "drum_hat2.wav"
sound = AudioSegment.from_mp3(bass_drum_path)
sound.export(bass_drum_dst, format="wav")

bass_drum_path = 'drum_hat3.mp3'
bass_drum_dst = "drum_hat3.wav"
sound = AudioSegment.from_mp3(bass_drum_path)
sound.export(bass_drum_dst, format="wav")

bass_drum_path = 'drum_low_tom1.mp3'
bass_drum_dst = "drum_low_tom1.wav"
sound = AudioSegment.from_mp3(bass_drum_path)
sound.export(bass_drum_dst, format="wav")

bass_drum_path = 'snare_drum.mp3'
bass_drum_dst = "snare_drum.wav"
sound = AudioSegment.from_mp3(bass_drum_path)
sound.export(bass_drum_dst, format="wav")

bass_drum_path = 'snare_drum2.mp3'
bass_drum_dst = "snare_drum2.wav"
sound = AudioSegment.from_mp3(bass_drum_path)
sound.export(bass_drum_dst, format="wav")

bass_drum_path = 'snare_drum3.mp3'
bass_drum_dst = "snare_drum3.wav"
sound = AudioSegment.from_mp3(bass_drum_path)
sound.export(bass_drum_dst, format="wav")

def generate_drum_notes(note, duration, velocity=100, sample_rate=44100):
    drum_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
    note_number = pretty_midi.note_name_to_number(note)
    # Create a PrettyMIDI object
    # Maybe change initial_tempo accordingly to the actual tempo given by librosa
    midi_data = pretty_midi.PrettyMIDI(initial_tempo=135)
    # Create an Instrument instance
    drum = pretty_midi.Instrument(program=drum_program, is_drum=True)
    # Add a drum note
    drum.notes.append(pretty_midi.Note(velocity, note_number, 0, duration))

    # Add the drum instrument to the PrettyMIDI object
    midi_data.instruments.append(drum)
    # Synthesize the audio and return samples
    samples = midi_data.synthesize(fs=sample_rate)
    # Check if the synthesized audio is silent
    max_abs_value = np.abs(samples).max()
    if max_abs_value == 0:
        # Generate a silent AudioSegment of the desired length
        silence_duration_ms = int(duration * 1000)
        silent_audio = AudioSegment.silent(duration=silence_duration_ms)
        return silent_audio.get_array_of_samples(), sample_rate

    return samples, sample_rate


# Load the original audio file
file_path = 'song_without_drum.mp3'
sound = AudioSegment.from_mp3(file_path)

# Prepare the samples for each drum instrument
kick_samples, sr_kick = generate_drum_notes('C2', 0.5) # Kick drum
snare_samples, sr_snare = generate_drum_notes('D2', 0.5) # Snare drum
hihat_samples, sr_hihat = generate_drum_notes('G2', 0.5) # Hi-hat

# Convert the samples to AudioSegments
def audio_segment_from_samples(samples, sample_rate):
    samples_16bit = (samples * 2**15).astype(np.int16)
    audio_segment = AudioSegment(samples_16bit.tobytes(), frame_rate=sample_rate, sample_width=2, channels=1)
    return audio_segment

kick = audio_segment_from_samples(kick_samples, sr_kick)
snare = audio_segment_from_samples(snare_samples, sr_snare)
hihat = audio_segment_from_samples(hihat_samples, sr_hihat)

file_path_chunks = 'concatenated_chunks.wav'
# Detect beats in the original audio file
y, sr = librosa.load(file_path_chunks, sr=None)  # Set sr=None to use the native sample rate
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
beat_times = librosa.frames_to_time(beat_frames, sr=sr)

print("The tempo of this song is: " + str(tempo) + " Beats per minute")

# Create an empty AudioSegment to hold the mixed sounds
output = AudioSegment.silent(duration=len(sound))

seconds_between_beats = len(sound)/(tempo*1000)
amount = tempo.__floor__()

# Add the drum samples at each detected beat
bass = AudioSegment.from_mp3('bass_drum.mp3')
snare_drum = AudioSegment.from_mp3('snare_drum.mp3')
hat = AudioSegment.from_mp3('drum_hat1.mp3')



i = 0
print(beat_times)
for beat_time in beat_times:
    beat_ms = (beat_time * 1000)
    output = output.overlay(bass, position=beat_ms)

    if i == 1:
        output = output.overlay(snare_drum, position=beat_ms)  # Add some offset to the snare
        i = 0
    else:
        i += 1
        #output = output.overlay(hat, position=beat_ms + 500)  # Add some offset to the hi-hat


#Testing with len(sound)/tempo, does not always sound too good

# i = 0
#
# while i < amount-1:
#     output = output.overlay(bass, position=(i*seconds_between_beats*500))
#     if i % 2 == 0:
#         #Aanpassen voor de grap als je het wil
#         output = output.overlay(bass, position=(i*seconds_between_beats*500))
#     i += 1


# Mix the original audio with the added drum samples
mixed_audio = sound.overlay(output)


# Export the mixed audio to a WAV file
output.export("only_drums.wav", format='wav')
mixed_audio.export('output_audio_with_drums.wav', format='wav')

print('WAV file created: output_audio_with_drums.wav')

# Load the original audio file
original_audio = AudioSegment.from_wav("output_audio_with_drums.wav")

# Create a sine wave for the piano note
piano_note = Sine(220).to_audio_segment(duration=len(sound))
sound = AudioSegment.from_mp3("output_audio_with_drums.wav")

# Calculate the duration of each interval (in milliseconds)
interval_duration = int(len(sound)/int(tempo))

# Create an empty audio segment to hold the final result
final_audio = AudioSegment.silent(duration=len(original_audio))

# Reduce the volume of segment2 by 6 dB
piano_note_low_volume = piano_note - 40

final_audio = final_audio.overlay(piano_note_low_volume, position=0)

# Overlay the original audio onto the final audio with a 1-second crossfade
final_audio = final_audio.overlay(original_audio)

# Export the final audio to a new file
final_audio.export("final_audio.wav", format="wav")



#This part could work, but not very good at the moment
# from pydub import AudioSegment, generators
# from math import pow
#

# # Set the parameters for the melody
# tempo = int(tempo)   # Beats per minute (BPM)
# notes = ['C', 'F', 'G', 'C']   # List of notes
# octave = 4   # Octave of the notes
# beats_per_note = 1   # Number of beats per note
#
# # Calculate the duration of each beat (in milliseconds)
# beat_duration = 60000 / tempo
#
# # Calculate the duration of each note and pause based on the beat duration
# note_duration = int(beat_duration * beats_per_note)
# note_pause = int(beat_duration - note_duration)
#
# # Create an empty audio segment to hold the melody
# melody = AudioSegment.empty()
#
# # Generate the notes using the Sine generator
# for i, note in enumerate(notes):
#     frequency = pow(2, (i + (octave - 4) * 12) / 12) * 440   # Calculate the frequency of the note
#     note_audio = generators.Sine(freq=frequency).to_audio_segment(duration=note_duration)
#     pause_audio = AudioSegment.silent(duration=note_pause)
#     start_time = int(len(sound) / tempo) * i
#     melody = melody.overlay(note_audio, position=start_time) + pause_audio
#
# # Trim the melody to the same length as the sound file
# melody = melody[:len(sound)]
#
# melody = melody - 35
#
# # Mix the melody with the sound file
# mixed = sound.overlay(melody)
#
# # Export the mixed audio to a new file
# mixed.export("mixed.wav", format="wav")
#
# final_audio = final_audio.overlay(AudioSegment.from_mp3("melody.wav"))
#
# final_audio.export("test.wav", format="wav")



