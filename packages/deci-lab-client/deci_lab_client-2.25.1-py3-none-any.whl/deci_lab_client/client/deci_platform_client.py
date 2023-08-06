import os
import time
import getpass
from pathlib import Path
from typing import Tuple, List, Optional
from uuid import UUID
import jwt
from jwt.exceptions import ExpiredSignatureError
import tempfile

import requests
from cryptography.fernet import Fernet, InvalidToken
from pydantic import BaseModel

from deci_lab_client.api.platform_api import PlatformApi
from deci_lab_client.api_client import ApiClient
from deci_lab_client.client.helpers import wait_until
from deci_lab_client.configuration import Configuration
from deci_lab_client.exceptions import ApiException
from deci_lab_client.models import (
    OptimizeModelResponse,
    FrameworkType,
    OptimizationRequestForm,
    APIResponse,
    ModelBenchmarkState,
)
from deci_lab_client.models.add_model_response import AddModelResponse
from deci_lab_client.models.model_metadata import ModelMetadata
from deci_lab_client.models.model_source import ModelSource


BEARER_TYPE = "Bearer"
ENCRYPT_KEY = b"VSyHy9dIgVpdZo03eG0XR0J8RJh6t1vX7BNXkt2WANo="
f_encryptor = Fernet(ENCRYPT_KEY)


class InvalidAuthenticationTokenError(Exception):
    pass


class DownloadModelError(Exception):
    pass


def get_docstring_from(original_function):
    """
    A decorator that attaches the docstring one function to another function in real time (for transparent auto completion).
    """

    def doc_wrapper(target):
        target.__doc__ = original_function.__doc__
        return target

    return doc_wrapper


class RequirementsInstallationFailedError(Exception):
    pass


class UnsupportedLoadedModelFramework(Exception):
    pass


class AddAndOptimizeResponse(BaseModel):
    model_id: UUID = None
    benchmark_request_id: UUID = None
    optimized_model_id: UUID = None
    optimization_request_id: UUID = None


class TimeoutWasReachedBeforeBenchmarkFinishedError(Exception):
    pass


