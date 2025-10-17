class Reflection:
    # def __init__(self,llm):
    #     self.llm = llm
    def __init__(self):
        pass
    def concat_and_format_text(self,texts):
        concat_text = []
        for text in texts:
            role = text.get('role')
            if text.get('content'):
                all_text = ' '.join(entry.get('content') for entry in text.get('content'))
            concat_text.append(f"{role}: {all_text} \n")
        return ''.join(concat_text)

if __name__ == '__main__':
    a = Reflection()
    texts = [
        {
            "role": "user",
            "content": [
                {"content": "Hello"},
                {"content": "How are you?"}
            ]
        },
        {
            "role": "assistant",
            "content": [
                {"content": "Hi!"},
                {"content": "I'm fine, thank you!"}
            ]
        }
    ]
    print(a.concat_and_format_text(texts))