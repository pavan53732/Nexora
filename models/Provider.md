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
```
