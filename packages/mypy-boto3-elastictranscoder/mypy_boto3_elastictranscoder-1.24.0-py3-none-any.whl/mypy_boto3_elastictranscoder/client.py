"""
Type annotations for elastictranscoder service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_elastictranscoder.client import ElasticTranscoderClient

    session = Session()
    client: ElasticTranscoderClient = session.client("elastictranscoder")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListJobsByPipelinePaginator,
    ListJobsByStatusPaginator,
    ListPipelinesPaginator,
    ListPresetsPaginator,
)
from .type_defs import (
    AudioParametersTypeDef,
    CreateJobOutputTypeDef,
    CreateJobPlaylistTypeDef,
    CreateJobResponseTypeDef,
    CreatePipelineResponseTypeDef,
    CreatePresetResponseTypeDef,
    JobInputTypeDef,
    ListJobsByPipelineResponseTypeDef,
    ListJobsByStatusResponseTypeDef,
    ListPipelinesResponseTypeDef,
    ListPresetsResponseTypeDef,
    NotificationsTypeDef,
    PipelineOutputConfigTypeDef,
    ReadJobResponseTypeDef,
    ReadPipelineResponseTypeDef,
    ReadPresetResponseTypeDef,
    TestRoleResponseTypeDef,
    ThumbnailsTypeDef,
    UpdatePipelineNotificationsResponseTypeDef,
    UpdatePipelineResponseTypeDef,
    UpdatePipelineStatusResponseTypeDef,
    VideoParametersTypeDef,
)
from .waiter import JobCompleteWaiter

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ElasticTranscoderClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    IncompatibleVersionException: Type[BotocoreClientError]
    InternalServiceException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class ElasticTranscoderClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ElasticTranscoderClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#can_paginate)
        """

    def cancel_job(self, *, Id: str) -> Dict[str, Any]:
        """
        The CancelJob operation cancels an unfinished job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client.cancel_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#cancel_job)
        """

    def create_job(
        self,
        *,
        PipelineId: str,
        Input: JobInputTypeDef = ...,
        Inputs: Sequence[JobInputTypeDef] = ...,
        Output: CreateJobOutputTypeDef = ...,
        Outputs: Sequence[CreateJobOutputTypeDef] = ...,
        OutputKeyPrefix: str = ...,
        Playlists: Sequence[CreateJobPlaylistTypeDef] = ...,
        UserMetadata: Mapping[str, str] = ...
    ) -> CreateJobResponseTypeDef:
        """
        When you create a job, Elastic Transcoder returns JSON data that includes the
        values that you specified plus information about the job that is created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client.create_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#create_job)
        """

    def create_pipeline(
        self,
        *,
        Name: str,
        InputBucket: str,
        Role: str,
        OutputBucket: str = ...,
        AwsKmsKeyArn: str = ...,
        Notifications: NotificationsTypeDef = ...,
        ContentConfig: PipelineOutputConfigTypeDef = ...,
        ThumbnailConfig: PipelineOutputConfigTypeDef = ...
    ) -> CreatePipelineResponseTypeDef:
        """
        The CreatePipeline operation creates a pipeline with settings that you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client.create_pipeline)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#create_pipeline)
        """

    def create_preset(
        self,
        *,
        Name: str,
        Container: str,
        Description: str = ...,
        Video: VideoParametersTypeDef = ...,
        Audio: AudioParametersTypeDef = ...,
        Thumbnails: ThumbnailsTypeDef = ...
    ) -> CreatePresetResponseTypeDef:
        """
        The CreatePreset operation creates a preset with settings that you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client.create_preset)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#create_preset)
        """

    def delete_pipeline(self, *, Id: str) -> Dict[str, Any]:
        """
        The DeletePipeline operation removes a pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client.delete_pipeline)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#delete_pipeline)
        """

    def delete_preset(self, *, Id: str) -> Dict[str, Any]:
        """
        The DeletePreset operation removes a preset that you've added in an AWS region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client.delete_preset)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#delete_preset)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#generate_presigned_url)
        """

    def list_jobs_by_pipeline(
        self, *, PipelineId: str, Ascending: str = ..., PageToken: str = ...
    ) -> ListJobsByPipelineResponseTypeDef:
        """
        The ListJobsByPipeline operation gets a list of the jobs currently in a
        pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client.list_jobs_by_pipeline)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#list_jobs_by_pipeline)
        """

    def list_jobs_by_status(
        self, *, Status: str, Ascending: str = ..., PageToken: str = ...
    ) -> ListJobsByStatusResponseTypeDef:
        """
        The ListJobsByStatus operation gets a list of jobs that have a specified status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client.list_jobs_by_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#list_jobs_by_status)
        """

    def list_pipelines(
        self, *, Ascending: str = ..., PageToken: str = ...
    ) -> ListPipelinesResponseTypeDef:
        """
        The ListPipelines operation gets a list of the pipelines associated with the
        current AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client.list_pipelines)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#list_pipelines)
        """

    def list_presets(
        self, *, Ascending: str = ..., PageToken: str = ...
    ) -> ListPresetsResponseTypeDef:
        """
        The ListPresets operation gets a list of the default presets included with
        Elastic Transcoder and the presets that you've added in an AWS region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client.list_presets)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#list_presets)
        """

    def read_job(self, *, Id: str) -> ReadJobResponseTypeDef:
        """
        The ReadJob operation returns detailed information about a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client.read_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#read_job)
        """

    def read_pipeline(self, *, Id: str) -> ReadPipelineResponseTypeDef:
        """
        The ReadPipeline operation gets detailed information about a pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client.read_pipeline)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#read_pipeline)
        """

    def read_preset(self, *, Id: str) -> ReadPresetResponseTypeDef:
        """
        The ReadPreset operation gets detailed information about a preset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client.read_preset)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#read_preset)
        """

    def test_role(
        self, *, Role: str, InputBucket: str, OutputBucket: str, Topics: Sequence[str]
    ) -> TestRoleResponseTypeDef:
        """
        The TestRole operation tests the IAM role used to create the pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client.test_role)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#test_role)
        """

    def update_pipeline(
        self,
        *,
        Id: str,
        Name: str = ...,
        InputBucket: str = ...,
        Role: str = ...,
        AwsKmsKeyArn: str = ...,
        Notifications: NotificationsTypeDef = ...,
        ContentConfig: PipelineOutputConfigTypeDef = ...,
        ThumbnailConfig: PipelineOutputConfigTypeDef = ...
    ) -> UpdatePipelineResponseTypeDef:
        """
        Use the `UpdatePipeline` operation to update settings for a pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client.update_pipeline)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#update_pipeline)
        """

    def update_pipeline_notifications(
        self, *, Id: str, Notifications: NotificationsTypeDef
    ) -> UpdatePipelineNotificationsResponseTypeDef:
        """
        With the UpdatePipelineNotifications operation, you can update Amazon Simple
        Notification Service (Amazon SNS) notifications for a pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client.update_pipeline_notifications)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#update_pipeline_notifications)
        """

    def update_pipeline_status(
        self, *, Id: str, Status: str
    ) -> UpdatePipelineStatusResponseTypeDef:
        """
        The UpdatePipelineStatus operation pauses or reactivates a pipeline, so that the
        pipeline stops or restarts the processing of jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client.update_pipeline_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#update_pipeline_status)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_jobs_by_pipeline"]
    ) -> ListJobsByPipelinePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_jobs_by_status"]
    ) -> ListJobsByStatusPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_pipelines"]) -> ListPipelinesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_presets"]) -> ListPresetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#get_paginator)
        """

    def get_waiter(self, waiter_name: Literal["job_complete"]) -> JobCompleteWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/client/#get_waiter)
        """
