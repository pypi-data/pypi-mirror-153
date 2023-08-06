import grpc
import jwt  # pip install pyJWT, ATTENTION, no pip install jwt!!
import time
import os
from retry import retry

from . import auth_pb2
from . import auth_pb2_grpc

# CONSTANTS
BX_HEADER_TOKEN_NAME = "bx_token"
CHANNEL_TIMEOUT = 40  # In seconds

# CONFIG
CALL_DELAY = 0.5      # Initial delay (in seconds) between remote method call attempts.
CALL_BACKOFF = 2      # Multiplier applied to delay between attempts.
CALL_MAX_DELAY = 60   # Maximum value of delay (in seconds).
MAX_TRIES = 10        # The maximum number of attempts. default: -1 (infinite).
CALL_TIMEOUT = 60     # Unary call timeout in seconds.

channel = None  # Connection managed at module level. One common channel for all service classes within the module.
bx_token = None
access_token = None
bx_endpoint = None


class RecoverableException(Exception):
    """Raised when a recoverable error occurs.
    It's used just to detect failed connections attempts and try again.
    So, do nothing.
    """
    pass


def is_recoverable(exception):
    if exception is None or exception.code() is None:
        return False
    return grpc.StatusCode.NOT_FOUND != exception.code() and \
           grpc.StatusCode.ALREADY_EXISTS != exception.code() and \
           grpc.StatusCode.UNKNOWN != exception.code() and \
           grpc.StatusCode.INVALID_ARGUMENT != exception.code() and \
           grpc.StatusCode.FAILED_PRECONDITION != exception.code() and \
           grpc.StatusCode.UNAUTHENTICATED != exception.code() and \
           grpc.StatusCode.PERMISSION_DENIED != exception.code()


def connect():
    connectTo(os.environ["BATCHX_ENDPOINT"], os.environ["BATCHX_TOKEN"], True);

@retry(RecoverableException, delay=CALL_DELAY, backoff=CALL_BACKOFF, max_delay=CALL_MAX_DELAY, tries=MAX_TRIES)
def connectTo(endpoint, token, secure):
    global channel, bx_token, bx_endpoint
    if channel is None:
        try:
            if secure:
                channel = grpc.secure_channel(endpoint, grpc.ssl_channel_credentials())
            else:
                channel = grpc.insecure_channel(endpoint)
            grpc.channel_ready_future(channel).result(CHANNEL_TIMEOUT)
        except grpc.FutureTimeoutError as exc:
            channel = None
            raise RecoverableException
    bx_token = token
    bx_endpoint = endpoint


def channel_is_working():
    global channel
    if channel is not None:
        try:
            grpc.channel_ready_future(channel).result(CHANNEL_TIMEOUT)
            return True
        except grpc.FutureTimeoutError:
            pass
    return False


def current_access_token_is_valid():
    global access_token
    if access_token is None:
        return False
    else:
        access_token_dict = jwt.decode(access_token, options={"verify_signature":False})
        return access_token_dict['exp'] > time.time()


def check():
    """Check whether there exist a working channel and a valid access token."""
    global bx_endpoint, bx_token
    if not channel_is_working() and bx_endpoint is not None and bx_token is not None:
        connect(bx_endpoint, bx_token)
    if not current_access_token_is_valid():
        login()


@retry(RecoverableException, delay=CALL_DELAY, backoff=CALL_BACKOFF, max_delay=CALL_MAX_DELAY, tries=MAX_TRIES)
def make_call(func, request, include_metadata=True):
    """Wrapper to manage remote method calls. It implements a retry policy with exponential backoff.

    :param str func: Function in charge of calling remote methods.
    :param str request: grpc message.
    :param str include_metadata: if set to True or not passed, token header will be sent.
    :return: response returned by executing the function passed as parameter (func).
    """
    try:
        if include_metadata:
            return func(request, metadata=[(BX_HEADER_TOKEN_NAME, access_token)], timeout=CALL_TIMEOUT)
        else:
            return func(request, timeout=CALL_TIMEOUT)
    except grpc.RpcError as exc:
        if is_recoverable(exc):
            raise RecoverableException  # If error is recoverable, retry call
        else:
            raise exc


