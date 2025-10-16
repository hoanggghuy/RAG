import numpy as np
from sentence_transformers import SentenceTransformer

from data.SemanticRouter.Sample import chitchatSample,productsSample

from  app.services.SemanticRouter import SemanticRouter,Route

if __name__ == '__main__':
    model = SentenceTransformer(model_name_or_path="Qwen/Qwen3-Embedding-0.6B", trust_remote_code=True)
    product_route = Route(name="product", sample=productsSample)
    chitchat_route = Route(name="chitchat", sample=chitchatSample)
    router =SemanticRouter(model,routes=[product_route,chitchat_route])
    while True:
        # Nhận query từ người dùng
        query = input("Nhập câu truy vấn của bạn (gõ 'exit' để thoát): ")

        # Điều kiện để thoát khỏi vòng lặp
        if query.lower() == 'exit':
            print("Đã thoát chương trình. Tạm biệt!")
            break

        # Nếu người dùng không nhập gì, bỏ qua và lặp lại
        if not query:
            continue

        # Gọi router để phân loại
        score, route_name = router.guide(query)

        # In kết quả
        print(f"  ==> Route: '{route_name}' (Score: {score})\n")