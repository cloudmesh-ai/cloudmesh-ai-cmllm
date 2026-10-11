# Chaos Engineering Guide

The Chaos Engine in Cloudmesh AI llm-mock is designed to help you build resilient LLM applications. In the real world, LLM APIs are not perfectly stable—they experience latency spikes, rate limits, and occasional catastrophic failures.

By simulating these conditions, you can ensure your application handles errors gracefully, implements proper retry logic, and provides a good user experience even when the backend is struggling.

## Chaos Features

You can configure all chaos settings in real-time via the **Admin Dashboard** (`/admin`).

### 1. Random Failures
Simulate intermittent API instability by setting a **Failure Rate**.
- **How it works**: For every request, the server rolls a die. If the result is within the failure rate, the request fails.
- **Simulated Errors**: The server randomly injects either a `429 Too Many Requests` or a `500 Internal Server Error`.
- **Use Case**: Test if your application implements exponential backoff and retry logic.

### 2. Simulated Latency
Test how your UI handles slow responses by configuring a **Latency Range** (Min/Max).
- **How it works**: The server adds a random delay between the minimum and maximum configured values before returning the response.
- **Use Case**: Verify that your frontend displays loading states and that your API clients have appropriate timeout settings.

### 3. The Meltdown Profile
The **Panic Button** in the Admin Dashboard triggers "Meltdown Mode," a simulated cascading service failure that progresses through three stages:

| Stage | Duration | Effect | Simulated State |
| :--- | :--- | :--- | :--- |
| **1. Degradation** | 0-15s | Max Latency | The API becomes extremely slow. |
| **2. Outage** | 15-30s | 100% Failure | Every request returns a `500 Internal Server Error`. |
| **3. Collapse** | 30s+ | Service Unavailable | The API returns `503 Service Unavailable`. |

**Use Case**: Test how your system behaves during a total provider outage and whether your failover mechanisms (e.g., switching to a backup provider) trigger correctly.

### 4. TPM (Tokens Per Minute) Limiting
Simulate the strict rate limits imposed by providers like OpenAI or Anthropic.
- **How it works**: The server tracks the number of tokens processed per minute. If the limit is exceeded, it returns a `429 Too Many Requests` error with a `Retry-After` header.
- **Use Case**: Test your token-counting logic and rate-limiting middleware.

### 5. Context Window Simulation
Test how your application handles prompts that are too large for the model.
- **How it works**: You can configure a maximum **Context Window** (in tokens). If the prompt (or the combined prompt and response) exceeds this limit, the server returns a `400 Bad Request`.
- **Use Case**: Verify that your application correctly truncates history or warns the user when the context limit is reached.

### 6. GPU OOM (Out-of-Memory) Simulation
Simulate the behavior of a provider that can only load a limited number of models into VRAM.
- **How it works**: In the Admin Dashboard, you can specify a list of **Loaded Models**. If a request is made for a model not in this list, the server returns a `404 Not Found`, simulating an OOM error or a model-not-loaded state.
- **Use Case**: Test your application's ability to handle "Model Not Found" errors and prompt the user to select a different model.

## Testing Recipes

Transform the Chaos Engine's features into solutions for specific production problems. Use these recipes to validate your application's resilience.

### Recipe: The "Flaky API"
**Goal**: Test exponential backoff and retry logic.

**Configuration Steps**:
1. Open the **Admin Dashboard** (`/admin`).
2. Set the **Failure Rate** to `5%`.
3. Set the **Latency Range** to `Min: 1s`, `Max: 3s`.

**What to look for**:
- Ensure the application does not immediately surface an error to the user on the first failure.
- Verify that retries occur with increasing delays (exponential backoff).
- The request should eventually succeed once the random failure roll passes.

### Recipe: The "Cold Start"
**Goal**: Test handling of model loading/OOM errors.

**Configuration Steps**:
1. Open the **Admin Dashboard** (`/admin`).
2. Locate the **Loaded Models** list.
3. Remove the model your application is currently targeting from the list.

**What to look for**:
- The server will return a `404 Not Found` (simulating a GPU OOM or unloaded model).
- Verify that the application handles this gracefully (e.g., by notifying the user that the model is loading or automatically falling back to a different available model).

### Recipe: The "Safety Wall"
**Goal**: Test if the application correctly handles safety refusals without crashing.

**Configuration Steps**:
1. Send a prompt containing restricted keywords such as `"illegal"` or `"exploit"`.
2. Ensure the server is configured to return a standard safety refusal for these terms.

**What to look for**:
- The application should receive the refusal response from the API.
- The UI should display the refusal message clearly to the user.
- Verify that no unhandled exceptions or "empty response" errors are triggered in the frontend.
