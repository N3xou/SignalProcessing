import pyaudio
import wave
import threading

# Parametry audio
CHUNK = 1024  # Rozmiar bufora
FORMAT = pyaudio.paInt16  # Format danych audio (16-bitowy int)
CHANNELS = 1  # Liczba kanałów (1 = mono)
RATE = 44100  # Częstotliwość próbkowania (Hz)
OUTPUT_FILENAME = "nagranie.wav"  # Nazwa pliku wyjściowego

# Flaga kontrolująca stan nagrywania
is_recording = False


def record_audio():
    """Nagrywa dźwięk do pliku, dopóki flaga `is_recording` jest True."""
    global is_recording

    # Inicjalizacja PyAudio
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    frames = []
    print("Nagrywanie... Naciśnij ENTER, aby zatrzymać.")

    while is_recording:
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)

    print("Nagrywanie zakończone.")

    # Zamknij strumień i zakończ PyAudio
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Zapisz nagranie do pliku WAV
    with wave.open(OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"Plik zapisano jako: {OUTPUT_FILENAME}")


def main():
    global is_recording

    while True:
        command = input("Wpisz 'start', aby rozpocząć nagrywanie lub 'exit', aby zakończyć program: ").strip().lower()

        if command == 'start' and not is_recording:
            is_recording = True
            # Uruchom nagrywanie w osobnym wątku, aby można było zatrzymać je w dowolnym momencie
            recording_thread = threading.Thread(target=record_audio)
            recording_thread.start()

            # Czekaj na ENTER, aby zatrzymać nagrywanie
            input()
            is_recording = False
            recording_thread.join()

        elif command == 'exit':
            print("Zamykam program.")
            break
        else:
            print("Nieznana komenda. Wpisz 'start' lub 'exit'.")


if __name__ == "__main__":
    main()
