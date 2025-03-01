from openai import OpenAI

client = OpenAI(
    api_key="sk-Eyzpa0mEN1PmHSS3vhaA3dVMknRacl7FTcUYnb21wVlOlcf6",  # 在这里将 MOONSHOT_API_KEY 替换为你从 Kimi 开放平台申请的 API Key
    base_url="https://api.moonshot.cn/v1",
)

stream = client.chat.completions.create(
    model="moonshot-v1-8k",
    messages=[
        {
            "role": "system",
            "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。",
        },
        {"role": "user", "content": "你好，我叫李雷，1+1等于多少？"},
    ],
    temperature=0.1,
    stream=True,  # <-- 注意这里，我们通过设置 stream=True 开启流式输出模式
)

# 当启用流式输出模式（stream=True），SDK 返回的内容也发生了变化，我们不再直接访问返回值中的 choice
# 而是通过 for 循环逐个访问返回值中每个单独的块（chunk）

for chunk in stream:
    # 在这里，每个 chunk 的结构都与之前的 completion 相似，但 message 字段被替换成了 delta 字段
    delta = chunk.choices[0].delta  # <-- message 字段被替换成了 delta 字段

    if delta.content:
        # 我们在打印内容时，由于是流式输出，为了保证句子的连贯性，我们不人为地添加
        # 换行符，因此通过设置 end="" 来取消 print 自带的换行符。
        print(delta.content, end="")
