from huggingface_hub import InferenceClient

HF_API_KEY = " "
client = InferenceClient("mistralai/Mistral-7B-Instruct-v0.2", token=HF_API_KEY)

def get_chatbot_response(user_input):
    """
    Takes user input as a string and returns the chatbot response.
    """
    try:
        response = client.chat_completion(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            messages=[{"role": "user", "content": user_input}],
            max_tokens=1000,
            temperature=0.7
        )

        # 🔹 Debug: print full response in terminal
        print("Raw HF Response:", response)

        # Safely extract reply
        if hasattr(response, "choices") and len(response.choices) > 0:
            choice = response.choices[0]
            if hasattr(choice, "message") and "content" in choice.message:
                return choice.message["content"]
            elif hasattr(choice, "delta") and "content" in choice.delta:
                return choice.delta["content"]

        return "⚠️ Sorry, I couldn't generate a reply."

    except Exception as e:
        return f"⚠️ Error: {str(e)}"
