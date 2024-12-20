# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations
import json

import os
import psutil
import subprocess
from typing import Any, Union, Mapping
from typing_extensions import Self, override

import httpx

from . import resources, _exceptions
from ._qs import Querystring
from ._types import (
    NOT_GIVEN,
    Omit,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
)
from ._utils import (
    is_given,
    get_async_library,
)
from ._version import __version__
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

__all__ = [
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "resources",
    "LlamaStackClient",
    "AsyncLlamaStackClient",
    "Client",
    "AsyncClient",
]


class LlamaStackClient(SyncAPIClient):
    agents: resources.AgentsResource
    batch_inference: resources.BatchInferenceResource
    datasets: resources.DatasetsResource
    eval: resources.EvalResource
    inspect: resources.InspectResource
    inference: resources.InferenceResource
    memory: resources.MemoryResource
    memory_banks: resources.MemoryBanksResource
    models: resources.ModelsResource
    post_training: resources.PostTrainingResource
    providers: resources.ProvidersResource
    routes: resources.RoutesResource
    safety: resources.SafetyResource
    shields: resources.ShieldsResource
    synthetic_data_generation: resources.SyntheticDataGenerationResource
    telemetry: resources.TelemetryResource
    datasetio: resources.DatasetioResource
    scoring: resources.ScoringResource
    scoring_functions: resources.ScoringFunctionsResource
    eval_tasks: resources.EvalTasksResource
    with_raw_response: LlamaStackClientWithRawResponse
    with_streaming_response: LlamaStackClientWithStreamedResponse

    # client options

    def __init__(
        self,
        *,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
        provider_data: Mapping[str, Any] | None = None,
    ) -> None:
        """Construct a new synchronous llama-stack-client client instance."""
        if base_url is None:
            base_url = os.environ.get("LLAMA_STACK_CLIENT_BASE_URL")
        if base_url is None:
            base_url = f"http://any-hosted-llama-stack.com"

        if provider_data is not None:
            if default_headers is None:
                default_headers = {}
            default_headers["X-LlamaStack-ProviderData"] = json.dumps(provider_data)
        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.agents = resources.AgentsResource(self)
        self.batch_inference = resources.BatchInferenceResource(self)
        self.datasets = resources.DatasetsResource(self)
        self.eval = resources.EvalResource(self)
        self.inspect = resources.InspectResource(self)
        self.inference = resources.InferenceResource(self)
        self.memory = resources.MemoryResource(self)
        self.memory_banks = resources.MemoryBanksResource(self)
        self.models = resources.ModelsResource(self)
        self.post_training = resources.PostTrainingResource(self)
        self.providers = resources.ProvidersResource(self)
        self.routes = resources.RoutesResource(self)
        self.safety = resources.SafetyResource(self)
        self.shields = resources.ShieldsResource(self)
        self.synthetic_data_generation = resources.SyntheticDataGenerationResource(self)
        self.telemetry = resources.TelemetryResource(self)
        self.datasetio = resources.DatasetioResource(self)
        self.scoring = resources.ScoringResource(self)
        self.scoring_functions = resources.ScoringFunctionsResource(self)
        self.eval_tasks = resources.EvalTasksResource(self)
        self.with_raw_response = LlamaStackClientWithRawResponse(self)
        self.with_streaming_response = LlamaStackClientWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }
    

    def _get_size(self, bytes):
        for unit in ['', 'K', 'M', 'G', 'T', 'P']:
            if bytes < 1024:
                return f"{bytes:.2f}{unit}B"
            bytes /= 1024
            
    def check_system_resources(self, model_name):
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Memory
        mem = psutil.virtual_memory()
        mem_used = self._get_size(mem.used)
        mem_total = self._get_size(mem.total)
        mem_percent = mem.percent
        
        # GPU
        try:
            gpu_info = subprocess.check_output(
                ['nvidia-smi', '--query-gpu=utilization.gpu,memory.used,memory.total', '--format=csv,noheader,nounits']
            ).decode('utf-8').strip().split(',')
            gpu_util = f"{gpu_info[0].strip()}%"
            gpu_mem = f"{gpu_info[1].strip()}MB / {gpu_info[2].strip()}MB"
        except:
            gpu_util = "N/A"
            gpu_mem = "N/A"
            
        print(f"Available resources for {model_name}")
        print(f"CPU Usage: {cpu_percent}%")
        print(f"Memory: {mem_used} / {mem_total} ({mem_percent}%)")
        print(f"GPU Util: {gpu_util}")
        print(f"GPU Memory: {gpu_mem}")
        
        return {
            "cpu_percent": cpu_percent,
            "mem_used": mem_used,
            "mem_total": mem_total,
            "mem_percent": mem_percent,
            "gpu_util": gpu_util,
            "gpu_mem": gpu_mem
        }

    def check_recommended_resources(self, model_name, recommendation_json) -> None:
       if recommendation_json["system_resources"]["cpu"] < model_requirements_dict[model_name]["cpu"]:
           raise ValueError(f"CPU does not meet the recommended requirements: {model_requirements_dict[model_name]['cpu']} cores")
        if recommendation_json["system_resources"]["ram"] < model_requirements_dict[model_name]["ram"]:
            raise ValueError(f"RAM does not meet the recommended requirements: {model_requirements_dict[model_name]['ram']} GB")
        if recommendation_json["system_resources"]["gpu"] < model_requirements_dict[model_name]["gpu"]:
            raise ValueError(f"GPU does not meet the recommended requirements: {model_requirements_dict[model_name]['gpu']} GB")
        if recommendation_json["system_resources"]["storage"] < model_requirements_dict[model_name]["storage"]:
            raise ValueError(f"Storage does not meet the recommended requirements: {model_requirements_dict[model_name]['storage']} GB")
        

    def copy(
        self,
        *,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncLlamaStackClient(AsyncAPIClient):
    agents: resources.AsyncAgentsResource
    batch_inference: resources.AsyncBatchInferenceResource
    datasets: resources.AsyncDatasetsResource
    eval: resources.AsyncEvalResource
    inspect: resources.AsyncInspectResource
    inference: resources.AsyncInferenceResource
    memory: resources.AsyncMemoryResource
    memory_banks: resources.AsyncMemoryBanksResource
    models: resources.AsyncModelsResource
    post_training: resources.AsyncPostTrainingResource
    providers: resources.AsyncProvidersResource
    routes: resources.AsyncRoutesResource
    safety: resources.AsyncSafetyResource
    shields: resources.AsyncShieldsResource
    synthetic_data_generation: resources.AsyncSyntheticDataGenerationResource
    telemetry: resources.AsyncTelemetryResource
    datasetio: resources.AsyncDatasetioResource
    scoring: resources.AsyncScoringResource
    scoring_functions: resources.AsyncScoringFunctionsResource
    eval_tasks: resources.AsyncEvalTasksResource
    with_raw_response: AsyncLlamaStackClientWithRawResponse
    with_streaming_response: AsyncLlamaStackClientWithStreamedResponse

    # client options

    def __init__(
        self,
        *,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
        provider_data: Mapping[str, Any] | None = None,
    ) -> None:
        """Construct a new async llama-stack-client client instance."""
        if base_url is None:
            base_url = os.environ.get("LLAMA_STACK_CLIENT_BASE_URL")
        if base_url is None:
            base_url = f"http://any-hosted-llama-stack.com"

        if provider_data is not None:
            if default_headers is None:
                default_headers = {}
            default_headers["X-LlamaStack-ProviderData"] = json.dumps(provider_data)
        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.agents = resources.AsyncAgentsResource(self)
        self.batch_inference = resources.AsyncBatchInferenceResource(self)
        self.datasets = resources.AsyncDatasetsResource(self)
        self.eval = resources.AsyncEvalResource(self)
        self.inspect = resources.AsyncInspectResource(self)
        self.inference = resources.AsyncInferenceResource(self)
        self.memory = resources.AsyncMemoryResource(self)
        self.memory_banks = resources.AsyncMemoryBanksResource(self)
        self.models = resources.AsyncModelsResource(self)
        self.post_training = resources.AsyncPostTrainingResource(self)
        self.providers = resources.AsyncProvidersResource(self)
        self.routes = resources.AsyncRoutesResource(self)
        self.safety = resources.AsyncSafetyResource(self)
        self.shields = resources.AsyncShieldsResource(self)
        self.synthetic_data_generation = resources.AsyncSyntheticDataGenerationResource(self)
        self.telemetry = resources.AsyncTelemetryResource(self)
        self.datasetio = resources.AsyncDatasetioResource(self)
        self.scoring = resources.AsyncScoringResource(self)
        self.scoring_functions = resources.AsyncScoringFunctionsResource(self)
        self.eval_tasks = resources.AsyncEvalTasksResource(self)
        self.with_raw_response = AsyncLlamaStackClientWithRawResponse(self)
        self.with_streaming_response = AsyncLlamaStackClientWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class LlamaStackClientWithRawResponse:
    def __init__(self, client: LlamaStackClient) -> None:
        self.agents = resources.AgentsResourceWithRawResponse(client.agents)
        self.batch_inference = resources.BatchInferenceResourceWithRawResponse(client.batch_inference)
        self.datasets = resources.DatasetsResourceWithRawResponse(client.datasets)
        self.eval = resources.EvalResourceWithRawResponse(client.eval)
        self.inspect = resources.InspectResourceWithRawResponse(client.inspect)
        self.inference = resources.InferenceResourceWithRawResponse(client.inference)
        self.memory = resources.MemoryResourceWithRawResponse(client.memory)
        self.memory_banks = resources.MemoryBanksResourceWithRawResponse(client.memory_banks)
        self.models = resources.ModelsResourceWithRawResponse(client.models)
        self.post_training = resources.PostTrainingResourceWithRawResponse(client.post_training)
        self.providers = resources.ProvidersResourceWithRawResponse(client.providers)
        self.routes = resources.RoutesResourceWithRawResponse(client.routes)
        self.safety = resources.SafetyResourceWithRawResponse(client.safety)
        self.shields = resources.ShieldsResourceWithRawResponse(client.shields)
        self.synthetic_data_generation = resources.SyntheticDataGenerationResourceWithRawResponse(
            client.synthetic_data_generation
        )
        self.telemetry = resources.TelemetryResourceWithRawResponse(client.telemetry)
        self.datasetio = resources.DatasetioResourceWithRawResponse(client.datasetio)
        self.scoring = resources.ScoringResourceWithRawResponse(client.scoring)
        self.scoring_functions = resources.ScoringFunctionsResourceWithRawResponse(client.scoring_functions)
        self.eval_tasks = resources.EvalTasksResourceWithRawResponse(client.eval_tasks)


class AsyncLlamaStackClientWithRawResponse:
    def __init__(self, client: AsyncLlamaStackClient) -> None:
        self.agents = resources.AsyncAgentsResourceWithRawResponse(client.agents)
        self.batch_inference = resources.AsyncBatchInferenceResourceWithRawResponse(client.batch_inference)
        self.datasets = resources.AsyncDatasetsResourceWithRawResponse(client.datasets)
        self.eval = resources.AsyncEvalResourceWithRawResponse(client.eval)
        self.inspect = resources.AsyncInspectResourceWithRawResponse(client.inspect)
        self.inference = resources.AsyncInferenceResourceWithRawResponse(client.inference)
        self.memory = resources.AsyncMemoryResourceWithRawResponse(client.memory)
        self.memory_banks = resources.AsyncMemoryBanksResourceWithRawResponse(client.memory_banks)
        self.models = resources.AsyncModelsResourceWithRawResponse(client.models)
        self.post_training = resources.AsyncPostTrainingResourceWithRawResponse(client.post_training)
        self.providers = resources.AsyncProvidersResourceWithRawResponse(client.providers)
        self.routes = resources.AsyncRoutesResourceWithRawResponse(client.routes)
        self.safety = resources.AsyncSafetyResourceWithRawResponse(client.safety)
        self.shields = resources.AsyncShieldsResourceWithRawResponse(client.shields)
        self.synthetic_data_generation = resources.AsyncSyntheticDataGenerationResourceWithRawResponse(
            client.synthetic_data_generation
        )
        self.telemetry = resources.AsyncTelemetryResourceWithRawResponse(client.telemetry)
        self.datasetio = resources.AsyncDatasetioResourceWithRawResponse(client.datasetio)
        self.scoring = resources.AsyncScoringResourceWithRawResponse(client.scoring)
        self.scoring_functions = resources.AsyncScoringFunctionsResourceWithRawResponse(client.scoring_functions)
        self.eval_tasks = resources.AsyncEvalTasksResourceWithRawResponse(client.eval_tasks)


class LlamaStackClientWithStreamedResponse:
    def __init__(self, client: LlamaStackClient) -> None:
        self.agents = resources.AgentsResourceWithStreamingResponse(client.agents)
        self.batch_inference = resources.BatchInferenceResourceWithStreamingResponse(client.batch_inference)
        self.datasets = resources.DatasetsResourceWithStreamingResponse(client.datasets)
        self.eval = resources.EvalResourceWithStreamingResponse(client.eval)
        self.inspect = resources.InspectResourceWithStreamingResponse(client.inspect)
        self.inference = resources.InferenceResourceWithStreamingResponse(client.inference)
        self.memory = resources.MemoryResourceWithStreamingResponse(client.memory)
        self.memory_banks = resources.MemoryBanksResourceWithStreamingResponse(client.memory_banks)
        self.models = resources.ModelsResourceWithStreamingResponse(client.models)
        self.post_training = resources.PostTrainingResourceWithStreamingResponse(client.post_training)
        self.providers = resources.ProvidersResourceWithStreamingResponse(client.providers)
        self.routes = resources.RoutesResourceWithStreamingResponse(client.routes)
        self.safety = resources.SafetyResourceWithStreamingResponse(client.safety)
        self.shields = resources.ShieldsResourceWithStreamingResponse(client.shields)
        self.synthetic_data_generation = resources.SyntheticDataGenerationResourceWithStreamingResponse(
            client.synthetic_data_generation
        )
        self.telemetry = resources.TelemetryResourceWithStreamingResponse(client.telemetry)
        self.datasetio = resources.DatasetioResourceWithStreamingResponse(client.datasetio)
        self.scoring = resources.ScoringResourceWithStreamingResponse(client.scoring)
        self.scoring_functions = resources.ScoringFunctionsResourceWithStreamingResponse(client.scoring_functions)
        self.eval_tasks = resources.EvalTasksResourceWithStreamingResponse(client.eval_tasks)


class AsyncLlamaStackClientWithStreamedResponse:
    def __init__(self, client: AsyncLlamaStackClient) -> None:
        self.agents = resources.AsyncAgentsResourceWithStreamingResponse(client.agents)
        self.batch_inference = resources.AsyncBatchInferenceResourceWithStreamingResponse(client.batch_inference)
        self.datasets = resources.AsyncDatasetsResourceWithStreamingResponse(client.datasets)
        self.eval = resources.AsyncEvalResourceWithStreamingResponse(client.eval)
        self.inspect = resources.AsyncInspectResourceWithStreamingResponse(client.inspect)
        self.inference = resources.AsyncInferenceResourceWithStreamingResponse(client.inference)
        self.memory = resources.AsyncMemoryResourceWithStreamingResponse(client.memory)
        self.memory_banks = resources.AsyncMemoryBanksResourceWithStreamingResponse(client.memory_banks)
        self.models = resources.AsyncModelsResourceWithStreamingResponse(client.models)
        self.post_training = resources.AsyncPostTrainingResourceWithStreamingResponse(client.post_training)
        self.providers = resources.AsyncProvidersResourceWithStreamingResponse(client.providers)
        self.routes = resources.AsyncRoutesResourceWithStreamingResponse(client.routes)
        self.safety = resources.AsyncSafetyResourceWithStreamingResponse(client.safety)
        self.shields = resources.AsyncShieldsResourceWithStreamingResponse(client.shields)
        self.synthetic_data_generation = resources.AsyncSyntheticDataGenerationResourceWithStreamingResponse(
            client.synthetic_data_generation
        )
        self.telemetry = resources.AsyncTelemetryResourceWithStreamingResponse(client.telemetry)
        self.datasetio = resources.AsyncDatasetioResourceWithStreamingResponse(client.datasetio)
        self.scoring = resources.AsyncScoringResourceWithStreamingResponse(client.scoring)
        self.scoring_functions = resources.AsyncScoringFunctionsResourceWithStreamingResponse(client.scoring_functions)
        self.eval_tasks = resources.AsyncEvalTasksResourceWithStreamingResponse(client.eval_tasks)


Client = LlamaStackClient

AsyncClient = AsyncLlamaStackClient

LLAMA_32_3B_REQUIREMENTS = {
    "hardware_requirements": {
        "cpu": {
            "type": "Multicore processor",
            "minimum_cores": None,  # Not specified
            "notes": "General multicore processor required"
        },
        "ram": {
            "minimum_gb": 16,
            "notes": "Recommended minimum"
        },
        "gpu": {
            "recommended_type": "NVIDIA RTX series",
            "minimum_vram_gb": 8,
            "notes": "For optimal performance"
        },
        "storage": {
            "space_required": "Variable",
            "notes": "Sufficient for model files, size varies by model"
        }
    }
}

LLAMA_32_90B_VISION_REQUIREMENTS = {
    "model_name": "Llama-3.2-90B-Vision",
    "hardware_requirements": {
        "gpu": {
            "minimum_vram_gb": 180,
            "recommended_cards": ["NVIDIA A100 80GB"],
            "notes": "Multiple lower-capacity GPUs can be used in parallel for inference"
        },
        "cpu": {
            "minimum_cores": 32,
            "recommended": [
                "Latest AMD EPYC",
                "Latest Intel Xeon"
            ]
        },
        "ram": {
            "minimum_gb": 256,
            "recommended_gb": 512,
            "notes": "For optimal performance"
        },
        "storage": {
            "type": "NVMe SSD",
            "minimum_free_space_gb": 500,
            "model_size_gb": 180
        }
    },
    "software_requirements": {
        "operating_system": {
            "primary": "Linux",
            "recommended": "Ubuntu 20.04 LTS or higher",
            "alternative": {
                "name": "Windows",
                "notes": "Supported with specific optimizations"
            }
        }
    },
    "quantization_options": {
        "supported": True,
        "notes": "Can be quantized for lower resource usage"
    }
}

model_requirements_dict = {
    "Llama-3.2:latest": LLAMA_32_3B_REQUIREMENTS,
    "Llama-3.2-90B-Vision": LLAMA_32_90B_VISION_REQUIREMENTS
}