def login():
    """ Connect to server and obtain an access token if needed."""
    global channel, bx_token, access_token
    if bx_token is not None:
        user_id = jwt.decode(bx_token, options={"verify_signature":False})['batchx-id']
        request_data = auth_pb2.RefreshTokenRequest(user_name=user_id, refresh_token=bx_token)
        response = make_call(auth_pb2_grpc.AuthServiceStub(channel).RefreshToken, request_data, include_metadata=False)
        access_token = response.access_token
    else:
        raise Exception("Batchx token not set. Please run: bx.connect(<endpoint>, <token>)")


from . import environment_pb2
from . import environment_pb2_grpc


class EnvironmentService:

    def GetEnvironment(self, request):
        check()
        return make_call(environment_pb2_grpc.EnvironmentServiceStub(channel).GetEnvironment, request)

    def GetEnvironmentRequest(self, **kwargs):
        return environment_pb2.GetEnvironmentRequest(**kwargs)

    def GetEnvironmentResponse(self, **kwargs):
        return environment_pb2.GetEnvironmentResponse(**kwargs)


from . import common_pb2
from . import common_pb2_grpc


class CommonService:

    def IntRangeFilter(self, **kwargs):
        return common_pb2.IntRangeFilter(**kwargs)

    def LongRangeFilter(self, **kwargs):
        return common_pb2.LongRangeFilter(**kwargs)

    def Organization(self, **kwargs):
        return common_pb2.Organization(**kwargs)

    def PageInfo(self, **kwargs):
        return common_pb2.PageInfo(**kwargs)

    def Picture(self, **kwargs):
        return common_pb2.Picture(**kwargs)

    def RateLimit(self, **kwargs):
        return common_pb2.RateLimit(**kwargs)

    def Region(self, **kwargs):
        return common_pb2.Region(**kwargs)

    def Thumbnail(self, **kwargs):
        return common_pb2.Thumbnail(**kwargs)

    def User(self, **kwargs):
        return common_pb2.User(**kwargs)


from . import health_pb2
from . import health_pb2_grpc


class HealthService:

    def HealthCheckRequest(self, **kwargs):
        return health_pb2.HealthCheckRequest(**kwargs)

    def HealthCheckResponse(self, **kwargs):
        return health_pb2.HealthCheckResponse(**kwargs)


from . import tag_pb2
from . import tag_pb2_grpc


class TagService:

    def CreateTag(self, request):
        check()
        return make_call(tag_pb2_grpc.TagServiceStub(channel).CreateTag, request)

    def DeleteTag(self, request):
        check()
        return make_call(tag_pb2_grpc.TagServiceStub(channel).DeleteTag, request)

    def DisableTag(self, request):
        check()
        return make_call(tag_pb2_grpc.TagServiceStub(channel).DisableTag, request)

    def GetTag(self, request):
        check()
        return make_call(tag_pb2_grpc.TagServiceStub(channel).GetTag, request)

    def ListEnvironmentTags(self, request):
        check()
        return make_call(tag_pb2_grpc.TagServiceStub(channel).ListEnvironmentTags, request)

    def UpdateTag(self, request):
        check()
        return make_call(tag_pb2_grpc.TagServiceStub(channel).UpdateTag, request)

    def CreateTagRequest(self, **kwargs):
        return tag_pb2.CreateTagRequest(**kwargs)

    def CreateTagResponse(self, **kwargs):
        return tag_pb2.CreateTagResponse(**kwargs)

    def DeleteTagRequest(self, **kwargs):
        return tag_pb2.DeleteTagRequest(**kwargs)

    def DeleteTagResponse(self, **kwargs):
        return tag_pb2.DeleteTagResponse(**kwargs)

    def DisableTagRequest(self, **kwargs):
        return tag_pb2.DisableTagRequest(**kwargs)

    def DisableTagResponse(self, **kwargs):
        return tag_pb2.DisableTagResponse(**kwargs)

    def GetTagRequest(self, **kwargs):
        return tag_pb2.GetTagRequest(**kwargs)

    def GetTagResponse(self, **kwargs):
        return tag_pb2.GetTagResponse(**kwargs)

    def ListEnvironmentTagsRequest(self, **kwargs):
        return tag_pb2.ListEnvironmentTagsRequest(**kwargs)

    def ListEnvironmentTagsResponse(self, **kwargs):
        return tag_pb2.ListEnvironmentTagsResponse(**kwargs)

    def Tag(self, **kwargs):
        return tag_pb2.Tag(**kwargs)

    def TagCoordinates(self, **kwargs):
        return tag_pb2.TagCoordinates(**kwargs)

    def TagData(self, **kwargs):
        return tag_pb2.TagData(**kwargs)

    def UpdateTagRequest(self, **kwargs):
        return tag_pb2.UpdateTagRequest(**kwargs)

    def UpdateTagResponse(self, **kwargs):
        return tag_pb2.UpdateTagResponse(**kwargs)


