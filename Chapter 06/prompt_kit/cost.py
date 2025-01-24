import tiktoken
from tiktoken import Encoding

ip_price = 0.0015 / 1000 # price per 1000 tokens
op_price = 0.002 / 1000 # price per 1000 tokens

'''A decorator takes a function as arg add come functionality t and returns a modified version of that function. The purpose of a decorator'''

def cost_decorator(response):
    """
    A decorator to calculate the input and output cost of Large Language Models like ChatGPT.
    This decorator takes llm_function function pointer to pass the prompt and get the response.
    :param llm_function: Any Large Language Model which takes prompt as string and gives response as string
    :return: Function Pointer
    """

    def inner_func(*args):
        """
        Calculates the cost of the prompt for a given LLM engine rounded to 4 decimal places
        :param args: This is a prompt argument given to llm_function
        :return: Returns the response given by the LLM engine
        """
        prompt: str = args[0]
        temperature: str = args[1]
        model: str = args[2]
        system_message: str = args[3]


        prompt_response: str = response(prompt,temperature,model,system_message)
        print(prompt_response)
        enc: Encoding = tiktoken.get_encoding("cl100k_base")
        ip_token_length: int = len(enc.encode(prompt))
        print(ip_token_length)
        op_token_length: int = len(enc.encode(prompt_response['text']))
        print(op_token_length)

        content_price: float = ip_price * ip_token_length
        response_price: float = op_price * op_token_length
        total_price: float = content_price + response_price
        print(f"The cost of the below prompt is: ${round(total_price, 4)}.\n `{prompt}`")
        return prompt_response,total_price

    return inner_func