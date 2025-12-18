"""
RAG Chatbot module for answering questions about non-communicable diseases.
Uses LangChain to combine retrieval and generation with Google Gemini.
"""

import os
from typing import Optional
from langchain_classic.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from src.vector_store import VectorStoreManager


class NCDChatbot:
    """RAG-based chatbot for non-communicable diseases information."""
    
    def __init__(
        self,
        model_name: str = "models/gemini-2.5-flash",
        temperature: float = 0.7,
        google_api_key: Optional[str] = None
    ):
        """
        Initialize the chatbot.
        
        Args:
            model_name: Google Gemini model to use
            temperature: Response creativity (0-1)
            google_api_key: Google API key
        """
        # Load environment variables
        load_dotenv()
        
        if google_api_key:
            os.environ["GOOGLE_API_KEY"] = google_api_key
        
        self.model_name = model_name
        self.temperature = temperature
        
        # Initialize Gemini LLM
        self.llm = ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=self.temperature,
            convert_system_message_to_human=True
        )
        
        # Initialize vector store manager
        self.vs_manager = VectorStoreManager()
        
        # Load vector store
        try:
            self.vs_manager.load_vector_store()
        except FileNotFoundError:
            raise FileNotFoundError(
                "Vector store not found. Please run the setup script first to create it."
            )
        
        # Create custom prompt template
        self.prompt_template = """You are a medical information assistant specializing in non-communicable diseases (NCDs). 
Your role is to provide accurate, helpful information about diseases like diabetes, cancer, heart disease, obesity, and high blood pressure.

IMPORTANT INSTRUCTIONS:
- Respond in PLAIN TEXT only. Do NOT use Markdown formatting (no **, no *, no #)
- Use simple text for section headers ending with colon
- Use bullet symbol • for lists
- Never mention "context", "provided information", or reference system limitations
- If information is incomplete, naturally say "I don't have complete information about that aspect" within your answer

Use the following context to answer the question:

Context:
{context}

Question: {question}

Answer format:
1. Start with a clear 1-2 sentence definition/overview
2. Add a blank line
3. Use section headers in plain text (e.g., "Common symptoms:", "Where it can start:")
4. List items with • bullet symbol, one per line
5. Keep each bullet point concise
6. Add blank line between sections
7. End with: "Note: This is educational information. Always consult a healthcare professional for medical advice."

Keep response focused, scannable, and limited to 3-4 key sections."""

        self.prompt = PromptTemplate(
            template=self.prompt_template,
            input_variables=["context", "question"]
        )
        
        # Create retrieval QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vs_manager.get_retriever(search_kwargs={"k": 4}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt}
        )
    
    def ask(self, question: str, return_sources: bool = False) -> dict:
        """
        Ask a question and get an answer.
        
        Args:
            question: User's question
            return_sources: Whether to return source documents
            
        Returns:
            Dictionary with 'answer' and optionally 'sources'
        """
        if not question or not question.strip():
            return {
                "answer": "Please provide a valid question.",
                "sources": []
            }
        
        # Get answer from the chain
        result = self.qa_chain.invoke({"query": question})
        
        response = {
            "answer": result["result"]
        }
        
        if return_sources:
            sources = []
            for doc in result.get("source_documents", []):
                sources.append({
                    "source": doc.metadata.get("source", "Unknown"),
                    "content": doc.page_content[:300]  # First 300 chars
                })
            response["sources"] = sources
        
        return response
    
    def chat(self):
        """
        Interactive chat mode.
        """
        print("=" * 70)
        print("Non-Communicable Diseases Chatbot")
        print("=" * 70)
        print("Ask me anything about non-communicable diseases!")
        print("Type 'quit', 'exit', or 'q' to end the conversation.\n")
        
        while True:
            question = input("You: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("\nThank you for using the NCD Chatbot. Stay healthy!")
                break
            
            if not question:
                continue
            
            print("\nChatbot: ", end="", flush=True)
            
            try:
                response = self.ask(question, return_sources=True)
                print(response["answer"])
                
                # Show sources if available
                if response.get("sources"):
                    print("\n📚 Sources:")
                    for i, source in enumerate(response["sources"], 1):
                        print(f"  {i}. {source['source']}")
                
                print()
            
            except Exception as e:
                print(f"Error: {str(e)}\n")


if __name__ == "__main__":
    try:
        # Initialize and start chatbot
        chatbot = NCDChatbot()
        chatbot.chat()
    except Exception as e:
        print(f"Failed to initialize chatbot: {str(e)}")
        print("Make sure you have:")
        print("1. Set your OPENAI_API_KEY in .env file")
        print("2. Run the setup script to create the vector store")