from . import audit_pb2
from . import audit_pb2_grpc


class AuditService:

    def ListEvents(self, request):
        check()
        return make_call(audit_pb2_grpc.AuditServiceStub(channel).ListEvents, request)

    def Event(self, **kwargs):
        return audit_pb2.Event(**kwargs)

    def ListEventsRequest(self, **kwargs):
        return audit_pb2.ListEventsRequest(**kwargs)

    def ListEventsResponse(self, **kwargs):
        return audit_pb2.ListEventsResponse(**kwargs)


from . import docker_pb2
from . import docker_pb2_grpc


class DockerService:

    def DockerImageCoordinates(self, **kwargs):
        return docker_pb2.DockerImageCoordinates(**kwargs)


from . import profile_pb2
from . import profile_pb2_grpc


class ProfileService:

    def Profile(self, **kwargs):
        return profile_pb2.Profile(**kwargs)


from . import filesystem_pb2
from . import filesystem_pb2_grpc


class FilesystemService:

    def CancelUpload(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).CancelUpload, request)

    def CompleteUpload(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).CompleteUpload, request)

    def Copy(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).Copy, request)

    def DeleteFile(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).DeleteFile, request)

    def DownloadPresigned(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).DownloadPresigned, request)

    def GetBlob(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).GetBlob, request)

    def GetFile(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).GetFile, request)

    def ListBlobPointers(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).ListBlobPointers, request)

    def ListBlobs(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).ListBlobs, request)

    def ListFolder(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).ListFolder, request)

    def ReportUploadStatus(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).ReportUploadStatus, request)

    def SetBlobStatus(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).SetBlobStatus, request)

    def UploadPresigned(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).UploadPresigned, request)

    def Blob(self, **kwargs):
        return filesystem_pb2.Blob(**kwargs)

    def CancelUploadRequest(self, **kwargs):
        return filesystem_pb2.CancelUploadRequest(**kwargs)

    def CancelUploadResponse(self, **kwargs):
        return filesystem_pb2.CancelUploadResponse(**kwargs)

    def CompleteUploadRequest(self, **kwargs):
        return filesystem_pb2.CompleteUploadRequest(**kwargs)

    def CompleteUploadResponse(self, **kwargs):
        return filesystem_pb2.CompleteUploadResponse(**kwargs)

    def CopyRequest(self, **kwargs):
        return filesystem_pb2.CopyRequest(**kwargs)

    def CopyResponse(self, **kwargs):
        return filesystem_pb2.CopyResponse(**kwargs)

    def CreateFolderRequest(self, **kwargs):
        return filesystem_pb2.CreateFolderRequest(**kwargs)

    def CreateFolderResponse(self, **kwargs):
        return filesystem_pb2.CreateFolderResponse(**kwargs)

    def DeleteFileRequest(self, **kwargs):
        return filesystem_pb2.DeleteFileRequest(**kwargs)

    def DeleteFileResponse(self, **kwargs):
        return filesystem_pb2.DeleteFileResponse(**kwargs)

    def DeleteFolderRequest(self, **kwargs):
        return filesystem_pb2.DeleteFolderRequest(**kwargs)

    def DeleteFolderResponse(self, **kwargs):
        return filesystem_pb2.DeleteFolderResponse(**kwargs)

    def DownloadPresignedRequest(self, **kwargs):
        return filesystem_pb2.DownloadPresignedRequest(**kwargs)

    def DownloadPresignedResponse(self, **kwargs):
        return filesystem_pb2.DownloadPresignedResponse(**kwargs)

    def File(self, **kwargs):
        return filesystem_pb2.File(**kwargs)

    def GetBlobRequest(self, **kwargs):
        return filesystem_pb2.GetBlobRequest(**kwargs)

    def GetBlobResponse(self, **kwargs):
        return filesystem_pb2.GetBlobResponse(**kwargs)

    def GetFileRequest(self, **kwargs):
        return filesystem_pb2.GetFileRequest(**kwargs)

    def GetFileResponse(self, **kwargs):
        return filesystem_pb2.GetFileResponse(**kwargs)

    def ListBlobPointersRequest(self, **kwargs):
        return filesystem_pb2.ListBlobPointersRequest(**kwargs)

    def ListBlobPointersResponse(self, **kwargs):
        return filesystem_pb2.ListBlobPointersResponse(**kwargs)

    def ListBlobsRequest(self, **kwargs):
        return filesystem_pb2.ListBlobsRequest(**kwargs)

    def ListBlobsResponse(self, **kwargs):
        return filesystem_pb2.ListBlobsResponse(**kwargs)

    def ListFolderRequest(self, **kwargs):
        return filesystem_pb2.ListFolderRequest(**kwargs)

    def ListFolderResponse(self, **kwargs):
        return filesystem_pb2.ListFolderResponse(**kwargs)

    def Metadata(self, **kwargs):
        return filesystem_pb2.Metadata(**kwargs)

    def ReportUploadStatusRequest(self, **kwargs):
        return filesystem_pb2.ReportUploadStatusRequest(**kwargs)

    def ReportUploadStatusResponse(self, **kwargs):
        return filesystem_pb2.ReportUploadStatusResponse(**kwargs)

    def SetBlobStatusRequest(self, **kwargs):
        return filesystem_pb2.SetBlobStatusRequest(**kwargs)

    def SetBlobStatusResponse(self, **kwargs):
        return filesystem_pb2.SetBlobStatusResponse(**kwargs)

    def UploadPresignedRequest(self, **kwargs):
        return filesystem_pb2.UploadPresignedRequest(**kwargs)

    def UploadPresignedResponse(self, **kwargs):
        return filesystem_pb2.UploadPresignedResponse(**kwargs)


