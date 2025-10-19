from app.models import llm
class Reflection:
    def __init__(self,llm):
        self.llm = llm
    # def __init__(self):
    #     pass
    # def concat_and_format_text(self,texts):
    #     concat_text = []
    #     for text in texts:
    #         role = text.get('role')
    #         if text.get('content'):
    #             all_text = ' '.join(entry.get('content') for entry in text.get('content'))
    #         concat_text.append(f"{role}: {all_text} \n")
    #     return ''.join(concat_text)

    def concat_and_format_text(self, texts):
        """
        SỬA LỖI: 'text.get('content')' là một string, không phải list.
        """
        concat_text = []
        for text in texts:
            role = text.get('role')
            content = text.get('content')  # Lấy thẳng content (là string)

            # Kiểm tra xem role và content có tồn tại không
            if role and content:
                # Nối chuỗi đã định dạng
                concat_text.append(f"{role}: {content}\n")
        return ''.join(concat_text)

    def __call__(self, chat_history,query,length = 20):
        if not chat_history: return query
        if len(chat_history) >= length:
            chat_history = chat_history[len(chat_history) - length:]

        history_string =self.concat_and_format_text(chat_history)
        conversation = {
            "role": "user",
            "content": f"Given a chat history and the latest user question which might reference context in the chat history, formulate a standalone question in Vietnamese which can be understood without the chat history. Do NOT answer the question, just reformulate it if needed and otherwise return it as is. {history_string}"
        }
        completion = self.llm.generate_content([conversation])
        return completion





if __name__ == '__main__':
    a = Reflection()
    texts = [
        {
            "role": "user",
            "content": [
                {"content": "Có iphone không?"},
                {"content": "hello"}
            ]
        }
    ]
    print(a.concat_and_format_text(texts))