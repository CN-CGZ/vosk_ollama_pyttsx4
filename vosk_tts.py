import requests
import pyttsx4
import pyaudio
from vosk import Model, KaldiRecognizer
import json
import sys

CONFIG = {
    "base_url": "http://大模型接口地址",# 替换为实际的URL
    "history_file": "chat_history.json",# 替换为实际的历史记录文件名
    "max_history": 0,# 最大历史记录条数，0表示不限制
    "model": "model_name",# 替换为实际的模型名称
    "enable_tts": False
}

def text_to_speech(text):
    clean_text = text.replace("<think>", "").replace("</think>", "").strip()
    if not clean_text:
        return
    engine = pyttsx4.init()
    try:
        engine.setProperty('rate', 150)    # 中等语速
        engine.setProperty('volume', 0.9)  # 音量(0-1)
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'chinese' in voice.languages or 'zh' in voice.id.lower():
                engine.setProperty('voice', voice.id)
                break
        engine.say(clean_text)
        engine.runAndWait()
    except Exception as e:
        print(f"语音合成出错: {e}")
    finally:
        engine.stop()

class VoiceAssistant:
    def __init__(self):
        self.model_path = "model/PATH"# 替换为实际的模型路径
        self.hotword = "你好"# 唤醒词
        self.model = None
        self.rec = None
        self.stream = None
        self.pa = None
        self.is_wakeup = False
        
    def initialize(self):
        self.model = Model(self.model_path)
        self.rec = KaldiRecognizer(self.model, 16000)
        self.rec.SetWords(True)
        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(
            rate=16000,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=8000
        )
        return True

    def listen_loop(self):
        print(f"等待唤醒词: '{self.hotword}' (说'关闭'可退出程序)...")
        try:
            while True:
                data = self.stream.read(4000)
                if self.rec.AcceptWaveform(data):
                    result = json.loads(self.rec.Result())
                    text = result.get("text", "").strip()
                    if text:
                        print(f"\n识别结果: {text}")
                        if self.hotword in text and not self.is_wakeup:
                            self.handle_wakeup()
                        elif "关闭" in text and not self.is_wakeup:
                            text_to_speech("正在退出程序")
                            self.cleanup()
                            sys.exit(0)
                else:
                    partial = json.loads(self.rec.PartialResult())
        except KeyboardInterrupt:
            print("\n停止监听")
        finally:
            self.cleanup()

    def cleanup(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.pa:
            self.pa.terminate()

    def handle_wakeup(self):
        self.is_wakeup = True
        text_to_speech("唤醒成功")
        messages = [{"role": "system", "content": "你好"}]
        
        while self.is_wakeup:
            data = self.stream.read(8000)
            if self.rec.AcceptWaveform(data):
                text = json.loads(self.rec.Result()).get("text", "").strip()
                if not text:
                    continue
                    
                print(f"\n用户输入: {text}")
                
                if "退出" in text:
                    text_to_speech("退出对话模式")
                    self.is_wakeup = False
                    break
                elif "关闭" in text:
                    text_to_speech("正在退出程序")
                    self.cleanup()
                    sys.exit(0)
                
                messages.append({"role": "user", "content": text})
                payload = {
                    "model": CONFIG["model"],
                    "messages": messages[-CONFIG["max_history"]*2:] if CONFIG["max_history"] > 0 else messages,
                    "stream": False
                }
                headers = {'Content-Type': 'application/json'}
                
                try:
                    response = requests.post(CONFIG["base_url"], headers=headers, json=payload)
                    if response.status_code == 200:
                        ai_response = response.json().get('message', {}).get('content') \
                                    or response.json().get('response') \
                                    or str(response.json())
                        clean_response = ai_response.replace("<think>", "").replace("</think>", "").strip()
                        print(f"\nAI回复: {clean_response}")
                        if CONFIG["enable_tts"] and clean_response:
                            text_to_speech(clean_response)
                        messages.append({"role": "assistant", "content": clean_response})
                    else:
                        print(f"API请求失败，状态码: {response.status_code}")
                except Exception as e:
                    print(f"请求异常: {str(e)}")

def main():
    assistant = VoiceAssistant()
    if assistant.initialize():
        assistant.listen_loop()

if __name__ == "__main__":
    main()