from . import user_pb2
from . import user_pb2_grpc


class UserService:

    def GetUser(self, request):
        check()
        return make_call(user_pb2_grpc.UserServiceStub(channel).GetUser, request)

    def UpdateUser(self, request):
        check()
        return make_call(user_pb2_grpc.UserServiceStub(channel).UpdateUser, request)

    def GetUserRequest(self, **kwargs):
        return user_pb2.GetUserRequest(**kwargs)

    def GetUserResponse(self, **kwargs):
        return user_pb2.GetUserResponse(**kwargs)

    def UpdateUserRequest(self, **kwargs):
        return user_pb2.UpdateUserRequest(**kwargs)

    def UpdateUserResponse(self, **kwargs):
        return user_pb2.UpdateUserResponse(**kwargs)


from . import job_pb2
from . import job_pb2_grpc


class JobService:

    def Cancel(self, request):
        check()
        return make_call(job_pb2_grpc.JobServiceStub(channel).Cancel, request)

    def CloseWorkflow(self, request):
        check()
        return make_call(job_pb2_grpc.JobServiceStub(channel).CloseWorkflow, request)

    def CreateWorkflow(self, request):
        check()
        return make_call(job_pb2_grpc.JobServiceStub(channel).CreateWorkflow, request)

    def Delete(self, request):
        check()
        return make_call(job_pb2_grpc.JobServiceStub(channel).Delete, request)

    def DeleteWorkflow(self, request):
        check()
        return make_call(job_pb2_grpc.JobServiceStub(channel).DeleteWorkflow, request)

    def GetComputationalCost(self, request):
        check()
        return make_call(job_pb2_grpc.JobServiceStub(channel).GetComputationalCost, request)

    def GetJob(self, request):
        check()
        return make_call(job_pb2_grpc.JobServiceStub(channel).GetJob, request)

    def GetLogs(self, request):
        check()
        return make_call(job_pb2_grpc.JobServiceStub(channel).GetLogs, request)

    def GetWorkflow(self, request):
        check()
        return make_call(job_pb2_grpc.JobServiceStub(channel).GetWorkflow, request)

    def ListJobs(self, request):
        check()
        return make_call(job_pb2_grpc.JobServiceStub(channel).ListJobs, request)

    def ListWorkflows(self, request):
        check()
        return make_call(job_pb2_grpc.JobServiceStub(channel).ListWorkflows, request)

    def Stream(self, request):
        check()
        return make_call(job_pb2_grpc.JobServiceStub(channel).Stream, request)

    def Submit(self, request):
        check()
        return make_call(job_pb2_grpc.JobServiceStub(channel).Submit, request)

    def TagJob(self, request):
        check()
        return make_call(job_pb2_grpc.JobServiceStub(channel).TagJob, request)

    def TagWorkflow(self, request):
        check()
        return make_call(job_pb2_grpc.JobServiceStub(channel).TagWorkflow, request)

    def CancelRequest(self, **kwargs):
        return job_pb2.CancelRequest(**kwargs)

    def CancelResponse(self, **kwargs):
        return job_pb2.CancelResponse(**kwargs)

    def CloseWorkflowRequest(self, **kwargs):
        return job_pb2.CloseWorkflowRequest(**kwargs)

    def CloseWorkflowResponse(self, **kwargs):
        return job_pb2.CloseWorkflowResponse(**kwargs)

    def CreateWorkflowRequest(self, **kwargs):
        return job_pb2.CreateWorkflowRequest(**kwargs)

    def CreateWorkflowResponse(self, **kwargs):
        return job_pb2.CreateWorkflowResponse(**kwargs)

    def DeleteRequest(self, **kwargs):
        return job_pb2.DeleteRequest(**kwargs)

    def DeleteResponse(self, **kwargs):
        return job_pb2.DeleteResponse(**kwargs)

    def DeleteWorkflowRequest(self, **kwargs):
        return job_pb2.DeleteWorkflowRequest(**kwargs)

    def DeleteWorkflowResponse(self, **kwargs):
        return job_pb2.DeleteWorkflowResponse(**kwargs)

    def GetComputationalCostRequest(self, **kwargs):
        return job_pb2.GetComputationalCostRequest(**kwargs)

    def GetComputationalCostResponse(self, **kwargs):
        return job_pb2.GetComputationalCostResponse(**kwargs)

    def GetJobRequest(self, **kwargs):
        return job_pb2.GetJobRequest(**kwargs)

    def GetJobResponse(self, **kwargs):
        return job_pb2.GetJobResponse(**kwargs)

    def GetLogsRequest(self, **kwargs):
        return job_pb2.GetLogsRequest(**kwargs)

    def GetWorkflowRequest(self, **kwargs):
        return job_pb2.GetWorkflowRequest(**kwargs)

    def GetWorkflowResponse(self, **kwargs):
        return job_pb2.GetWorkflowResponse(**kwargs)

    def Job(self, **kwargs):
        return job_pb2.Job(**kwargs)

    def JobEvent(self, **kwargs):
        return job_pb2.JobEvent(**kwargs)

    def JobStateMessage(self, **kwargs):
        return job_pb2.JobStateMessage(**kwargs)

    def ListJobsRequest(self, **kwargs):
        return job_pb2.ListJobsRequest(**kwargs)

    def ListJobsResponse(self, **kwargs):
        return job_pb2.ListJobsResponse(**kwargs)

    def ListWorkflowsRequest(self, **kwargs):
        return job_pb2.ListWorkflowsRequest(**kwargs)

    def ListWorkflowsResponse(self, **kwargs):
        return job_pb2.ListWorkflowsResponse(**kwargs)

    def StreamRequest(self, **kwargs):
        return job_pb2.StreamRequest(**kwargs)

    def StreamResponse(self, **kwargs):
        return job_pb2.StreamResponse(**kwargs)

    def SubmitRequest(self, **kwargs):
        return job_pb2.SubmitRequest(**kwargs)

    def SubmitResponse(self, **kwargs):
        return job_pb2.SubmitResponse(**kwargs)

    def TagJobRequest(self, **kwargs):
        return job_pb2.TagJobRequest(**kwargs)

    def TagJobResponse(self, **kwargs):
        return job_pb2.TagJobResponse(**kwargs)

    def TagWorkflowRequest(self, **kwargs):
        return job_pb2.TagWorkflowRequest(**kwargs)

    def TagWorkflowResponse(self, **kwargs):
        return job_pb2.TagWorkflowResponse(**kwargs)

    def Workflow(self, **kwargs):
        return job_pb2.Workflow(**kwargs)


