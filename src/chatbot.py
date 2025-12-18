"""
RAG Chatbot module for answering questions about non-communicable diseases.
Uses LangChain to combine retrieval and generation.
"""

import os
from typing import Optional
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from src.vector_store import VectorStoreManager


class NCDChatbot:
    """RAG-based chatbot for non-communicable diseases information."""
    
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        openai_api_key: Optional[str] = None
    ):
        """
        Initialize the chatbot.
        
        Args:
            model_name: OpenAI model to use
            temperature: Response creativity (0-1)
            openai_api_key: OpenAI API key
        """
        # Load environment variables
        load_dotenv()
        
        if openai_api_key:
            os.environ["OPENAI_API_KEY"] = openai_api_key
        
        self.model_name = model_name
        self.temperature = temperature
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model_name=self.model_name,
            temperature=self.temperature
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

Use the following pieces of context to answer the question at the end. If you don't know the answer based on the context, 
say that you don't have enough information to answer accurately. Don't make up information.

Context:
{context}

Question: {question}

Answer: Provide a clear, informative answer based on the context above. Include relevant details about symptoms, 
risk factors, prevention, or treatment as applicable to the question."""

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
