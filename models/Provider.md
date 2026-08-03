# Domain Model: Provider

> Canonical domain model. See [architecture/PROVIDER_SYSTEM.md](../architecture/PROVIDER_SYSTEM.md).

```kotlin
package com.nexora.app.core.providers

data class ProviderConfig(
    val id: String,
    val type: ProviderType,
    val name: String,
    val baseUrl: String,
    val defaultModel: String,
    val maxTokens: Int = 4096,
    val temperature: Double = 0.7
    // API key stored separately in SecureKeyStore
)

data class Model(
    val id: String,
    val name: String,
    val providerId: String,
    val capabilities: Set<ProviderCapability>,
    val contextWindow: Int,
    val inputPricePer1k: Double?,
    val outputPricePer1k: Double?
)

/**
 * A named, user-configurable provider configuration.
 * Users may create multiple profiles per provider (e.g. different API keys,
 * endpoints, models, or streaming settings) and switch between them at any
 * time. One profile is the default per workspace.
 */
data class ProviderProfile(
    val id: String,
    val name: String,               // e.g. "OpenAI Work", "Local Fast"
    val providerType: ProviderType,
    val config: ProviderConfig,     // endpoint, default model, params
    val apiKeyRef: String?,         // SecureKeyStore alias (key never in plaintext)
    val streamingEnabled: Boolean = true,
    val capabilities: Set<ProviderCapability> = emptySet(),
    val isDefault: Boolean = false
)
```