from . import image_pb2
from . import image_pb2_grpc


class ImageService:

    def CloneImage(self, request):
        check()
        return make_call(image_pb2_grpc.ImageServiceStub(channel).CloneImage, request)

    def DeleteImage(self, request):
        check()
        return make_call(image_pb2_grpc.ImageServiceStub(channel).DeleteImage, request)

    def GetImage(self, request):
        check()
        return make_call(image_pb2_grpc.ImageServiceStub(channel).GetImage, request)

    def GetPushCredentials(self, request):
        check()
        return make_call(image_pb2_grpc.ImageServiceStub(channel).GetPushCredentials, request)

    def ImportImage(self, request):
        check()
        return make_call(image_pb2_grpc.ImageServiceStub(channel).ImportImage, request)

    def ListImages(self, request):
        check()
        return make_call(image_pb2_grpc.ImageServiceStub(channel).ListImages, request)

    def SearchImages(self, request):
        check()
        return make_call(image_pb2_grpc.ImageServiceStub(channel).SearchImages, request)

    def ShareImage(self, request):
        check()
        return make_call(image_pb2_grpc.ImageServiceStub(channel).ShareImage, request)

    def TagImage(self, request):
        check()
        return make_call(image_pb2_grpc.ImageServiceStub(channel).TagImage, request)

    def CloneImageRequest(self, **kwargs):
        return image_pb2.CloneImageRequest(**kwargs)

    def CloneImageResponse(self, **kwargs):
        return image_pb2.CloneImageResponse(**kwargs)

    def DeleteImageRequest(self, **kwargs):
        return image_pb2.DeleteImageRequest(**kwargs)

    def GetImageRequest(self, **kwargs):
        return image_pb2.GetImageRequest(**kwargs)

    def GetImageResponse(self, **kwargs):
        return image_pb2.GetImageResponse(**kwargs)

    def GetPushCredentialsRequest(self, **kwargs):
        return image_pb2.GetPushCredentialsRequest(**kwargs)

    def GetPushCredentialsResponse(self, **kwargs):
        return image_pb2.GetPushCredentialsResponse(**kwargs)

    def Image(self, **kwargs):
        return image_pb2.Image(**kwargs)

    def ImportImageRequest(self, **kwargs):
        return image_pb2.ImportImageRequest(**kwargs)

    def ListImagesRequest(self, **kwargs):
        return image_pb2.ListImagesRequest(**kwargs)

    def ListImagesResponse(self, **kwargs):
        return image_pb2.ListImagesResponse(**kwargs)

    def SearchImagesRequest(self, **kwargs):
        return image_pb2.SearchImagesRequest(**kwargs)

    def SearchImagesResponse(self, **kwargs):
        return image_pb2.SearchImagesResponse(**kwargs)

    def ShareImageRequest(self, **kwargs):
        return image_pb2.ShareImageRequest(**kwargs)

    def ShareImageResponse(self, **kwargs):
        return image_pb2.ShareImageResponse(**kwargs)

    def TagImageRequest(self, **kwargs):
        return image_pb2.TagImageRequest(**kwargs)

    def TagImageResponse(self, **kwargs):
        return image_pb2.TagImageResponse(**kwargs)


