import openai
import os
import language_tool_python

openai.api_key = "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"



def improve_transcription(transcription):
    try:
        # Call GPT model to improve the transcription's syntax and grammar
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Updated to GPT-4 or use "gpt-3.5-turbo" as needed
            messages=[
                {"role": "system", "content": "You are a helpful assistant improving grammar and syntax."},
                {"role": "user", "content": f"Improve the grammar and syntax of the following text:\n\n{transcription}"}
            ],
            max_tokens=1000
        )

        improved_text = response['choices'][0]['message']['content'].strip()
        return improved_text

    except Exception as e:
        print(f"Error improving transcription: {e}")
        return transcription

def transcribe_audio(audio_file_path):
    try:
        # Open the audio file
        with open(audio_file_path, "rb") as audio_file:
            # Send the audio file to OpenAI's Whisper model for transcription
            response = openai.Audio.transcribe(
                model="whisper-1",  # Whisper model ID
                file=audio_file
            )
        
        # Get the transcribed text
        transcription = response['text']
        
        # Improve the transcription's grammar and syntax
        improved_transcription = improve_transcription(transcription)

        # Save the improved transcription to a text file with utf-8 encoding
        with open("improved_transcription_result.txt", "w", encoding="utf-8") as text_file:
            text_file.write(improved_transcription)
        
        return improved_transcription

    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None

# Example usage
audio_path = "theking.mp3"  # Path to the audio file you extracted
transcription = transcribe_audio(audio_path)

if transcription:
    print("Improved Transcription Result:", transcription)
