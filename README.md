# vosk_ollama_pyttsx4

# 中文简介
本项目是基于Python的智能语音助手，集成Vosk语音识别、大语言模型对话及语音合成。支持唤醒词激活、离线对话与多场景扩展，提供高可定制跨平台解决方案。
# English Summary
A Python-based voice assistant integrating Vosk speech recognition, LLM dialogue, and TTS. Features wake-word activation, offline interaction, and cross-platform customizability for diverse applications.

# 语音智能助手开发与使用手册
# 1. 项目概述
# 1.1 项目简介
本语音智能助手是一个基于Python开发的语音交互应用程序，集成了语音识别、大型语言模型对话和语音合成功能。用户可以通过语音唤醒词启动对话，与AI助手进行自然语言交流。

# 1.2 主要功能
  语音唤醒：通过特定关键词唤醒助手
  语音识别：实时将语音转换为文本
  智能对话：与大型语言模型进行交互
  语音合成：将AI回复转换为语音输出
  对话历史管理：支持对话记录的保存和管理

# 2. 环境要求与安装
# 2.1 系统要求
  操作系统：Windows 10/11，macOS 10.14+，Linux（Ubuntu 18.04+）
  Python版本：Python 3.7 - 3.10（强烈推荐使用Conda环境运行，本人使用的Conda环境为Python 3.9.23）

# 2.2 依赖安装
  步骤1：安装Python包
    pip install requests pyttsx4 pyaudio vosk
  步骤2：安装系统依赖（Linux/macOS）
    # Ubuntu/Debian
      sudo apt-get install portaudio19-dev python3-dev
    # macOS
      brew install portaudio
  步骤3：下载Vosk语音识别模型
    访问Vosk官方模型库：https://alphacephei.com/vosk/models
    下载适合的中文模型（推荐：vosk-model-small-cn-0.22）
    解压到项目目录下的 model/ 文件夹

# 3. 配置说明
# 3.1 配置文件详解
编辑代码中的 CONFIG 字典：
    #python
        CONFIG = {
          "base_url": "http://your-api-endpoint",       # 大模型API地址
          "history_file": "chat_history.json",          # 对话历史保存文件
          "max_history": 10,                            # 最大历史记录条数
          "model": "your-model-name",                   # 模型名称
          "enable_tts": True                            # 是否启用语音合成
        }
# 3.2 必需配置项
3.2.1 大模型API配置
    #python
        #OpenAI兼容API配置示例
        CONFIG = {
          "base_url": "https://api.openai.com/v1/chat/completions",
          "model": "gpt-3.5-turbo",
          "headers": {
              "Authorization": "Bearer your-api-key",
              "Content-Type": "application/json"
            }
          }
3.2.2 Vosk模型路径
  #python
    #Windows示例
        model_path = "model/vosk-model-small-cn-0.22"
    #Linux/macOS示例
        model_path = "./model/vosk-model-small-cn-0.22"
# 4. 使用方法
# 4.1 首次运行准备
  确保所有依赖已安装
  下载并放置Vosk模型文件
  配置API密钥和模型参数
  检查音频输入设备是否正常

# 4.2 启动程序
  #bash
      python voice_assistant.py
# 4.3 语音命令说明
4.3.1 唤醒与退出
  唤醒词：说"你好"启动对话模式
  退出对话：说"退出"返回待机状态
  关闭程序：说"关闭"完全退出程序
4.3.2 对话模式
唤醒后进入对话模式，可以直接与AI助手对话：
  #text
      用户：天气怎么样？
      AI：今天天气晴朗，温度25度...
# 4.4 运行状态指示
  等待唤醒：控制台显示"等待唤醒词：'你好'..."
  唤醒成功：语音提示"唤醒成功"
  识别结果：控制台显示识别的文本
  AI回复：控制台显示AI回复内容，同时语音播报（如果启用）

# 5. 开发指南
# 5.1 项目结构
    #text
      voice_assistant/
      ├── voice_assistant.py    # 主程序文件
      ├── model/                # Vosk模型目录
      │   └── vosk-model-*     # 语音识别模型
      ├── chat_history.json     # 对话历史记录
      ├── requirements.txt      # 依赖列表
      └── README.md            # 说明文档
# 5.2 核心类说明
VoiceAssistant 类
    #python
      class VoiceAssistant:
        def __init__(self):
            # 初始化语音识别组件
            self.model = None      # Vosk模型
            self.rec = None       # 识别器
            self.stream = None    # 音频流
            self.pa = None        # PyAudio实例
            self.is_wakeup = False # 唤醒状态
    
        def initialize(self):     # 初始化音频设备  
        def listen_loop(self):    # 主监听循环
        def handle_wakeup(self):  # 处理唤醒逻辑
        def cleanup(self):        # 清理资源
# 5.3 自定义功能扩展
5.3.1 添加新的唤醒词
  #python
      class VoiceAssistant:
        def __init__(self):
            self.hotwords = ["你好", "助手", "小助手"]  # 多唤醒词支持
        
        def check_wakeup(self, text):
            for word in self.hotwords:
                if word in text:
                    return True
            return False
5.3.2 添加本地命令
  #python
      def handle_local_command(self, text):
          """处理本地命令，不调用大模型"""
          if "时间" in text:
            current_time = datetime.now().strftime("%H:%M")
            text_to_speech(f"现在是{current_time}")
            return True
          elif "日期" in text:
            current_date = datetime.now().strftime("%Y年%m月%d日")
            text_to_speech(f"今天是{current_date}")
            return True
          return False
# 6. 调试与故障排除
# 6.1 常见问题
    # 问题1：无法识别音频设备
      症状：程序启动时报错或无法录音
      解决方案：
        检查麦克风是否连接正常
      更新
        PyAudio：pip install --upgrade pyaudio
      在代码中指定设备索引：
        #python
            self.stream = self.pa.open(
            input_device_index=0,  # 指定设备索引
            # ... 其他参数
          )
    # 问题2：语音识别不准确
      解决方案：
        更换更大的Vosk模型
        调整录音参数：
        #python
          # 调整采样率或缓冲区大小
            rate=16000,  # 尝试8000或44100
            frames_per_buffer=2048  # 调整缓冲区大小
      确保环境安静，麦克风质量良好

    # 问题3：API调用失败
      解决方案：
        检查网络连接
        验证API密钥和URL
        查看返回状态码：
        #python
          print(f"状态码: {response.status_code}")
          print(f"响应内容: {response.text}")
# 6.2 调试模式
  添加调试参数：
    #python
        import logging
        logging.basicConfig(level=logging.DEBUG)
# 7. 性能优化
# 7.1 内存优化
  设置合适的 max_history 值
  定期清理对话历史
  使用较小的Vosk模型

# 7.2 响应优化
  设置超时时间：
    #python
        response = requests.post(url, timeout=30)
  启用流式响应减少等待时间

# 7.3 语音合成优化
    #python
        def text_to_speech(text):
        # 预处理文本
        text = text[:500]  # 限制文本长度
        # 使用异步合成
        engine.startLoop(False)
        engine.say(text)
        engine.iterate()

# 附录
  Vosk模型下载地址
      小型中文模型：https://alphacephei.com/vosk/models/vosk-model-small-cn-0.22.zip  
      完整中文模型：https://alphacephei.com/vosk/models/vosk-model-cn-0.22.zip