from . import admin_pb2
from . import admin_pb2_grpc


class AdminService:

    def AddEnvironmentCredits(self, request):
        check()
        return make_call(admin_pb2_grpc.AdminServiceStub(channel).AddEnvironmentCredits, request)

    def CreateOrg(self, request):
        check()
        return make_call(admin_pb2_grpc.AdminServiceStub(channel).CreateOrg, request)

    def CreateUser(self, request):
        check()
        return make_call(admin_pb2_grpc.AdminServiceStub(channel).CreateUser, request)

    def GetGlobalProperties(self, request):
        check()
        return make_call(admin_pb2_grpc.AdminServiceStub(channel).GetGlobalProperties, request)

    def SetGlobalProperty(self, request):
        check()
        return make_call(admin_pb2_grpc.AdminServiceStub(channel).SetGlobalProperty, request)

    def AddEnvironmentCreditsRequest(self, **kwargs):
        return admin_pb2.AddEnvironmentCreditsRequest(**kwargs)

    def AddEnvironmentCreditsResponse(self, **kwargs):
        return admin_pb2.AddEnvironmentCreditsResponse(**kwargs)

    def Assignment(self, **kwargs):
        return admin_pb2.Assignment(**kwargs)

    def CreateOrgRequest(self, **kwargs):
        return admin_pb2.CreateOrgRequest(**kwargs)

    def CreateOrgResponse(self, **kwargs):
        return admin_pb2.CreateOrgResponse(**kwargs)

    def CreateUserRequest(self, **kwargs):
        return admin_pb2.CreateUserRequest(**kwargs)

    def CreateUserResponse(self, **kwargs):
        return admin_pb2.CreateUserResponse(**kwargs)

    def GetGlobalPropertiesRequest(self, **kwargs):
        return admin_pb2.GetGlobalPropertiesRequest(**kwargs)

    def GetGlobalPropertiesResponse(self, **kwargs):
        return admin_pb2.GetGlobalPropertiesResponse(**kwargs)

    def SetGlobalPropertyRequest(self, **kwargs):
        return admin_pb2.SetGlobalPropertyRequest(**kwargs)

    def SetGlobalPropertyResponse(self, **kwargs):
        return admin_pb2.SetGlobalPropertyResponse(**kwargs)


