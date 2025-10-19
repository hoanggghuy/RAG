import os
from sentence_transformers import SentenceTransformer
from data.SemanticRouter.Sample import chitchatSample,productsSample
from  app.services.SemanticRouter import SemanticRouter,Route
import openai
from dotenv import load_dotenv
from app.services.SemanticRouter import SemanticRouter
from data.SemanticRouter.Sample import chitchatSample,productsSample
from app.services import search_service
from app.models import llm
from app.services import reflection

load_dotenv()


def main():
    query = input("Enter query: ")
    llms = llm.CallAPIOpenAI(model_name="gpt-5-mini", api_key=os.getenv("API_KEY"))
    reflec = reflection.Reflection(llm= llms)
    reflected_query = reflec(data,query=query)
    product_route = Route(name="product", sample=productsSample)
    chitchat_route = Route(name="chitchat", sample=chitchatSample)
    router =SemanticRouter(model,routes=[product_route,chitchat_route])
    score, router_name = router.guide(reflected_query)
    if router_name == "product":
        docs = search_service.search_qdrant(query=reflected_query, top_k=3)
        source_information = ""
        for doc in docs:
            source_information += doc["text"]

        combined_information = f"Hãy trở thành chuyên gia tư vấn bán hàng cho một cửa hàng điện thoại. Câu hỏi của khách hàng: {reflected_query}\nTrả lời câu hỏi dựa vào các thông tin sản phẩm dưới đây: {source_information}."
        data.append({
            "role": "user",
            "content": combined_information
        })
        response = llms.generate_content(data)
    elif router_name == "chitchat":
        query_chitchat = [{
            "role": "user",
            "content": query
        }]
        for data_chitchat in query_chitchat:
            data.append(data_chitchat)
        response = llms.generate_content(query_chitchat)
    print(response)
    print("-----------------------------")
    print(reflected_query)
    print("-----------------------------")
    print(data)


if __name__ == "__main__":
    data = []
    model = SentenceTransformer(model_name_or_path="Qwen/Qwen3-Embedding-0.6B", trust_remote_code=True)
    while True:
        main()








