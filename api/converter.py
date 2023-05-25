import uuid
from pydub import AudioSegment

from fastapi import UploadFile, HTTPException


def save_audio(user_id: str, file: UploadFile, file_id: uuid.uuid4):
    path = f"./{user_id}_{file_id}.mp3"
    if file.content_type != "audio/wav":
        raise HTTPException(
            status_code=406, detail="Not an .mp3 format file were provided"
        )
    to_mp3(path, file)
    return path


def to_mp3(file_name: str, file: UploadFile):
    AudioSegment.from_wav(file.file).export(file_name, format="mp3")