from . import organization_pb2
from . import organization_pb2_grpc


class OrganizationService:

    def GetOrganization(self, request):
        check()
        return make_call(organization_pb2_grpc.OrganizationServiceStub(channel).GetOrganization, request)

    def SetMembership(self, request):
        check()
        return make_call(organization_pb2_grpc.OrganizationServiceStub(channel).SetMembership, request)

    def SetMembershipVisibility(self, request):
        check()
        return make_call(organization_pb2_grpc.OrganizationServiceStub(channel).SetMembershipVisibility, request)

    def UpdateOrganization(self, request):
        check()
        return make_call(organization_pb2_grpc.OrganizationServiceStub(channel).UpdateOrganization, request)

    def GetOrganizationRequest(self, **kwargs):
        return organization_pb2.GetOrganizationRequest(**kwargs)

    def GetOrganizationResponse(self, **kwargs):
        return organization_pb2.GetOrganizationResponse(**kwargs)

    def SetMembershipRequest(self, **kwargs):
        return organization_pb2.SetMembershipRequest(**kwargs)

    def SetMembershipResponse(self, **kwargs):
        return organization_pb2.SetMembershipResponse(**kwargs)

    def SetMembershipVisibilityRequest(self, **kwargs):
        return organization_pb2.SetMembershipVisibilityRequest(**kwargs)

    def SetMembershipVisibilityResponse(self, **kwargs):
        return organization_pb2.SetMembershipVisibilityResponse(**kwargs)

    def UpdateOrganizationRequest(self, **kwargs):
        return organization_pb2.UpdateOrganizationRequest(**kwargs)

    def UpdateOrganizationResponse(self, **kwargs):
        return organization_pb2.UpdateOrganizationResponse(**kwargs)


from . import picture_pb2
from . import picture_pb2_grpc


class PictureService:

    def CompleteUpload(self, request):
        check()
        return make_call(picture_pb2_grpc.PictureServiceStub(channel).CompleteUpload, request)

    def CropPicture(self, request):
        check()
        return make_call(picture_pb2_grpc.PictureServiceStub(channel).CropPicture, request)

    def Upload(self, request):
        check()
        return make_call(picture_pb2_grpc.PictureServiceStub(channel).Upload, request)

    def CompleteUploadRequest(self, **kwargs):
        return picture_pb2.CompleteUploadRequest(**kwargs)

    def CompleteUploadResponse(self, **kwargs):
        return picture_pb2.CompleteUploadResponse(**kwargs)

    def CropPictureRequest(self, **kwargs):
        return picture_pb2.CropPictureRequest(**kwargs)

    def CropPictureResponse(self, **kwargs):
        return picture_pb2.CropPictureResponse(**kwargs)

    def UploadRequest(self, **kwargs):
        return picture_pb2.UploadRequest(**kwargs)

    def UploadResponse(self, **kwargs):
        return picture_pb2.UploadResponse(**kwargs)


from . import token_pb2
from . import token_pb2_grpc


class TokenService:

    def AddToken(self, request):
        check()
        return make_call(token_pb2_grpc.TokenServiceStub(channel).AddToken, request)

    def AddTokenRequest(self, **kwargs):
        return token_pb2.AddTokenRequest(**kwargs)

    def AddTokenResponse(self, **kwargs):
        return token_pb2.AddTokenResponse(**kwargs)


