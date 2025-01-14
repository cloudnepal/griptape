## Overview

Griptape provides several abstractions for working with data.

![Data Architecture](../../assets/img/data-architecture.png)

[Artifacts](./artifacts.md) are used for passing different types of data, such as text, lists, and blobs, between Griptape components.

[Embedding Drivers](../drivers/embedding-drivers.md) are used to generate vector embeddings from text.

[Loaders](./loaders.md) are used to load textual data from different sources.

[Chunkers](./chunkers.md) are used to split arbitrarily long text into chunks of certain token length.

**Tokenizers** are used to tokenize and detokenize text in order to track LLM token limits.

[RAG Engines](../engines/rag-engines.md) are used for implementing modular RAG pipelines.

[Extraction Engines](../engines/extraction-engines.md) are used for extracting structured content.

[Summary Engines](../engines/summary-engines.md) are used for summarizing text content.

[Vector Store Drivers](../drivers/vector-store-drivers.md) are used to store and query vector databases.

[Prompt Drivers](../drivers/prompt-drivers.md) are used to call LLM APIs.
