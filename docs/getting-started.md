# Getting Started: Your First 15 Minutes with Cloudmesh AI llm-mock

Welcome to **Cloudmesh AI llm-mock**! This interactive tutorial is designed to get you up and running in minutes. Instead of just showing you how to start the server, we're going to walk you through a complete "resilience loop": from a successful request to a total system meltdown, and finally, how to fix your code to handle it.

By the end of this guide, you'll understand how to use `cmm` to battle-test your LLM application.

---

## 1. Install `cmm`

First, ensure you have Python 3.10+ installed. If you've cloned the repository, install the package in editable mode:

```bash
git clone https://github.com/cloudmesh-ai/cloudmesh-ai-llm-mock.git
cd cloudmesh-ai-llm-mock
pip install -e .
```

## 2. Start the Server

Launch the mock server to expose the OpenAI-compatible API:

```bash
cmm serve
```

The server is now running at `http://localhost:8888`. Keep this terminal open!

## 3. Send a Successful Prompt

Let's verify everything is working. You can do this in two ways:

### Option A: Using the User GUI (Recommended)
Open your browser and go to: [http://localhost:8888/chat](http://localhost:8888/chat)
Type a message and hit enter. You should see a smooth, streaming response.

### Option B: Using `curl`
Open a new terminal and run:

```bash
curl http://localhost:8888/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ollama-llama3",
    "messages": [{"role": "user", "content": "Hello! Are you working?"}]
  }'
```

**Result:** You should receive a JSON response with a successful AI completion.

---

## 4. Trigger a "Meltdown"

Now for the fun part. Real-world APIs don't always work. Let's simulate a catastrophic provider failure using the **Admin Dashboard**.

1. Open your browser to: [http://localhost:8888/admin](http://localhost:8888/admin)
2. Scroll down to the **Panic Button** section.
3. Click the **"Trigger Meltdown"** button.

You have just activated **Meltdown Mode**.

---

## 5. Observe the Failure

The Meltdown Profile doesn't just crash the server; it simulates a cascading failure. Try sending another prompt via the Chat UI or `curl` and watch what happens over the next 30 seconds:

| Time | What you'll see | What's happening |
| :--- | :--- | :--- |
| **0-15s** | Extreme slowness | **Degradation**: The server injects maximum latency. Your app might hang or time out. |
| **15-30s** | `500 Internal Server Error` | **Outage**: Every single request now fails immediately. |
| **30s+** | `503 Service Unavailable` | **Collapse**: The service is completely offline. |

**Notice:** If your application crashed or showed a raw error message to the user, you've found a resilience gap!

---

## 6. Fix the Application

How do we stop a provider "meltdown" from breaking our user experience? The gold standard is implementing **Exponential Backoff and Retries**.

Instead of a simple API call, wrap your request in a retry loop. Here is a conceptual example using Python and the popular `tenacity` library:

```python
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# We only want to retry on server errors (500, 503) or rate limits (429)
def is_retryable_error(exception):
    if isinstance(exception, requests.exceptions.HTTPError):
        return exception.response.status_code in [429, 500, 503]
    return False

@retry(
    stop=stop_after_attempt(5), 
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(requests.exceptions.HTTPError)
)
def call_llm_with_retry(prompt):
    response = requests.post(
        "http://localhost:8888/v1/chat/completions",
        json={"model": "ollama-llama3", "messages": [{"role": "user", "content": prompt}]}
    )
    response.raise_for_status()
    return response.json()

try:
    print(call_llm_with_retry("Hello!"))
except Exception as e:
    print(f"Even after retries, the service is down: {e}")
```

### Why this helps:
1. **Wait Exponential**: Instead of hammering the server, it waits 2s, then 4s, then 8s... giving the provider time to recover.
2. **Graceful Failure**: By catching the final exception, you can show the user a friendly message ("Our AI is taking a nap, please try again in a moment") instead of a crash.

---

## Next Steps

You've mastered the basics! Now that you know how to trigger a meltdown, explore the other Chaos tools in the Admin Dashboard:
- **Failure Rate**: Inject random 429s to test your retry logic more subtly.
- **TPM Limits**: Test how your app handles strict token quotas.
- **GPU OOM**: Simulate "Model Not Found" errors by restricting the **Loaded Models** list.

Happy testing!