from . import auth_pb2
from . import auth_pb2_grpc


class AuthService:

    def ConfirmForgotPassword(self, request):
        check()
        return make_call(auth_pb2_grpc.AuthServiceStub(channel).ConfirmForgotPassword, request)

    def ForgotPassword(self, request):
        check()
        return make_call(auth_pb2_grpc.AuthServiceStub(channel).ForgotPassword, request)

    def Login(self, request):
        check()
        return make_call(auth_pb2_grpc.AuthServiceStub(channel).Login, request)

    def RefreshToken(self, request):
        check()
        return make_call(auth_pb2_grpc.AuthServiceStub(channel).RefreshToken, request)

    def RevokeRefreshToken(self, request):
        check()
        return make_call(auth_pb2_grpc.AuthServiceStub(channel).RevokeRefreshToken, request)

    def ConfirmForgotPasswordRequest(self, **kwargs):
        return auth_pb2.ConfirmForgotPasswordRequest(**kwargs)

    def ConfirmForgotPasswordResponse(self, **kwargs):
        return auth_pb2.ConfirmForgotPasswordResponse(**kwargs)

    def ForgotPasswordRequest(self, **kwargs):
        return auth_pb2.ForgotPasswordRequest(**kwargs)

    def ForgotPasswordResponse(self, **kwargs):
        return auth_pb2.ForgotPasswordResponse(**kwargs)

    def LoginRequest(self, **kwargs):
        return auth_pb2.LoginRequest(**kwargs)

    def LoginResponse(self, **kwargs):
        return auth_pb2.LoginResponse(**kwargs)

    def RefreshTokenRequest(self, **kwargs):
        return auth_pb2.RefreshTokenRequest(**kwargs)

    def RefreshTokenResponse(self, **kwargs):
        return auth_pb2.RefreshTokenResponse(**kwargs)

    def RevokeRefreshTokenRequest(self, **kwargs):
        return auth_pb2.RevokeRefreshTokenRequest(**kwargs)

    def RevokeRefreshTokenResponse(self, **kwargs):
        return auth_pb2.RevokeRefreshTokenResponse(**kwargs)


from . import log_pb2
from . import log_pb2_grpc


class LogService:

    def LogRecord(self, **kwargs):
        return log_pb2.LogRecord(**kwargs)


from . import provider_pb2
from . import provider_pb2_grpc


class ProviderService:

    def GetMetrics(self, request):
        check()
        return make_call(provider_pb2_grpc.ProviderServiceStub(channel).GetMetrics, request)

    def ListPayouts(self, request):
        check()
        return make_call(provider_pb2_grpc.ProviderServiceStub(channel).ListPayouts, request)

    def ListRevenueByCustomer(self, request):
        check()
        return make_call(provider_pb2_grpc.ProviderServiceStub(channel).ListRevenueByCustomer, request)

    def ListRevenueByTools(self, request):
        check()
        return make_call(provider_pb2_grpc.ProviderServiceStub(channel).ListRevenueByTools, request)

    def GetMetricsRequest(self, **kwargs):
        return provider_pb2.GetMetricsRequest(**kwargs)

    def GetMetricsResponse(self, **kwargs):
        return provider_pb2.GetMetricsResponse(**kwargs)

    def ListPayoutsRequest(self, **kwargs):
        return provider_pb2.ListPayoutsRequest(**kwargs)

    def ListPayoutsResponse(self, **kwargs):
        return provider_pb2.ListPayoutsResponse(**kwargs)

    def ListRevenueByCustomerRequest(self, **kwargs):
        return provider_pb2.ListRevenueByCustomerRequest(**kwargs)

    def ListRevenueByCustomerResponse(self, **kwargs):
        return provider_pb2.ListRevenueByCustomerResponse(**kwargs)

    def ListRevenueByToolsRequest(self, **kwargs):
        return provider_pb2.ListRevenueByToolsRequest(**kwargs)

    def ListRevenueByToolsResponse(self, **kwargs):
        return provider_pb2.ListRevenueByToolsResponse(**kwargs)

    def Payout(self, **kwargs):
        return provider_pb2.Payout(**kwargs)