class DeciPlatformClient(PlatformApi):
    """
    A wrapper for OpenAPI's generated client http library to deci's API.
    Extends the functionality of generated platform client and ease it's usage and experience.
    """

    TOKEN_PATH = f"{os.path.join(os.path.expanduser('~'), '.deci/auth/token')}"

    @staticmethod
    def _token_path_exists():
        return os.path.isfile(DeciPlatformClient.TOKEN_PATH)

    @staticmethod
    def _create_token_path_if_missing():
        if not DeciPlatformClient._token_path_exists():
            Path(os.path.dirname(DeciPlatformClient.TOKEN_PATH)).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _get_local_auth_token():
        if DeciPlatformClient._token_path_exists():
            try:
                with open(DeciPlatformClient.TOKEN_PATH, "rb") as file:
                    encrypted_text = file.read()
                    return f_encryptor.decrypt(encrypted_text).decode()
            except Exception:
                raise InvalidAuthenticationTokenError(
                    "Bad authentication token. Please log in to Deci lab in order to generate a new token"
                )
        return None

    def _append_auth_token_to_headers(self, auth_token):
        self.api_client.default_headers["Authorization"] = f"{BEARER_TYPE} {auth_token}"

    def __init__(self, api_host="api.deci.ai", api_port=443, https=True):
        """
        :param api_host: The host of deci's platform HTTP API.
        :type api_host: str
        :param api_host: The port of deci's platform HTTP API.
        :type api_port: int
        :param https: Whether to use https instead of HTTP. Using https Will add latency.
        :type https: bool
        """
        assert isinstance(api_port, int), "The api_port must be an int object"
        endpoint_host = "{api_host}:{api_port}".format(api_host=api_host, api_port=api_port)
        self._api_host = api_host
        self._endpoint_host = endpoint_host
        if https:
            base_url = "https://{endpoint}".format(endpoint=endpoint_host)
        else:
            base_url = "http://{endpoint}".format(endpoint=endpoint_host)
        self._base_url = base_url
        client_config = ApiClient(configuration=Configuration(host=base_url))
        super().__init__(client_config)

        try:
            local_token = DeciPlatformClient._get_local_auth_token()
            valid, token = DeciPlatformClient.verify_token_exp(token=local_token)
        except InvalidAuthenticationTokenError as e:
            print(e)
        else:
            if valid:
                self._append_auth_token_to_headers(token)
                print("Your Current session is valid. If you wish to login with another user call logout on the client")

    @staticmethod
    def verify_token_exp(token: str):
        """
        Checks the JWT token validity. If a token param is not provided it attempts to validate the currently stored
        token
        :param token:  A token obtained from the user settings page in the Lab
        :type token: str
        """
        if token:
            try:
                if token.index(" ") == 0:
                    print("Please provide a token without its type")
                    return False, None
            except ValueError:
                # This means that the token format does not include bearer/Bearer which is the desired behavior.
                pass
        else:
            return False, None

        try:
            jwt.decode(token, options={"verify_signature": False, "verify_exp": True})
        except ExpiredSignatureError:
            print(
                "It seems your authentication token has expired, Please login with your regular credentials first. You \
                may as well log in to the Lab UI and copy your token from the settings page."
            )
            return False, None

        return True, token

    def _store_auth_token(self, auth_token: str, persist_locally):
        self._append_auth_token_to_headers(auth_token)
        if persist_locally:
            DeciPlatformClient._create_token_path_if_missing()
            print(
                f"Warning: turn off the store_token flag on non safe environments or remove {DeciPlatformClient.TOKEN_PATH} "
                f"after the use."
            )
            encrypted_text = f_encryptor.encrypt(auth_token.encode())
            with open(DeciPlatformClient.TOKEN_PATH, "wb") as file:
                file.write(encrypted_text)

    def _login_with_user_credentials(self, username: str, password: str, store_token: bool):
        if not username or not password:
            username = username or input("Email: ")
            password = password or getpass.getpass()

        response = super(DeciPlatformClient, self).login(username, password)
        self._store_auth_token(auth_token=response.access_token, persist_locally=store_token)

    def login(self, username: str = None, password: str = None, token: str = None, store_token: bool = True):
        """
        Login to the platform.
        Provides a mechanism to log in to the Deci lab. A previously generated token can be provided and in such case
        the username and password won't be necessary (the token will be verified). A new token will be requested if both
        the username and password are provided. If neither a token, username and password is provided a check for a
        local token will be executed

        :param username: The user email which was used to register in the Deci lab
        :type username: str
        :param password: The user password provided upon account creation in Deci lab.
        :type password: str
        :param token: A token provided by Deci lab
        :type token: str
        :param store_token: By default when you use your credentials, a token will be saved on your machine to allow
            future auto-login.
        :type store_token: bool
        IMPORTANT: turn off the store_token flag on non safe environments.
        """

        force_login = bool(username or password)
        token_valid, token_str = DeciPlatformClient.verify_token_exp(token=token)
        try:
            if force_login:
                self._login_with_user_credentials(username=username, password=password, store_token=store_token)
            elif token_valid:
                self._store_auth_token(auth_token=token_str, persist_locally=store_token)
            else:
                print("No parameter was provided. We'll search for a token stored locally")
                local_token = DeciPlatformClient._get_local_auth_token()
                valid, token = DeciPlatformClient.verify_token_exp(token=local_token)
                if valid:
                    self._append_auth_token_to_headers(token)
                    print("A local token was found and it contains a valid signature")
                elif not token:
                    print("A local token was not found. Please log in with your Deci lab credentials")
                    self._login_with_user_credentials(username=username, password=password, store_token=store_token)
        except InvalidToken:
            raise InvalidAuthenticationTokenError(
                "It seems your authentication token is not valid or has been expired, Please login with your regular \n"
                "credentials first."
            )

        print("Successfully logged in to the platform.")

    def logout(self):
        """
        Log out of the platform (Disposes the credentials).
        """
        self.api_client.default_headers.pop("Authorization")
        if DeciPlatformClient._token_path_exists():
            os.remove(DeciPlatformClient.TOKEN_PATH)
        print("Successfully logged out.")

    def add_model(
        self,
        add_model_request: ModelMetadata,
        optimization_request: OptimizationRequestForm = None,
        model_local_path: str = None,
        local_loaded_model=None,
        wait_async=False,
        **kwargs,
    ):
        """
        Adds a new model to the company's model repository.
        The new model arguments are passed to the API, and the model itself is uploaded to s3 from the local machine.
        For pytorch local_loaded_model is expected, for other framework use model_local path instead.
        :param add_model_request: The model metadata
        :param optimization_request: The params to due optimize the model, if not given model will not be optimized. You can always request the optimization later.
        :param model_local_path: The path of the model on the local operating system.
        :param local_loaded_model: Pytorch loaded model object.
        :param wait_async: If true function will wait unitl the benchmark process was finished, otherwise will return on request acknowledgement.
        if your model's framework is pytorch you may pass the following parameters as kwargs in order to control the conversion to onnx:
        :param opset_version
        :param do_constant_folding
        :param dynamic_axes
        :param input_names
        :param output_names
        """
        if local_loaded_model and not model_local_path:
            if add_model_request.framework == FrameworkType.PYTORCH:
                model_local_path = self.convert_pytorch_to_onnx(
                    local_loaded_model=local_loaded_model,
                    primary_batch_size=add_model_request.primary_batch_size,
                    input_dimensions=add_model_request.input_dimensions,
                    **kwargs,
                )
                add_model_request.framework = FrameworkType.ONNX
            else:
                raise UnsupportedLoadedModelFramework(
                    "For the current moment loaded model is only supported for Pytorch models. Try to specify a model_local_path instead"
                )

        add_model_request.source = ModelSource.SDK
        s3_file_etag = ""
        try:
            # Making sure the model arguments are OK before uploading the file
            try:
                super(DeciPlatformClient, self).assert_model_arguments(model_metadata=add_model_request)
            except ApiException as e:
                print(f"Found bad arguments: {e}")
                raise e

            try:
                s3_file_etag = self._upload_file_to_s3(model_local_path, add_model_request.name)
            except PermissionError as e:
                print("The given local path doesn't have enough permissions")
                raise e

            # Adding the model metadata via the API, after verification that the file exists.
            add_model_response: AddModelResponse = super(DeciPlatformClient, self).add_model(
                model_metadata=add_model_request, etag=s3_file_etag, **kwargs
            )
            response = AddAndOptimizeResponse(**add_model_response.data.to_dict())
            new_model_id = add_model_response.data.model_id
            if wait_async and not optimization_request:
                return_value = wait_until(
                    self._wait_for_benchmark_To_finish, 20 * 60, optimized_model_id=str(new_model_id)
                )
                if not return_value:
                    raise TimeoutWasReachedBeforeBenchmarkFinishedError(
                        "Add model with async_wait flag was called. Benchmark process was started but waiting for results took too long."
                    )
        except Exception as ex:
            print(f"Failed to add the model to the repository. {ex}")
            raise ex
        else:
            print("Successfully added the model to the repository.")
            print(
                f"Starting to benchmark the model on the required hardwares. You can check the status on console.deci.ai/insights/{response.model_id} or by querying the platform. "
            )
        finally:
            try:
                os.remove(model_local_path)
            except (OSError, UnboundLocalError):
                pass
        if not optimization_request:
            return APIResponse(success=True, message=add_model_response.message, data=response)
        # Requesting to optimize the added model metadata via the API.
        optimize_model_response: OptimizeModelResponse = super(DeciPlatformClient, self).optimize_model(
            model_id=new_model_id, optimization_request_form=optimization_request, **kwargs
        )
        response_dict = response.dict()
        response_dict.update(optimize_model_response.data.to_dict())
        response = AddAndOptimizeResponse(**response_dict)
        if wait_async:
            return_value = wait_until(
                self._wait_for_benchmark_To_finish, 20 * 60, model_id=str(response.optimized_model_id)
            )
            if return_value:
                print(
                    "successfully added and optimized "
                    + str(return_value.name)
                    + f" on your model repository. You can see the benchmark results at console.deci.ai/insights/{add_model_response.data.model_id}/optimized/{optimize_model_response.data.optimized_model_id}  "
                )
            else:
                raise TimeoutWasReachedBeforeBenchmarkFinishedError(
                    "Add model with async_wait flag was called. Benchmark process was started but waiting for results took too long."
                )

        return APIResponse(
            success=True,
            message="Successfully added the model the the model repository and optimized it. ",
            data=response,
        )

    def download_model(self, model_id: str, stream: bool = True):
        """
        Fetches a remote (Deci cloud) model with the specified UUID.
        :param model_id: The model UUID
        :param stream: Whether the request should be performed as a stream or not
        """
        try:
            download_url = self.get_model_signed_url_for_download(model_id=model_id)
            print("Downloading...")
            return requests.get(download_url.data, stream=stream)
        except Exception as e:
            print(f"Model with ID - {model_id} could not be fetched due to {e}")
            raise DownloadModelError

    def store_remote_model_to_local(self, model_id: str, download_to_path: str):
        """
        Downloads a model with the specified UUID to the specified path.
        :param model_id: The model UUID
        :param download_to_path: The full path to which the model will be written to.
        """
        response = self.download_model(model_id=model_id)
        with open(download_to_path, "wb") as model_file:
            for model_chunk in response.iter_content():
                if model_chunk:
                    model_file.write(model_chunk)
            print(f"The model stored at {download_to_path}")
        return True

    def _all_models(self) -> List[ModelMetadata]:
        models = self.get_all_models()
        return [model for model in models.data if not model.deleted]

    def find_model_id(self, model_name: str) -> ModelMetadata:
        return next((model for model in self._all_models() if model.name == model_name), None)

    def convert_pytorch_to_onnx(
        self,
        local_loaded_model,
        primary_batch_size: int,
        input_dimensions: Tuple[int],
        export_path: str = None,
        **kwargs,
    ):
        """
        Convert frameworks.
        Only support Pytorch to Onnx for the current moment.
        :param local_loaded_model: Pytorch loaded model object (nn.module).
        :param primary_batch_size: The batch_size for your model
        :param input_dimensions: The input dims of the model. ex:(3, 224, 224)
        :param export_path: Path to where to save the converted model file. If not given "converted_model_{time.time()}.onnx" will be used.
        if your model's framework is pytorch you may pass the following parameters as kwargs in order to control the conversion to onnx:
        :param opset_version
        :param do_constant_folding
        :param dynamic_axes
        :param input_names
        :param output_names
        """
        try:
            import onnx
            import torch
        except Exception as e:
            msg = "Failed to convert_pytorch_to_onnx model because something went wrong in the package requirements installation, this is not a direct error of deci-client. "
            raise RequirementsInstallationFailedError(msg) from e
        # Input to the model
        model_input = torch.randn(primary_batch_size, *input_dimensions, requires_grad=False)
        model_path = export_path if export_path else f"converted_model_{time.time()}.onnx"
        # Export the model
        kwargs.setdefault("opset_version", 10)
        local_loaded_model.eval()  # Put model into eval mode
        torch.onnx.export(
            local_loaded_model,  # Model being run
            model_input,
            # Model input - its a torch tensor contains the model input dims and the primary_batch_size.
            model_path,  # Where to save the model (can be a file or file-like object)
            export_params=True,  # Store the trained parameter weights inside the model file
            # The ONNX version to export the model to
            do_constant_folding=kwargs.get("do_constant_folding", True),
            # Whether to execute constant folding for optimization
            input_names=kwargs.get("input_names", ["input"]),
            # The model's input names
            output_names=kwargs.get("output_names", ["output"]),
            # The model's output names
            dynamic_axes=kwargs.get(
                "dynamic_axes",
                {
                    "input": {0: "batch_size"},
                    # Variable length axes
                    "output": {0: "batch_size"},
                },
            ),
            **kwargs,
        )
        onnx_model = onnx.load(model_path)
        onnx.checker.check_model(onnx_model)
        return model_path

    def _wait_for_benchmark_To_finish(self, model_id: str):
        your_model_from_repo = self.get_model_by_id(model_id=model_id).data
        if your_model_from_repo.benchmark_state not in [ModelBenchmarkState.IN_PROGRESS, ModelBenchmarkState.PENDING]:
            return your_model_from_repo
        return False

    def _upload_file_to_s3(self, model_local_path: str, model_name: str, model_version: Optional[str] = None):
        with open(model_local_path, "rb") as f:
            # Upload the model to the s3 bucket of the company
            signed_url_upload_request = self.get_model_signed_url_for_upload(
                model_name=model_name, model_version=model_version
            )
            upload_request_parameters = signed_url_upload_request.data
            requests.post(upload_request_parameters["url"], data=[])
            print("Uploading the model file...")
            files = {"file": (upload_request_parameters["fields"]["key"], f)}
            http_response = requests.post(
                upload_request_parameters["url"], data=upload_request_parameters["fields"], files=files
            )
            # Getting the s3 created Etag from the http headers, and passing it to the 'add_model' call
            s3_file_etag = http_response.headers.get("ETag")  # Verify the model was uploaded
            http_response.raise_for_status()
            print("Finished uploading the model file.")
            return s3_file_etag
