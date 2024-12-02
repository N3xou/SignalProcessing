import numpy as np
import soundfile as sf
from scipy.signal import butter, filtfilt
import os


def lowpass_filter(data, cutoff, fs, order=5):
    """
    Zastosuj filtr dolnoprzepustowy do sygnału audio.

    Parameters:
        data (np.ndarray): Tablica z danymi audio.
        cutoff (float): Częstotliwość odcięcia filtra (Hz).
        fs (int): Częstotliwość próbkowania (Hz).
        order (int): Rząd filtra.

    Returns:
        np.ndarray: Przefiltrowane dane audio.
    """
    nyquist = 0.5 * fs  # Częstotliwość Nyquista
    normal_cutoff = cutoff / nyquist  # Znormalizowana częstotliwość odcięcia
    b, a = butter(order, normal_cutoff, btype='low', analog=False)  # Współczynniki filtra
    filtered_data = filtfilt(b, a, data)  # Przefiltrowany sygnał
    return filtered_data


def main():
    # Wczytaj plik audio
    input_file = input("Podaj ścieżkę do pliku audio (np. 'plik.wav'): ").strip()
    if not os.path.exists(input_file):
        print("Plik nie istnieje. Upewnij się, że podałeś poprawną ścieżkę.")
        return

    data, samplerate = sf.read(input_file)

    # Obsługa plików stereo: konwertuj na mono, jeśli jest potrzebne
    if len(data.shape) > 1:
        print("Wykryto sygnał stereo. Konwertuję na mono, uśredniając kanały.")
        data = data.mean(axis=1)

    # Parametry filtra
    cutoff = float(input("Podaj częstotliwość odcięcia filtra (Hz) (np. 15000): ").strip())
    order = int(input("Podaj rząd filtra (np. 5): ").strip())

    # Przefiltruj dane
    print("Nakładam filtr dolnoprzepustowy...")
    filtered_data = lowpass_filter(data, cutoff, samplerate, order)

    # Zapisz wynik do nowego pliku
    output_file = "filtered_" + os.path.basename(input_file)
    sf.write(output_file, filtered_data, samplerate)
    print(f"Przefiltrowany plik zapisano jako: {output_file}")


if __name__ == "__main__":
    main()
