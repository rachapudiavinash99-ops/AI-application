from abc import ABC, abstractmethod
import time

class AIProvider(ABC):
    @abstractmethod
    def generate_content(self, prompt: str) -> str:
        pass

class MockDevelopmentProvider(AIProvider):
    def generate_content(self, prompt: str) -> str:
        # Simulate network latency
        time.sleep(1)
        return f"[Mock Development AI Response] Simulated result for: {prompt[:50]}..."

# Factory to get provider
def get_ai_provider() -> AIProvider:
    # In production, check environment variables to instantiate real provider
    return MockDevelopmentProvider()
