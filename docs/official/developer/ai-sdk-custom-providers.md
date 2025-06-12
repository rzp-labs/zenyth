[AI SDK](/)

* [Docs](/docs)
* [Cookbook](/cookbook)
* [Providers](/providers)
* [Showcase](/showcase)
* [Playground](/playground)
* [Model Library](/model-library)

Announcing AI SDK 5 Alpha!

[Learn more](https://ai-sdk.dev/docs/announcing-ai-sdk-5-alpha)Menu[AI SDK Providers](/providers/ai-sdk-providers)[xAI Grok](/providers/ai-sdk-providers/xai)[Vercel](/providers/ai-sdk-providers/vercel)[OpenAI](/providers/ai-sdk-providers/openai)[Azure OpenAI](/providers/ai-sdk-providers/azure)[Anthropic](/providers/ai-sdk-providers/anthropic)[Amazon Bedrock](/providers/ai-sdk-providers/amazon-bedrock)[Groq](/providers/ai-sdk-providers/groq)[Fal](/providers/ai-sdk-providers/fal)[DeepInfra](/providers/ai-sdk-providers/deepinfra)[Google Generative AI](/providers/ai-sdk-providers/google-generative-ai)[Google Vertex AI](/providers/ai-sdk-providers/google-vertex)[Mistral AI](/providers/ai-sdk-providers/mistral)[Together.ai](/providers/ai-sdk-providers/togetherai)[Cohere](/providers/ai-sdk-providers/cohere)[Fireworks](/providers/ai-sdk-providers/fireworks)[DeepSeek](/providers/ai-sdk-providers/deepseek)[Cerebras](/providers/ai-sdk-providers/cerebras)[Replicate](/providers/ai-sdk-providers/replicate)[Perplexity](/providers/ai-sdk-providers/perplexity)[Luma](/providers/ai-sdk-providers/luma)[ElevenLabs](/providers/ai-sdk-providers/elevenlabs)[AssemblyAI](/providers/ai-sdk-providers/assemblyai)[Deepgram](/providers/ai-sdk-providers/deepgram)[Gladia](/providers/ai-sdk-providers/gladia)[LMNT](/providers/ai-sdk-providers/lmnt)[Hume](/providers/ai-sdk-providers/hume)[Rev.ai](/providers/ai-sdk-providers/revai)[OpenAI Compatible Providers](/providers/openai-compatible-providers)[Writing a Custom Provider](/providers/openai-compatible-providers/custom-providers)[LM Studio](/providers/openai-compatible-providers/lmstudio)[NVIDIA NIM](/providers/openai-compatible-providers/nim)[Baseten](/providers/openai-compatible-providers/baseten)[Community Providers](/providers/community-providers)[Writing a Custom Provider](/providers/community-providers/custom-providers)[Qwen](/providers/community-providers/qwen)[Ollama](/providers/community-providers/ollama)[Chrome AI](/providers/community-providers/chrome-ai)[Requesty](/providers/community-providers/requesty)[FriendliAI](/providers/community-providers/friendliai)[Portkey](/providers/community-providers/portkey)[Cloudflare Workers AI](/providers/community-providers/cloudflare-workers-ai)[Cloudflare AI Gateway](/providers/community-providers/cloudflare-ai-gateway)[OpenRouter](/providers/community-providers/openrouter)[Azure AI](/providers/community-providers/azure-ai)[Crosshatch](/providers/community-providers/crosshatch)[Mixedbread](/providers/community-providers/mixedbread)[Voyage AI](/providers/community-providers/voyage-ai)[Mem0](/providers/community-providers/mem0)[Letta](/providers/community-providers/letta)[LLamaCpp](/providers/community-providers/llama-cpp)[Anthropic Vertex](/providers/community-providers/anthropic-vertex-ai)[Spark](/providers/community-providers/spark)[Inflection AI](/providers/community-providers/inflection-ai)[LangDB](/providers/community-providers/langdb)[Zhipu AI](/providers/community-providers/zhipu)[SambaNova](/providers/community-providers/sambanova)[Dify](/providers/community-providers/dify)[Sarvam](/providers/community-providers/sarvam)[Adapters](/providers/adapters)[LangChain](/providers/adapters/langchain)[LlamaIndex](/providers/adapters/llamaindex)[Observability Integrations](/providers/observability)[Braintrust](/providers/observability/braintrust)[Helicone](/providers/observability/helicone)[Laminar](/providers/observability/laminar)[Langfuse](/providers/observability/langfuse)[LangSmith](/providers/observability/langsmith)[LangWatch](/providers/observability/langwatch)[Patronus](/providers/observability/patronus)[Traceloop](/providers/observability/traceloop)[Weave](/providers/observability/weave)[Community Providers](/providers/community-providers)Writing a Custom Provider
# [Writing a Custom Provider](#writing-a-custom-provider)

The AI SDK provides a [Language Model Specification](https://github.com/vercel/ai/tree/main/packages/provider/src/language-model/v1).
You can write your own provider that adheres to the specification and it will be compatible with the AI SDK.

You can find the Language Model Specification in the [AI SDK repository](https://github.com/vercel/ai/tree/main/packages/provider/src/language-model/v1).
It can be imported from `'@ai-sdk/provider'`. We also provide utilities that make it easier to implement a custom provider. You can find them in the `@ai-sdk/provider-utils` package ([source code](https://github.com/vercel/ai/tree/main/packages/provider-utils)).

If you open-source a provider, we'd love to promote it here. Please send us a
PR to add it to the [Community Providers](/providers/community-providers)
section.

## [Provider Implementation Guide](#provider-implementation-guide)

Implementing a custom language model provider involves several steps:

* Creating an entry point
* Adding a language model implementation
* Mapping the input (prompt, tools, settings)
* Processing the results (generate, streaming, tool calls)
* Supporting object generation

The best way to get started is to copy a reference implementation and modify it to fit your needs.
Check out the [Mistral reference implementation](https://github.com/vercel/ai/tree/main/packages/mistral)
to see how the project is structured, and feel free to copy the setup.

### [Creating an Entry Point](#creating-an-entry-point)

Each AI SDK provider should follow the pattern of using a factory function that returns a provider instance
and provide a default instance.

custom-provider.ts
```
import {  generateId,  loadApiKey,  withoutTrailingSlash,} from '@ai-sdk/provider-utils';import { CustomChatLanguageModel } from './custom-chat-language-model';import { CustomChatModelId, CustomChatSettings } from './custom-chat-settings';
// model factory function with additional methods and propertiesexport interface CustomProvider {  (    modelId: CustomChatModelId,    settings?: CustomChatSettings,  ): CustomChatLanguageModel;
  // explicit method for targeting a specific API in case there are several  chat(    modelId: CustomChatModelId,    settings?: CustomChatSettings,  ): CustomChatLanguageModel;}
// optional settings for the providerexport interface CustomProviderSettings {  /**Use a different URL prefix for API calls, e.g. to use proxy servers.   */  baseURL?: string;
  /**API key.   */  apiKey?: string;
  /**Custom headers to include in the requests.     */  headers?: Record<string, string>;}
// provider factory functionexport function createCustomProvider(  options: CustomProviderSettings = {},): CustomProvider {  const createModel = (    modelId: CustomChatModelId,    settings: CustomChatSettings = {},  ) =>    new CustomChatLanguageModel(modelId, settings, {      provider: 'custom.chat',      baseURL:        withoutTrailingSlash(options.baseURL) ?? 'https://custom.ai/api/v1',      headers: () => ({        Authorization: `Bearer ${loadApiKey({          apiKey: options.apiKey,          environmentVariableName: 'CUSTOM_API_KEY',          description: 'Custom Provider',        })}`,        ...options.headers,      }),      generateId: options.generateId ?? generateId,    });
  const provider = function (    modelId: CustomChatModelId,    settings?: CustomChatSettings,  ) {    if (new.target) {      throw new Error(        'The model factory function cannot be called with the new keyword.',      );    }
    return createModel(modelId, settings);  };
  provider.chat = createModel;
  return provider;}
/** * Default custom provider instance. */export const customProvider = createCustomProvider();
```
### [Implementing the Language Model](#implementing-the-language-model)

A [language model](https://github.com/vercel/ai/blob/main/packages/provider/src/language-model/v1/language-model-v1.ts) needs to implement:

* metadata fields
  + `specificationVersion: 'v1'` - always `'v1'`
  + `provider: string` - name of the provider
  + `modelId: string` - unique identifier of the model
  + `defaultObjectGenerationMode` - default object generation mode, e.g. "json"
* `doGenerate` method
* `doStream` method

Check out the [Mistral language model](https://github.com/vercel/ai/blob/main/packages/mistral/src/mistral-chat-language-model.ts) as an example.

At a high level, both `doGenerate` and `doStream` methods should:

1. **Map the prompt and the settings to the format required by the provider API.** This can be extracted, e.g. the Mistral provider contains a `getArgs` method.
2. **Call the provider API.** You could e.g. use fetch calls or a library offered by the provider.
3. **Process the results.** You need to convert the response to the format required by the AI SDK.

### [Errors](#errors)

The AI SDK provides [standardized errors](https://github.com/vercel/ai/tree/main/packages/provider/src/errors) that should be used by providers where possible. This will make it easy for user to debug them.

### [Retries, timeouts, and abort signals](#retries-timeouts-and-abort-signals)

The AI SDK will handle retries, timeouts, and aborting requests in a unified way. The model classes should not implement retries or timeouts themselves. Instead, they should use the `abortSignal` parameter to determine when the call should be aborted, and they should throw `ApiCallErrors` (or similar) with a correct `isRetryable` flag when errors such as network errors occur.

On this page[Writing a Custom Provider](#writing-a-custom-provider)[Provider Implementation Guide](#provider-implementation-guide)[Creating an Entry Point](#creating-an-entry-point)[Implementing the Language Model](#implementing-the-language-model)[Errors](#errors)[Retries, timeouts, and abort signals](#retries-timeouts-and-abort-signals)Elevate your AI applications with Vercel.Trusted by OpenAI, Replicate, Suno, Pinecone, and more.Vercel provides tools and infrastructure to deploy AI apps and features at scale.[Talk to an expert](https://vercel.com/contact/sales?utm_source=ai_sdk&utm_medium=web&utm_campaign=contact_sales_cta&utm_content=talk_to_an_expert_sdk_docs)
#### Resources

[Docs](/docs)[Cookbook](/cookbook)[Providers](/providers)[Showcase](/showcase)[GitHub](https://github.com/vercel/ai)[Discussions](https://github.com/vercel/ai/discussions)
#### More

[Playground](/playground)[Contact Sales](https://vercel.com/contact/sales)
#### About Vercel

[Next.js + Vercel](https://vercel.com/frameworks/nextjs)[Open Source Software](https://vercel.com/oss)[GitHub](https://github.com/vercel)[X](https://x.com/vercel)
#### Legal

[Privacy Policy](https://vercel.com/legal/privacy-policy)

© 2025 Vercel, Inc.


