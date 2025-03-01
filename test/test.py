from openai import OpenAI
import tkinter as tk
from threading import Thread



# 创建主窗口
root = tk.Tk()
root.title("快捷回答")
root.geometry("400x150")
# 创建仿Mac风格的文本框
text_box = tk.Text(
    root,
    wrap=tk.WORD,
    font=("San Francisco", 12),
    bg="#333233"
)
text_box.pack(fill=tk.BOTH,
              expand=True, 
              padx=5, 
              pady=5
              )



def stream_response():
    client = OpenAI(
        # 在这里将 MOONSHOT_API_KEY 替换为你从 Kimi 开放平台申请的 API Key
        api_key="sk-Eyzpa0mEN1PmHSS3vhaA3dVMknRacl7FTcUYnb21wVlOlcf6",
        base_url="https://api.moonshot.cn/v1",
    )

    stream = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {
                "role": "system",
                "content": """
                            1. 回答字数尽量不要超过800字，越简洁明了越好，不用无用礼貌用语。
                            2. 如果问题是英文、外文句子，翻译成中文解释.
                            3. 如果问题是中文，先把问题翻译成英文，再回答问题。
                            """,
            },
            {"role": "user", "content":  """
                            讲一个故事，500字
                            """,},
        ],
        temperature=0.1,
        stream=True,  # <-- 注意这里，我们通过设置 stream=True 开启流式输出模式
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            # 在GUI线程中更新文本框
            root.after(0, lambda c=chunk: text_box.insert(tk.END, c.choices[0].delta.content))
            root.after(0, text_box.see, tk.END)


# 在新线程中启动流式请求
Thread(target=stream_response, daemon=True).start()

# 运行主循环
root.mainloop()
