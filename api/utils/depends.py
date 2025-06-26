from config.Database import ollama_url, model_name
from repositories.Message import MessageRepository
from services.Message import MessageService
from services.OllamaService import OllamaService

message_repository = MessageRepository()
message_service = MessageService(message_repository)
ollama_service = OllamaService(ollama_url, model_name)