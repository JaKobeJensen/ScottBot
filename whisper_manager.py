from transformers import WhisperProcessor, WhisperForConditionalGeneration
from scipy.io import wavfile


class WhisperManager:
    def __init__(self, model: str="large-v2") -> None:
        self.processor = WhisperProcessor.from_pretrained("openai/whisper-{model}")
        self.model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-{model}")
        self.model.config.forced_decoder_ids = None
        return

    # transcirbes audio from an audio file
    def transcribe_audio_file(self, audio_file_path: str) -> str:
        # opening and reading audio file
        sample_rate, data = wavfile.read(audio_file_path)
        return self.transcribe_audio_data(data, sample_rate)

    # transcribes audio from audio data
    def transcribe_audio_data(self, data: list, sample_rate: int=44100) -> str:
        # reading audio data
        input_features = self.processor(data, sampling_rate=sample_rate, return_tensors="pt").input_features 
        
        # generate token ids
        predicted_ids = self.model.generate(input_features)
        
        # decode token ids to text
        transcription = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        return transcription
