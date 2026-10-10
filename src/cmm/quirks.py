from typing import Dict, Any, Optional, Tuple

class ProviderQuirkProfile:
    def __init__(
        self,
        error_format: Dict[str, Any],
        headers: Dict[str, str] = None,
        error_code_map: Dict[int, str] = None
    ):
        """
        Defines the quirks for a specific provider.

        :param error_format: A template for the error response body.
                             Placeholders like {message} and {code} should be used.
        :param headers: Default headers that should be present in every response.
        :param error_code_map: Mapping of HTTP status codes to provider-specific error codes.
        """
        self.error_format = error_format
        self.headers = headers or {}
        self.error_code_map = error_code_map or {}

    def format_error(self, status_code: int, message: str) -> Dict[str, Any]:
        """Formats the error message according to the provider's quirk profile."""
        code = self.error_code_map.get(status_code, "internal_error")
        # Simple string replacement for placeholders
        formatted_error = self.error_format.copy()

        # Recursively replace placeholders in the dictionary
        def replace_placeholders(obj):
            if isinstance(obj, str):
                return obj.replace("{message}", message).replace("{code}", code)
            elif isinstance(obj, dict):
                return {k: replace_placeholders(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [replace_placeholders(i) for i in obj]
            return obj

        return replace_placeholders(formatted_error)

# --- Provider Profiles ---

# Anthropic: Typical error format has 'type' and 'message'
ANTHROPIC_QUIRKS = ProviderQuirkProfile(
    error_format={
        "type": "{code}",
        "message": "{message}"
    },
    headers={
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    },
    error_code_map={
        400: "invalid_request_error",
        401: "authentication_error",
        403: "permission_denied_error",
        404: "not_found_error",
        429: "rate_limit_error",
        500: "api_error",
    }
)

# Azure OpenAI: Usually has an 'error' object with 'code' and 'message'
AZURE_QUIRKS = ProviderQuirkProfile(
    error_format={
        "error": {
            "code": "{code}",
            "message": "{message}"
        }
    },
    headers={
        "api-version": "2024-02-15-preview",
        "content-type": "application/json"
    },
    error_code_map={
        400: "InvalidRequest",
        401: "AuthenticationError",
        403: "AccessDenied",
        404: "ResourceNotFound",
        429: "TooManyRequests",
        500: "InternalServerError",
    }
)

# AWS Bedrock: Often uses a specific error structure depending on the model,
# but generally has a message and a code.
BEDROCK_QUIRKS = ProviderQuirkProfile(
    error_format={
        "errorMessage": "{message}",
        "errorCode": "{code}"
    },
    headers={
        "x-amzn-bedrock-version": "1.0",
        "content-type": "application/json"
    },
    error_code_map={
        400: "ValidationException",
        401: "UnrecognizedClientException",
        403: "AccessDeniedException",
        404: "ResourceNotFoundException",
        429: "ThrottlingException",
        500: "InternalServerError",
    }
)

# Default / Generic profile (e.g., for Ollama)
DEFAULT_QUIRKS = ProviderQuirkProfile(
    error_format={
        "error": "{message}"
    },
    headers={
        "content-type": "application/json"
    },
    error_code_map={
        400: "bad_request",
        401: "unauthorized",
        403: "forbidden",
        404: "not_found",
        429: "too_many_requests",
        500: "internal_server_error",
    }
)

QUIRK_PROFILES = {
    "anthropic": ANTHROPIC_QUIRKS,
    "azure": AZURE_QUIRKS,
    "bedrock": BEDROCK_QUIRKS,
    "default": DEFAULT_QUIRKS
}

def get_quirk_profile(provider_name: str) -> ProviderQuirkProfile:
    """Retrieves the quirk profile for a given provider, falling back to default."""
    return QUIRK_PROFILES.get(provider_name.lower(), DEFAULT_QUIRKS)
