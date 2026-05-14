import io
import wave
from pathlib import Path

import numpy as np
import onnxruntime as rt

from kokoro_onnx.config import SAMPLE_RATE, MAX_PHONEME_LENGTH
from kokoro_onnx.tokenizer import Tokenizer

MODEL_PATH  = Path(__file__).parent.parent / "tts-models" / "model.onnx"
VOICES_PATH = Path(__file__).parent.parent / "tts-models" / "voices.npz"
VOICE = "ff_siwis"
LANG  = "fr-fr"
SPEED = 1.0

_sess   = None
_voices = None
_tok    = None


def _load():
    global _sess, _voices, _tok
    if _sess is None:
        _sess   = rt.InferenceSession(str(MODEL_PATH), providers=["CPUExecutionProvider"])
        _voices = np.load(str(VOICES_PATH))
        _tok    = Tokenizer()


def _synth_chunk(phonemes: str, voice_row: np.ndarray) -> np.ndarray:
    tokens     = np.array(_tok.tokenize(phonemes), dtype=np.int64)
    style      = voice_row[len(tokens)].reshape(1, -1)   # (1, 256)
    input_ids  = np.array([[0, *tokens.tolist(), 0]], dtype=np.int64)
    speed      = np.array([SPEED], dtype=np.float32)
    audio      = _sess.run(None, {"input_ids": input_ids, "style": style, "speed": speed})[0]
    return audio


def synthesize(text: str) -> bytes:
    _load()
    voice_row = _voices[VOICE]              # (510, 256)
    phonemes  = _tok.phonemize(text, LANG)

    # Split en morceaux si trop long
    chunks = []
    current = ""
    for part in phonemes.split():
        if len(current) + len(part) + 1 >= MAX_PHONEME_LENGTH:
            if current:
                chunks.append(current.strip())
            current = part
        else:
            current += " " + part
    if current.strip():
        chunks.append(current.strip())

    audio = np.concatenate([_synth_chunk(c, voice_row) for c in chunks]) if chunks else np.array([], dtype=np.float32)

    audio_i16 = (np.clip(audio, -1, 1) * 32767).astype(np.int16)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_i16.tobytes())
    return buf.getvalue()
