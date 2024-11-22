from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Use Flan-T5 as an alternative
model_name = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


def generate_rest_request(prompt):
    """
    Generate a REST API request using Flan-T5.
    """
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(inputs.input_ids, max_length=100,
                             num_beams=5, no_repeat_ngram_size=2, early_stopping=True)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


# Example usage
prompt = """You are a highly advanced AI assistant specializing in generating REST API requests based on natural language instructions. Your goal is to understand the user's request and create a complete and properly formatted REST API request with the required URL, HTTP method, headers, and body. Follow these rules:
1. Identify the endpoint, method(GET, POST, etc.), and query or body parameters from the input.
2. Include sample data for placeholders.
3. Format the response in proper JSON format for easy integration.

# Example:
Input: "Get the current stock price for Tesla."
Output:
{
    "method": "GET",
    "url": "https://api.example.com/stocks?symbol={{symbol}}}",
    "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
    }
}
"""
rest_request = generate_rest_request(prompt)
print("Generated REST Request:")
print(rest_request)
