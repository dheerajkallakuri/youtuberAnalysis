from langchain_community.llms import CTransformers

# Local CTransformers model
llm = CTransformers(model='TheBloke/Llama-2-7B-Chat-GGML',
                    model_type='llama',
                    config={'max_new_tokens': 200,
                            'temperature': 0.01}
                    )

def SummarizeYoutuber(name):
    summary = llm.invoke(f"Summarize about youtube channel of {name} in 100 words.")
    print(summary)
    return summary
    

