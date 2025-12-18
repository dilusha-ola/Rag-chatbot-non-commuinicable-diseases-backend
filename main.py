"""
Main application file for the NCD RAG Chatbot.
Entry point for running the chatbot.
"""

import sys
from src.chatbot import NCDChatbot


def main():
    """
    Main function to run the chatbot.
    """
    try:
        print("Initializing NCD Chatbot...")
        chatbot = NCDChatbot()
        chatbot.chat()
    except FileNotFoundError as e:
        print("\n" + "=" * 70)
        print("⚠️  Vector Store Not Found")
        print("=" * 70)
        print("\nIt looks like you haven't run the setup yet.")
        print("\nPlease run the following command first:")
        print("  python -m src.setup")
        print("\nThis will:")
        print("  1. Load your PDF documents from the 'data' folder")
        print("  2. Process and chunk the documents")
        print("  3. Create embeddings and store them in the vector database")
        print("\nAfter setup completes, you can run this chatbot again.")
        sys.exit(1)
    except Exception as e:
        print("\n" + "=" * 70)
        print("❌ Error Starting Chatbot")
        print("=" * 70)
        print(f"\n{str(e)}")
        print("\nPlease check:")
        print("  1. Your OPENAI_API_KEY is set in the .env file")
        print("  2. You have run: python -m src.setup")
        print("  3. The 'data' folder contains PDF files")
        sys.exit(1)


if __name__ == "__main__":
    main()
