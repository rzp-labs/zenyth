"""Minimal LLM interface protocol for Zenyth SPARC orchestration system.

This module defines the core abstraction layer for Large Language Model providers
used throughout the Zenyth system. The interface follows the Interface Segregation
Principle (ISP) by providing only the minimal contract required for SPARC phase
execution, allowing for flexible provider implementations without unnecessary coupling.

The protocol-based design enables runtime type checking and supports dependency
injection patterns critical for testing and provider swapping in homelab environments
where different LLM services may be used based on availability and performance.

Key Design Principles:
    - Minimal interface surface area for maximum flexibility
    - Async-first design for non-blocking orchestration
    - Runtime protocol checking for type safety
    - Provider-agnostic abstraction

Examples:
    Implementing a concrete LLM provider::

        class ClaudeProvider:
            async def generate(self, prompt: str, **kwargs: Any) -> str:
                # Claude-specific implementation
                response = await self.claude_client.complete(prompt, **kwargs)
                return response.content

    Using with type checking::

        def create_orchestrator(llm: LLMInterface) -> SPARCOrchestrator:
            # Type checker ensures llm implements the protocol
            return SPARCOrchestrator(llm)

    Runtime protocol verification::

        provider = SomeProvider()
        if isinstance(provider, LLMInterface):
            # Safe to use as LLM provider
            result = await provider.generate("Hello")
"""

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class LLMInterface(Protocol):
    """Minimal protocol for Large Language Model provider integration.

    Defines the essential contract that all LLM providers must implement to
    participate in SPARC phase execution. The interface is deliberately minimal
    to maximize compatibility across different LLM services while providing the
    core functionality required for text generation.

    This protocol follows the Dependency Inversion Principle (DIP) by allowing
    high-level orchestration logic to depend on this abstraction rather than
    concrete LLM implementations. This enables provider swapping, testing with
    mocks, and adaptation to different LLM services in homelab environments.

    The async design ensures non-blocking execution during long-running phase
    operations, which is critical for responsive orchestration and resource
    efficiency in constrained homelab environments.

    Methods:
        generate: Asynchronously generate text response from a given prompt.
                 Accepts arbitrary keyword arguments to support provider-specific
                 parameters like temperature, max_tokens, model selection, etc.

    Examples:
        Implementing for OpenAI GPT::

            class OpenAIProvider:
                def __init__(self, api_key: str, model: str = "gpt-4"):
                    self.client = openai.AsyncOpenAI(api_key=api_key)
                    self.model = model

                async def generate(self, prompt: str, **kwargs: Any) -> str:
                    response = await self.client.chat.completions.create(
                        model=kwargs.get("model", self.model),
                        messages=[{"role": "user", "content": prompt}],
                        temperature=kwargs.get("temperature", 0.7),
                        max_tokens=kwargs.get("max_tokens", 1000)
                    )
                    return response.choices[0].message.content

        Implementing for local Ollama::

            class OllamaProvider:
                def __init__(self, base_url: str, model: str):
                    self.base_url = base_url
                    self.model = model

                async def generate(self, prompt: str, **kwargs: Any) -> str:
                    async with aiohttp.ClientSession() as session:
                        payload = {
                            "model": kwargs.get("model", self.model),
                            "prompt": prompt,
                            "stream": False
                        }
                        async with session.post(f"{self.base_url}/api/generate",
                                               json=payload) as response:
                            result = await response.json()
                            return result["response"]

        Testing with mock implementation::

            class MockLLMProvider:
                def __init__(self, responses: list[str]):
                    self.responses = responses
                    self.call_count = 0

                async def generate(self, prompt: str, **kwargs: Any) -> str:
                    response = self.responses[self.call_count % len(self.responses)]
                    self.call_count += 1
                    return f"Mock response to '{prompt}': {response}"

    Note:
        Implementations should handle errors appropriately and may raise exceptions
        for network failures, API errors, or invalid parameters. The protocol does
        not specify error handling to allow providers flexibility in error management
        strategies appropriate for their service characteristics.

        The **kwargs parameter allows providers to accept arbitrary configuration
        parameters without requiring interface changes, supporting extensibility
        while maintaining backward compatibility.
    """

    async def generate(self, prompt: str, **kwargs: Any) -> str:
        """Generate text response from the given prompt.

        Asynchronously processes the input prompt using the underlying LLM service
        and returns the generated text response. This method serves as the primary
        interface for all text generation operations in SPARC phase execution.

        Args:
            prompt: The input text prompt to process. Should be well-formatted
                   and contain clear instructions or questions for the LLM.
                   Maximum length depends on the provider's context window.
            **kwargs: Additional provider-specific parameters that may include:
                     - temperature: Randomness control (0.0-2.0 typical range)
                     - max_tokens: Maximum tokens to generate
                     - model: Specific model variant to use
                     - top_p: Nucleus sampling parameter
                     - frequency_penalty: Repetition penalty
                     - presence_penalty: Topic penalty
                     - stop: Stop sequences for generation termination
                     - timeout: Request timeout in seconds

        Returns:
            The generated text response as a string. The content and length
            depend on the prompt, provider capabilities, and configuration
            parameters. Empty strings are valid responses for certain prompts.

        Raises:
            The protocol does not specify exact exceptions to allow provider
            flexibility, but implementations typically raise:
            - ConnectionError: For network connectivity issues
            - TimeoutError: For request timeouts
            - ValueError: For invalid parameters or prompt format
            - AuthenticationError: For API key or credential issues
            - RateLimitError: For API rate limit exceeded
            - ProviderError: For service-specific errors

        Examples:
            Basic text generation::

                llm = SomeLLMProvider()
                response = await llm.generate("Explain quantum computing")
                print(response)

            With provider-specific parameters::

                response = await llm.generate(
                    "Write a Python function to sort a list",
                    temperature=0.2,
                    max_tokens=500,
                    model="gpt-4-turbo"
                )

            Error handling::

                try:
                    response = await llm.generate(prompt, timeout=30)
                except TimeoutError:
                    response = "Generation timed out, please try again"
                except Exception as e:
                    logger.error(f"LLM generation failed: {e}")
                    response = "Error occurred during generation"

        Note:
            Implementations should be thread-safe and support concurrent calls
            where the underlying service allows. Response times can vary significantly
            based on prompt complexity, model size, and service load.

            For homelab deployments, implementations should include appropriate
            retry logic and fallback strategies to handle temporary service
            unavailability or network issues.
        """
        ...
