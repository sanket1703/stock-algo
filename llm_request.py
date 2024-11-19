import openai

# Set up OpenAI API key
openai.api_key = "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"


def generate_rest_request(user_input):
    """
    Convert natural language input into a REST API request using OpenAI GPT.
    """
    # Define a prompt for text-to-REST conversion
    # prompt = f"""
    # Convert the following natural language instruction into a REST API request for weather of cities.
    # Example REST API: GET https://wttr.in/{"{Place}"}?format=3
    
    # Instruction: "{user_input}"
    # REST Request:"""


        
    messages = [
            {"role": "system", "content": "You are an assistant that converts user instructions into REST API requests."},
            {"role": "user", "content": f"Convert this instruction into a REST API request: {user_input}"}
        ]

    try:
        # Call the ChatGPT API
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Use "gpt-4" if available
            messages=messages,
            max_tokens=100,
            temperature=0  # Lower temperature for deterministic output
        )

        # Extract and return the assistant's message
        rest_request = response['choices'][0]['message']['content']
        return rest_request

    except Exception as e:
        return f"Error: {e}"


# User input
user_instruction = "Get the latest weather of Mumbai."

# Generate the REST API request
rest_request = generate_rest_request(user_instruction)
print("Generated REST Request:")
print(rest_request)
