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
        query = input("Enter your query: ")
        if query.lower() == 'exit':
            print("Exiting...")
            break
        if not query:
            continue
        score, route_name = router.guide(query)
        print(f"  ==> Route: '{route_name}' (Score: {score})\n")
