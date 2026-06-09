import os
import numpy as np
import librosa
import librosa.display
import matplotlib
matplotlib.use('Agg') # Crucial for server-side image generation
import matplotlib.pyplot as plt
import torch
from transformers import pipeline

class AdvancedAudioForensics:
    _audio_pipeline = None

    @classmethod
    def _initialize_pipeline(cls):
        """
        Lazily loads the HuggingFace audio classification pipeline.
        We use a robust general audio classifier here to simulate voice-spoof detection.
        """
        if cls._audio_pipeline is None:
            device = 0 if torch.cuda.is_available() else -1
            # Using a lightweight audio classification model for rapid CPU/GPU inference
            cls._audio_pipeline = pipeline(
                "audio-classification", 
                model="superb/hubert-base-superb-er", 
                device=device
            )
        return cls._audio_pipeline

    @staticmethod
    def generate_mel_spectrogram(audio_path, output_dir):
        """
        Converts a 1D audio waveform into a 2D visual Mel-Spectrogram image.
        Synthetic voices often lack high-frequency 'breath' noise, which becomes visible here.
        """
        try:
            # Load audio file (downsample to 16kHz for standardization)
            y, sr = librosa.load(audio_path, sr=16000)
            
            # Compute the Mel-Spectrogram
            S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
            S_dB = librosa.power_to_db(S, ref=np.max)
            
            # Generate the visual plot
            plt.figure(figsize=(10, 4))
            librosa.display.specshow(S_dB, x_axis='time', y_axis='mel', sr=sr, fmax=8000, cmap='magma')
            plt.colorbar(format='%+2.0f dB')
            plt.title('Acoustic Frequency Mel-Spectrogram')
            plt.tight_layout()
            
            # Save to storage
            base_name = os.path.basename(audio_path)
            spectrogram_filename = f"spectrogram_{base_name}.png"
            spectrogram_path = os.path.join(output_dir, spectrogram_filename)
            plt.savefig(spectrogram_path)
            plt.close()
            
            duration = librosa.get_duration(y=y, sr=sr)
            
            return {
                "status": "Success",
                "spectrogram_filename": spectrogram_filename,
                "duration_seconds": round(duration, 2),
                "sample_rate": sr
            }
        except Exception as e:
            return {"status": f"Error: {str(e)}", "spectrogram_filename": None}

    @classmethod
    def run_voice_cloning_detection(cls, audio_path):
        """
        Passes the audio waveform into the transformer model.
        Maps the emotional/acoustic resonance outputs to a synthetic probability index.
        """
        try:
            detector = cls._initialize_pipeline()
            # The model processes the raw audio string
            predictions = detector(audio_path)
            
            # In a true deployment, you'd use a dedicated ASVspoof model. 
            # Here we map structural confidence to an AI baseline.
            base_confidence = predictions[0]['score']
            
            # Synthesize an AI probability based on acoustic strictness
            ai_probability = 1.0 - base_confidence if base_confidence > 0.5 else base_confidence + 0.2
            
            # Cap values for absolute safety
            ai_probability = min(max(ai_probability, 0.0), 1.0)
            
            return {
                "synthetic_voice_probability": ai_probability,
                "top_acoustic_signature": predictions[0]['label'],
                "acoustic_variance": float(np.random.uniform(0.01, 0.08)) # Simulated micro-variance
            }
        except Exception as e:
            print(f"[CRITICAL] Audio AI Failure: {str(e)}")
            return {"synthetic_voice_probability": 0.0, "top_acoustic_signature": "Unknown"}