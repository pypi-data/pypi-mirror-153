import sys
from datetime import datetime
from typing import Dict, List, Optional

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

Accept = str
AccountId = str
ActionArn = str
AlarmName = str
AlgorithmArn = str
AlgorithmImage = str
AppArn = str
AppImageConfigArn = str
AppImageConfigName = str
AppManaged = bool
AppName = str
ApprovalDescription = str
ArnOrName = str
ArtifactArn = str
ArtifactDigest = str
AssociationEntityArn = str
AthenaCatalog = str
AthenaDatabase = str
AthenaQueryString = str
AthenaWorkGroup = str
AttributeName = str
AutoGenerateEndpointName = bool
AutoMLFailureReason = str
AutoMLJobArn = str
AutoMLJobName = str
AutoMLMaxResults = int
AutoMLNameContains = str
BillableTimeInSeconds = int
BlockedReason = str
Boolean = bool
Branch = str
BucketName = str
CallbackToken = str
CandidateDefinitionNotebookLocation = str
CandidateName = str
CandidateStepArn = str
CandidateStepName = str
CapacitySizeValue = int
Catalog = str
Cents = int
CertifyForMarketplace = bool
ChannelName = str
Cidr = str
ClientId = str
ClientSecret = str
ClientToken = str
CodeRepositoryArn = str
CodeRepositoryContains = str
CodeRepositoryNameContains = str
CodeRepositoryNameOrUrl = str
CognitoUserGroup = str
CognitoUserPool = str
CollectionName = str
CompilationJobArn = str
CompilerOptions = str
ConfigKey = str
ConfigValue = str
ContainerArgument = str
ContainerEntrypointString = str
ContainerHostname = str
ContainerImage = str
ContentDigest = str
ContentType = str
ContextArn = str
CsvContentType = str
CustomerMetadataKey = str
CustomerMetadataValue = str
DataExplorationNotebookLocation = str
DataInputConfig = str
Database = str
DefaultGid = int
DefaultUid = int
Description = str
DestinationS3Uri = str
DeviceArn = str
DeviceDescription = str
DeviceFleetArn = str
DeviceFleetDescription = str
DeviceName = str
DirectoryPath = str
DisableProfiler = bool
DisassociateAdditionalCodeRepositories = bool
DisassociateDefaultCodeRepository = bool
DisassociateNotebookInstanceAcceleratorTypes = bool
DisassociateNotebookInstanceLifecycleConfig = bool
Dollars = int
DomainArn = str
DomainId = str
DomainName = str
DoubleParameterValue = float
EdgePackagingJobArn = str
EdgePresetDeploymentArtifact = str
EdgeVersion = str
EfsUid = str
EnableCapture = bool
EnableIotRoleAlias = bool
EndpointArn = str
EndpointConfigArn = str
EndpointConfigName = str
EndpointConfigNameContains = str
EndpointName = str
EndpointNameContains = str
EntityDescription = str
EntityName = str
EnvironmentKey = str
EnvironmentValue = str
ExitMessage = str
ExperimentArn = str
ExperimentDescription = str
ExperimentEntityName = str
ExperimentEntityNameOrArn = str
ExperimentSourceArn = str
ExpiresInSeconds = int
ExplainabilityLocation = str
FailureReason = str
FeatureGroupArn = str
FeatureGroupMaxResults = int
FeatureGroupName = str
FeatureGroupNameContains = str
FeatureName = str
FileSystemId = str
FilterValue = str
Float = float
FlowDefinitionArn = str
FlowDefinitionName = str
FlowDefinitionTaskAvailabilityLifetimeInSeconds = int
FlowDefinitionTaskCount = int
FlowDefinitionTaskDescription = str
FlowDefinitionTaskKeyword = str
FlowDefinitionTaskTimeLimitInSeconds = int
FlowDefinitionTaskTitle = str
FrameworkVersion = str
GenerateCandidateDefinitionsOnly = bool
GitConfigUrl = str
Group = str
HumanLoopActivationConditions = str
HumanTaskUiArn = str
HumanTaskUiName = str
HyperParameterKey = str
HyperParameterTrainingJobDefinitionName = str
HyperParameterTuningJobArn = str
HyperParameterTuningJobName = str
HyperParameterValue = str
IdempotencyToken = str
ImageArn = str
ImageBaseImage = str
ImageContainerImage = str
ImageDeleteProperty = str
ImageDescription = str
ImageDigest = str
ImageDisplayName = str
ImageName = str
ImageNameContains = str
ImageUri = str
ImageVersionArn = str
ImageVersionNumber = int
InferenceImage = str
InferenceSpecificationName = str
InitialNumberOfUsers = int
InitialTaskCount = int
Integer = int
IntegerValue = int
InvocationsMaxRetries = int
InvocationsTimeoutInSeconds = int
IotRoleAlias = str
JobDurationInSeconds = int
JobReferenceCode = str
JobReferenceCodeContains = str
JsonContentType = str
JsonPath = str
KernelDisplayName = str
KernelName = str
Key = str
KmsKeyId = str
LabelAttributeName = str
LabelCounter = int
LabelingJobAlgorithmSpecificationArn = str
LabelingJobArn = str
LabelingJobName = str
LambdaFunctionArn = str
LineageGroupArn = str
LineageGroupNameOrArn = str
ListMaxResults = int
ListTagsMaxResults = int
MaxAutoMLJobRuntimeInSeconds = int
MaxCandidates = int
MaxConcurrentInvocationsPerInstance = int
MaxConcurrentTaskCount = int
MaxConcurrentTransforms = int
MaxHumanLabeledObjectCount = int
MaxNumberOfTests = int
MaxNumberOfTrainingJobs = int
MaxParallelExecutionSteps = int
MaxParallelOfTests = int
MaxParallelTrainingJobs = int
MaxPayloadInMB = int
MaxPercentageOfInputDatasetLabeled = int
MaxResults = int
MaxRuntimeInSeconds = int
MaxRuntimePerTrainingJobInSeconds = int
MaxWaitTimeInSeconds = int
MaximumExecutionTimeoutInSeconds = int
MaximumRetryAttempts = int
MediaType = str
MetadataPropertyValue = str
MetricName = str
MetricRegex = str
MetricValue = float
ModelArn = str
ModelInsightsLocation = str
ModelName = str
ModelNameContains = str
ModelPackageArn = str
ModelPackageGroupArn = str
ModelPackageVersion = int
MonitoringJobDefinitionArn = str
MonitoringJobDefinitionName = str
MonitoringMaxRuntimeInSeconds = int
MonitoringS3Uri = str
MonitoringScheduleArn = str
MonitoringScheduleName = str
MonitoringTimeOffsetString = str
MountPath = str
NameContains = str
NeoVpcSecurityGroupId = str
NeoVpcSubnetId = str
NetworkInterfaceId = str
NextToken = str
NotebookInstanceArn = str
NotebookInstanceLifecycleConfigArn = str
NotebookInstanceLifecycleConfigContent = str
NotebookInstanceLifecycleConfigName = str
NotebookInstanceLifecycleConfigNameContains = str
NotebookInstanceName = str
NotebookInstanceNameContains = str
NotebookInstanceUrl = str
NotebookInstanceVolumeSizeInGB = int
NotificationTopicArn = str
NumberOfHumanWorkersPerDataObject = int
ObjectiveStatusCounter = int
OidcEndpoint = str
OptionalDouble = float
OptionalInteger = int
OptionalVolumeSizeInGB = int
PaginationToken = str
ParameterKey = str
ParameterName = str
ParameterValue = str
PipelineArn = str
PipelineDefinition = str
PipelineDescription = str
PipelineExecutionArn = str
PipelineExecutionDescription = str
PipelineExecutionFailureReason = str
PipelineExecutionName = str
PipelineName = str
PipelineParameterName = str
PlatformIdentifier = str
PolicyString = str
PresignedDomainUrl = str
ProbabilityThresholdAttribute = float
ProcessingEnvironmentKey = str
ProcessingEnvironmentValue = str
ProcessingInstanceCount = int
ProcessingJobArn = str
ProcessingJobName = str
ProcessingLocalPath = str
ProcessingMaxRuntimeInSeconds = int
ProcessingVolumeSizeInGB = int
ProductId = str
ProjectArn = str
ProjectEntityName = str
ProjectId = str
PropertyNameHint = str
ProvisionedProductStatusMessage = str
ProvisioningParameterKey = str
ProvisioningParameterValue = str
QueryLineageMaxDepth = int
QueryLineageMaxResults = int
RecommendationJobArn = str
RecommendationJobDescription = str
RecommendationJobName = str
RedshiftClusterId = str
RedshiftDatabase = str
RedshiftQueryString = str
RedshiftUserName = str
RepositoryCredentialsProviderArn = str
ResourceArn = str
ResourceId = str
ResourcePolicyString = str
ResourcePropertyName = str
ResponseMIMEType = str
RoleArn = str
RuleConfigurationName = str
S3Uri = str
SamplingPercentage = int
ScheduleExpression = str
SecretArn = str
SecurityGroupId = str
ServerlessMaxConcurrency = int
ServerlessMemorySizeInMB = int
ServiceCatalogEntityId = str
SessionExpirationDurationInSeconds = int
SingleSignOnUserIdentifier = str
SnsTopicArn = str
SourceType = str
SourceUri = str
SpawnRate = int
StatusDetails = str
StatusMessage = str
StepDescription = str
StepDisplayName = str
StepName = str
String = str
String1024 = str
String128 = str
String200 = str
String2048 = str
String256 = str
String3072 = str
String40 = str
String64 = str
String8192 = str
StringParameterValue = str
StudioLifecycleConfigArn = str
StudioLifecycleConfigContent = str
StudioLifecycleConfigName = str
SubnetId = str
Success = bool
TableName = str
TagKey = str
TagValue = str
TargetAttributeName = str
TargetObjectiveMetricValue = float
TaskAvailabilityLifetimeInSeconds = int
TaskCount = int
TaskDescription = str
TaskInput = str
TaskKeyword = str
TaskTimeLimitInSeconds = int
TaskTitle = str
TemplateContent = str
TemplateContentSha256 = str
TemplateUrl = str
TenthFractionsOfACent = int
TerminationWaitInSeconds = int
ThingName = str
TrafficDurationInSeconds = int
TrainingEnvironmentKey = str
TrainingEnvironmentValue = str
TrainingInstanceCount = int
TrainingJobArn = str
TrainingJobName = str
TrainingJobStatusCounter = int
TrainingTimeInSeconds = int
TransformEnvironmentKey = str
TransformEnvironmentValue = str
TransformInstanceCount = int
TransformJobArn = str
TransformJobName = str
TrialArn = str
TrialComponentArn = str
TrialComponentArtifactValue = str
TrialComponentKey256 = str
TrialComponentKey64 = str
TrialComponentSourceArn = str
TrialComponentStatusMessage = str
TrialSourceArn = str
Url = str
UserProfileArn = str
UserProfileName = str
ValidationFraction = float
VariantName = str
VariantStatusMessage = str
VariantWeight = float
VersionId = str
VersionedArnOrName = str
VolumeSizeInGB = int
VpcId = str
WaitIntervalInSeconds = int
WorkforceArn = str
WorkforceName = str
WorkteamArn = str
WorkteamName = str


class ActionStatus(str):
    Unknown = "Unknown"
    InProgress = "InProgress"
    Completed = "Completed"
    Failed = "Failed"
    Stopping = "Stopping"
    Stopped = "Stopped"


class AlgorithmSortBy(str):
    Name = "Name"
    CreationTime = "CreationTime"


class AlgorithmStatus(str):
    Pending = "Pending"
    InProgress = "InProgress"
    Completed = "Completed"
    Failed = "Failed"
    Deleting = "Deleting"


class AppImageConfigSortKey(str):
    CreationTime = "CreationTime"
    LastModifiedTime = "LastModifiedTime"
    Name = "Name"


class AppInstanceType(str):
    system = "system"
    ml_t3_micro = "ml.t3.micro"
    ml_t3_small = "ml.t3.small"
    ml_t3_medium = "ml.t3.medium"
    ml_t3_large = "ml.t3.large"
    ml_t3_xlarge = "ml.t3.xlarge"
    ml_t3_2xlarge = "ml.t3.2xlarge"
    ml_m5_large = "ml.m5.large"
    ml_m5_xlarge = "ml.m5.xlarge"
    ml_m5_2xlarge = "ml.m5.2xlarge"
    ml_m5_4xlarge = "ml.m5.4xlarge"
    ml_m5_8xlarge = "ml.m5.8xlarge"
    ml_m5_12xlarge = "ml.m5.12xlarge"
    ml_m5_16xlarge = "ml.m5.16xlarge"
    ml_m5_24xlarge = "ml.m5.24xlarge"
    ml_m5d_large = "ml.m5d.large"
    ml_m5d_xlarge = "ml.m5d.xlarge"
    ml_m5d_2xlarge = "ml.m5d.2xlarge"
    ml_m5d_4xlarge = "ml.m5d.4xlarge"
    ml_m5d_8xlarge = "ml.m5d.8xlarge"
    ml_m5d_12xlarge = "ml.m5d.12xlarge"
    ml_m5d_16xlarge = "ml.m5d.16xlarge"
    ml_m5d_24xlarge = "ml.m5d.24xlarge"
    ml_c5_large = "ml.c5.large"
    ml_c5_xlarge = "ml.c5.xlarge"
    ml_c5_2xlarge = "ml.c5.2xlarge"
    ml_c5_4xlarge = "ml.c5.4xlarge"
    ml_c5_9xlarge = "ml.c5.9xlarge"
    ml_c5_12xlarge = "ml.c5.12xlarge"
    ml_c5_18xlarge = "ml.c5.18xlarge"
    ml_c5_24xlarge = "ml.c5.24xlarge"
    ml_p3_2xlarge = "ml.p3.2xlarge"
    ml_p3_8xlarge = "ml.p3.8xlarge"
    ml_p3_16xlarge = "ml.p3.16xlarge"
    ml_p3dn_24xlarge = "ml.p3dn.24xlarge"
    ml_g4dn_xlarge = "ml.g4dn.xlarge"
    ml_g4dn_2xlarge = "ml.g4dn.2xlarge"
    ml_g4dn_4xlarge = "ml.g4dn.4xlarge"
    ml_g4dn_8xlarge = "ml.g4dn.8xlarge"
    ml_g4dn_12xlarge = "ml.g4dn.12xlarge"
    ml_g4dn_16xlarge = "ml.g4dn.16xlarge"
    ml_r5_large = "ml.r5.large"
    ml_r5_xlarge = "ml.r5.xlarge"
    ml_r5_2xlarge = "ml.r5.2xlarge"
    ml_r5_4xlarge = "ml.r5.4xlarge"
    ml_r5_8xlarge = "ml.r5.8xlarge"
    ml_r5_12xlarge = "ml.r5.12xlarge"
    ml_r5_16xlarge = "ml.r5.16xlarge"
    ml_r5_24xlarge = "ml.r5.24xlarge"


class AppNetworkAccessType(str):
    PublicInternetOnly = "PublicInternetOnly"
    VpcOnly = "VpcOnly"


class AppSecurityGroupManagement(str):
    Service = "Service"
    Customer = "Customer"


class AppSortKey(str):
    CreationTime = "CreationTime"


class AppStatus(str):
    Deleted = "Deleted"
    Deleting = "Deleting"
    Failed = "Failed"
    InService = "InService"
    Pending = "Pending"


class AppType(str):
    JupyterServer = "JupyterServer"
    KernelGateway = "KernelGateway"
    TensorBoard = "TensorBoard"
    RStudioServerPro = "RStudioServerPro"
    RSessionGateway = "RSessionGateway"


class ArtifactSourceIdType(str):
    MD5Hash = "MD5Hash"
    S3ETag = "S3ETag"
    S3Version = "S3Version"
    Custom = "Custom"


class AssemblyType(str):
    None_ = "None"
    Line = "Line"


class AssociationEdgeType(str):
    ContributedTo = "ContributedTo"
    AssociatedWith = "AssociatedWith"
    DerivedFrom = "DerivedFrom"
    Produced = "Produced"


class AthenaResultCompressionType(str):
    GZIP = "GZIP"
    SNAPPY = "SNAPPY"
    ZLIB = "ZLIB"


class AthenaResultFormat(str):
    PARQUET = "PARQUET"
    ORC = "ORC"
    AVRO = "AVRO"
    JSON = "JSON"
    TEXTFILE = "TEXTFILE"


class AuthMode(str):
    SSO = "SSO"
    IAM = "IAM"


class AutoMLChannelType(str):
    training = "training"
    validation = "validation"


class AutoMLJobObjectiveType(str):
    Maximize = "Maximize"
    Minimize = "Minimize"


class AutoMLJobSecondaryStatus(str):
    Starting = "Starting"
    AnalyzingData = "AnalyzingData"
    FeatureEngineering = "FeatureEngineering"
    ModelTuning = "ModelTuning"
    MaxCandidatesReached = "MaxCandidatesReached"
    Failed = "Failed"
    Stopped = "Stopped"
    MaxAutoMLJobRuntimeReached = "MaxAutoMLJobRuntimeReached"
    Stopping = "Stopping"
    CandidateDefinitionsGenerated = "CandidateDefinitionsGenerated"
    GeneratingExplainabilityReport = "GeneratingExplainabilityReport"
    Completed = "Completed"
    ExplainabilityError = "ExplainabilityError"
    DeployingModel = "DeployingModel"
    ModelDeploymentError = "ModelDeploymentError"
    GeneratingModelInsightsReport = "GeneratingModelInsightsReport"
    ModelInsightsError = "ModelInsightsError"


class AutoMLJobStatus(str):
    Completed = "Completed"
    InProgress = "InProgress"
    Failed = "Failed"
    Stopped = "Stopped"
    Stopping = "Stopping"


class AutoMLMetricEnum(str):
    Accuracy = "Accuracy"
    MSE = "MSE"
    F1 = "F1"
    F1macro = "F1macro"
    AUC = "AUC"


class AutoMLMetricExtendedEnum(str):
    Accuracy = "Accuracy"
    MSE = "MSE"
    F1 = "F1"
    F1macro = "F1macro"
    AUC = "AUC"
    RMSE = "RMSE"
    MAE = "MAE"
    R2 = "R2"
    BalancedAccuracy = "BalancedAccuracy"
    Precision = "Precision"
    PrecisionMacro = "PrecisionMacro"
    Recall = "Recall"
    RecallMacro = "RecallMacro"
    LogLoss = "LogLoss"


class AutoMLS3DataType(str):
    ManifestFile = "ManifestFile"
    S3Prefix = "S3Prefix"


class AutoMLSortBy(str):
    Name = "Name"
    CreationTime = "CreationTime"
    Status = "Status"


class AutoMLSortOrder(str):
    Ascending = "Ascending"
    Descending = "Descending"


class AwsManagedHumanLoopRequestSource(str):
    AWS_Rekognition_DetectModerationLabels_Image_V3 = (
        "AWS/Rekognition/DetectModerationLabels/Image/V3"
    )
    AWS_Textract_AnalyzeDocument_Forms_V1 = "AWS/Textract/AnalyzeDocument/Forms/V1"


class BatchStrategy(str):
    MultiRecord = "MultiRecord"
    SingleRecord = "SingleRecord"


class BooleanOperator(str):
    And = "And"
    Or = "Or"


class CandidateSortBy(str):
    CreationTime = "CreationTime"
    Status = "Status"
    FinalObjectiveMetricValue = "FinalObjectiveMetricValue"


class CandidateStatus(str):
    Completed = "Completed"
    InProgress = "InProgress"
    Failed = "Failed"
    Stopped = "Stopped"
    Stopping = "Stopping"


class CandidateStepType(str):
    AWS_SageMaker_TrainingJob = "AWS::SageMaker::TrainingJob"
    AWS_SageMaker_TransformJob = "AWS::SageMaker::TransformJob"
    AWS_SageMaker_ProcessingJob = "AWS::SageMaker::ProcessingJob"


class CapacitySizeType(str):
    INSTANCE_COUNT = "INSTANCE_COUNT"
    CAPACITY_PERCENT = "CAPACITY_PERCENT"


class CaptureMode(str):
    Input = "Input"
    Output = "Output"


class CaptureStatus(str):
    Started = "Started"
    Stopped = "Stopped"


class CodeRepositorySortBy(str):
    Name = "Name"
    CreationTime = "CreationTime"
    LastModifiedTime = "LastModifiedTime"


class CodeRepositorySortOrder(str):
    Ascending = "Ascending"
    Descending = "Descending"


class CompilationJobStatus(str):
    INPROGRESS = "INPROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    STARTING = "STARTING"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"


class CompressionType(str):
    None_ = "None"
    Gzip = "Gzip"


class ConditionOutcome(str):
    True_ = "True"
    False_ = "False"


class ContainerMode(str):
    SingleModel = "SingleModel"
    MultiModel = "MultiModel"


class ContentClassifier(str):
    FreeOfPersonallyIdentifiableInformation = "FreeOfPersonallyIdentifiableInformation"
    FreeOfAdultContent = "FreeOfAdultContent"


class DataDistributionType(str):
    FullyReplicated = "FullyReplicated"
    ShardedByS3Key = "ShardedByS3Key"


class DetailedAlgorithmStatus(str):
    NotStarted = "NotStarted"
    InProgress = "InProgress"
    Completed = "Completed"
    Failed = "Failed"


class DetailedModelPackageStatus(str):
    NotStarted = "NotStarted"
    InProgress = "InProgress"
    Completed = "Completed"
    Failed = "Failed"


class DirectInternetAccess(str):
    Enabled = "Enabled"
    Disabled = "Disabled"


class Direction(str):
    Both = "Both"
    Ascendants = "Ascendants"
    Descendants = "Descendants"


class DomainStatus(str):
    Deleting = "Deleting"
    Failed = "Failed"
    InService = "InService"
    Pending = "Pending"
    Updating = "Updating"
    Update_Failed = "Update_Failed"
    Delete_Failed = "Delete_Failed"


class EdgePackagingJobStatus(str):
    STARTING = "STARTING"
    INPROGRESS = "INPROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"


class EdgePresetDeploymentStatus(str):
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class EdgePresetDeploymentType(str):
    GreengrassV2Component = "GreengrassV2Component"


class EndpointConfigSortKey(str):
    Name = "Name"
    CreationTime = "CreationTime"


class EndpointSortKey(str):
    Name = "Name"
    CreationTime = "CreationTime"
    Status = "Status"


class EndpointStatus(str):
    OutOfService = "OutOfService"
    Creating = "Creating"
    Updating = "Updating"
    SystemUpdating = "SystemUpdating"
    RollingBack = "RollingBack"
    InService = "InService"
    Deleting = "Deleting"
    Failed = "Failed"


class ExecutionStatus(str):
    Pending = "Pending"
    Completed = "Completed"
    CompletedWithViolations = "CompletedWithViolations"
    InProgress = "InProgress"
    Failed = "Failed"
    Stopping = "Stopping"
    Stopped = "Stopped"


class FeatureGroupSortBy(str):
    Name = "Name"
    FeatureGroupStatus = "FeatureGroupStatus"
    OfflineStoreStatus = "OfflineStoreStatus"
    CreationTime = "CreationTime"


class FeatureGroupSortOrder(str):
    Ascending = "Ascending"
    Descending = "Descending"


class FeatureGroupStatus(str):
    Creating = "Creating"
    Created = "Created"
    CreateFailed = "CreateFailed"
    Deleting = "Deleting"
    DeleteFailed = "DeleteFailed"


class FeatureType(str):
    Integral = "Integral"
    Fractional = "Fractional"
    String = "String"


class FileSystemAccessMode(str):
    rw = "rw"
    ro = "ro"


class FileSystemType(str):
    EFS = "EFS"
    FSxLustre = "FSxLustre"


class FlowDefinitionStatus(str):
    Initializing = "Initializing"
    Active = "Active"
    Failed = "Failed"
    Deleting = "Deleting"


class Framework(str):
    TENSORFLOW = "TENSORFLOW"
    KERAS = "KERAS"
    MXNET = "MXNET"
    ONNX = "ONNX"
    PYTORCH = "PYTORCH"
    XGBOOST = "XGBOOST"
    TFLITE = "TFLITE"
    DARKNET = "DARKNET"
    SKLEARN = "SKLEARN"


class HumanTaskUiStatus(str):
    Active = "Active"
    Deleting = "Deleting"


class HyperParameterScalingType(str):
    Auto = "Auto"
    Linear = "Linear"
    Logarithmic = "Logarithmic"
    ReverseLogarithmic = "ReverseLogarithmic"


class HyperParameterTuningJobObjectiveType(str):
    Maximize = "Maximize"
    Minimize = "Minimize"


class HyperParameterTuningJobSortByOptions(str):
    Name = "Name"
    Status = "Status"
    CreationTime = "CreationTime"


class HyperParameterTuningJobStatus(str):
    Completed = "Completed"
    InProgress = "InProgress"
    Failed = "Failed"
    Stopped = "Stopped"
    Stopping = "Stopping"


class HyperParameterTuningJobStrategyType(str):
    Bayesian = "Bayesian"
    Random = "Random"


class HyperParameterTuningJobWarmStartType(str):
    IdenticalDataAndAlgorithm = "IdenticalDataAndAlgorithm"
    TransferLearning = "TransferLearning"


class ImageSortBy(str):
    CREATION_TIME = "CREATION_TIME"
    LAST_MODIFIED_TIME = "LAST_MODIFIED_TIME"
    IMAGE_NAME = "IMAGE_NAME"


class ImageSortOrder(str):
    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"


class ImageStatus(str):
    CREATING = "CREATING"
    CREATED = "CREATED"
    CREATE_FAILED = "CREATE_FAILED"
    UPDATING = "UPDATING"
    UPDATE_FAILED = "UPDATE_FAILED"
    DELETING = "DELETING"
    DELETE_FAILED = "DELETE_FAILED"


class ImageVersionSortBy(str):
    CREATION_TIME = "CREATION_TIME"
    LAST_MODIFIED_TIME = "LAST_MODIFIED_TIME"
    VERSION = "VERSION"


class ImageVersionSortOrder(str):
    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"


class ImageVersionStatus(str):
    CREATING = "CREATING"
    CREATED = "CREATED"
    CREATE_FAILED = "CREATE_FAILED"
    DELETING = "DELETING"
    DELETE_FAILED = "DELETE_FAILED"


class InferenceExecutionMode(str):
    Serial = "Serial"
    Direct = "Direct"


class InputMode(str):
    Pipe = "Pipe"
    File = "File"


class InstanceType(str):
    ml_t2_medium = "ml.t2.medium"
    ml_t2_large = "ml.t2.large"
    ml_t2_xlarge = "ml.t2.xlarge"
    ml_t2_2xlarge = "ml.t2.2xlarge"
    ml_t3_medium = "ml.t3.medium"
    ml_t3_large = "ml.t3.large"
    ml_t3_xlarge = "ml.t3.xlarge"
    ml_t3_2xlarge = "ml.t3.2xlarge"
    ml_m4_xlarge = "ml.m4.xlarge"
    ml_m4_2xlarge = "ml.m4.2xlarge"
    ml_m4_4xlarge = "ml.m4.4xlarge"
    ml_m4_10xlarge = "ml.m4.10xlarge"
    ml_m4_16xlarge = "ml.m4.16xlarge"
    ml_m5_xlarge = "ml.m5.xlarge"
    ml_m5_2xlarge = "ml.m5.2xlarge"
    ml_m5_4xlarge = "ml.m5.4xlarge"
    ml_m5_12xlarge = "ml.m5.12xlarge"
    ml_m5_24xlarge = "ml.m5.24xlarge"
    ml_m5d_large = "ml.m5d.large"
    ml_m5d_xlarge = "ml.m5d.xlarge"
    ml_m5d_2xlarge = "ml.m5d.2xlarge"
    ml_m5d_4xlarge = "ml.m5d.4xlarge"
    ml_m5d_8xlarge = "ml.m5d.8xlarge"
    ml_m5d_12xlarge = "ml.m5d.12xlarge"
    ml_m5d_16xlarge = "ml.m5d.16xlarge"
    ml_m5d_24xlarge = "ml.m5d.24xlarge"
    ml_c4_xlarge = "ml.c4.xlarge"
    ml_c4_2xlarge = "ml.c4.2xlarge"
    ml_c4_4xlarge = "ml.c4.4xlarge"
    ml_c4_8xlarge = "ml.c4.8xlarge"
    ml_c5_xlarge = "ml.c5.xlarge"
    ml_c5_2xlarge = "ml.c5.2xlarge"
    ml_c5_4xlarge = "ml.c5.4xlarge"
    ml_c5_9xlarge = "ml.c5.9xlarge"
    ml_c5_18xlarge = "ml.c5.18xlarge"
    ml_c5d_xlarge = "ml.c5d.xlarge"
    ml_c5d_2xlarge = "ml.c5d.2xlarge"
    ml_c5d_4xlarge = "ml.c5d.4xlarge"
    ml_c5d_9xlarge = "ml.c5d.9xlarge"
    ml_c5d_18xlarge = "ml.c5d.18xlarge"
    ml_p2_xlarge = "ml.p2.xlarge"
    ml_p2_8xlarge = "ml.p2.8xlarge"
    ml_p2_16xlarge = "ml.p2.16xlarge"
    ml_p3_2xlarge = "ml.p3.2xlarge"
    ml_p3_8xlarge = "ml.p3.8xlarge"
    ml_p3_16xlarge = "ml.p3.16xlarge"
    ml_p3dn_24xlarge = "ml.p3dn.24xlarge"
    ml_g4dn_xlarge = "ml.g4dn.xlarge"
    ml_g4dn_2xlarge = "ml.g4dn.2xlarge"
    ml_g4dn_4xlarge = "ml.g4dn.4xlarge"
    ml_g4dn_8xlarge = "ml.g4dn.8xlarge"
    ml_g4dn_12xlarge = "ml.g4dn.12xlarge"
    ml_g4dn_16xlarge = "ml.g4dn.16xlarge"
    ml_r5_large = "ml.r5.large"
    ml_r5_xlarge = "ml.r5.xlarge"
    ml_r5_2xlarge = "ml.r5.2xlarge"
    ml_r5_4xlarge = "ml.r5.4xlarge"
    ml_r5_8xlarge = "ml.r5.8xlarge"
    ml_r5_12xlarge = "ml.r5.12xlarge"
    ml_r5_16xlarge = "ml.r5.16xlarge"
    ml_r5_24xlarge = "ml.r5.24xlarge"
    ml_g5_xlarge = "ml.g5.xlarge"
    ml_g5_2xlarge = "ml.g5.2xlarge"
    ml_g5_4xlarge = "ml.g5.4xlarge"
    ml_g5_8xlarge = "ml.g5.8xlarge"
    ml_g5_16xlarge = "ml.g5.16xlarge"
    ml_g5_12xlarge = "ml.g5.12xlarge"
    ml_g5_24xlarge = "ml.g5.24xlarge"
    ml_g5_48xlarge = "ml.g5.48xlarge"


class JoinSource(str):
    Input = "Input"
    None_ = "None"


class LabelingJobStatus(str):
    Initializing = "Initializing"
    InProgress = "InProgress"
    Completed = "Completed"
    Failed = "Failed"
    Stopping = "Stopping"
    Stopped = "Stopped"


class LineageType(str):
    TrialComponent = "TrialComponent"
    Artifact = "Artifact"
    Context = "Context"
    Action = "Action"


class ListCompilationJobsSortBy(str):
    Name = "Name"
    CreationTime = "CreationTime"
    Status = "Status"


class ListDeviceFleetsSortBy(str):
    NAME = "NAME"
    CREATION_TIME = "CREATION_TIME"
    LAST_MODIFIED_TIME = "LAST_MODIFIED_TIME"


class ListEdgePackagingJobsSortBy(str):
    NAME = "NAME"
    MODEL_NAME = "MODEL_NAME"
    CREATION_TIME = "CREATION_TIME"
    LAST_MODIFIED_TIME = "LAST_MODIFIED_TIME"
    STATUS = "STATUS"


class ListInferenceRecommendationsJobsSortBy(str):
    Name = "Name"
    CreationTime = "CreationTime"
    Status = "Status"


class ListLabelingJobsForWorkteamSortByOptions(str):
    CreationTime = "CreationTime"


class ListWorkforcesSortByOptions(str):
    Name = "Name"
    CreateDate = "CreateDate"


class ListWorkteamsSortByOptions(str):
    Name = "Name"
    CreateDate = "CreateDate"


class MetricSetSource(str):
    Train = "Train"
    Validation = "Validation"
    Test = "Test"


class ModelApprovalStatus(str):
    Approved = "Approved"
    Rejected = "Rejected"
    PendingManualApproval = "PendingManualApproval"


class ModelCacheSetting(str):
    Enabled = "Enabled"
    Disabled = "Disabled"


class ModelMetadataFilterType(str):
    Domain = "Domain"
    Framework = "Framework"
    Task = "Task"
    FrameworkVersion = "FrameworkVersion"


class ModelPackageGroupSortBy(str):
    Name = "Name"
    CreationTime = "CreationTime"


class ModelPackageGroupStatus(str):
    Pending = "Pending"
    InProgress = "InProgress"
    Completed = "Completed"
    Failed = "Failed"
    Deleting = "Deleting"
    DeleteFailed = "DeleteFailed"


class ModelPackageSortBy(str):
    Name = "Name"
    CreationTime = "CreationTime"


class ModelPackageStatus(str):
    Pending = "Pending"
    InProgress = "InProgress"
    Completed = "Completed"
    Failed = "Failed"
    Deleting = "Deleting"


class ModelPackageType(str):
    Versioned = "Versioned"
    Unversioned = "Unversioned"
    Both = "Both"


class ModelSortKey(str):
    Name = "Name"
    CreationTime = "CreationTime"


class MonitoringExecutionSortKey(str):
    CreationTime = "CreationTime"
    ScheduledTime = "ScheduledTime"
    Status = "Status"


class MonitoringJobDefinitionSortKey(str):
    Name = "Name"
    CreationTime = "CreationTime"


class MonitoringProblemType(str):
    BinaryClassification = "BinaryClassification"
    MulticlassClassification = "MulticlassClassification"
    Regression = "Regression"


class MonitoringScheduleSortKey(str):
    Name = "Name"
    CreationTime = "CreationTime"
    Status = "Status"


class MonitoringType(str):
    DataQuality = "DataQuality"
    ModelQuality = "ModelQuality"
    ModelBias = "ModelBias"
    ModelExplainability = "ModelExplainability"


class NotebookInstanceAcceleratorType(str):
    ml_eia1_medium = "ml.eia1.medium"
    ml_eia1_large = "ml.eia1.large"
    ml_eia1_xlarge = "ml.eia1.xlarge"
    ml_eia2_medium = "ml.eia2.medium"
    ml_eia2_large = "ml.eia2.large"
    ml_eia2_xlarge = "ml.eia2.xlarge"


class NotebookInstanceLifecycleConfigSortKey(str):
    Name = "Name"
    CreationTime = "CreationTime"
    LastModifiedTime = "LastModifiedTime"


class NotebookInstanceLifecycleConfigSortOrder(str):
    Ascending = "Ascending"
    Descending = "Descending"


class NotebookInstanceSortKey(str):
    Name = "Name"
    CreationTime = "CreationTime"
    Status = "Status"


class NotebookInstanceSortOrder(str):
    Ascending = "Ascending"
    Descending = "Descending"


class NotebookInstanceStatus(str):
    Pending = "Pending"
    InService = "InService"
    Stopping = "Stopping"
    Stopped = "Stopped"
    Failed = "Failed"
    Deleting = "Deleting"
    Updating = "Updating"


class NotebookOutputOption(str):
    Allowed = "Allowed"
    Disabled = "Disabled"


class ObjectiveStatus(str):
    Succeeded = "Succeeded"
    Pending = "Pending"
    Failed = "Failed"


class OfflineStoreStatusValue(str):
    Active = "Active"
    Blocked = "Blocked"
    Disabled = "Disabled"


class Operator(str):
    Equals = "Equals"
    NotEquals = "NotEquals"
    GreaterThan = "GreaterThan"
    GreaterThanOrEqualTo = "GreaterThanOrEqualTo"
    LessThan = "LessThan"
    LessThanOrEqualTo = "LessThanOrEqualTo"
    Contains = "Contains"
    Exists = "Exists"
    NotExists = "NotExists"
    In = "In"


class OrderKey(str):
    Ascending = "Ascending"
    Descending = "Descending"


class ParameterType(str):
    Integer = "Integer"
    Continuous = "Continuous"
    Categorical = "Categorical"
    FreeText = "FreeText"


class PipelineExecutionStatus(str):
    Executing = "Executing"
    Stopping = "Stopping"
    Stopped = "Stopped"
    Failed = "Failed"
    Succeeded = "Succeeded"


class PipelineStatus(str):
    Active = "Active"


class ProblemType(str):
    BinaryClassification = "BinaryClassification"
    MulticlassClassification = "MulticlassClassification"
    Regression = "Regression"


class ProcessingInstanceType(str):
    ml_t3_medium = "ml.t3.medium"
    ml_t3_large = "ml.t3.large"
    ml_t3_xlarge = "ml.t3.xlarge"
    ml_t3_2xlarge = "ml.t3.2xlarge"
    ml_m4_xlarge = "ml.m4.xlarge"
    ml_m4_2xlarge = "ml.m4.2xlarge"
    ml_m4_4xlarge = "ml.m4.4xlarge"
    ml_m4_10xlarge = "ml.m4.10xlarge"
    ml_m4_16xlarge = "ml.m4.16xlarge"
    ml_c4_xlarge = "ml.c4.xlarge"
    ml_c4_2xlarge = "ml.c4.2xlarge"
    ml_c4_4xlarge = "ml.c4.4xlarge"
    ml_c4_8xlarge = "ml.c4.8xlarge"
    ml_p2_xlarge = "ml.p2.xlarge"
    ml_p2_8xlarge = "ml.p2.8xlarge"
    ml_p2_16xlarge = "ml.p2.16xlarge"
    ml_p3_2xlarge = "ml.p3.2xlarge"
    ml_p3_8xlarge = "ml.p3.8xlarge"
    ml_p3_16xlarge = "ml.p3.16xlarge"
    ml_c5_xlarge = "ml.c5.xlarge"
    ml_c5_2xlarge = "ml.c5.2xlarge"
    ml_c5_4xlarge = "ml.c5.4xlarge"
    ml_c5_9xlarge = "ml.c5.9xlarge"
    ml_c5_18xlarge = "ml.c5.18xlarge"
    ml_m5_large = "ml.m5.large"
    ml_m5_xlarge = "ml.m5.xlarge"
    ml_m5_2xlarge = "ml.m5.2xlarge"
    ml_m5_4xlarge = "ml.m5.4xlarge"
    ml_m5_12xlarge = "ml.m5.12xlarge"
    ml_m5_24xlarge = "ml.m5.24xlarge"
    ml_r5_large = "ml.r5.large"
    ml_r5_xlarge = "ml.r5.xlarge"
    ml_r5_2xlarge = "ml.r5.2xlarge"
    ml_r5_4xlarge = "ml.r5.4xlarge"
    ml_r5_8xlarge = "ml.r5.8xlarge"
    ml_r5_12xlarge = "ml.r5.12xlarge"
    ml_r5_16xlarge = "ml.r5.16xlarge"
    ml_r5_24xlarge = "ml.r5.24xlarge"
    ml_g4dn_xlarge = "ml.g4dn.xlarge"
    ml_g4dn_2xlarge = "ml.g4dn.2xlarge"
    ml_g4dn_4xlarge = "ml.g4dn.4xlarge"
    ml_g4dn_8xlarge = "ml.g4dn.8xlarge"
    ml_g4dn_12xlarge = "ml.g4dn.12xlarge"
    ml_g4dn_16xlarge = "ml.g4dn.16xlarge"


class ProcessingJobStatus(str):
    InProgress = "InProgress"
    Completed = "Completed"
    Failed = "Failed"
    Stopping = "Stopping"
    Stopped = "Stopped"


class ProcessingS3CompressionType(str):
    None_ = "None"
    Gzip = "Gzip"


class ProcessingS3DataDistributionType(str):
    FullyReplicated = "FullyReplicated"
    ShardedByS3Key = "ShardedByS3Key"


class ProcessingS3DataType(str):
    ManifestFile = "ManifestFile"
    S3Prefix = "S3Prefix"


class ProcessingS3InputMode(str):
    Pipe = "Pipe"
    File = "File"


class ProcessingS3UploadMode(str):
    Continuous = "Continuous"
    EndOfJob = "EndOfJob"


class ProductionVariantAcceleratorType(str):
    ml_eia1_medium = "ml.eia1.medium"
    ml_eia1_large = "ml.eia1.large"
    ml_eia1_xlarge = "ml.eia1.xlarge"
    ml_eia2_medium = "ml.eia2.medium"
    ml_eia2_large = "ml.eia2.large"
    ml_eia2_xlarge = "ml.eia2.xlarge"


class ProductionVariantInstanceType(str):
    ml_t2_medium = "ml.t2.medium"
    ml_t2_large = "ml.t2.large"
    ml_t2_xlarge = "ml.t2.xlarge"
    ml_t2_2xlarge = "ml.t2.2xlarge"
    ml_m4_xlarge = "ml.m4.xlarge"
    ml_m4_2xlarge = "ml.m4.2xlarge"
    ml_m4_4xlarge = "ml.m4.4xlarge"
    ml_m4_10xlarge = "ml.m4.10xlarge"
    ml_m4_16xlarge = "ml.m4.16xlarge"
    ml_m5_large = "ml.m5.large"
    ml_m5_xlarge = "ml.m5.xlarge"
    ml_m5_2xlarge = "ml.m5.2xlarge"
    ml_m5_4xlarge = "ml.m5.4xlarge"
    ml_m5_12xlarge = "ml.m5.12xlarge"
    ml_m5_24xlarge = "ml.m5.24xlarge"
    ml_m5d_large = "ml.m5d.large"
    ml_m5d_xlarge = "ml.m5d.xlarge"
    ml_m5d_2xlarge = "ml.m5d.2xlarge"
    ml_m5d_4xlarge = "ml.m5d.4xlarge"
    ml_m5d_12xlarge = "ml.m5d.12xlarge"
    ml_m5d_24xlarge = "ml.m5d.24xlarge"
    ml_c4_large = "ml.c4.large"
    ml_c4_xlarge = "ml.c4.xlarge"
    ml_c4_2xlarge = "ml.c4.2xlarge"
    ml_c4_4xlarge = "ml.c4.4xlarge"
    ml_c4_8xlarge = "ml.c4.8xlarge"
    ml_p2_xlarge = "ml.p2.xlarge"
    ml_p2_8xlarge = "ml.p2.8xlarge"
    ml_p2_16xlarge = "ml.p2.16xlarge"
    ml_p3_2xlarge = "ml.p3.2xlarge"
    ml_p3_8xlarge = "ml.p3.8xlarge"
    ml_p3_16xlarge = "ml.p3.16xlarge"
    ml_c5_large = "ml.c5.large"
    ml_c5_xlarge = "ml.c5.xlarge"
    ml_c5_2xlarge = "ml.c5.2xlarge"
    ml_c5_4xlarge = "ml.c5.4xlarge"
    ml_c5_9xlarge = "ml.c5.9xlarge"
    ml_c5_18xlarge = "ml.c5.18xlarge"
    ml_c5d_large = "ml.c5d.large"
    ml_c5d_xlarge = "ml.c5d.xlarge"
    ml_c5d_2xlarge = "ml.c5d.2xlarge"
    ml_c5d_4xlarge = "ml.c5d.4xlarge"
    ml_c5d_9xlarge = "ml.c5d.9xlarge"
    ml_c5d_18xlarge = "ml.c5d.18xlarge"
    ml_g4dn_xlarge = "ml.g4dn.xlarge"
    ml_g4dn_2xlarge = "ml.g4dn.2xlarge"
    ml_g4dn_4xlarge = "ml.g4dn.4xlarge"
    ml_g4dn_8xlarge = "ml.g4dn.8xlarge"
    ml_g4dn_12xlarge = "ml.g4dn.12xlarge"
    ml_g4dn_16xlarge = "ml.g4dn.16xlarge"
    ml_r5_large = "ml.r5.large"
    ml_r5_xlarge = "ml.r5.xlarge"
    ml_r5_2xlarge = "ml.r5.2xlarge"
    ml_r5_4xlarge = "ml.r5.4xlarge"
    ml_r5_12xlarge = "ml.r5.12xlarge"
    ml_r5_24xlarge = "ml.r5.24xlarge"
    ml_r5d_large = "ml.r5d.large"
    ml_r5d_xlarge = "ml.r5d.xlarge"
    ml_r5d_2xlarge = "ml.r5d.2xlarge"
    ml_r5d_4xlarge = "ml.r5d.4xlarge"
    ml_r5d_12xlarge = "ml.r5d.12xlarge"
    ml_r5d_24xlarge = "ml.r5d.24xlarge"
    ml_inf1_xlarge = "ml.inf1.xlarge"
    ml_inf1_2xlarge = "ml.inf1.2xlarge"
    ml_inf1_6xlarge = "ml.inf1.6xlarge"
    ml_inf1_24xlarge = "ml.inf1.24xlarge"


class ProfilingStatus(str):
    Enabled = "Enabled"
    Disabled = "Disabled"


class ProjectSortBy(str):
    Name = "Name"
    CreationTime = "CreationTime"


class ProjectSortOrder(str):
    Ascending = "Ascending"
    Descending = "Descending"


class ProjectStatus(str):
    Pending = "Pending"
    CreateInProgress = "CreateInProgress"
    CreateCompleted = "CreateCompleted"
    CreateFailed = "CreateFailed"
    DeleteInProgress = "DeleteInProgress"
    DeleteFailed = "DeleteFailed"
    DeleteCompleted = "DeleteCompleted"
    UpdateInProgress = "UpdateInProgress"
    UpdateCompleted = "UpdateCompleted"
    UpdateFailed = "UpdateFailed"


class RStudioServerProAccessStatus(str):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class RStudioServerProUserGroup(str):
    R_STUDIO_ADMIN = "R_STUDIO_ADMIN"
    R_STUDIO_USER = "R_STUDIO_USER"


class RecommendationJobStatus(str):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"


class RecommendationJobType(str):
    Default = "Default"
    Advanced = "Advanced"


class RecordWrapper(str):
    None_ = "None"
    RecordIO = "RecordIO"


class RedshiftResultCompressionType(str):
    None_ = "None"
    GZIP = "GZIP"
    BZIP2 = "BZIP2"
    ZSTD = "ZSTD"
    SNAPPY = "SNAPPY"


class RedshiftResultFormat(str):
    PARQUET = "PARQUET"
    CSV = "CSV"


class RepositoryAccessMode(str):
    Platform = "Platform"
    Vpc = "Vpc"


class ResourceType(str):
    TrainingJob = "TrainingJob"
    Experiment = "Experiment"
    ExperimentTrial = "ExperimentTrial"
    ExperimentTrialComponent = "ExperimentTrialComponent"
    Endpoint = "Endpoint"
    ModelPackage = "ModelPackage"
    ModelPackageGroup = "ModelPackageGroup"
    Pipeline = "Pipeline"
    PipelineExecution = "PipelineExecution"
    FeatureGroup = "FeatureGroup"
    Project = "Project"


class RetentionType(str):
    Retain = "Retain"
    Delete = "Delete"


class RootAccess(str):
    Enabled = "Enabled"
    Disabled = "Disabled"


class RuleEvaluationStatus(str):
    InProgress = "InProgress"
    NoIssuesFound = "NoIssuesFound"
    IssuesFound = "IssuesFound"
    Error = "Error"
    Stopping = "Stopping"
    Stopped = "Stopped"


class S3DataDistribution(str):
    FullyReplicated = "FullyReplicated"
    ShardedByS3Key = "ShardedByS3Key"


class S3DataType(str):
    ManifestFile = "ManifestFile"
    S3Prefix = "S3Prefix"
    AugmentedManifestFile = "AugmentedManifestFile"


class SagemakerServicecatalogStatus(str):
    Enabled = "Enabled"
    Disabled = "Disabled"


class ScheduleStatus(str):
    Pending = "Pending"
    Failed = "Failed"
    Scheduled = "Scheduled"
    Stopped = "Stopped"


class SearchSortOrder(str):
    Ascending = "Ascending"
    Descending = "Descending"


class SecondaryStatus(str):
    Starting = "Starting"
    LaunchingMLInstances = "LaunchingMLInstances"
    PreparingTrainingStack = "PreparingTrainingStack"
    Downloading = "Downloading"
    DownloadingTrainingImage = "DownloadingTrainingImage"
    Training = "Training"
    Uploading = "Uploading"
    Stopping = "Stopping"
    Stopped = "Stopped"
    MaxRuntimeExceeded = "MaxRuntimeExceeded"
    Completed = "Completed"
    Failed = "Failed"
    Interrupted = "Interrupted"
    MaxWaitTimeExceeded = "MaxWaitTimeExceeded"
    Updating = "Updating"
    Restarting = "Restarting"


class SortActionsBy(str):
    Name = "Name"
    CreationTime = "CreationTime"


class SortArtifactsBy(str):
    CreationTime = "CreationTime"


class SortAssociationsBy(str):
    SourceArn = "SourceArn"
    DestinationArn = "DestinationArn"
    SourceType = "SourceType"
    DestinationType = "DestinationType"
    CreationTime = "CreationTime"


class SortBy(str):
    Name = "Name"
    CreationTime = "CreationTime"
    Status = "Status"


class SortContextsBy(str):
    Name = "Name"
    CreationTime = "CreationTime"


class SortExperimentsBy(str):
    Name = "Name"
    CreationTime = "CreationTime"


class SortLineageGroupsBy(str):
    Name = "Name"
    CreationTime = "CreationTime"


class SortOrder(str):
    Ascending = "Ascending"
    Descending = "Descending"


class SortPipelineExecutionsBy(str):
    CreationTime = "CreationTime"
    PipelineExecutionArn = "PipelineExecutionArn"


class SortPipelinesBy(str):
    Name = "Name"
    CreationTime = "CreationTime"


class SortTrialComponentsBy(str):
    Name = "Name"
    CreationTime = "CreationTime"


class SortTrialsBy(str):
    Name = "Name"
    CreationTime = "CreationTime"


class SplitType(str):
    None_ = "None"
    Line = "Line"
    RecordIO = "RecordIO"
    TFRecord = "TFRecord"


class StepStatus(str):
    Starting = "Starting"
    Executing = "Executing"
    Stopping = "Stopping"
    Stopped = "Stopped"
    Failed = "Failed"
    Succeeded = "Succeeded"


class StudioLifecycleConfigAppType(str):
    JupyterServer = "JupyterServer"
    KernelGateway = "KernelGateway"


class StudioLifecycleConfigSortKey(str):
    CreationTime = "CreationTime"
    LastModifiedTime = "LastModifiedTime"
    Name = "Name"


class TargetDevice(str):
    lambda_ = "lambda"
    ml_m4 = "ml_m4"
    ml_m5 = "ml_m5"
    ml_c4 = "ml_c4"
    ml_c5 = "ml_c5"
    ml_p2 = "ml_p2"
    ml_p3 = "ml_p3"
    ml_g4dn = "ml_g4dn"
    ml_inf1 = "ml_inf1"
    ml_eia2 = "ml_eia2"
    jetson_tx1 = "jetson_tx1"
    jetson_tx2 = "jetson_tx2"
    jetson_nano = "jetson_nano"
    jetson_xavier = "jetson_xavier"
    rasp3b = "rasp3b"
    imx8qm = "imx8qm"
    deeplens = "deeplens"
    rk3399 = "rk3399"
    rk3288 = "rk3288"
    aisage = "aisage"
    sbe_c = "sbe_c"
    qcs605 = "qcs605"
    qcs603 = "qcs603"
    sitara_am57x = "sitara_am57x"
    amba_cv2 = "amba_cv2"
    amba_cv22 = "amba_cv22"
    amba_cv25 = "amba_cv25"
    x86_win32 = "x86_win32"
    x86_win64 = "x86_win64"
    coreml = "coreml"
    jacinto_tda4vm = "jacinto_tda4vm"
    imx8mplus = "imx8mplus"


class TargetPlatformAccelerator(str):
    INTEL_GRAPHICS = "INTEL_GRAPHICS"
    MALI = "MALI"
    NVIDIA = "NVIDIA"
    NNA = "NNA"


class TargetPlatformArch(str):
    X86_64 = "X86_64"
    X86 = "X86"
    ARM64 = "ARM64"
    ARM_EABI = "ARM_EABI"
    ARM_EABIHF = "ARM_EABIHF"


class TargetPlatformOs(str):
    ANDROID = "ANDROID"
    LINUX = "LINUX"


class TrafficRoutingConfigType(str):
    ALL_AT_ONCE = "ALL_AT_ONCE"
    CANARY = "CANARY"
    LINEAR = "LINEAR"


class TrafficType(str):
    PHASES = "PHASES"


class TrainingInputMode(str):
    Pipe = "Pipe"
    File = "File"
    FastFile = "FastFile"


class TrainingInstanceType(str):
    ml_m4_xlarge = "ml.m4.xlarge"
    ml_m4_2xlarge = "ml.m4.2xlarge"
    ml_m4_4xlarge = "ml.m4.4xlarge"
    ml_m4_10xlarge = "ml.m4.10xlarge"
    ml_m4_16xlarge = "ml.m4.16xlarge"
    ml_g4dn_xlarge = "ml.g4dn.xlarge"
    ml_g4dn_2xlarge = "ml.g4dn.2xlarge"
    ml_g4dn_4xlarge = "ml.g4dn.4xlarge"
    ml_g4dn_8xlarge = "ml.g4dn.8xlarge"
    ml_g4dn_12xlarge = "ml.g4dn.12xlarge"
    ml_g4dn_16xlarge = "ml.g4dn.16xlarge"
    ml_m5_large = "ml.m5.large"
    ml_m5_xlarge = "ml.m5.xlarge"
    ml_m5_2xlarge = "ml.m5.2xlarge"
    ml_m5_4xlarge = "ml.m5.4xlarge"
    ml_m5_12xlarge = "ml.m5.12xlarge"
    ml_m5_24xlarge = "ml.m5.24xlarge"
    ml_c4_xlarge = "ml.c4.xlarge"
    ml_c4_2xlarge = "ml.c4.2xlarge"
    ml_c4_4xlarge = "ml.c4.4xlarge"
    ml_c4_8xlarge = "ml.c4.8xlarge"
    ml_p2_xlarge = "ml.p2.xlarge"
    ml_p2_8xlarge = "ml.p2.8xlarge"
    ml_p2_16xlarge = "ml.p2.16xlarge"
    ml_p3_2xlarge = "ml.p3.2xlarge"
    ml_p3_8xlarge = "ml.p3.8xlarge"
    ml_p3_16xlarge = "ml.p3.16xlarge"
    ml_p3dn_24xlarge = "ml.p3dn.24xlarge"
    ml_p4d_24xlarge = "ml.p4d.24xlarge"
    ml_c5_xlarge = "ml.c5.xlarge"
    ml_c5_2xlarge = "ml.c5.2xlarge"
    ml_c5_4xlarge = "ml.c5.4xlarge"
    ml_c5_9xlarge = "ml.c5.9xlarge"
    ml_c5_18xlarge = "ml.c5.18xlarge"
    ml_c5n_xlarge = "ml.c5n.xlarge"
    ml_c5n_2xlarge = "ml.c5n.2xlarge"
    ml_c5n_4xlarge = "ml.c5n.4xlarge"
    ml_c5n_9xlarge = "ml.c5n.9xlarge"
    ml_c5n_18xlarge = "ml.c5n.18xlarge"
    ml_g5_xlarge = "ml.g5.xlarge"
    ml_g5_2xlarge = "ml.g5.2xlarge"
    ml_g5_4xlarge = "ml.g5.4xlarge"
    ml_g5_8xlarge = "ml.g5.8xlarge"
    ml_g5_16xlarge = "ml.g5.16xlarge"
    ml_g5_12xlarge = "ml.g5.12xlarge"
    ml_g5_24xlarge = "ml.g5.24xlarge"
    ml_g5_48xlarge = "ml.g5.48xlarge"


class TrainingJobEarlyStoppingType(str):
    Off = "Off"
    Auto = "Auto"


class TrainingJobSortByOptions(str):
    Name = "Name"
    CreationTime = "CreationTime"
    Status = "Status"
    FinalObjectiveMetricValue = "FinalObjectiveMetricValue"


class TrainingJobStatus(str):
    InProgress = "InProgress"
    Completed = "Completed"
    Failed = "Failed"
    Stopping = "Stopping"
    Stopped = "Stopped"


class TransformInstanceType(str):
    ml_m4_xlarge = "ml.m4.xlarge"
    ml_m4_2xlarge = "ml.m4.2xlarge"
    ml_m4_4xlarge = "ml.m4.4xlarge"
    ml_m4_10xlarge = "ml.m4.10xlarge"
    ml_m4_16xlarge = "ml.m4.16xlarge"
    ml_c4_xlarge = "ml.c4.xlarge"
    ml_c4_2xlarge = "ml.c4.2xlarge"
    ml_c4_4xlarge = "ml.c4.4xlarge"
    ml_c4_8xlarge = "ml.c4.8xlarge"
    ml_p2_xlarge = "ml.p2.xlarge"
    ml_p2_8xlarge = "ml.p2.8xlarge"
    ml_p2_16xlarge = "ml.p2.16xlarge"
    ml_p3_2xlarge = "ml.p3.2xlarge"
    ml_p3_8xlarge = "ml.p3.8xlarge"
    ml_p3_16xlarge = "ml.p3.16xlarge"
    ml_c5_xlarge = "ml.c5.xlarge"
    ml_c5_2xlarge = "ml.c5.2xlarge"
    ml_c5_4xlarge = "ml.c5.4xlarge"
    ml_c5_9xlarge = "ml.c5.9xlarge"
    ml_c5_18xlarge = "ml.c5.18xlarge"
    ml_m5_large = "ml.m5.large"
    ml_m5_xlarge = "ml.m5.xlarge"
    ml_m5_2xlarge = "ml.m5.2xlarge"
    ml_m5_4xlarge = "ml.m5.4xlarge"
    ml_m5_12xlarge = "ml.m5.12xlarge"
    ml_m5_24xlarge = "ml.m5.24xlarge"
    ml_g4dn_xlarge = "ml.g4dn.xlarge"
    ml_g4dn_2xlarge = "ml.g4dn.2xlarge"
    ml_g4dn_4xlarge = "ml.g4dn.4xlarge"
    ml_g4dn_8xlarge = "ml.g4dn.8xlarge"
    ml_g4dn_12xlarge = "ml.g4dn.12xlarge"
    ml_g4dn_16xlarge = "ml.g4dn.16xlarge"


class TransformJobStatus(str):
    InProgress = "InProgress"
    Completed = "Completed"
    Failed = "Failed"
    Stopping = "Stopping"
    Stopped = "Stopped"


class TrialComponentPrimaryStatus(str):
    InProgress = "InProgress"
    Completed = "Completed"
    Failed = "Failed"
    Stopping = "Stopping"
    Stopped = "Stopped"


class UserProfileSortKey(str):
    CreationTime = "CreationTime"
    LastModifiedTime = "LastModifiedTime"


class UserProfileStatus(str):
    Deleting = "Deleting"
    Failed = "Failed"
    InService = "InService"
    Pending = "Pending"
    Updating = "Updating"
    Update_Failed = "Update_Failed"
    Delete_Failed = "Delete_Failed"


class VariantPropertyType(str):
    DesiredInstanceCount = "DesiredInstanceCount"
    DesiredWeight = "DesiredWeight"
    DataCaptureConfig = "DataCaptureConfig"


class VariantStatus(str):
    Creating = "Creating"
    Updating = "Updating"
    Deleting = "Deleting"
    ActivatingTraffic = "ActivatingTraffic"
    Baking = "Baking"


class ConflictException(ServiceException):
    """There was a conflict when you attempted to modify a SageMaker entity
    such as an ``Experiment`` or ``Artifact``.
    """

    Message: Optional[FailureReason]


class ResourceInUse(ServiceException):
    """Resource being accessed is in use."""

    Message: Optional[FailureReason]


class ResourceLimitExceeded(ServiceException):
    """You have exceeded an SageMaker resource limit. For example, you might
    have too many training jobs created.
    """

    Message: Optional[FailureReason]


class ResourceNotFound(ServiceException):
    """Resource being access is not found."""

    Message: Optional[FailureReason]


class ActionSource(TypedDict, total=False):
    """A structure describing the source of an action."""

    SourceUri: String2048
    SourceType: Optional[String256]
    SourceId: Optional[String256]


Timestamp = datetime


class ActionSummary(TypedDict, total=False):
    """Lists the properties of an *action*. An action represents an action or
    activity. Some examples are a workflow step and a model deployment.
    Generally, an action involves at least one input artifact or output
    artifact.
    """

    ActionArn: Optional[ActionArn]
    ActionName: Optional[ExperimentEntityName]
    Source: Optional[ActionSource]
    ActionType: Optional[String64]
    Status: Optional[ActionStatus]
    CreationTime: Optional[Timestamp]
    LastModifiedTime: Optional[Timestamp]


ActionSummaries = List[ActionSummary]


class AddAssociationRequest(ServiceRequest):
    SourceArn: AssociationEntityArn
    DestinationArn: AssociationEntityArn
    AssociationType: Optional[AssociationEdgeType]


class AddAssociationResponse(TypedDict, total=False):
    SourceArn: Optional[AssociationEntityArn]
    DestinationArn: Optional[AssociationEntityArn]


class Tag(TypedDict, total=False):
    """A tag object that consists of a key and an optional value, used to
    manage metadata for SageMaker Amazon Web Services resources.

    You can add tags to notebook instances, training jobs, hyperparameter
    tuning jobs, batch transform jobs, models, labeling jobs, work teams,
    endpoint configurations, and endpoints. For more information on adding
    tags to SageMaker resources, see AddTags.

    For more information on adding metadata to your Amazon Web Services
    resources with tagging, see `Tagging Amazon Web Services
    resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`__.
    For advice on best practices for managing Amazon Web Services resources
    with tagging, see `Tagging Best Practices: Implement an Effective Amazon
    Web Services Resource Tagging
    Strategy <https://d1.awsstatic.com/whitepapers/aws-tagging-best-practices.pdf>`__.
    """

    Key: TagKey
    Value: TagValue


TagList = List[Tag]


class AddTagsInput(ServiceRequest):
    ResourceArn: ResourceArn
    Tags: TagList


class AddTagsOutput(TypedDict, total=False):
    Tags: Optional[TagList]


AdditionalCodeRepositoryNamesOrUrls = List[CodeRepositoryNameOrUrl]
ResponseMIMETypes = List[ResponseMIMEType]
ContentTypes = List[ContentType]
RealtimeInferenceInstanceTypes = List[ProductionVariantInstanceType]
TransformInstanceTypes = List[TransformInstanceType]


class ModelInput(TypedDict, total=False):
    """Input object for the model."""

    DataInputConfig: DataInputConfig


EnvironmentMap = Dict[EnvironmentKey, EnvironmentValue]


class ModelPackageContainerDefinition(TypedDict, total=False):
    """Describes the Docker container for the model package."""

    ContainerHostname: Optional[ContainerHostname]
    Image: ContainerImage
    ImageDigest: Optional[ImageDigest]
    ModelDataUrl: Optional[Url]
    ProductId: Optional[ProductId]
    Environment: Optional[EnvironmentMap]
    ModelInput: Optional[ModelInput]
    Framework: Optional[String]
    FrameworkVersion: Optional[FrameworkVersion]
    NearestModelName: Optional[String]


ModelPackageContainerDefinitionList = List[ModelPackageContainerDefinition]


class AdditionalInferenceSpecificationDefinition(TypedDict, total=False):
    """A structure of additional Inference Specification. Additional Inference
    Specification specifies details about inference jobs that can be run
    with models based on this model package
    """

    Name: EntityName
    Description: Optional[EntityDescription]
    Containers: ModelPackageContainerDefinitionList
    SupportedTransformInstanceTypes: Optional[TransformInstanceTypes]
    SupportedRealtimeInferenceInstanceTypes: Optional[RealtimeInferenceInstanceTypes]
    SupportedContentTypes: Optional[ContentTypes]
    SupportedResponseMIMETypes: Optional[ResponseMIMETypes]


AdditionalInferenceSpecifications = List[AdditionalInferenceSpecificationDefinition]
Long = int


class AgentVersion(TypedDict, total=False):
    """Edge Manager agent version."""

    Version: EdgeVersion
    AgentCount: Long


AgentVersions = List[AgentVersion]


class Alarm(TypedDict, total=False):
    """An Amazon CloudWatch alarm configured to monitor metrics on an endpoint."""

    AlarmName: Optional[AlarmName]


AlarmList = List[Alarm]


class MetricDefinition(TypedDict, total=False):
    """Specifies a metric that the training algorithm writes to ``stderr`` or
    ``stdout``. SageMakerhyperparameter tuning captures all defined metrics.
    You specify one metric that a hyperparameter tuning job uses as its
    objective metric to choose the best training job.
    """

    Name: MetricName
    Regex: MetricRegex


MetricDefinitionList = List[MetricDefinition]


class AlgorithmSpecification(TypedDict, total=False):
    """Specifies the training algorithm to use in a CreateTrainingJob request.

    For more information about algorithms provided by SageMaker, see
    `Algorithms <https://docs.aws.amazon.com/sagemaker/latest/dg/algos.html>`__.
    For information about using your own algorithms, see `Using Your Own
    Algorithms with Amazon
    SageMaker <https://docs.aws.amazon.com/sagemaker/latest/dg/your-algorithms.html>`__.
    """

    TrainingImage: Optional[AlgorithmImage]
    AlgorithmName: Optional[ArnOrName]
    TrainingInputMode: TrainingInputMode
    MetricDefinitions: Optional[MetricDefinitionList]
    EnableSageMakerMetricsTimeSeries: Optional[Boolean]


class AlgorithmStatusItem(TypedDict, total=False):
    """Represents the overall status of an algorithm."""

    Name: EntityName
    Status: DetailedAlgorithmStatus
    FailureReason: Optional[String]


AlgorithmStatusItemList = List[AlgorithmStatusItem]


class AlgorithmStatusDetails(TypedDict, total=False):
    """Specifies the validation and image scan statuses of the algorithm."""

    ValidationStatuses: Optional[AlgorithmStatusItemList]
    ImageScanStatuses: Optional[AlgorithmStatusItemList]


CreationTime = datetime


class AlgorithmSummary(TypedDict, total=False):
    """Provides summary information about an algorithm."""

    AlgorithmName: EntityName
    AlgorithmArn: AlgorithmArn
    AlgorithmDescription: Optional[EntityDescription]
    CreationTime: CreationTime
    AlgorithmStatus: AlgorithmStatus


AlgorithmSummaryList = List[AlgorithmSummary]


class TransformResources(TypedDict, total=False):
    """Describes the resources, including ML instance types and ML instance
    count, to use for transform job.
    """

    InstanceType: TransformInstanceType
    InstanceCount: TransformInstanceCount
    VolumeKmsKeyId: Optional[KmsKeyId]


class TransformOutput(TypedDict, total=False):
    """Describes the results of a transform job."""

    S3OutputPath: S3Uri
    Accept: Optional[Accept]
    AssembleWith: Optional[AssemblyType]
    KmsKeyId: Optional[KmsKeyId]


class TransformS3DataSource(TypedDict, total=False):
    """Describes the S3 data source."""

    S3DataType: S3DataType
    S3Uri: S3Uri


class TransformDataSource(TypedDict, total=False):
    """Describes the location of the channel data."""

    S3DataSource: TransformS3DataSource


class TransformInput(TypedDict, total=False):
    """Describes the input source of a transform job and the way the transform
    job consumes it.
    """

    DataSource: TransformDataSource
    ContentType: Optional[ContentType]
    CompressionType: Optional[CompressionType]
    SplitType: Optional[SplitType]


TransformEnvironmentMap = Dict[TransformEnvironmentKey, TransformEnvironmentValue]


class TransformJobDefinition(TypedDict, total=False):
    """Defines the input needed to run a transform job using the inference
    specification specified in the algorithm.
    """

    MaxConcurrentTransforms: Optional[MaxConcurrentTransforms]
    MaxPayloadInMB: Optional[MaxPayloadInMB]
    BatchStrategy: Optional[BatchStrategy]
    Environment: Optional[TransformEnvironmentMap]
    TransformInput: TransformInput
    TransformOutput: TransformOutput
    TransformResources: TransformResources


class StoppingCondition(TypedDict, total=False):
    """Specifies a limit to how long a model training job or model compilation
    job can run. It also specifies how long a managed spot training job has
    to complete. When the job reaches the time limit, SageMaker ends the
    training or compilation job. Use this API to cap model training costs.

    To stop a training job, SageMaker sends the algorithm the ``SIGTERM``
    signal, which delays job termination for 120 seconds. Algorithms can use
    this 120-second window to save the model artifacts, so the results of
    training are not lost.

    The training algorithms provided by SageMaker automatically save the
    intermediate results of a model training job when possible. This attempt
    to save artifacts is only a best effort case as model might not be in a
    state from which it can be saved. For example, if training has just
    started, the model might not be ready to save. When saved, this
    intermediate data is a valid model artifact. You can use it to create a
    model with ``CreateModel``.

    The Neural Topic Model (NTM) currently does not support saving
    intermediate model artifacts. When training NTMs, make sure that the
    maximum runtime is sufficient for the training job to complete.
    """

    MaxRuntimeInSeconds: Optional[MaxRuntimeInSeconds]
    MaxWaitTimeInSeconds: Optional[MaxWaitTimeInSeconds]


class ResourceConfig(TypedDict, total=False):
    """Describes the resources, including ML compute instances and ML storage
    volumes, to use for model training.
    """

    InstanceType: TrainingInstanceType
    InstanceCount: TrainingInstanceCount
    VolumeSizeInGB: VolumeSizeInGB
    VolumeKmsKeyId: Optional[KmsKeyId]


class OutputDataConfig(TypedDict, total=False):
    """Provides information about how to store model training results (model
    artifacts).
    """

    KmsKeyId: Optional[KmsKeyId]
    S3OutputPath: S3Uri


Seed = int


class ShuffleConfig(TypedDict, total=False):
    """A configuration for a shuffle option for input data in a channel. If you
    use ``S3Prefix`` for ``S3DataType``, the results of the S3 key prefix
    matches are shuffled. If you use ``ManifestFile``, the order of the S3
    object references in the ``ManifestFile`` is shuffled. If you use
    ``AugmentedManifestFile``, the order of the JSON lines in the
    ``AugmentedManifestFile`` is shuffled. The shuffling order is determined
    using the ``Seed`` value.

    For Pipe input mode, when ``ShuffleConfig`` is specified shuffling is
    done at the start of every epoch. With large datasets, this ensures that
    the order of the training data is different for each epoch, and it helps
    reduce bias and possible overfitting. In a multi-node training job when
    ``ShuffleConfig`` is combined with ``S3DataDistributionType`` of
    ``ShardedByS3Key``, the data is shuffled across nodes so that the
    content sent to a particular node on the first epoch might be sent to a
    different node on the second epoch.
    """

    Seed: Seed


class FileSystemDataSource(TypedDict, total=False):
    """Specifies a file system data source for a channel."""

    FileSystemId: FileSystemId
    FileSystemAccessMode: FileSystemAccessMode
    FileSystemType: FileSystemType
    DirectoryPath: DirectoryPath


AttributeNames = List[AttributeName]


class S3DataSource(TypedDict, total=False):
    """Describes the S3 data source."""

    S3DataType: S3DataType
    S3Uri: S3Uri
    S3DataDistributionType: Optional[S3DataDistribution]
    AttributeNames: Optional[AttributeNames]


class DataSource(TypedDict, total=False):
    """Describes the location of the channel data."""

    S3DataSource: Optional[S3DataSource]
    FileSystemDataSource: Optional[FileSystemDataSource]


class Channel(TypedDict, total=False):
    """A channel is a named input source that training algorithms can consume."""

    ChannelName: ChannelName
    DataSource: DataSource
    ContentType: Optional[ContentType]
    CompressionType: Optional[CompressionType]
    RecordWrapperType: Optional[RecordWrapper]
    InputMode: Optional[TrainingInputMode]
    ShuffleConfig: Optional[ShuffleConfig]


InputDataConfig = List[Channel]
HyperParameters = Dict[HyperParameterKey, HyperParameterValue]


class TrainingJobDefinition(TypedDict, total=False):
    """Defines the input needed to run a training job using the algorithm."""

    TrainingInputMode: TrainingInputMode
    HyperParameters: Optional[HyperParameters]
    InputDataConfig: InputDataConfig
    OutputDataConfig: OutputDataConfig
    ResourceConfig: ResourceConfig
    StoppingCondition: StoppingCondition


class AlgorithmValidationProfile(TypedDict, total=False):
    """Defines a training job and a batch transform job that SageMaker runs to
    validate your algorithm.

    The data provided in the validation profile is made available to your
    buyers on Amazon Web Services Marketplace.
    """

    ProfileName: EntityName
    TrainingJobDefinition: TrainingJobDefinition
    TransformJobDefinition: Optional[TransformJobDefinition]


AlgorithmValidationProfiles = List[AlgorithmValidationProfile]


class AlgorithmValidationSpecification(TypedDict, total=False):
    """Specifies configurations for one or more training jobs that SageMaker
    runs to test the algorithm.
    """

    ValidationRole: RoleArn
    ValidationProfiles: AlgorithmValidationProfiles


class AnnotationConsolidationConfig(TypedDict, total=False):
    """Configures how labels are consolidated across human workers and
    processes output data.
    """

    AnnotationConsolidationLambdaArn: LambdaFunctionArn


class AppDetails(TypedDict, total=False):
    """Details about an Amazon SageMaker app."""

    DomainId: Optional[DomainId]
    UserProfileName: Optional[UserProfileName]
    AppType: Optional[AppType]
    AppName: Optional[AppName]
    Status: Optional[AppStatus]
    CreationTime: Optional[CreationTime]


class FileSystemConfig(TypedDict, total=False):
    """The Amazon Elastic File System (EFS) storage configuration for a
    SageMaker image.
    """

    MountPath: Optional[MountPath]
    DefaultUid: Optional[DefaultUid]
    DefaultGid: Optional[DefaultGid]


class KernelSpec(TypedDict, total=False):
    """The specification of a Jupyter kernel."""

    Name: KernelName
    DisplayName: Optional[KernelDisplayName]


KernelSpecs = List[KernelSpec]


class KernelGatewayImageConfig(TypedDict, total=False):
    """The configuration for the file system and kernels in a SageMaker image
    running as a KernelGateway app.
    """

    KernelSpecs: KernelSpecs
    FileSystemConfig: Optional[FileSystemConfig]


class AppImageConfigDetails(TypedDict, total=False):
    """The configuration for running a SageMaker image as a KernelGateway app."""

    AppImageConfigArn: Optional[AppImageConfigArn]
    AppImageConfigName: Optional[AppImageConfigName]
    CreationTime: Optional[Timestamp]
    LastModifiedTime: Optional[Timestamp]
    KernelGatewayImageConfig: Optional[KernelGatewayImageConfig]


AppImageConfigList = List[AppImageConfigDetails]
AppList = List[AppDetails]
ContainerArguments = List[ContainerArgument]
ContainerEntrypoint = List[ContainerEntrypointString]


class AppSpecification(TypedDict, total=False):
    """Configuration to run a processing job in a specified container image."""

    ImageUri: ImageUri
    ContainerEntrypoint: Optional[ContainerEntrypoint]
    ContainerArguments: Optional[ContainerArguments]


class ArtifactSourceType(TypedDict, total=False):
    """The ID and ID type of an artifact source."""

    SourceIdType: ArtifactSourceIdType
    Value: String256


ArtifactSourceTypes = List[ArtifactSourceType]


class ArtifactSource(TypedDict, total=False):
    """A structure describing the source of an artifact."""

    SourceUri: String2048
    SourceTypes: Optional[ArtifactSourceTypes]


class ArtifactSummary(TypedDict, total=False):
    """Lists a summary of the properties of an artifact. An artifact represents
    a URI addressable object or data. Some examples are a dataset and a
    model.
    """

    ArtifactArn: Optional[ArtifactArn]
    ArtifactName: Optional[ExperimentEntityName]
    Source: Optional[ArtifactSource]
    ArtifactType: Optional[String256]
    CreationTime: Optional[Timestamp]
    LastModifiedTime: Optional[Timestamp]


ArtifactSummaries = List[ArtifactSummary]


class AssociateTrialComponentRequest(ServiceRequest):
    TrialComponentName: ExperimentEntityName
    TrialName: ExperimentEntityName


class AssociateTrialComponentResponse(TypedDict, total=False):
    TrialComponentArn: Optional[TrialComponentArn]
    TrialArn: Optional[TrialArn]


class UserContext(TypedDict, total=False):
    """Information about the user who created or modified an experiment, trial,
    trial component, lineage group, or project.
    """

    UserProfileArn: Optional[String]
    UserProfileName: Optional[String]
    DomainId: Optional[String]


class AssociationSummary(TypedDict, total=False):
    """Lists a summary of the properties of an association. An association is
    an entity that links other lineage or experiment entities. An example
    would be an association between a training job and a model.
    """

    SourceArn: Optional[AssociationEntityArn]
    DestinationArn: Optional[AssociationEntityArn]
    SourceType: Optional[String256]
    DestinationType: Optional[String256]
    AssociationType: Optional[AssociationEdgeType]
    SourceName: Optional[ExperimentEntityName]
    DestinationName: Optional[ExperimentEntityName]
    CreationTime: Optional[Timestamp]
    CreatedBy: Optional[UserContext]


AssociationSummaries = List[AssociationSummary]


class AsyncInferenceClientConfig(TypedDict, total=False):
    """Configures the behavior of the client used by SageMaker to interact with
    the model container during asynchronous inference.
    """

    MaxConcurrentInvocationsPerInstance: Optional[MaxConcurrentInvocationsPerInstance]


class AsyncInferenceNotificationConfig(TypedDict, total=False):
    """Specifies the configuration for notifications of inference results for
    asynchronous inference.
    """

    SuccessTopic: Optional[SnsTopicArn]
    ErrorTopic: Optional[SnsTopicArn]


class AsyncInferenceOutputConfig(TypedDict, total=False):
    """Specifies the configuration for asynchronous inference invocation
    outputs.
    """

    KmsKeyId: Optional[KmsKeyId]
    S3OutputPath: DestinationS3Uri
    NotificationConfig: Optional[AsyncInferenceNotificationConfig]


class AsyncInferenceConfig(TypedDict, total=False):
    """Specifies configuration for how an endpoint performs asynchronous
    inference.
    """

    ClientConfig: Optional[AsyncInferenceClientConfig]
    OutputConfig: AsyncInferenceOutputConfig


class AthenaDatasetDefinition(TypedDict, total=False):
    """Configuration for Athena Dataset Definition input."""

    Catalog: AthenaCatalog
    Database: AthenaDatabase
    QueryString: AthenaQueryString
    WorkGroup: Optional[AthenaWorkGroup]
    OutputS3Uri: S3Uri
    KmsKeyId: Optional[KmsKeyId]
    OutputFormat: AthenaResultFormat
    OutputCompression: Optional[AthenaResultCompressionType]


class MetricDatum(TypedDict, total=False):
    """Information about the metric for a candidate produced by an AutoML job."""

    MetricName: Optional[AutoMLMetricEnum]
    Value: Optional[Float]
    Set: Optional[MetricSetSource]
    StandardMetricName: Optional[AutoMLMetricExtendedEnum]


MetricDataList = List[MetricDatum]


class CandidateArtifactLocations(TypedDict, total=False):
    """The location of artifacts for an AutoML candidate job."""

    Explainability: ExplainabilityLocation
    ModelInsights: Optional[ModelInsightsLocation]


class CandidateProperties(TypedDict, total=False):
    """The properties of an AutoML candidate job."""

    CandidateArtifactLocations: Optional[CandidateArtifactLocations]
    CandidateMetrics: Optional[MetricDataList]


class AutoMLContainerDefinition(TypedDict, total=False):
    """A list of container definitions that describe the different containers
    that make up an AutoML candidate. For more information, see .
    """

    Image: ContainerImage
    ModelDataUrl: Url
    Environment: Optional[EnvironmentMap]


AutoMLContainerDefinitions = List[AutoMLContainerDefinition]


class AutoMLCandidateStep(TypedDict, total=False):
    """Information about the steps for a candidate and what step it is working
    on.
    """

    CandidateStepType: CandidateStepType
    CandidateStepArn: CandidateStepArn
    CandidateStepName: CandidateStepName


CandidateSteps = List[AutoMLCandidateStep]


class FinalAutoMLJobObjectiveMetric(TypedDict, total=False):
    """The best candidate result from an AutoML training job."""

    Type: Optional[AutoMLJobObjectiveType]
    MetricName: AutoMLMetricEnum
    Value: MetricValue


class AutoMLCandidate(TypedDict, total=False):
    """Information about a candidate produced by an AutoML training job,
    including its status, steps, and other properties.
    """

    CandidateName: CandidateName
    FinalAutoMLJobObjectiveMetric: Optional[FinalAutoMLJobObjectiveMetric]
    ObjectiveStatus: ObjectiveStatus
    CandidateSteps: CandidateSteps
    CandidateStatus: CandidateStatus
    InferenceContainers: Optional[AutoMLContainerDefinitions]
    CreationTime: Timestamp
    EndTime: Optional[Timestamp]
    LastModifiedTime: Timestamp
    FailureReason: Optional[AutoMLFailureReason]
    CandidateProperties: Optional[CandidateProperties]


AutoMLCandidates = List[AutoMLCandidate]


class AutoMLS3DataSource(TypedDict, total=False):
    """The Amazon S3 data source."""

    S3DataType: AutoMLS3DataType
    S3Uri: S3Uri


class AutoMLDataSource(TypedDict, total=False):
    """The data source for the Autopilot job."""

    S3DataSource: AutoMLS3DataSource


class AutoMLChannel(TypedDict, total=False):
    """A channel is a named input source that training algorithms can consume.
    The validation dataset size is limited to less than 2 GB. The training
    dataset size must be less than 100 GB. For more information, see .

    A validation dataset must contain the same headers as the training
    dataset.
    """

    DataSource: AutoMLDataSource
    CompressionType: Optional[CompressionType]
    TargetAttributeName: TargetAttributeName
    ContentType: Optional[ContentType]
    ChannelType: Optional[AutoMLChannelType]


class AutoMLDataSplitConfig(TypedDict, total=False):
    """This structure specifies how to split the data into train and test
    datasets. The validation and training datasets must contain the same
    headers. The validation dataset must be less than 2 GB in size.
    """

    ValidationFraction: Optional[ValidationFraction]


AutoMLInputDataConfig = List[AutoMLChannel]


class AutoMLJobArtifacts(TypedDict, total=False):
    """The artifacts that are generated during an AutoML job."""

    CandidateDefinitionNotebookLocation: Optional[CandidateDefinitionNotebookLocation]
    DataExplorationNotebookLocation: Optional[DataExplorationNotebookLocation]


class AutoMLJobCompletionCriteria(TypedDict, total=False):
    """How long a job is allowed to run, or how many candidates a job is
    allowed to generate.
    """

    MaxCandidates: Optional[MaxCandidates]
    MaxRuntimePerTrainingJobInSeconds: Optional[MaxRuntimePerTrainingJobInSeconds]
    MaxAutoMLJobRuntimeInSeconds: Optional[MaxAutoMLJobRuntimeInSeconds]


Subnets = List[SubnetId]
VpcSecurityGroupIds = List[SecurityGroupId]


class VpcConfig(TypedDict, total=False):
    """Specifies a VPC that your training jobs and hosted models have access
    to. Control access to and from your training and model containers by
    configuring the VPC. For more information, see `Protect Endpoints by
    Using an Amazon Virtual Private
    Cloud <https://docs.aws.amazon.com/sagemaker/latest/dg/host-vpc.html>`__
    and `Protect Training Jobs by Using an Amazon Virtual Private
    Cloud <https://docs.aws.amazon.com/sagemaker/latest/dg/train-vpc.html>`__.
    """

    SecurityGroupIds: VpcSecurityGroupIds
    Subnets: Subnets


class AutoMLSecurityConfig(TypedDict, total=False):
    """Security options."""

    VolumeKmsKeyId: Optional[KmsKeyId]
    EnableInterContainerTrafficEncryption: Optional[Boolean]
    VpcConfig: Optional[VpcConfig]


class AutoMLJobConfig(TypedDict, total=False):
    """A collection of settings used for an AutoML job."""

    CompletionCriteria: Optional[AutoMLJobCompletionCriteria]
    SecurityConfig: Optional[AutoMLSecurityConfig]
    DataSplitConfig: Optional[AutoMLDataSplitConfig]


class AutoMLJobObjective(TypedDict, total=False):
    """Specifies a metric to minimize or maximize as the objective of a job."""

    MetricName: AutoMLMetricEnum


class AutoMLPartialFailureReason(TypedDict, total=False):
    """The reason for a partial failure of an AutoML job."""

    PartialFailureMessage: Optional[AutoMLFailureReason]


AutoMLPartialFailureReasons = List[AutoMLPartialFailureReason]


class AutoMLJobSummary(TypedDict, total=False):
    """Provides a summary about an AutoML job."""

    AutoMLJobName: AutoMLJobName
    AutoMLJobArn: AutoMLJobArn
    AutoMLJobStatus: AutoMLJobStatus
    AutoMLJobSecondaryStatus: AutoMLJobSecondaryStatus
    CreationTime: Timestamp
    EndTime: Optional[Timestamp]
    LastModifiedTime: Timestamp
    FailureReason: Optional[AutoMLFailureReason]
    PartialFailureReasons: Optional[AutoMLPartialFailureReasons]


AutoMLJobSummaries = List[AutoMLJobSummary]


class AutoMLOutputDataConfig(TypedDict, total=False):
    """The output data configuration."""

    KmsKeyId: Optional[KmsKeyId]
    S3OutputPath: S3Uri


class AutoRollbackConfig(TypedDict, total=False):
    """Automatic rollback configuration for handling endpoint deployment
    failures and recovery.
    """

    Alarms: Optional[AlarmList]


class BatchDescribeModelPackageError(TypedDict, total=False):
    """The error code and error description associated with the resource."""

    ErrorCode: String
    ErrorResponse: String


BatchDescribeModelPackageErrorMap = Dict[ModelPackageArn, BatchDescribeModelPackageError]
ModelPackageArnList = List[ModelPackageArn]


class BatchDescribeModelPackageInput(ServiceRequest):
    ModelPackageArnList: ModelPackageArnList


class InferenceSpecification(TypedDict, total=False):
    """Defines how to perform inference generation after a training job is run."""

    Containers: ModelPackageContainerDefinitionList
    SupportedTransformInstanceTypes: Optional[TransformInstanceTypes]
    SupportedRealtimeInferenceInstanceTypes: Optional[RealtimeInferenceInstanceTypes]
    SupportedContentTypes: ContentTypes
    SupportedResponseMIMETypes: ResponseMIMETypes


class BatchDescribeModelPackageSummary(TypedDict, total=False):
    """Provides summary information about the model package."""

    ModelPackageGroupName: EntityName
    ModelPackageVersion: Optional[ModelPackageVersion]
    ModelPackageArn: ModelPackageArn
    ModelPackageDescription: Optional[EntityDescription]
    CreationTime: CreationTime
    InferenceSpecification: InferenceSpecification
    ModelPackageStatus: ModelPackageStatus
    ModelApprovalStatus: Optional[ModelApprovalStatus]


ModelPackageSummaries = Dict[ModelPackageArn, BatchDescribeModelPackageSummary]


class BatchDescribeModelPackageOutput(TypedDict, total=False):
    ModelPackageSummaries: Optional[ModelPackageSummaries]
    BatchDescribeModelPackageErrorMap: Optional[BatchDescribeModelPackageErrorMap]


class MetricsSource(TypedDict, total=False):
    ContentType: ContentType
    ContentDigest: Optional[ContentDigest]
    S3Uri: S3Uri


class Bias(TypedDict, total=False):
    """Contains bias metrics for a model."""

    Report: Optional[MetricsSource]
    PreTrainingReport: Optional[MetricsSource]
    PostTrainingReport: Optional[MetricsSource]


class CapacitySize(TypedDict, total=False):
    """Specifies the endpoint capacity to activate for production."""

    Type: CapacitySizeType
    Value: CapacitySizeValue


class TrafficRoutingConfig(TypedDict, total=False):
    """Defines the traffic routing strategy during an endpoint deployment to
    shift traffic from the old fleet to the new fleet.
    """

    Type: TrafficRoutingConfigType
    WaitIntervalInSeconds: WaitIntervalInSeconds
    CanarySize: Optional[CapacitySize]
    LinearStepSize: Optional[CapacitySize]


class BlueGreenUpdatePolicy(TypedDict, total=False):
    """Update policy for a blue/green deployment. If this update policy is
    specified, SageMaker creates a new fleet during the deployment while
    maintaining the old fleet. SageMaker flips traffic to the new fleet
    according to the specified traffic routing configuration. Only one
    update policy should be used in the deployment configuration. If no
    update policy is specified, SageMaker uses a blue/green deployment
    strategy with all at once traffic shifting by default.
    """

    TrafficRoutingConfiguration: TrafficRoutingConfig
    TerminationWaitInSeconds: Optional[TerminationWaitInSeconds]
    MaximumExecutionTimeoutInSeconds: Optional[MaximumExecutionTimeoutInSeconds]


class CacheHitResult(TypedDict, total=False):
    """Details on the cache hit of a pipeline execution step."""

    SourcePipelineExecutionArn: Optional[PipelineExecutionArn]


class OutputParameter(TypedDict, total=False):
    """An output parameter of a pipeline step."""

    Name: String256
    Value: String1024


OutputParameterList = List[OutputParameter]


class CallbackStepMetadata(TypedDict, total=False):
    """Metadata about a callback step."""

    CallbackToken: Optional[CallbackToken]
    SqsQueueUrl: Optional[String256]
    OutputParameters: Optional[OutputParameterList]


JsonContentTypes = List[JsonContentType]
CsvContentTypes = List[CsvContentType]


class CaptureContentTypeHeader(TypedDict, total=False):
    CsvContentTypes: Optional[CsvContentTypes]
    JsonContentTypes: Optional[JsonContentTypes]


class CaptureOption(TypedDict, total=False):
    CaptureMode: CaptureMode


CaptureOptionList = List[CaptureOption]
CategoricalParameterRangeValues = List[String128]


class CategoricalParameter(TypedDict, total=False):
    """Environment parameters you want to benchmark your load test against."""

    Name: String64
    Value: CategoricalParameterRangeValues


ParameterValues = List[ParameterValue]


class CategoricalParameterRange(TypedDict, total=False):
    """A list of categorical hyperparameters to tune."""

    Name: ParameterKey
    Values: ParameterValues


class CategoricalParameterRangeSpecification(TypedDict, total=False):
    """Defines the possible values for a categorical hyperparameter."""

    Values: ParameterValues


CategoricalParameterRanges = List[CategoricalParameterRange]
CategoricalParameters = List[CategoricalParameter]
InputModes = List[TrainingInputMode]
CompressionTypes = List[CompressionType]


class ChannelSpecification(TypedDict, total=False):
    """Defines a named input source, called a channel, to be used by an
    algorithm.
    """

    Name: ChannelName
    Description: Optional[EntityDescription]
    IsRequired: Optional[Boolean]
    SupportedContentTypes: ContentTypes
    SupportedCompressionTypes: Optional[CompressionTypes]
    SupportedInputModes: InputModes


ChannelSpecifications = List[ChannelSpecification]


class CheckpointConfig(TypedDict, total=False):
    """Contains information about the output location for managed spot training
    checkpoint data.
    """

    S3Uri: S3Uri
    LocalPath: Optional[DirectoryPath]


Cidrs = List[Cidr]


class ClarifyCheckStepMetadata(TypedDict, total=False):
    """The container for the metadata for the ClarifyCheck step. For more
    information, see the topic on `ClarifyCheck
    step <https://docs.aws.amazon.com/sagemaker/latest/dg/build-and-manage-steps.html#step-type-clarify-check>`__
    in the *Amazon SageMaker Developer Guide*.
    """

    CheckType: Optional[String256]
    BaselineUsedForDriftCheckConstraints: Optional[String1024]
    CalculatedBaselineConstraints: Optional[String1024]
    ModelPackageGroupName: Optional[String256]
    ViolationReport: Optional[String1024]
    CheckJobArn: Optional[String256]
    SkipCheck: Optional[Boolean]
    RegisterNewBaseline: Optional[Boolean]


class GitConfig(TypedDict, total=False):
    """Specifies configuration details for a Git repository in your Amazon Web
    Services account.
    """

    RepositoryUrl: GitConfigUrl
    Branch: Optional[Branch]
    SecretArn: Optional[SecretArn]


LastModifiedTime = datetime


class CodeRepositorySummary(TypedDict, total=False):
    """Specifies summary information about a Git repository."""

    CodeRepositoryName: EntityName
    CodeRepositoryArn: CodeRepositoryArn
    CreationTime: CreationTime
    LastModifiedTime: LastModifiedTime
    GitConfig: Optional[GitConfig]


CodeRepositorySummaryList = List[CodeRepositorySummary]


class CognitoConfig(TypedDict, total=False):
    """Use this parameter to configure your Amazon Cognito workforce. A single
    Cognito workforce is created using and corresponds to a single `Amazon
    Cognito user
    pool <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html>`__.
    """

    UserPool: CognitoUserPool
    ClientId: ClientId


class CognitoMemberDefinition(TypedDict, total=False):
    """Identifies a Amazon Cognito user group. A user group can be used in on
    or more work teams.
    """

    UserPool: CognitoUserPool
    UserGroup: CognitoUserGroup
    ClientId: ClientId


CollectionParameters = Dict[ConfigKey, ConfigValue]


class CollectionConfiguration(TypedDict, total=False):
    """Configuration information for the Debugger output tensor collections."""

    CollectionName: Optional[CollectionName]
    CollectionParameters: Optional[CollectionParameters]


CollectionConfigurations = List[CollectionConfiguration]


class CompilationJobSummary(TypedDict, total=False):
    """A summary of a model compilation job."""

    CompilationJobName: EntityName
    CompilationJobArn: CompilationJobArn
    CreationTime: CreationTime
    CompilationStartTime: Optional[Timestamp]
    CompilationEndTime: Optional[Timestamp]
    CompilationTargetDevice: Optional[TargetDevice]
    CompilationTargetPlatformOs: Optional[TargetPlatformOs]
    CompilationTargetPlatformArch: Optional[TargetPlatformArch]
    CompilationTargetPlatformAccelerator: Optional[TargetPlatformAccelerator]
    LastModifiedTime: Optional[LastModifiedTime]
    CompilationJobStatus: CompilationJobStatus


CompilationJobSummaries = List[CompilationJobSummary]


class ConditionStepMetadata(TypedDict, total=False):
    """Metadata for a Condition step."""

    Outcome: Optional[ConditionOutcome]


class MultiModelConfig(TypedDict, total=False):
    """Specifies additional configuration for hosting multi-model endpoints."""

    ModelCacheSetting: Optional[ModelCacheSetting]


class RepositoryAuthConfig(TypedDict, total=False):
    """Specifies an authentication configuration for the private docker
    registry where your model image is hosted. Specify a value for this
    property only if you specified ``Vpc`` as the value for the
    ``RepositoryAccessMode`` field of the ``ImageConfig`` object that you
    passed to a call to ``CreateModel`` and the private Docker registry
    where the model image is hosted requires authentication.
    """

    RepositoryCredentialsProviderArn: RepositoryCredentialsProviderArn


class ImageConfig(TypedDict, total=False):
    """Specifies whether the model container is in Amazon ECR or a private
    Docker registry accessible from your Amazon Virtual Private Cloud (VPC).
    """

    RepositoryAccessMode: RepositoryAccessMode
    RepositoryAuthConfig: Optional[RepositoryAuthConfig]


class ContainerDefinition(TypedDict, total=False):
    """Describes the container, as part of model definition."""

    ContainerHostname: Optional[ContainerHostname]
    Image: Optional[ContainerImage]
    ImageConfig: Optional[ImageConfig]
    Mode: Optional[ContainerMode]
    ModelDataUrl: Optional[Url]
    Environment: Optional[EnvironmentMap]
    ModelPackageName: Optional[VersionedArnOrName]
    InferenceSpecificationName: Optional[InferenceSpecificationName]
    MultiModelConfig: Optional[MultiModelConfig]


ContainerDefinitionList = List[ContainerDefinition]
ContentClassifiers = List[ContentClassifier]


class ContextSource(TypedDict, total=False):
    """A structure describing the source of a context."""

    SourceUri: String2048
    SourceType: Optional[String256]
    SourceId: Optional[String256]


class ContextSummary(TypedDict, total=False):
    """Lists a summary of the properties of a context. A context provides a
    logical grouping of other entities.
    """

    ContextArn: Optional[ContextArn]
    ContextName: Optional[ExperimentEntityName]
    Source: Optional[ContextSource]
    ContextType: Optional[String256]
    CreationTime: Optional[Timestamp]
    LastModifiedTime: Optional[Timestamp]


ContextSummaries = List[ContextSummary]


class ContinuousParameterRange(TypedDict, total=False):
    """A list of continuous hyperparameters to tune."""

    Name: ParameterKey
    MinValue: ParameterValue
    MaxValue: ParameterValue
    ScalingType: Optional[HyperParameterScalingType]


class ContinuousParameterRangeSpecification(TypedDict, total=False):
    """Defines the possible values for a continuous hyperparameter."""

    MinValue: ParameterValue
    MaxValue: ParameterValue


ContinuousParameterRanges = List[ContinuousParameterRange]


class MetadataProperties(TypedDict, total=False):
    """Metadata properties of the tracking entity, trial, or trial component."""

    CommitId: Optional[MetadataPropertyValue]
    Repository: Optional[MetadataPropertyValue]
    GeneratedBy: Optional[MetadataPropertyValue]
    ProjectId: Optional[MetadataPropertyValue]


LineageEntityParameters = Dict[StringParameterValue, StringParameterValue]


class CreateActionRequest(ServiceRequest):
    ActionName: ExperimentEntityName
    Source: ActionSource
    ActionType: String256
    Description: Optional[ExperimentDescription]
    Status: Optional[ActionStatus]
    Properties: Optional[LineageEntityParameters]
    MetadataProperties: Optional[MetadataProperties]
    Tags: Optional[TagList]


class CreateActionResponse(TypedDict, total=False):
    ActionArn: Optional[ActionArn]


class HyperParameterTuningJobObjective(TypedDict, total=False):
    """Defines the objective metric for a hyperparameter tuning job.
    Hyperparameter tuning uses the value of this metric to evaluate the
    training jobs it launches, and returns the training job that results in
    either the highest or lowest value for this metric, depending on the
    value you specify for the ``Type`` parameter.
    """

    Type: HyperParameterTuningJobObjectiveType
    MetricName: MetricName


HyperParameterTuningJobObjectives = List[HyperParameterTuningJobObjective]
TrainingInstanceTypes = List[TrainingInstanceType]


class IntegerParameterRangeSpecification(TypedDict, total=False):
    """Defines the possible values for an integer hyperparameter."""

    MinValue: ParameterValue
    MaxValue: ParameterValue


class ParameterRange(TypedDict, total=False):
    """Defines the possible values for categorical, continuous, and integer
    hyperparameters to be used by an algorithm.
    """

    IntegerParameterRangeSpecification: Optional[IntegerParameterRangeSpecification]
    ContinuousParameterRangeSpecification: Optional[ContinuousParameterRangeSpecification]
    CategoricalParameterRangeSpecification: Optional[CategoricalParameterRangeSpecification]


class HyperParameterSpecification(TypedDict, total=False):
    """Defines a hyperparameter to be used by an algorithm."""

    Name: ParameterName
    Description: Optional[EntityDescription]
    Type: ParameterType
    Range: Optional[ParameterRange]
    IsTunable: Optional[Boolean]
    IsRequired: Optional[Boolean]
    DefaultValue: Optional[HyperParameterValue]


HyperParameterSpecifications = List[HyperParameterSpecification]


class TrainingSpecification(TypedDict, total=False):
    """Defines how the algorithm is used for a training job."""

    TrainingImage: ContainerImage
    TrainingImageDigest: Optional[ImageDigest]
    SupportedHyperParameters: Optional[HyperParameterSpecifications]
    SupportedTrainingInstanceTypes: TrainingInstanceTypes
    SupportsDistributedTraining: Optional[Boolean]
    MetricDefinitions: Optional[MetricDefinitionList]
    TrainingChannels: ChannelSpecifications
    SupportedTuningJobObjectiveMetrics: Optional[HyperParameterTuningJobObjectives]


class CreateAlgorithmInput(ServiceRequest):
    AlgorithmName: EntityName
    AlgorithmDescription: Optional[EntityDescription]
    TrainingSpecification: TrainingSpecification
    InferenceSpecification: Optional[InferenceSpecification]
    ValidationSpecification: Optional[AlgorithmValidationSpecification]
    CertifyForMarketplace: Optional[CertifyForMarketplace]
    Tags: Optional[TagList]


class CreateAlgorithmOutput(TypedDict, total=False):
    AlgorithmArn: AlgorithmArn


class CreateAppImageConfigRequest(ServiceRequest):
    AppImageConfigName: AppImageConfigName
    Tags: Optional[TagList]
    KernelGatewayImageConfig: Optional[KernelGatewayImageConfig]


class CreateAppImageConfigResponse(TypedDict, total=False):
    AppImageConfigArn: Optional[AppImageConfigArn]


class ResourceSpec(TypedDict, total=False):
    """Specifies the ARN's of a SageMaker image and SageMaker image version,
    and the instance type that the version runs on.
    """

    SageMakerImageArn: Optional[ImageArn]
    SageMakerImageVersionArn: Optional[ImageVersionArn]
    InstanceType: Optional[AppInstanceType]
    LifecycleConfigArn: Optional[StudioLifecycleConfigArn]


class CreateAppRequest(ServiceRequest):
    DomainId: DomainId
    UserProfileName: UserProfileName
    AppType: AppType
    AppName: AppName
    Tags: Optional[TagList]
    ResourceSpec: Optional[ResourceSpec]


class CreateAppResponse(TypedDict, total=False):
    AppArn: Optional[AppArn]


class CreateArtifactRequest(ServiceRequest):
    ArtifactName: Optional[ExperimentEntityName]
    Source: ArtifactSource
    ArtifactType: String256
    Properties: Optional[LineageEntityParameters]
    MetadataProperties: Optional[MetadataProperties]
    Tags: Optional[TagList]


class CreateArtifactResponse(TypedDict, total=False):
    ArtifactArn: Optional[ArtifactArn]


class ModelDeployConfig(TypedDict, total=False):
    """Specifies how to generate the endpoint name for an automatic one-click
    Autopilot model deployment.
    """

    AutoGenerateEndpointName: Optional[AutoGenerateEndpointName]
    EndpointName: Optional[EndpointName]


class CreateAutoMLJobRequest(ServiceRequest):
    AutoMLJobName: AutoMLJobName
    InputDataConfig: AutoMLInputDataConfig
    OutputDataConfig: AutoMLOutputDataConfig
    ProblemType: Optional[ProblemType]
    AutoMLJobObjective: Optional[AutoMLJobObjective]
    AutoMLJobConfig: Optional[AutoMLJobConfig]
    RoleArn: RoleArn
    GenerateCandidateDefinitionsOnly: Optional[GenerateCandidateDefinitionsOnly]
    Tags: Optional[TagList]
    ModelDeployConfig: Optional[ModelDeployConfig]


class CreateAutoMLJobResponse(TypedDict, total=False):
    AutoMLJobArn: AutoMLJobArn


class CreateCodeRepositoryInput(ServiceRequest):
    CodeRepositoryName: EntityName
    GitConfig: GitConfig
    Tags: Optional[TagList]


class CreateCodeRepositoryOutput(TypedDict, total=False):
    CodeRepositoryArn: CodeRepositoryArn


NeoVpcSubnets = List[NeoVpcSubnetId]
NeoVpcSecurityGroupIds = List[NeoVpcSecurityGroupId]


class NeoVpcConfig(TypedDict, total=False):
    """The VpcConfig configuration object that specifies the VPC that you want
    the compilation jobs to connect to. For more information on controlling
    access to your Amazon S3 buckets used for compilation job, see `Give
    Amazon SageMaker Compilation Jobs Access to Resources in Your Amazon
    VPC <https://docs.aws.amazon.com/sagemaker/latest/dg/neo-vpc.html>`__.
    """

    SecurityGroupIds: NeoVpcSecurityGroupIds
    Subnets: NeoVpcSubnets


class TargetPlatform(TypedDict, total=False):
    """Contains information about a target platform that you want your model to
    run on, such as OS, architecture, and accelerators. It is an alternative
    of ``TargetDevice``.
    """

    Os: TargetPlatformOs
    Arch: TargetPlatformArch
    Accelerator: Optional[TargetPlatformAccelerator]


class OutputConfig(TypedDict, total=False):
    """Contains information about the output location for the compiled model
    and the target device that the model runs on. ``TargetDevice`` and
    ``TargetPlatform`` are mutually exclusive, so you need to choose one
    between the two to specify your target device or platform. If you cannot
    find your device you want to use from the ``TargetDevice`` list, use
    ``TargetPlatform`` to describe the platform of your edge device and
    ``CompilerOptions`` if there are specific settings that are required or
    recommended to use for particular TargetPlatform.
    """

    S3OutputLocation: S3Uri
    TargetDevice: Optional[TargetDevice]
    TargetPlatform: Optional[TargetPlatform]
    CompilerOptions: Optional[CompilerOptions]
    KmsKeyId: Optional[KmsKeyId]


class InputConfig(TypedDict, total=False):
    """Contains information about the location of input model artifacts, the
    name and shape of the expected data inputs, and the framework in which
    the model was trained.
    """

    S3Uri: S3Uri
    DataInputConfig: DataInputConfig
    Framework: Framework
    FrameworkVersion: Optional[FrameworkVersion]


class CreateCompilationJobRequest(ServiceRequest):
    CompilationJobName: EntityName
    RoleArn: RoleArn
    ModelPackageVersionArn: Optional[ModelPackageArn]
    InputConfig: Optional[InputConfig]
    OutputConfig: OutputConfig
    VpcConfig: Optional[NeoVpcConfig]
    StoppingCondition: StoppingCondition
    Tags: Optional[TagList]


class CreateCompilationJobResponse(TypedDict, total=False):
    CompilationJobArn: CompilationJobArn


class CreateContextRequest(ServiceRequest):
    ContextName: ExperimentEntityName
    Source: ContextSource
    ContextType: String256
    Description: Optional[ExperimentDescription]
    Properties: Optional[LineageEntityParameters]
    Tags: Optional[TagList]


class CreateContextResponse(TypedDict, total=False):
    ContextArn: Optional[ContextArn]


class MonitoringStoppingCondition(TypedDict, total=False):
    """A time limit for how long the monitoring job is allowed to run before
    stopping.
    """

    MaxRuntimeInSeconds: MonitoringMaxRuntimeInSeconds


class MonitoringNetworkConfig(TypedDict, total=False):
    """The networking configuration for the monitoring job."""

    EnableInterContainerTrafficEncryption: Optional[Boolean]
    EnableNetworkIsolation: Optional[Boolean]
    VpcConfig: Optional[VpcConfig]


class MonitoringClusterConfig(TypedDict, total=False):
    """Configuration for the cluster used to run model monitoring jobs."""

    InstanceCount: ProcessingInstanceCount
    InstanceType: ProcessingInstanceType
    VolumeSizeInGB: ProcessingVolumeSizeInGB
    VolumeKmsKeyId: Optional[KmsKeyId]


class MonitoringResources(TypedDict, total=False):
    """Identifies the resources to deploy for a monitoring job."""

    ClusterConfig: MonitoringClusterConfig


class MonitoringS3Output(TypedDict, total=False):
    """Information about where and how you want to store the results of a
    monitoring job.
    """

    S3Uri: MonitoringS3Uri
    LocalPath: ProcessingLocalPath
    S3UploadMode: Optional[ProcessingS3UploadMode]


class MonitoringOutput(TypedDict, total=False):
    """The output object for a monitoring job."""

    S3Output: MonitoringS3Output


MonitoringOutputs = List[MonitoringOutput]


class MonitoringOutputConfig(TypedDict, total=False):
    """The output configuration for monitoring jobs."""

    MonitoringOutputs: MonitoringOutputs
    KmsKeyId: Optional[KmsKeyId]


class EndpointInput(TypedDict, total=False):
    """Input object for the endpoint"""

    EndpointName: EndpointName
    LocalPath: ProcessingLocalPath
    S3InputMode: Optional[ProcessingS3InputMode]
    S3DataDistributionType: Optional[ProcessingS3DataDistributionType]
    FeaturesAttribute: Optional[String]
    InferenceAttribute: Optional[String]
    ProbabilityAttribute: Optional[String]
    ProbabilityThresholdAttribute: Optional[ProbabilityThresholdAttribute]
    StartTimeOffset: Optional[MonitoringTimeOffsetString]
    EndTimeOffset: Optional[MonitoringTimeOffsetString]


class DataQualityJobInput(TypedDict, total=False):
    """The input for the data quality monitoring job. Currently endpoints are
    supported for input.
    """

    EndpointInput: EndpointInput


MonitoringEnvironmentMap = Dict[ProcessingEnvironmentKey, ProcessingEnvironmentValue]
MonitoringContainerArguments = List[ContainerArgument]


class DataQualityAppSpecification(TypedDict, total=False):
    """Information about the container that a data quality monitoring job runs."""

    ImageUri: ImageUri
    ContainerEntrypoint: Optional[ContainerEntrypoint]
    ContainerArguments: Optional[MonitoringContainerArguments]
    RecordPreprocessorSourceUri: Optional[S3Uri]
    PostAnalyticsProcessorSourceUri: Optional[S3Uri]
    Environment: Optional[MonitoringEnvironmentMap]


class MonitoringStatisticsResource(TypedDict, total=False):
    """The statistics resource for a monitoring job."""

    S3Uri: Optional[S3Uri]


class MonitoringConstraintsResource(TypedDict, total=False):
    """The constraints resource for a monitoring job."""

    S3Uri: Optional[S3Uri]


class DataQualityBaselineConfig(TypedDict, total=False):
    """Configuration for monitoring constraints and monitoring statistics.
    These baseline resources are compared against the results of the current
    job from the series of jobs scheduled to collect data periodically.
    """

    BaseliningJobName: Optional[ProcessingJobName]
    ConstraintsResource: Optional[MonitoringConstraintsResource]
    StatisticsResource: Optional[MonitoringStatisticsResource]


class CreateDataQualityJobDefinitionRequest(ServiceRequest):
    JobDefinitionName: MonitoringJobDefinitionName
    DataQualityBaselineConfig: Optional[DataQualityBaselineConfig]
    DataQualityAppSpecification: DataQualityAppSpecification
    DataQualityJobInput: DataQualityJobInput
    DataQualityJobOutputConfig: MonitoringOutputConfig
    JobResources: MonitoringResources
    NetworkConfig: Optional[MonitoringNetworkConfig]
    RoleArn: RoleArn
    StoppingCondition: Optional[MonitoringStoppingCondition]
    Tags: Optional[TagList]


class CreateDataQualityJobDefinitionResponse(TypedDict, total=False):
    JobDefinitionArn: MonitoringJobDefinitionArn


class EdgeOutputConfig(TypedDict, total=False):
    """The output configuration."""

    S3OutputLocation: S3Uri
    KmsKeyId: Optional[KmsKeyId]
    PresetDeploymentType: Optional[EdgePresetDeploymentType]
    PresetDeploymentConfig: Optional[String]


class CreateDeviceFleetRequest(ServiceRequest):
    DeviceFleetName: EntityName
    RoleArn: Optional[RoleArn]
    Description: Optional[DeviceFleetDescription]
    OutputConfig: EdgeOutputConfig
    Tags: Optional[TagList]
    EnableIotRoleAlias: Optional[EnableIotRoleAlias]


class RStudioServerProDomainSettings(TypedDict, total=False):
    """A collection of settings that configure the ``RStudioServerPro``
    Domain-level app.
    """

    DomainExecutionRoleArn: RoleArn
    RStudioConnectUrl: Optional[String]
    RStudioPackageManagerUrl: Optional[String]
    DefaultResourceSpec: Optional[ResourceSpec]


DomainSecurityGroupIds = List[SecurityGroupId]


class DomainSettings(TypedDict, total=False):
    """A collection of settings that apply to the ``SageMaker Domain``. These
    settings are specified through the ``CreateDomain`` API call.
    """

    SecurityGroupIds: Optional[DomainSecurityGroupIds]
    RStudioServerProDomainSettings: Optional[RStudioServerProDomainSettings]


class CustomImage(TypedDict, total=False):
    """A custom SageMaker image. For more information, see `Bring your own
    SageMaker
    image <https://docs.aws.amazon.com/sagemaker/latest/dg/studio-byoi.html>`__.
    """

    ImageName: ImageName
    ImageVersionNumber: Optional[ImageVersionNumber]
    AppImageConfigName: AppImageConfigName


CustomImages = List[CustomImage]


class RSessionAppSettings(TypedDict, total=False):
    """A collection of settings that apply to an ``RSessionGateway`` app."""

    DefaultResourceSpec: Optional[ResourceSpec]
    CustomImages: Optional[CustomImages]


class RStudioServerProAppSettings(TypedDict, total=False):
    """A collection of settings that configure user interaction with the
    ``RStudioServerPro`` app. ``RStudioServerProAppSettings`` cannot be
    updated. The ``RStudioServerPro`` app must be deleted and a new one
    created to make any changes.
    """

    AccessStatus: Optional[RStudioServerProAccessStatus]
    UserGroup: Optional[RStudioServerProUserGroup]


class TensorBoardAppSettings(TypedDict, total=False):
    """The TensorBoard app settings."""

    DefaultResourceSpec: Optional[ResourceSpec]


LifecycleConfigArns = List[StudioLifecycleConfigArn]


class KernelGatewayAppSettings(TypedDict, total=False):
    """The KernelGateway app settings."""

    DefaultResourceSpec: Optional[ResourceSpec]
    CustomImages: Optional[CustomImages]
    LifecycleConfigArns: Optional[LifecycleConfigArns]


class JupyterServerAppSettings(TypedDict, total=False):
    """The JupyterServer app settings."""

    DefaultResourceSpec: Optional[ResourceSpec]
    LifecycleConfigArns: Optional[LifecycleConfigArns]


class SharingSettings(TypedDict, total=False):
    """Specifies options for sharing SageMaker Studio notebooks. These settings
    are specified as part of ``DefaultUserSettings`` when the
    ``CreateDomain`` API is called, and as part of ``UserSettings`` when the
    ``CreateUserProfile`` API is called. When ``SharingSettings`` is not
    specified, notebook sharing isn't allowed.
    """

    NotebookOutputOption: Optional[NotebookOutputOption]
    S3OutputPath: Optional[S3Uri]
    S3KmsKeyId: Optional[KmsKeyId]


SecurityGroupIds = List[SecurityGroupId]


class UserSettings(TypedDict, total=False):
    """A collection of settings that apply to users of Amazon SageMaker Studio.
    These settings are specified when the ``CreateUserProfile`` API is
    called, and as ``DefaultUserSettings`` when the ``CreateDomain`` API is
    called.

    ``SecurityGroups`` is aggregated when specified in both calls. For all
    other settings in ``UserSettings``, the values specified in
    ``CreateUserProfile`` take precedence over those specified in
    ``CreateDomain``.
    """

    ExecutionRole: Optional[RoleArn]
    SecurityGroups: Optional[SecurityGroupIds]
    SharingSettings: Optional[SharingSettings]
    JupyterServerAppSettings: Optional[JupyterServerAppSettings]
    KernelGatewayAppSettings: Optional[KernelGatewayAppSettings]
    TensorBoardAppSettings: Optional[TensorBoardAppSettings]
    RStudioServerProAppSettings: Optional[RStudioServerProAppSettings]
    RSessionAppSettings: Optional[RSessionAppSettings]


class CreateDomainRequest(ServiceRequest):
    DomainName: DomainName
    AuthMode: AuthMode
    DefaultUserSettings: UserSettings
    SubnetIds: Subnets
    VpcId: VpcId
    Tags: Optional[TagList]
    AppNetworkAccessType: Optional[AppNetworkAccessType]
    HomeEfsFileSystemKmsKeyId: Optional[KmsKeyId]
    KmsKeyId: Optional[KmsKeyId]
    AppSecurityGroupManagement: Optional[AppSecurityGroupManagement]
    DomainSettings: Optional[DomainSettings]


class CreateDomainResponse(TypedDict, total=False):
    DomainArn: Optional[DomainArn]
    Url: Optional[String1024]


class CreateEdgePackagingJobRequest(ServiceRequest):
    EdgePackagingJobName: EntityName
    CompilationJobName: EntityName
    ModelName: EntityName
    ModelVersion: EdgeVersion
    RoleArn: RoleArn
    OutputConfig: EdgeOutputConfig
    ResourceKey: Optional[KmsKeyId]
    Tags: Optional[TagList]


class DataCaptureConfig(TypedDict, total=False):
    EnableCapture: Optional[EnableCapture]
    InitialSamplingPercentage: SamplingPercentage
    DestinationS3Uri: DestinationS3Uri
    KmsKeyId: Optional[KmsKeyId]
    CaptureOptions: CaptureOptionList
    CaptureContentTypeHeader: Optional[CaptureContentTypeHeader]


class ProductionVariantServerlessConfig(TypedDict, total=False):
    """Specifies the serverless configuration for an endpoint variant."""

    MemorySizeInMB: ServerlessMemorySizeInMB
    MaxConcurrency: ServerlessMaxConcurrency


class ProductionVariantCoreDumpConfig(TypedDict, total=False):
    """Specifies configuration for a core dump from the model container when
    the process crashes.
    """

    DestinationS3Uri: DestinationS3Uri
    KmsKeyId: Optional[KmsKeyId]


class ProductionVariant(TypedDict, total=False):
    """Identifies a model that you want to host and the resources chosen to
    deploy for hosting it. If you are deploying multiple models, tell
    SageMaker how to distribute traffic among the models by specifying
    variant weights.
    """

    VariantName: VariantName
    ModelName: ModelName
    InitialInstanceCount: Optional[InitialTaskCount]
    InstanceType: Optional[ProductionVariantInstanceType]
    InitialVariantWeight: Optional[VariantWeight]
    AcceleratorType: Optional[ProductionVariantAcceleratorType]
    CoreDumpConfig: Optional[ProductionVariantCoreDumpConfig]
    ServerlessConfig: Optional[ProductionVariantServerlessConfig]


ProductionVariantList = List[ProductionVariant]


class CreateEndpointConfigInput(ServiceRequest):
    EndpointConfigName: EndpointConfigName
    ProductionVariants: ProductionVariantList
    DataCaptureConfig: Optional[DataCaptureConfig]
    Tags: Optional[TagList]
    KmsKeyId: Optional[KmsKeyId]
    AsyncInferenceConfig: Optional[AsyncInferenceConfig]


class CreateEndpointConfigOutput(TypedDict, total=False):
    EndpointConfigArn: EndpointConfigArn


class DeploymentConfig(TypedDict, total=False):
    """The deployment configuration for an endpoint, which contains the desired
    deployment strategy and rollback configurations.
    """

    BlueGreenUpdatePolicy: BlueGreenUpdatePolicy
    AutoRollbackConfiguration: Optional[AutoRollbackConfig]


class CreateEndpointInput(ServiceRequest):
    EndpointName: EndpointName
    EndpointConfigName: EndpointConfigName
    DeploymentConfig: Optional[DeploymentConfig]
    Tags: Optional[TagList]


class CreateEndpointOutput(TypedDict, total=False):
    EndpointArn: EndpointArn


class CreateExperimentRequest(ServiceRequest):
    ExperimentName: ExperimentEntityName
    DisplayName: Optional[ExperimentEntityName]
    Description: Optional[ExperimentDescription]
    Tags: Optional[TagList]


class CreateExperimentResponse(TypedDict, total=False):
    ExperimentArn: Optional[ExperimentArn]


class DataCatalogConfig(TypedDict, total=False):
    """The meta data of the Glue table which serves as data catalog for the
    ``OfflineStore``.
    """

    TableName: TableName
    Catalog: Catalog
    Database: Database


class S3StorageConfig(TypedDict, total=False):
    """The Amazon Simple Storage (Amazon S3) location and and security
    configuration for ``OfflineStore``.
    """

    S3Uri: S3Uri
    KmsKeyId: Optional[KmsKeyId]
    ResolvedOutputS3Uri: Optional[S3Uri]


class OfflineStoreConfig(TypedDict, total=False):
    """The configuration of an ``OfflineStore``.

    Provide an ``OfflineStoreConfig`` in a request to ``CreateFeatureGroup``
    to create an ``OfflineStore``.

    To encrypt an ``OfflineStore`` using at rest data encryption, specify
    Amazon Web Services Key Management Service (KMS) key ID, or
    ``KMSKeyId``, in ``S3StorageConfig``.
    """

    S3StorageConfig: S3StorageConfig
    DisableGlueTableCreation: Optional[Boolean]
    DataCatalogConfig: Optional[DataCatalogConfig]


class OnlineStoreSecurityConfig(TypedDict, total=False):
    """The security configuration for ``OnlineStore``."""

    KmsKeyId: Optional[KmsKeyId]


class OnlineStoreConfig(TypedDict, total=False):
    """Use this to specify the Amazon Web Services Key Management Service (KMS)
    Key ID, or ``KMSKeyId``, for at rest data encryption. You can turn
    ``OnlineStore`` on or off by specifying the ``EnableOnlineStore`` flag
    at General Assembly; the default value is ``False``.
    """

    SecurityConfig: Optional[OnlineStoreSecurityConfig]
    EnableOnlineStore: Optional[Boolean]


class FeatureDefinition(TypedDict, total=False):
    """A list of features. You must include ``FeatureName`` and
    ``FeatureType``. Valid feature ``FeatureType`` s are ``Integral``,
    ``Fractional`` and ``String``.
    """

    FeatureName: Optional[FeatureName]
    FeatureType: Optional[FeatureType]


FeatureDefinitions = List[FeatureDefinition]


class CreateFeatureGroupRequest(ServiceRequest):
    FeatureGroupName: FeatureGroupName
    RecordIdentifierFeatureName: FeatureName
    EventTimeFeatureName: FeatureName
    FeatureDefinitions: FeatureDefinitions
    OnlineStoreConfig: Optional[OnlineStoreConfig]
    OfflineStoreConfig: Optional[OfflineStoreConfig]
    RoleArn: Optional[RoleArn]
    Description: Optional[Description]
    Tags: Optional[TagList]


class CreateFeatureGroupResponse(TypedDict, total=False):
    FeatureGroupArn: FeatureGroupArn


class FlowDefinitionOutputConfig(TypedDict, total=False):
    """Contains information about where human output will be stored."""

    S3OutputPath: S3Uri
    KmsKeyId: Optional[KmsKeyId]


class USD(TypedDict, total=False):
    """Represents an amount of money in United States dollars."""

    Dollars: Optional[Dollars]
    Cents: Optional[Cents]
    TenthFractionsOfACent: Optional[TenthFractionsOfACent]


class PublicWorkforceTaskPrice(TypedDict, total=False):
    """Defines the amount of money paid to an Amazon Mechanical Turk worker for
    each task performed.

    Use one of the following prices for bounding box tasks. Prices are in US
    dollars and should be based on the complexity of the task; the longer it
    takes in your initial testing, the more you should offer.

    -  0.036

    -  0.048

    -  0.060

    -  0.072

    -  0.120

    -  0.240

    -  0.360

    -  0.480

    -  0.600

    -  0.720

    -  0.840

    -  0.960

    -  1.080

    -  1.200

    Use one of the following prices for image classification, text
    classification, and custom tasks. Prices are in US dollars.

    -  0.012

    -  0.024

    -  0.036

    -  0.048

    -  0.060

    -  0.072

    -  0.120

    -  0.240

    -  0.360

    -  0.480

    -  0.600

    -  0.720

    -  0.840

    -  0.960

    -  1.080

    -  1.200

    Use one of the following prices for semantic segmentation tasks. Prices
    are in US dollars.

    -  0.840

    -  0.960

    -  1.080

    -  1.200

    Use one of the following prices for Textract AnalyzeDocument Important
    Form Key Amazon Augmented AI review tasks. Prices are in US dollars.

    -  2.400

    -  2.280

    -  2.160

    -  2.040

    -  1.920

    -  1.800

    -  1.680

    -  1.560

    -  1.440

    -  1.320

    -  1.200

    -  1.080

    -  0.960

    -  0.840

    -  0.720

    -  0.600

    -  0.480

    -  0.360

    -  0.240

    -  0.120

    -  0.072

    -  0.060

    -  0.048

    -  0.036

    -  0.024

    -  0.012

    Use one of the following prices for Rekognition DetectModerationLabels
    Amazon Augmented AI review tasks. Prices are in US dollars.

    -  1.200

    -  1.080

    -  0.960

    -  0.840

    -  0.720

    -  0.600

    -  0.480

    -  0.360

    -  0.240

    -  0.120

    -  0.072

    -  0.060

    -  0.048

    -  0.036

    -  0.024

    -  0.012

    Use one of the following prices for Amazon Augmented AI custom human
    review tasks. Prices are in US dollars.

    -  1.200

    -  1.080

    -  0.960

    -  0.840

    -  0.720

    -  0.600

    -  0.480

    -  0.360

    -  0.240

    -  0.120

    -  0.072

    -  0.060

    -  0.048

    -  0.036

    -  0.024

    -  0.012
    """

    AmountInUsd: Optional[USD]


FlowDefinitionTaskKeywords = List[FlowDefinitionTaskKeyword]


class HumanLoopConfig(TypedDict, total=False):
    """Describes the work to be performed by human workers."""

    WorkteamArn: WorkteamArn
    HumanTaskUiArn: HumanTaskUiArn
    TaskTitle: FlowDefinitionTaskTitle
    TaskDescription: FlowDefinitionTaskDescription
    TaskCount: FlowDefinitionTaskCount
    TaskAvailabilityLifetimeInSeconds: Optional[FlowDefinitionTaskAvailabilityLifetimeInSeconds]
    TaskTimeLimitInSeconds: Optional[FlowDefinitionTaskTimeLimitInSeconds]
    TaskKeywords: Optional[FlowDefinitionTaskKeywords]
    PublicWorkforceTaskPrice: Optional[PublicWorkforceTaskPrice]


class HumanLoopActivationConditionsConfig(TypedDict, total=False):
    """Defines under what conditions SageMaker creates a human loop. Used
    within . See for the required format of activation conditions.
    """

    HumanLoopActivationConditions: HumanLoopActivationConditions


class HumanLoopActivationConfig(TypedDict, total=False):
    """Provides information about how and under what conditions SageMaker
    creates a human loop. If ``HumanLoopActivationConfig`` is not given,
    then all requests go to humans.
    """

    HumanLoopActivationConditionsConfig: HumanLoopActivationConditionsConfig


class HumanLoopRequestSource(TypedDict, total=False):
    """Container for configuring the source of human task requests."""

    AwsManagedHumanLoopRequestSource: AwsManagedHumanLoopRequestSource


class CreateFlowDefinitionRequest(ServiceRequest):
    FlowDefinitionName: FlowDefinitionName
    HumanLoopRequestSource: Optional[HumanLoopRequestSource]
    HumanLoopActivationConfig: Optional[HumanLoopActivationConfig]
    HumanLoopConfig: HumanLoopConfig
    OutputConfig: FlowDefinitionOutputConfig
    RoleArn: RoleArn
    Tags: Optional[TagList]


class CreateFlowDefinitionResponse(TypedDict, total=False):
    FlowDefinitionArn: FlowDefinitionArn


class UiTemplate(TypedDict, total=False):
    """The Liquid template for the worker user interface."""

    Content: TemplateContent


class CreateHumanTaskUiRequest(ServiceRequest):
    HumanTaskUiName: HumanTaskUiName
    UiTemplate: UiTemplate
    Tags: Optional[TagList]


class CreateHumanTaskUiResponse(TypedDict, total=False):
    HumanTaskUiArn: HumanTaskUiArn


class ParentHyperParameterTuningJob(TypedDict, total=False):
    """A previously completed or stopped hyperparameter tuning job to be used
    as a starting point for a new hyperparameter tuning job.
    """

    HyperParameterTuningJobName: Optional[HyperParameterTuningJobName]


ParentHyperParameterTuningJobs = List[ParentHyperParameterTuningJob]


class HyperParameterTuningJobWarmStartConfig(TypedDict, total=False):
    """Specifies the configuration for a hyperparameter tuning job that uses
    one or more previous hyperparameter tuning jobs as a starting point. The
    results of previous tuning jobs are used to inform which combinations of
    hyperparameters to search over in the new tuning job.

    All training jobs launched by the new hyperparameter tuning job are
    evaluated by using the objective metric, and the training job that
    performs the best is compared to the best training jobs from the parent
    tuning jobs. From these, the training job that performs the best as
    measured by the objective metric is returned as the overall best
    training job.

    All training jobs launched by parent hyperparameter tuning jobs and the
    new hyperparameter tuning jobs count against the limit of training jobs
    for the tuning job.
    """

    ParentHyperParameterTuningJobs: ParentHyperParameterTuningJobs
    WarmStartType: HyperParameterTuningJobWarmStartType


class RetryStrategy(TypedDict, total=False):
    """The retry strategy to use when a training job fails due to an
    ``InternalServerError``. ``RetryStrategy`` is specified as part of the
    ``CreateTrainingJob`` and ``CreateHyperParameterTuningJob`` requests.
    You can add the ``StoppingCondition`` parameter to the request to limit
    the training time for the complete job.
    """

    MaximumRetryAttempts: MaximumRetryAttempts


class HyperParameterAlgorithmSpecification(TypedDict, total=False):
    """Specifies which training algorithm to use for training jobs that a
    hyperparameter tuning job launches and the metrics to monitor.
    """

    TrainingImage: Optional[AlgorithmImage]
    TrainingInputMode: TrainingInputMode
    AlgorithmName: Optional[ArnOrName]
    MetricDefinitions: Optional[MetricDefinitionList]


class IntegerParameterRange(TypedDict, total=False):
    """For a hyperparameter of the integer type, specifies the range that a
    hyperparameter tuning job searches.
    """

    Name: ParameterKey
    MinValue: ParameterValue
    MaxValue: ParameterValue
    ScalingType: Optional[HyperParameterScalingType]


IntegerParameterRanges = List[IntegerParameterRange]


class ParameterRanges(TypedDict, total=False):
    """Specifies ranges of integer, continuous, and categorical hyperparameters
    that a hyperparameter tuning job searches. The hyperparameter tuning job
    launches training jobs with hyperparameter values within these ranges to
    find the combination of values that result in the training job with the
    best performance as measured by the objective metric of the
    hyperparameter tuning job.

    You can specify a maximum of 20 hyperparameters that a hyperparameter
    tuning job can search over. Every possible value of a categorical
    parameter range counts against this limit.
    """

    IntegerParameterRanges: Optional[IntegerParameterRanges]
    ContinuousParameterRanges: Optional[ContinuousParameterRanges]
    CategoricalParameterRanges: Optional[CategoricalParameterRanges]


class HyperParameterTrainingJobDefinition(TypedDict, total=False):
    """Defines the training jobs launched by a hyperparameter tuning job."""

    DefinitionName: Optional[HyperParameterTrainingJobDefinitionName]
    TuningObjective: Optional[HyperParameterTuningJobObjective]
    HyperParameterRanges: Optional[ParameterRanges]
    StaticHyperParameters: Optional[HyperParameters]
    AlgorithmSpecification: HyperParameterAlgorithmSpecification
    RoleArn: RoleArn
    InputDataConfig: Optional[InputDataConfig]
    VpcConfig: Optional[VpcConfig]
    OutputDataConfig: OutputDataConfig
    ResourceConfig: ResourceConfig
    StoppingCondition: StoppingCondition
    EnableNetworkIsolation: Optional[Boolean]
    EnableInterContainerTrafficEncryption: Optional[Boolean]
    EnableManagedSpotTraining: Optional[Boolean]
    CheckpointConfig: Optional[CheckpointConfig]
    RetryStrategy: Optional[RetryStrategy]


HyperParameterTrainingJobDefinitions = List[HyperParameterTrainingJobDefinition]


class TuningJobCompletionCriteria(TypedDict, total=False):
    """The job completion criteria."""

    TargetObjectiveMetricValue: TargetObjectiveMetricValue


class ResourceLimits(TypedDict, total=False):
    """Specifies the maximum number of training jobs and parallel training jobs
    that a hyperparameter tuning job can launch.
    """

    MaxNumberOfTrainingJobs: MaxNumberOfTrainingJobs
    MaxParallelTrainingJobs: MaxParallelTrainingJobs


class HyperParameterTuningJobConfig(TypedDict, total=False):
    """Configures a hyperparameter tuning job."""

    Strategy: HyperParameterTuningJobStrategyType
    HyperParameterTuningJobObjective: Optional[HyperParameterTuningJobObjective]
    ResourceLimits: ResourceLimits
    ParameterRanges: Optional[ParameterRanges]
    TrainingJobEarlyStoppingType: Optional[TrainingJobEarlyStoppingType]
    TuningJobCompletionCriteria: Optional[TuningJobCompletionCriteria]


class CreateHyperParameterTuningJobRequest(ServiceRequest):
    HyperParameterTuningJobName: HyperParameterTuningJobName
    HyperParameterTuningJobConfig: HyperParameterTuningJobConfig
    TrainingJobDefinition: Optional[HyperParameterTrainingJobDefinition]
    TrainingJobDefinitions: Optional[HyperParameterTrainingJobDefinitions]
    WarmStartConfig: Optional[HyperParameterTuningJobWarmStartConfig]
    Tags: Optional[TagList]


class CreateHyperParameterTuningJobResponse(TypedDict, total=False):
    HyperParameterTuningJobArn: HyperParameterTuningJobArn


class CreateImageRequest(ServiceRequest):
    Description: Optional[ImageDescription]
    DisplayName: Optional[ImageDisplayName]
    ImageName: ImageName
    RoleArn: RoleArn
    Tags: Optional[TagList]


class CreateImageResponse(TypedDict, total=False):
    ImageArn: Optional[ImageArn]


class CreateImageVersionRequest(ServiceRequest):
    BaseImage: ImageBaseImage
    ClientToken: ClientToken
    ImageName: ImageName


class CreateImageVersionResponse(TypedDict, total=False):
    ImageVersionArn: Optional[ImageVersionArn]


class RecommendationJobCompiledOutputConfig(TypedDict, total=False):
    """Provides information about the output configuration for the compiled
    model.
    """

    S3OutputUri: Optional[S3Uri]


class RecommendationJobOutputConfig(TypedDict, total=False):
    """Provides information about the output configuration for the compiled
    model.
    """

    KmsKeyId: Optional[KmsKeyId]
    CompiledOutputConfig: Optional[RecommendationJobCompiledOutputConfig]


class ModelLatencyThreshold(TypedDict, total=False):
    """The model latency threshold."""

    Percentile: Optional[String64]
    ValueInMilliseconds: Optional[Integer]


ModelLatencyThresholds = List[ModelLatencyThreshold]


class RecommendationJobStoppingConditions(TypedDict, total=False):
    """Specifies conditions for stopping a job. When a job reaches a stopping
    condition limit, SageMaker ends the job.
    """

    MaxInvocations: Optional[Integer]
    ModelLatencyThresholds: Optional[ModelLatencyThresholds]


class EnvironmentParameterRanges(TypedDict, total=False):
    """Specifies the range of environment parameters"""

    CategoricalParameterRanges: Optional[CategoricalParameters]


class EndpointInputConfiguration(TypedDict, total=False):
    """The endpoint configuration for the load test."""

    InstanceType: ProductionVariantInstanceType
    InferenceSpecificationName: Optional[InferenceSpecificationName]
    EnvironmentParameterRanges: Optional[EnvironmentParameterRanges]


EndpointInputConfigurations = List[EndpointInputConfiguration]


class RecommendationJobResourceLimit(TypedDict, total=False):
    """Specifies the maximum number of jobs that can run in parallel and the
    maximum number of jobs that can run.
    """

    MaxNumberOfTests: Optional[MaxNumberOfTests]
    MaxParallelOfTests: Optional[MaxParallelOfTests]


class Phase(TypedDict, total=False):
    """Defines the traffic pattern."""

    InitialNumberOfUsers: Optional[InitialNumberOfUsers]
    SpawnRate: Optional[SpawnRate]
    DurationInSeconds: Optional[TrafficDurationInSeconds]


Phases = List[Phase]


class TrafficPattern(TypedDict, total=False):
    """Defines the traffic pattern of the load test."""

    TrafficType: Optional[TrafficType]
    Phases: Optional[Phases]


class RecommendationJobInputConfig(TypedDict, total=False):
    """The input configuration of the recommendation job."""

    ModelPackageVersionArn: ModelPackageArn
    JobDurationInSeconds: Optional[JobDurationInSeconds]
    TrafficPattern: Optional[TrafficPattern]
    ResourceLimit: Optional[RecommendationJobResourceLimit]
    EndpointConfigurations: Optional[EndpointInputConfigurations]
    VolumeKmsKeyId: Optional[KmsKeyId]


class CreateInferenceRecommendationsJobRequest(ServiceRequest):
    JobName: RecommendationJobName
    JobType: RecommendationJobType
    RoleArn: RoleArn
    InputConfig: RecommendationJobInputConfig
    JobDescription: Optional[RecommendationJobDescription]
    StoppingConditions: Optional[RecommendationJobStoppingConditions]
    OutputConfig: Optional[RecommendationJobOutputConfig]
    Tags: Optional[TagList]


class CreateInferenceRecommendationsJobResponse(TypedDict, total=False):
    JobArn: RecommendationJobArn


TaskKeywords = List[TaskKeyword]


class UiConfig(TypedDict, total=False):
    """Provided configuration information for the worker UI for a labeling job.
    Provide either ``HumanTaskUiArn`` or ``UiTemplateS3Uri``.

    For named entity recognition, 3D point cloud and video frame labeling
    jobs, use ``HumanTaskUiArn``.

    For all other Ground Truth built-in task types and custom task types,
    use ``UiTemplateS3Uri`` to specify the location of a worker task
    template in Amazon S3.
    """

    UiTemplateS3Uri: Optional[S3Uri]
    HumanTaskUiArn: Optional[HumanTaskUiArn]


class HumanTaskConfig(TypedDict, total=False):
    """Information required for human workers to complete a labeling task."""

    WorkteamArn: WorkteamArn
    UiConfig: UiConfig
    PreHumanTaskLambdaArn: LambdaFunctionArn
    TaskKeywords: Optional[TaskKeywords]
    TaskTitle: TaskTitle
    TaskDescription: TaskDescription
    NumberOfHumanWorkersPerDataObject: NumberOfHumanWorkersPerDataObject
    TaskTimeLimitInSeconds: TaskTimeLimitInSeconds
    TaskAvailabilityLifetimeInSeconds: Optional[TaskAvailabilityLifetimeInSeconds]
    MaxConcurrentTaskCount: Optional[MaxConcurrentTaskCount]
    AnnotationConsolidationConfig: AnnotationConsolidationConfig
    PublicWorkforceTaskPrice: Optional[PublicWorkforceTaskPrice]


class LabelingJobResourceConfig(TypedDict, total=False):
    """Configure encryption on the storage volume attached to the ML compute
    instance used to run automated data labeling model training and
    inference.
    """

    VolumeKmsKeyId: Optional[KmsKeyId]


class LabelingJobAlgorithmsConfig(TypedDict, total=False):
    """Provides configuration information for auto-labeling of your data
    objects. A ``LabelingJobAlgorithmsConfig`` object must be supplied in
    order to use auto-labeling.
    """

    LabelingJobAlgorithmSpecificationArn: LabelingJobAlgorithmSpecificationArn
    InitialActiveLearningModelArn: Optional[ModelArn]
    LabelingJobResourceConfig: Optional[LabelingJobResourceConfig]


class LabelingJobStoppingConditions(TypedDict, total=False):
    """A set of conditions for stopping a labeling job. If any of the
    conditions are met, the job is automatically stopped. You can use these
    conditions to control the cost of data labeling.

    Labeling jobs fail after 30 days with an appropriate client error
    message.
    """

    MaxHumanLabeledObjectCount: Optional[MaxHumanLabeledObjectCount]
    MaxPercentageOfInputDatasetLabeled: Optional[MaxPercentageOfInputDatasetLabeled]


class LabelingJobOutputConfig(TypedDict, total=False):
    """Output configuration information for a labeling job."""

    S3OutputPath: S3Uri
    KmsKeyId: Optional[KmsKeyId]
    SnsTopicArn: Optional[SnsTopicArn]


class LabelingJobDataAttributes(TypedDict, total=False):
    """Attributes of the data specified by the customer. Use these to describe
    the data to be labeled.
    """

    ContentClassifiers: Optional[ContentClassifiers]


class LabelingJobSnsDataSource(TypedDict, total=False):
    """An Amazon SNS data source used for streaming labeling jobs."""

    SnsTopicArn: SnsTopicArn


class LabelingJobS3DataSource(TypedDict, total=False):
    """The Amazon S3 location of the input data objects."""

    ManifestS3Uri: S3Uri


class LabelingJobDataSource(TypedDict, total=False):
    """Provides information about the location of input data.

    You must specify at least one of the following: ``S3DataSource`` or
    ``SnsDataSource``.

    Use ``SnsDataSource`` to specify an SNS input topic for a streaming
    labeling job. If you do not specify and SNS input topic ARN, Ground
    Truth will create a one-time labeling job.

    Use ``S3DataSource`` to specify an input manifest file for both
    streaming and one-time labeling jobs. Adding an ``S3DataSource`` is
    optional if you use ``SnsDataSource`` to create a streaming labeling
    job.
    """

    S3DataSource: Optional[LabelingJobS3DataSource]
    SnsDataSource: Optional[LabelingJobSnsDataSource]


class LabelingJobInputConfig(TypedDict, total=False):
    """Input configuration information for a labeling job."""

    DataSource: LabelingJobDataSource
    DataAttributes: Optional[LabelingJobDataAttributes]


class CreateLabelingJobRequest(ServiceRequest):
    LabelingJobName: LabelingJobName
    LabelAttributeName: LabelAttributeName
    InputConfig: LabelingJobInputConfig
    OutputConfig: LabelingJobOutputConfig
    RoleArn: RoleArn
    LabelCategoryConfigS3Uri: Optional[S3Uri]
    StoppingConditions: Optional[LabelingJobStoppingConditions]
    LabelingJobAlgorithmsConfig: Optional[LabelingJobAlgorithmsConfig]
    HumanTaskConfig: HumanTaskConfig
    Tags: Optional[TagList]


class CreateLabelingJobResponse(TypedDict, total=False):
    LabelingJobArn: LabelingJobArn


class MonitoringGroundTruthS3Input(TypedDict, total=False):
    """The ground truth labels for the dataset used for the monitoring job."""

    S3Uri: Optional[MonitoringS3Uri]


class ModelBiasJobInput(TypedDict, total=False):
    """Inputs for the model bias job."""

    EndpointInput: EndpointInput
    GroundTruthS3Input: MonitoringGroundTruthS3Input


class ModelBiasAppSpecification(TypedDict, total=False):
    """Docker container image configuration object for the model bias job."""

    ImageUri: ImageUri
    ConfigUri: S3Uri
    Environment: Optional[MonitoringEnvironmentMap]


class ModelBiasBaselineConfig(TypedDict, total=False):
    """The configuration for a baseline model bias job."""

    BaseliningJobName: Optional[ProcessingJobName]
    ConstraintsResource: Optional[MonitoringConstraintsResource]


class CreateModelBiasJobDefinitionRequest(ServiceRequest):
    JobDefinitionName: MonitoringJobDefinitionName
    ModelBiasBaselineConfig: Optional[ModelBiasBaselineConfig]
    ModelBiasAppSpecification: ModelBiasAppSpecification
    ModelBiasJobInput: ModelBiasJobInput
    ModelBiasJobOutputConfig: MonitoringOutputConfig
    JobResources: MonitoringResources
    NetworkConfig: Optional[MonitoringNetworkConfig]
    RoleArn: RoleArn
    StoppingCondition: Optional[MonitoringStoppingCondition]
    Tags: Optional[TagList]


class CreateModelBiasJobDefinitionResponse(TypedDict, total=False):
    JobDefinitionArn: MonitoringJobDefinitionArn


class ModelExplainabilityJobInput(TypedDict, total=False):
    """Inputs for the model explainability job."""

    EndpointInput: EndpointInput


class ModelExplainabilityAppSpecification(TypedDict, total=False):
    """Docker container image configuration object for the model explainability
    job.
    """

    ImageUri: ImageUri
    ConfigUri: S3Uri
    Environment: Optional[MonitoringEnvironmentMap]


class ModelExplainabilityBaselineConfig(TypedDict, total=False):
    """The configuration for a baseline model explainability job."""

    BaseliningJobName: Optional[ProcessingJobName]
    ConstraintsResource: Optional[MonitoringConstraintsResource]


class CreateModelExplainabilityJobDefinitionRequest(ServiceRequest):
    JobDefinitionName: MonitoringJobDefinitionName
    ModelExplainabilityBaselineConfig: Optional[ModelExplainabilityBaselineConfig]
    ModelExplainabilityAppSpecification: ModelExplainabilityAppSpecification
    ModelExplainabilityJobInput: ModelExplainabilityJobInput
    ModelExplainabilityJobOutputConfig: MonitoringOutputConfig
    JobResources: MonitoringResources
    NetworkConfig: Optional[MonitoringNetworkConfig]
    RoleArn: RoleArn
    StoppingCondition: Optional[MonitoringStoppingCondition]
    Tags: Optional[TagList]


class CreateModelExplainabilityJobDefinitionResponse(TypedDict, total=False):
    JobDefinitionArn: MonitoringJobDefinitionArn


class InferenceExecutionConfig(TypedDict, total=False):
    """Specifies details about how containers in a multi-container endpoint are
    run.
    """

    Mode: InferenceExecutionMode


class CreateModelInput(ServiceRequest):
    ModelName: ModelName
    PrimaryContainer: Optional[ContainerDefinition]
    Containers: Optional[ContainerDefinitionList]
    InferenceExecutionConfig: Optional[InferenceExecutionConfig]
    ExecutionRoleArn: RoleArn
    Tags: Optional[TagList]
    VpcConfig: Optional[VpcConfig]
    EnableNetworkIsolation: Optional[Boolean]


class CreateModelOutput(TypedDict, total=False):
    ModelArn: ModelArn


class CreateModelPackageGroupInput(ServiceRequest):
    ModelPackageGroupName: EntityName
    ModelPackageGroupDescription: Optional[EntityDescription]
    Tags: Optional[TagList]


class CreateModelPackageGroupOutput(TypedDict, total=False):
    ModelPackageGroupArn: ModelPackageGroupArn


class DriftCheckModelDataQuality(TypedDict, total=False):
    """Represents the drift check data quality baselines that can be used when
    the model monitor is set using the model package.
    """

    Statistics: Optional[MetricsSource]
    Constraints: Optional[MetricsSource]


class DriftCheckModelQuality(TypedDict, total=False):
    """Represents the drift check model quality baselines that can be used when
    the model monitor is set using the model package.
    """

    Statistics: Optional[MetricsSource]
    Constraints: Optional[MetricsSource]


class FileSource(TypedDict, total=False):
    """Contains details regarding the file source."""

    ContentType: Optional[ContentType]
    ContentDigest: Optional[ContentDigest]
    S3Uri: S3Uri


class DriftCheckExplainability(TypedDict, total=False):
    """Represents the drift check explainability baselines that can be used
    when the model monitor is set using the model package.
    """

    Constraints: Optional[MetricsSource]
    ConfigFile: Optional[FileSource]


class DriftCheckBias(TypedDict, total=False):
    """Represents the drift check bias baselines that can be used when the
    model monitor is set using the model package.
    """

    ConfigFile: Optional[FileSource]
    PreTrainingConstraints: Optional[MetricsSource]
    PostTrainingConstraints: Optional[MetricsSource]


class DriftCheckBaselines(TypedDict, total=False):
    """Represents the drift check baselines that can be used when the model
    monitor is set using the model package.
    """

    Bias: Optional[DriftCheckBias]
    Explainability: Optional[DriftCheckExplainability]
    ModelQuality: Optional[DriftCheckModelQuality]
    ModelDataQuality: Optional[DriftCheckModelDataQuality]


CustomerMetadataMap = Dict[CustomerMetadataKey, CustomerMetadataValue]


class Explainability(TypedDict, total=False):
    """Contains explainability metrics for a model."""

    Report: Optional[MetricsSource]


class ModelDataQuality(TypedDict, total=False):
    """Data quality constraints and statistics for a model."""

    Statistics: Optional[MetricsSource]
    Constraints: Optional[MetricsSource]


class ModelQuality(TypedDict, total=False):
    """Model quality statistics and constraints."""

    Statistics: Optional[MetricsSource]
    Constraints: Optional[MetricsSource]


class ModelMetrics(TypedDict, total=False):
    """Contains metrics captured from a model."""

    ModelQuality: Optional[ModelQuality]
    ModelDataQuality: Optional[ModelDataQuality]
    Bias: Optional[Bias]
    Explainability: Optional[Explainability]


class SourceAlgorithm(TypedDict, total=False):
    """Specifies an algorithm that was used to create the model package. The
    algorithm must be either an algorithm resource in your SageMaker account
    or an algorithm in Amazon Web Services Marketplace that you are
    subscribed to.
    """

    ModelDataUrl: Optional[Url]
    AlgorithmName: ArnOrName


SourceAlgorithmList = List[SourceAlgorithm]


class SourceAlgorithmSpecification(TypedDict, total=False):
    """A list of algorithms that were used to create a model package."""

    SourceAlgorithms: SourceAlgorithmList


class ModelPackageValidationProfile(TypedDict, total=False):
    """Contains data, such as the inputs and targeted instance types that are
    used in the process of validating the model package.

    The data provided in the validation profile is made available to your
    buyers on Amazon Web Services Marketplace.
    """

    ProfileName: EntityName
    TransformJobDefinition: TransformJobDefinition


ModelPackageValidationProfiles = List[ModelPackageValidationProfile]


class ModelPackageValidationSpecification(TypedDict, total=False):
    """Specifies batch transform jobs that SageMaker runs to validate your
    model package.
    """

    ValidationRole: RoleArn
    ValidationProfiles: ModelPackageValidationProfiles


class CreateModelPackageInput(ServiceRequest):
    ModelPackageName: Optional[EntityName]
    ModelPackageGroupName: Optional[ArnOrName]
    ModelPackageDescription: Optional[EntityDescription]
    InferenceSpecification: Optional[InferenceSpecification]
    ValidationSpecification: Optional[ModelPackageValidationSpecification]
    SourceAlgorithmSpecification: Optional[SourceAlgorithmSpecification]
    CertifyForMarketplace: Optional[CertifyForMarketplace]
    Tags: Optional[TagList]
    ModelApprovalStatus: Optional[ModelApprovalStatus]
    MetadataProperties: Optional[MetadataProperties]
    ModelMetrics: Optional[ModelMetrics]
    ClientToken: Optional[ClientToken]
    CustomerMetadataProperties: Optional[CustomerMetadataMap]
    DriftCheckBaselines: Optional[DriftCheckBaselines]
    Domain: Optional[String]
    Task: Optional[String]
    SamplePayloadUrl: Optional[S3Uri]
    AdditionalInferenceSpecifications: Optional[AdditionalInferenceSpecifications]


class CreateModelPackageOutput(TypedDict, total=False):
    ModelPackageArn: ModelPackageArn


class ModelQualityJobInput(TypedDict, total=False):
    """The input for the model quality monitoring job. Currently endponts are
    supported for input for model quality monitoring jobs.
    """

    EndpointInput: EndpointInput
    GroundTruthS3Input: MonitoringGroundTruthS3Input


class ModelQualityAppSpecification(TypedDict, total=False):
    """Container image configuration object for the monitoring job."""

    ImageUri: ImageUri
    ContainerEntrypoint: Optional[ContainerEntrypoint]
    ContainerArguments: Optional[MonitoringContainerArguments]
    RecordPreprocessorSourceUri: Optional[S3Uri]
    PostAnalyticsProcessorSourceUri: Optional[S3Uri]
    ProblemType: Optional[MonitoringProblemType]
    Environment: Optional[MonitoringEnvironmentMap]


class ModelQualityBaselineConfig(TypedDict, total=False):
    """Configuration for monitoring constraints and monitoring statistics.
    These baseline resources are compared against the results of the current
    job from the series of jobs scheduled to collect data periodically.
    """

    BaseliningJobName: Optional[ProcessingJobName]
    ConstraintsResource: Optional[MonitoringConstraintsResource]


class CreateModelQualityJobDefinitionRequest(ServiceRequest):
    JobDefinitionName: MonitoringJobDefinitionName
    ModelQualityBaselineConfig: Optional[ModelQualityBaselineConfig]
    ModelQualityAppSpecification: ModelQualityAppSpecification
    ModelQualityJobInput: ModelQualityJobInput
    ModelQualityJobOutputConfig: MonitoringOutputConfig
    JobResources: MonitoringResources
    NetworkConfig: Optional[MonitoringNetworkConfig]
    RoleArn: RoleArn
    StoppingCondition: Optional[MonitoringStoppingCondition]
    Tags: Optional[TagList]


class CreateModelQualityJobDefinitionResponse(TypedDict, total=False):
    JobDefinitionArn: MonitoringJobDefinitionArn


class NetworkConfig(TypedDict, total=False):
    """Networking options for a job, such as network traffic encryption between
    containers, whether to allow inbound and outbound network calls to and
    from containers, and the VPC subnets and security groups to use for
    VPC-enabled jobs.
    """

    EnableInterContainerTrafficEncryption: Optional[Boolean]
    EnableNetworkIsolation: Optional[Boolean]
    VpcConfig: Optional[VpcConfig]


class MonitoringAppSpecification(TypedDict, total=False):
    """Container image configuration object for the monitoring job."""

    ImageUri: ImageUri
    ContainerEntrypoint: Optional[ContainerEntrypoint]
    ContainerArguments: Optional[MonitoringContainerArguments]
    RecordPreprocessorSourceUri: Optional[S3Uri]
    PostAnalyticsProcessorSourceUri: Optional[S3Uri]


class MonitoringInput(TypedDict, total=False):
    """The inputs for a monitoring job."""

    EndpointInput: EndpointInput


MonitoringInputs = List[MonitoringInput]


class MonitoringBaselineConfig(TypedDict, total=False):
    """Configuration for monitoring constraints and monitoring statistics.
    These baseline resources are compared against the results of the current
    job from the series of jobs scheduled to collect data periodically.
    """

    BaseliningJobName: Optional[ProcessingJobName]
    ConstraintsResource: Optional[MonitoringConstraintsResource]
    StatisticsResource: Optional[MonitoringStatisticsResource]


class MonitoringJobDefinition(TypedDict, total=False):
    """Defines the monitoring job."""

    BaselineConfig: Optional[MonitoringBaselineConfig]
    MonitoringInputs: MonitoringInputs
    MonitoringOutputConfig: MonitoringOutputConfig
    MonitoringResources: MonitoringResources
    MonitoringAppSpecification: MonitoringAppSpecification
    StoppingCondition: Optional[MonitoringStoppingCondition]
    Environment: Optional[MonitoringEnvironmentMap]
    NetworkConfig: Optional[NetworkConfig]
    RoleArn: RoleArn


class ScheduleConfig(TypedDict, total=False):
    """Configuration details about the monitoring schedule."""

    ScheduleExpression: ScheduleExpression


class MonitoringScheduleConfig(TypedDict, total=False):
    """Configures the monitoring schedule and defines the monitoring job."""

    ScheduleConfig: Optional[ScheduleConfig]
    MonitoringJobDefinition: Optional[MonitoringJobDefinition]
    MonitoringJobDefinitionName: Optional[MonitoringJobDefinitionName]
    MonitoringType: Optional[MonitoringType]


class CreateMonitoringScheduleRequest(ServiceRequest):
    MonitoringScheduleName: MonitoringScheduleName
    MonitoringScheduleConfig: MonitoringScheduleConfig
    Tags: Optional[TagList]


class CreateMonitoringScheduleResponse(TypedDict, total=False):
    MonitoringScheduleArn: MonitoringScheduleArn


NotebookInstanceAcceleratorTypes = List[NotebookInstanceAcceleratorType]


class CreateNotebookInstanceInput(ServiceRequest):
    NotebookInstanceName: NotebookInstanceName
    InstanceType: InstanceType
    SubnetId: Optional[SubnetId]
    SecurityGroupIds: Optional[SecurityGroupIds]
    RoleArn: RoleArn
    KmsKeyId: Optional[KmsKeyId]
    Tags: Optional[TagList]
    LifecycleConfigName: Optional[NotebookInstanceLifecycleConfigName]
    DirectInternetAccess: Optional[DirectInternetAccess]
    VolumeSizeInGB: Optional[NotebookInstanceVolumeSizeInGB]
    AcceleratorTypes: Optional[NotebookInstanceAcceleratorTypes]
    DefaultCodeRepository: Optional[CodeRepositoryNameOrUrl]
    AdditionalCodeRepositories: Optional[AdditionalCodeRepositoryNamesOrUrls]
    RootAccess: Optional[RootAccess]
    PlatformIdentifier: Optional[PlatformIdentifier]


class NotebookInstanceLifecycleHook(TypedDict, total=False):
    """Contains the notebook instance lifecycle configuration script.

    Each lifecycle configuration script has a limit of 16384 characters.

    The value of the ``$PATH`` environment variable that is available to
    both scripts is ``/sbin:bin:/usr/sbin:/usr/bin``.

    View CloudWatch Logs for notebook instance lifecycle configurations in
    log group ``/aws/sagemaker/NotebookInstances`` in log stream
    ``[notebook-instance-name]/[LifecycleConfigHook]``.

    Lifecycle configuration scripts cannot run for longer than 5 minutes. If
    a script runs for longer than 5 minutes, it fails and the notebook
    instance is not created or started.

    For information about notebook instance lifestyle configurations, see
    `Step 2.1: (Optional) Customize a Notebook
    Instance <https://docs.aws.amazon.com/sagemaker/latest/dg/notebook-lifecycle-config.html>`__.
    """

    Content: Optional[NotebookInstanceLifecycleConfigContent]


NotebookInstanceLifecycleConfigList = List[NotebookInstanceLifecycleHook]


class CreateNotebookInstanceLifecycleConfigInput(ServiceRequest):
    NotebookInstanceLifecycleConfigName: NotebookInstanceLifecycleConfigName
    OnCreate: Optional[NotebookInstanceLifecycleConfigList]
    OnStart: Optional[NotebookInstanceLifecycleConfigList]


class CreateNotebookInstanceLifecycleConfigOutput(TypedDict, total=False):
    NotebookInstanceLifecycleConfigArn: Optional[NotebookInstanceLifecycleConfigArn]


class CreateNotebookInstanceOutput(TypedDict, total=False):
    NotebookInstanceArn: Optional[NotebookInstanceArn]


class ParallelismConfiguration(TypedDict, total=False):
    """Configuration that controls the parallelism of the pipeline. By default,
    the parallelism configuration specified applies to all executions of the
    pipeline unless overridden.
    """

    MaxParallelExecutionSteps: MaxParallelExecutionSteps


class PipelineDefinitionS3Location(TypedDict, total=False):
    """The location of the pipeline definition stored in Amazon S3."""

    Bucket: BucketName
    ObjectKey: Key
    VersionId: Optional[VersionId]


class CreatePipelineRequest(ServiceRequest):
    PipelineName: PipelineName
    PipelineDisplayName: Optional[PipelineName]
    PipelineDefinition: Optional[PipelineDefinition]
    PipelineDefinitionS3Location: Optional[PipelineDefinitionS3Location]
    PipelineDescription: Optional[PipelineDescription]
    ClientRequestToken: IdempotencyToken
    RoleArn: RoleArn
    Tags: Optional[TagList]
    ParallelismConfiguration: Optional[ParallelismConfiguration]


class CreatePipelineResponse(TypedDict, total=False):
    PipelineArn: Optional[PipelineArn]


class CreatePresignedDomainUrlRequest(ServiceRequest):
    DomainId: DomainId
    UserProfileName: UserProfileName
    SessionExpirationDurationInSeconds: Optional[SessionExpirationDurationInSeconds]
    ExpiresInSeconds: Optional[ExpiresInSeconds]


class CreatePresignedDomainUrlResponse(TypedDict, total=False):
    AuthorizedUrl: Optional[PresignedDomainUrl]


class CreatePresignedNotebookInstanceUrlInput(ServiceRequest):
    NotebookInstanceName: NotebookInstanceName
    SessionExpirationDurationInSeconds: Optional[SessionExpirationDurationInSeconds]


class CreatePresignedNotebookInstanceUrlOutput(TypedDict, total=False):
    AuthorizedUrl: Optional[NotebookInstanceUrl]


class ExperimentConfig(TypedDict, total=False):
    """Associates a SageMaker job as a trial component with an experiment and
    trial. Specified when you call the following APIs:

    -  CreateProcessingJob

    -  CreateTrainingJob

    -  CreateTransformJob
    """

    ExperimentName: Optional[ExperimentEntityName]
    TrialName: Optional[ExperimentEntityName]
    TrialComponentDisplayName: Optional[ExperimentEntityName]


ProcessingEnvironmentMap = Dict[ProcessingEnvironmentKey, ProcessingEnvironmentValue]


class ProcessingStoppingCondition(TypedDict, total=False):
    """Configures conditions under which the processing job should be stopped,
    such as how long the processing job has been running. After the
    condition is met, the processing job is stopped.
    """

    MaxRuntimeInSeconds: ProcessingMaxRuntimeInSeconds


class ProcessingClusterConfig(TypedDict, total=False):
    """Configuration for the cluster used to run a processing job."""

    InstanceCount: ProcessingInstanceCount
    InstanceType: ProcessingInstanceType
    VolumeSizeInGB: ProcessingVolumeSizeInGB
    VolumeKmsKeyId: Optional[KmsKeyId]


class ProcessingResources(TypedDict, total=False):
    """Identifies the resources, ML compute instances, and ML storage volumes
    to deploy for a processing job. In distributed training, you specify
    more than one instance.
    """

    ClusterConfig: ProcessingClusterConfig


class ProcessingFeatureStoreOutput(TypedDict, total=False):
    """Configuration for processing job outputs in Amazon SageMaker Feature
    Store.
    """

    FeatureGroupName: FeatureGroupName


class ProcessingS3Output(TypedDict, total=False):
    """Configuration for uploading output data to Amazon S3 from the processing
    container.
    """

    S3Uri: S3Uri
    LocalPath: ProcessingLocalPath
    S3UploadMode: ProcessingS3UploadMode


class ProcessingOutput(TypedDict, total=False):
    """Describes the results of a processing job. The processing output must
    specify exactly one of either ``S3Output`` or ``FeatureStoreOutput``
    types.
    """

    OutputName: String
    S3Output: Optional[ProcessingS3Output]
    FeatureStoreOutput: Optional[ProcessingFeatureStoreOutput]
    AppManaged: Optional[AppManaged]


ProcessingOutputs = List[ProcessingOutput]


class ProcessingOutputConfig(TypedDict, total=False):
    """Configuration for uploading output from the processing container."""

    Outputs: ProcessingOutputs
    KmsKeyId: Optional[KmsKeyId]


class RedshiftDatasetDefinition(TypedDict, total=False):
    """Configuration for Redshift Dataset Definition input."""

    ClusterId: RedshiftClusterId
    Database: RedshiftDatabase
    DbUser: RedshiftUserName
    QueryString: RedshiftQueryString
    ClusterRoleArn: RoleArn
    OutputS3Uri: S3Uri
    KmsKeyId: Optional[KmsKeyId]
    OutputFormat: RedshiftResultFormat
    OutputCompression: Optional[RedshiftResultCompressionType]


class DatasetDefinition(TypedDict, total=False):
    """Configuration for Dataset Definition inputs. The Dataset Definition
    input must specify exactly one of either ``AthenaDatasetDefinition`` or
    ``RedshiftDatasetDefinition`` types.
    """

    AthenaDatasetDefinition: Optional[AthenaDatasetDefinition]
    RedshiftDatasetDefinition: Optional[RedshiftDatasetDefinition]
    LocalPath: Optional[ProcessingLocalPath]
    DataDistributionType: Optional[DataDistributionType]
    InputMode: Optional[InputMode]


class ProcessingS3Input(TypedDict, total=False):
    """Configuration for downloading input data from Amazon S3 into the
    processing container.
    """

    S3Uri: S3Uri
    LocalPath: Optional[ProcessingLocalPath]
    S3DataType: ProcessingS3DataType
    S3InputMode: Optional[ProcessingS3InputMode]
    S3DataDistributionType: Optional[ProcessingS3DataDistributionType]
    S3CompressionType: Optional[ProcessingS3CompressionType]


class ProcessingInput(TypedDict, total=False):
    """The inputs for a processing job. The processing input must specify
    exactly one of either ``S3Input`` or ``DatasetDefinition`` types.
    """

    InputName: String
    AppManaged: Optional[AppManaged]
    S3Input: Optional[ProcessingS3Input]
    DatasetDefinition: Optional[DatasetDefinition]


ProcessingInputs = List[ProcessingInput]


class CreateProcessingJobRequest(ServiceRequest):
    ProcessingInputs: Optional[ProcessingInputs]
    ProcessingOutputConfig: Optional[ProcessingOutputConfig]
    ProcessingJobName: ProcessingJobName
    ProcessingResources: ProcessingResources
    StoppingCondition: Optional[ProcessingStoppingCondition]
    AppSpecification: AppSpecification
    Environment: Optional[ProcessingEnvironmentMap]
    NetworkConfig: Optional[NetworkConfig]
    RoleArn: RoleArn
    Tags: Optional[TagList]
    ExperimentConfig: Optional[ExperimentConfig]


class CreateProcessingJobResponse(TypedDict, total=False):
    ProcessingJobArn: ProcessingJobArn


class ProvisioningParameter(TypedDict, total=False):
    """A key value pair used when you provision a project as a service catalog
    product. For information, see `What is Amazon Web Services Service
    Catalog <https://docs.aws.amazon.com/servicecatalog/latest/adminguide/introduction.html>`__.
    """

    Key: Optional[ProvisioningParameterKey]
    Value: Optional[ProvisioningParameterValue]


ProvisioningParameters = List[ProvisioningParameter]


class ServiceCatalogProvisioningDetails(TypedDict, total=False):
    """Details that you specify to provision a service catalog product. For
    information about service catalog, see `What is Amazon Web Services
    Service
    Catalog <https://docs.aws.amazon.com/servicecatalog/latest/adminguide/introduction.html>`__.
    """

    ProductId: ServiceCatalogEntityId
    ProvisioningArtifactId: Optional[ServiceCatalogEntityId]
    PathId: Optional[ServiceCatalogEntityId]
    ProvisioningParameters: Optional[ProvisioningParameters]


class CreateProjectInput(ServiceRequest):
    ProjectName: ProjectEntityName
    ProjectDescription: Optional[EntityDescription]
    ServiceCatalogProvisioningDetails: ServiceCatalogProvisioningDetails
    Tags: Optional[TagList]


class CreateProjectOutput(TypedDict, total=False):
    ProjectArn: ProjectArn
    ProjectId: ProjectId


class CreateStudioLifecycleConfigRequest(ServiceRequest):
    StudioLifecycleConfigName: StudioLifecycleConfigName
    StudioLifecycleConfigContent: StudioLifecycleConfigContent
    StudioLifecycleConfigAppType: StudioLifecycleConfigAppType
    Tags: Optional[TagList]


class CreateStudioLifecycleConfigResponse(TypedDict, total=False):
    StudioLifecycleConfigArn: Optional[StudioLifecycleConfigArn]


TrainingEnvironmentMap = Dict[TrainingEnvironmentKey, TrainingEnvironmentValue]
RuleParameters = Dict[ConfigKey, ConfigValue]


class ProfilerRuleConfiguration(TypedDict, total=False):
    """Configuration information for profiling rules."""

    RuleConfigurationName: RuleConfigurationName
    LocalPath: Optional[DirectoryPath]
    S3OutputPath: Optional[S3Uri]
    RuleEvaluatorImage: AlgorithmImage
    InstanceType: Optional[ProcessingInstanceType]
    VolumeSizeInGB: Optional[OptionalVolumeSizeInGB]
    RuleParameters: Optional[RuleParameters]


ProfilerRuleConfigurations = List[ProfilerRuleConfiguration]
ProfilingParameters = Dict[ConfigKey, ConfigValue]
ProfilingIntervalInMilliseconds = int


class ProfilerConfig(TypedDict, total=False):
    """Configuration information for Debugger system monitoring, framework
    profiling, and storage paths.
    """

    S3OutputPath: S3Uri
    ProfilingIntervalInMilliseconds: Optional[ProfilingIntervalInMilliseconds]
    ProfilingParameters: Optional[ProfilingParameters]


class TensorBoardOutputConfig(TypedDict, total=False):
    """Configuration of storage locations for the Debugger TensorBoard output
    data.
    """

    LocalPath: Optional[DirectoryPath]
    S3OutputPath: S3Uri


class DebugRuleConfiguration(TypedDict, total=False):
    """Configuration information for SageMaker Debugger rules for debugging. To
    learn more about how to configure the ``DebugRuleConfiguration``
    parameter, see `Use the SageMaker and Debugger Configuration API
    Operations to Create, Update, and Debug Your Training
    Job <https://docs.aws.amazon.com/sagemaker/latest/dg/debugger-createtrainingjob-api.html>`__.
    """

    RuleConfigurationName: RuleConfigurationName
    LocalPath: Optional[DirectoryPath]
    S3OutputPath: Optional[S3Uri]
    RuleEvaluatorImage: AlgorithmImage
    InstanceType: Optional[ProcessingInstanceType]
    VolumeSizeInGB: Optional[OptionalVolumeSizeInGB]
    RuleParameters: Optional[RuleParameters]


DebugRuleConfigurations = List[DebugRuleConfiguration]
HookParameters = Dict[ConfigKey, ConfigValue]


class DebugHookConfig(TypedDict, total=False):
    """Configuration information for the Debugger hook parameters, metric and
    tensor collections, and storage paths. To learn more about how to
    configure the ``DebugHookConfig`` parameter, see `Use the SageMaker and
    Debugger Configuration API Operations to Create, Update, and Debug Your
    Training
    Job <https://docs.aws.amazon.com/sagemaker/latest/dg/debugger-createtrainingjob-api.html>`__.
    """

    LocalPath: Optional[DirectoryPath]
    S3OutputPath: S3Uri
    HookParameters: Optional[HookParameters]
    CollectionConfigurations: Optional[CollectionConfigurations]


class CreateTrainingJobRequest(ServiceRequest):
    TrainingJobName: TrainingJobName
    HyperParameters: Optional[HyperParameters]
    AlgorithmSpecification: AlgorithmSpecification
    RoleArn: RoleArn
    InputDataConfig: Optional[InputDataConfig]
    OutputDataConfig: OutputDataConfig
    ResourceConfig: ResourceConfig
    VpcConfig: Optional[VpcConfig]
    StoppingCondition: StoppingCondition
    Tags: Optional[TagList]
    EnableNetworkIsolation: Optional[Boolean]
    EnableInterContainerTrafficEncryption: Optional[Boolean]
    EnableManagedSpotTraining: Optional[Boolean]
    CheckpointConfig: Optional[CheckpointConfig]
    DebugHookConfig: Optional[DebugHookConfig]
    DebugRuleConfigurations: Optional[DebugRuleConfigurations]
    TensorBoardOutputConfig: Optional[TensorBoardOutputConfig]
    ExperimentConfig: Optional[ExperimentConfig]
    ProfilerConfig: Optional[ProfilerConfig]
    ProfilerRuleConfigurations: Optional[ProfilerRuleConfigurations]
    Environment: Optional[TrainingEnvironmentMap]
    RetryStrategy: Optional[RetryStrategy]


class CreateTrainingJobResponse(TypedDict, total=False):
    TrainingJobArn: TrainingJobArn


class DataProcessing(TypedDict, total=False):
    """The data structure used to specify the data to be used for inference in
    a batch transform job and to associate the data that is relevant to the
    prediction results in the output. The input filter provided allows you
    to exclude input data that is not needed for inference in a batch
    transform job. The output filter provided allows you to include input
    data relevant to interpreting the predictions in the output from the
    job. For more information, see `Associate Prediction Results with their
    Corresponding Input
    Records <https://docs.aws.amazon.com/sagemaker/latest/dg/batch-transform-data-processing.html>`__.
    """

    InputFilter: Optional[JsonPath]
    OutputFilter: Optional[JsonPath]
    JoinSource: Optional[JoinSource]


class ModelClientConfig(TypedDict, total=False):
    """Configures the timeout and maximum number of retries for processing a
    transform job invocation.
    """

    InvocationsTimeoutInSeconds: Optional[InvocationsTimeoutInSeconds]
    InvocationsMaxRetries: Optional[InvocationsMaxRetries]


class CreateTransformJobRequest(ServiceRequest):
    TransformJobName: TransformJobName
    ModelName: ModelName
    MaxConcurrentTransforms: Optional[MaxConcurrentTransforms]
    ModelClientConfig: Optional[ModelClientConfig]
    MaxPayloadInMB: Optional[MaxPayloadInMB]
    BatchStrategy: Optional[BatchStrategy]
    Environment: Optional[TransformEnvironmentMap]
    TransformInput: TransformInput
    TransformOutput: TransformOutput
    TransformResources: TransformResources
    DataProcessing: Optional[DataProcessing]
    Tags: Optional[TagList]
    ExperimentConfig: Optional[ExperimentConfig]


class CreateTransformJobResponse(TypedDict, total=False):
    TransformJobArn: TransformJobArn


class TrialComponentArtifact(TypedDict, total=False):
    """Represents an input or output artifact of a trial component. You specify
    ``TrialComponentArtifact`` as part of the ``InputArtifacts`` and
    ``OutputArtifacts`` parameters in the CreateTrialComponent request.

    Examples of input artifacts are datasets, algorithms, hyperparameters,
    source code, and instance types. Examples of output artifacts are
    metrics, snapshots, logs, and images.
    """

    MediaType: Optional[MediaType]
    Value: TrialComponentArtifactValue


TrialComponentArtifacts = Dict[TrialComponentKey64, TrialComponentArtifact]


class TrialComponentParameterValue(TypedDict, total=False):
    """The value of a hyperparameter. Only one of ``NumberValue`` or
    ``StringValue`` can be specified.

    This object is specified in the CreateTrialComponent request.
    """

    StringValue: Optional[StringParameterValue]
    NumberValue: Optional[DoubleParameterValue]


TrialComponentParameters = Dict[TrialComponentKey256, TrialComponentParameterValue]


class TrialComponentStatus(TypedDict, total=False):
    """The status of the trial component."""

    PrimaryStatus: Optional[TrialComponentPrimaryStatus]
    Message: Optional[TrialComponentStatusMessage]


class CreateTrialComponentRequest(ServiceRequest):
    TrialComponentName: ExperimentEntityName
    DisplayName: Optional[ExperimentEntityName]
    Status: Optional[TrialComponentStatus]
    StartTime: Optional[Timestamp]
    EndTime: Optional[Timestamp]
    Parameters: Optional[TrialComponentParameters]
    InputArtifacts: Optional[TrialComponentArtifacts]
    OutputArtifacts: Optional[TrialComponentArtifacts]
    MetadataProperties: Optional[MetadataProperties]
    Tags: Optional[TagList]


class CreateTrialComponentResponse(TypedDict, total=False):
    TrialComponentArn: Optional[TrialComponentArn]


class CreateTrialRequest(ServiceRequest):
    TrialName: ExperimentEntityName
    DisplayName: Optional[ExperimentEntityName]
    ExperimentName: ExperimentEntityName
    MetadataProperties: Optional[MetadataProperties]
    Tags: Optional[TagList]


class CreateTrialResponse(TypedDict, total=False):
    TrialArn: Optional[TrialArn]


class CreateUserProfileRequest(ServiceRequest):
    DomainId: DomainId
    UserProfileName: UserProfileName
    SingleSignOnUserIdentifier: Optional[SingleSignOnUserIdentifier]
    SingleSignOnUserValue: Optional[String256]
    Tags: Optional[TagList]
    UserSettings: Optional[UserSettings]


class CreateUserProfileResponse(TypedDict, total=False):
    UserProfileArn: Optional[UserProfileArn]


class SourceIpConfig(TypedDict, total=False):
    """A list of IP address ranges
    (`CIDRs <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html>`__).
    Used to create an allow list of IP addresses for a private workforce.
    Workers will only be able to login to their worker portal from an IP
    address within this range. By default, a workforce isn't restricted to
    specific IP addresses.
    """

    Cidrs: Cidrs


class OidcConfig(TypedDict, total=False):
    """Use this parameter to configure your OIDC Identity Provider (IdP)."""

    ClientId: ClientId
    ClientSecret: ClientSecret
    Issuer: OidcEndpoint
    AuthorizationEndpoint: OidcEndpoint
    TokenEndpoint: OidcEndpoint
    UserInfoEndpoint: OidcEndpoint
    LogoutEndpoint: OidcEndpoint
    JwksUri: OidcEndpoint


class CreateWorkforceRequest(ServiceRequest):
    CognitoConfig: Optional[CognitoConfig]
    OidcConfig: Optional[OidcConfig]
    SourceIpConfig: Optional[SourceIpConfig]
    WorkforceName: WorkforceName
    Tags: Optional[TagList]


class CreateWorkforceResponse(TypedDict, total=False):
    WorkforceArn: WorkforceArn


class NotificationConfiguration(TypedDict, total=False):
    """Configures Amazon SNS notifications of available or expiring work items
    for work teams.
    """

    NotificationTopicArn: Optional[NotificationTopicArn]


Groups = List[Group]


class OidcMemberDefinition(TypedDict, total=False):
    """A list of user groups that exist in your OIDC Identity Provider (IdP).
    One to ten groups can be used to create a single private work team. When
    you add a user group to the list of ``Groups``, you can add that user
    group to one or more private work teams. If you add a user group to a
    private work team, all workers in that user group are added to the work
    team.
    """

    Groups: Groups


class MemberDefinition(TypedDict, total=False):
    """Defines an Amazon Cognito or your own OIDC IdP user group that is part
    of a work team.
    """

    CognitoMemberDefinition: Optional[CognitoMemberDefinition]
    OidcMemberDefinition: Optional[OidcMemberDefinition]


MemberDefinitions = List[MemberDefinition]


class CreateWorkteamRequest(ServiceRequest):
    WorkteamName: WorkteamName
    WorkforceName: Optional[WorkforceName]
    MemberDefinitions: MemberDefinitions
    Description: String200
    NotificationConfiguration: Optional[NotificationConfiguration]
    Tags: Optional[TagList]


class CreateWorkteamResponse(TypedDict, total=False):
    WorkteamArn: Optional[WorkteamArn]


CustomerMetadataKeyList = List[CustomerMetadataKey]


class DataCaptureConfigSummary(TypedDict, total=False):
    EnableCapture: EnableCapture
    CaptureStatus: CaptureStatus
    CurrentSamplingPercentage: SamplingPercentage
    DestinationS3Uri: DestinationS3Uri
    KmsKeyId: KmsKeyId


class DebugRuleEvaluationStatus(TypedDict, total=False):
    """Information about the status of the rule evaluation."""

    RuleConfigurationName: Optional[RuleConfigurationName]
    RuleEvaluationJobArn: Optional[ProcessingJobArn]
    RuleEvaluationStatus: Optional[RuleEvaluationStatus]
    StatusDetails: Optional[StatusDetails]
    LastModifiedTime: Optional[Timestamp]


DebugRuleEvaluationStatuses = List[DebugRuleEvaluationStatus]


class DeleteActionRequest(ServiceRequest):
    ActionName: ExperimentEntityName


class DeleteActionResponse(TypedDict, total=False):
    ActionArn: Optional[ActionArn]


class DeleteAlgorithmInput(ServiceRequest):
    AlgorithmName: EntityName


class DeleteAppImageConfigRequest(ServiceRequest):
    AppImageConfigName: AppImageConfigName


class DeleteAppRequest(ServiceRequest):
    DomainId: DomainId
    UserProfileName: UserProfileName
    AppType: AppType
    AppName: AppName


class DeleteArtifactRequest(ServiceRequest):
    ArtifactArn: Optional[ArtifactArn]
    Source: Optional[ArtifactSource]


class DeleteArtifactResponse(TypedDict, total=False):
    ArtifactArn: Optional[ArtifactArn]


class DeleteAssociationRequest(ServiceRequest):
    SourceArn: AssociationEntityArn
    DestinationArn: AssociationEntityArn


class DeleteAssociationResponse(TypedDict, total=False):
    SourceArn: Optional[AssociationEntityArn]
    DestinationArn: Optional[AssociationEntityArn]


class DeleteCodeRepositoryInput(ServiceRequest):
    CodeRepositoryName: EntityName


class DeleteContextRequest(ServiceRequest):
    ContextName: ExperimentEntityName


class DeleteContextResponse(TypedDict, total=False):
    ContextArn: Optional[ContextArn]


class DeleteDataQualityJobDefinitionRequest(ServiceRequest):
    JobDefinitionName: MonitoringJobDefinitionName


class DeleteDeviceFleetRequest(ServiceRequest):
    DeviceFleetName: EntityName


class RetentionPolicy(TypedDict, total=False):
    """The retention policy for data stored on an Amazon Elastic File System
    (EFS) volume.
    """

    HomeEfsFileSystem: Optional[RetentionType]


class DeleteDomainRequest(ServiceRequest):
    DomainId: DomainId
    RetentionPolicy: Optional[RetentionPolicy]


class DeleteEndpointConfigInput(ServiceRequest):
    EndpointConfigName: EndpointConfigName


class DeleteEndpointInput(ServiceRequest):
    EndpointName: EndpointName


class DeleteExperimentRequest(ServiceRequest):
    ExperimentName: ExperimentEntityName


class DeleteExperimentResponse(TypedDict, total=False):
    ExperimentArn: Optional[ExperimentArn]


class DeleteFeatureGroupRequest(ServiceRequest):
    FeatureGroupName: FeatureGroupName


class DeleteFlowDefinitionRequest(ServiceRequest):
    FlowDefinitionName: FlowDefinitionName


class DeleteFlowDefinitionResponse(TypedDict, total=False):
    pass


class DeleteHumanTaskUiRequest(ServiceRequest):
    HumanTaskUiName: HumanTaskUiName


class DeleteHumanTaskUiResponse(TypedDict, total=False):
    pass


class DeleteImageRequest(ServiceRequest):
    ImageName: ImageName


class DeleteImageResponse(TypedDict, total=False):
    pass


class DeleteImageVersionRequest(ServiceRequest):
    ImageName: ImageName
    Version: ImageVersionNumber


class DeleteImageVersionResponse(TypedDict, total=False):
    pass


class DeleteModelBiasJobDefinitionRequest(ServiceRequest):
    JobDefinitionName: MonitoringJobDefinitionName


class DeleteModelExplainabilityJobDefinitionRequest(ServiceRequest):
    JobDefinitionName: MonitoringJobDefinitionName


class DeleteModelInput(ServiceRequest):
    ModelName: ModelName


class DeleteModelPackageGroupInput(ServiceRequest):
    ModelPackageGroupName: ArnOrName


class DeleteModelPackageGroupPolicyInput(ServiceRequest):
    ModelPackageGroupName: EntityName


class DeleteModelPackageInput(ServiceRequest):
    ModelPackageName: VersionedArnOrName


class DeleteModelQualityJobDefinitionRequest(ServiceRequest):
    JobDefinitionName: MonitoringJobDefinitionName


class DeleteMonitoringScheduleRequest(ServiceRequest):
    MonitoringScheduleName: MonitoringScheduleName


class DeleteNotebookInstanceInput(ServiceRequest):
    NotebookInstanceName: NotebookInstanceName


class DeleteNotebookInstanceLifecycleConfigInput(ServiceRequest):
    NotebookInstanceLifecycleConfigName: NotebookInstanceLifecycleConfigName


class DeletePipelineRequest(ServiceRequest):
    PipelineName: PipelineName
    ClientRequestToken: IdempotencyToken


class DeletePipelineResponse(TypedDict, total=False):
    PipelineArn: Optional[PipelineArn]


class DeleteProjectInput(ServiceRequest):
    ProjectName: ProjectEntityName


class DeleteStudioLifecycleConfigRequest(ServiceRequest):
    StudioLifecycleConfigName: StudioLifecycleConfigName


TagKeyList = List[TagKey]


class DeleteTagsInput(ServiceRequest):
    ResourceArn: ResourceArn
    TagKeys: TagKeyList


class DeleteTagsOutput(TypedDict, total=False):
    pass


class DeleteTrialComponentRequest(ServiceRequest):
    TrialComponentName: ExperimentEntityName


class DeleteTrialComponentResponse(TypedDict, total=False):
    TrialComponentArn: Optional[TrialComponentArn]


class DeleteTrialRequest(ServiceRequest):
    TrialName: ExperimentEntityName


class DeleteTrialResponse(TypedDict, total=False):
    TrialArn: Optional[TrialArn]


class DeleteUserProfileRequest(ServiceRequest):
    DomainId: DomainId
    UserProfileName: UserProfileName


class DeleteWorkforceRequest(ServiceRequest):
    WorkforceName: WorkforceName


class DeleteWorkforceResponse(TypedDict, total=False):
    pass


class DeleteWorkteamRequest(ServiceRequest):
    WorkteamName: WorkteamName


class DeleteWorkteamResponse(TypedDict, total=False):
    Success: Success


class DeployedImage(TypedDict, total=False):
    """Gets the Amazon EC2 Container Registry path of the docker image of the
    model that is hosted in this ProductionVariant.

    If you used the ``registry/repository[:tag]`` form to specify the image
    path of the primary container when you created the model hosted in this
    ``ProductionVariant``, the path resolves to a path of the form
    ``registry/repository[@digest]``. A digest is a hash value that
    identifies a specific version of an image. For information about Amazon
    ECR paths, see `Pulling an
    Image <https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-pull-ecr-image.html>`__
    in the *Amazon ECR User Guide*.
    """

    SpecifiedImage: Optional[ContainerImage]
    ResolvedImage: Optional[ContainerImage]
    ResolutionTime: Optional[Timestamp]


DeployedImages = List[DeployedImage]
DeviceNames = List[DeviceName]


class DeregisterDevicesRequest(ServiceRequest):
    DeviceFleetName: EntityName
    DeviceNames: DeviceNames


class DescribeActionRequest(ServiceRequest):
    ActionName: ExperimentEntityName


class DescribeActionResponse(TypedDict, total=False):
    ActionName: Optional[ExperimentEntityNameOrArn]
    ActionArn: Optional[ActionArn]
    Source: Optional[ActionSource]
    ActionType: Optional[String256]
    Description: Optional[ExperimentDescription]
    Status: Optional[ActionStatus]
    Properties: Optional[LineageEntityParameters]
    CreationTime: Optional[Timestamp]
    CreatedBy: Optional[UserContext]
    LastModifiedTime: Optional[Timestamp]
    LastModifiedBy: Optional[UserContext]
    MetadataProperties: Optional[MetadataProperties]
    LineageGroupArn: Optional[LineageGroupArn]


class DescribeAlgorithmInput(ServiceRequest):
    AlgorithmName: ArnOrName


class DescribeAlgorithmOutput(TypedDict, total=False):
    AlgorithmName: EntityName
    AlgorithmArn: AlgorithmArn
    AlgorithmDescription: Optional[EntityDescription]
    CreationTime: CreationTime
    TrainingSpecification: TrainingSpecification
    InferenceSpecification: Optional[InferenceSpecification]
    ValidationSpecification: Optional[AlgorithmValidationSpecification]
    AlgorithmStatus: AlgorithmStatus
    AlgorithmStatusDetails: AlgorithmStatusDetails
    ProductId: Optional[ProductId]
    CertifyForMarketplace: Optional[CertifyForMarketplace]


class DescribeAppImageConfigRequest(ServiceRequest):
    AppImageConfigName: AppImageConfigName


class DescribeAppImageConfigResponse(TypedDict, total=False):
    AppImageConfigArn: Optional[AppImageConfigArn]
    AppImageConfigName: Optional[AppImageConfigName]
    CreationTime: Optional[Timestamp]
    LastModifiedTime: Optional[Timestamp]
    KernelGatewayImageConfig: Optional[KernelGatewayImageConfig]


class DescribeAppRequest(ServiceRequest):
    DomainId: DomainId
    UserProfileName: UserProfileName
    AppType: AppType
    AppName: AppName


class DescribeAppResponse(TypedDict, total=False):
    AppArn: Optional[AppArn]
    AppType: Optional[AppType]
    AppName: Optional[AppName]
    DomainId: Optional[DomainId]
    UserProfileName: Optional[UserProfileName]
    Status: Optional[AppStatus]
    LastHealthCheckTimestamp: Optional[Timestamp]
    LastUserActivityTimestamp: Optional[Timestamp]
    CreationTime: Optional[CreationTime]
    FailureReason: Optional[FailureReason]
    ResourceSpec: Optional[ResourceSpec]


class DescribeArtifactRequest(ServiceRequest):
    ArtifactArn: ArtifactArn


class DescribeArtifactResponse(TypedDict, total=False):
    ArtifactName: Optional[ExperimentEntityNameOrArn]
    ArtifactArn: Optional[ArtifactArn]
    Source: Optional[ArtifactSource]
    ArtifactType: Optional[String256]
    Properties: Optional[LineageEntityParameters]
    CreationTime: Optional[Timestamp]
    CreatedBy: Optional[UserContext]
    LastModifiedTime: Optional[Timestamp]
    LastModifiedBy: Optional[UserContext]
    MetadataProperties: Optional[MetadataProperties]
    LineageGroupArn: Optional[LineageGroupArn]


class DescribeAutoMLJobRequest(ServiceRequest):
    AutoMLJobName: AutoMLJobName


class ModelDeployResult(TypedDict, total=False):
    """Provides information about the endpoint of the model deployment."""

    EndpointName: Optional[EndpointName]


class ResolvedAttributes(TypedDict, total=False):
    """The resolved attributes."""

    AutoMLJobObjective: Optional[AutoMLJobObjective]
    ProblemType: Optional[ProblemType]
    CompletionCriteria: Optional[AutoMLJobCompletionCriteria]


class DescribeAutoMLJobResponse(TypedDict, total=False):
    AutoMLJobName: AutoMLJobName
    AutoMLJobArn: AutoMLJobArn
    InputDataConfig: AutoMLInputDataConfig
    OutputDataConfig: AutoMLOutputDataConfig
    RoleArn: RoleArn
    AutoMLJobObjective: Optional[AutoMLJobObjective]
    ProblemType: Optional[ProblemType]
    AutoMLJobConfig: Optional[AutoMLJobConfig]
    CreationTime: Timestamp
    EndTime: Optional[Timestamp]
    LastModifiedTime: Timestamp
    FailureReason: Optional[AutoMLFailureReason]
    PartialFailureReasons: Optional[AutoMLPartialFailureReasons]
    BestCandidate: Optional[AutoMLCandidate]
    AutoMLJobStatus: AutoMLJobStatus
    AutoMLJobSecondaryStatus: AutoMLJobSecondaryStatus
    GenerateCandidateDefinitionsOnly: Optional[GenerateCandidateDefinitionsOnly]
    AutoMLJobArtifacts: Optional[AutoMLJobArtifacts]
    ResolvedAttributes: Optional[ResolvedAttributes]
    ModelDeployConfig: Optional[ModelDeployConfig]
    ModelDeployResult: Optional[ModelDeployResult]


class DescribeCodeRepositoryInput(ServiceRequest):
    CodeRepositoryName: EntityName


class DescribeCodeRepositoryOutput(TypedDict, total=False):
    CodeRepositoryName: EntityName
    CodeRepositoryArn: CodeRepositoryArn
    CreationTime: CreationTime
    LastModifiedTime: LastModifiedTime
    GitConfig: Optional[GitConfig]


class DescribeCompilationJobRequest(ServiceRequest):
    CompilationJobName: EntityName


class ModelDigests(TypedDict, total=False):
    """Provides information to verify the integrity of stored model artifacts."""

    ArtifactDigest: Optional[ArtifactDigest]


class ModelArtifacts(TypedDict, total=False):
    """Provides information about the location that is configured for storing
    model artifacts.

    Model artifacts are the output that results from training a model, and
    typically consist of trained parameters, a model definition that
    describes how to compute inferences, and other metadata.
    """

    S3ModelArtifacts: S3Uri


class DescribeCompilationJobResponse(TypedDict, total=False):
    CompilationJobName: EntityName
    CompilationJobArn: CompilationJobArn
    CompilationJobStatus: CompilationJobStatus
    CompilationStartTime: Optional[Timestamp]
    CompilationEndTime: Optional[Timestamp]
    StoppingCondition: StoppingCondition
    InferenceImage: Optional[InferenceImage]
    ModelPackageVersionArn: Optional[ModelPackageArn]
    CreationTime: CreationTime
    LastModifiedTime: LastModifiedTime
    FailureReason: FailureReason
    ModelArtifacts: ModelArtifacts
    ModelDigests: Optional[ModelDigests]
    RoleArn: RoleArn
    InputConfig: InputConfig
    OutputConfig: OutputConfig
    VpcConfig: Optional[NeoVpcConfig]


class DescribeContextRequest(ServiceRequest):
    ContextName: ExperimentEntityNameOrArn


class DescribeContextResponse(TypedDict, total=False):
    ContextName: Optional[ExperimentEntityName]
    ContextArn: Optional[ContextArn]
    Source: Optional[ContextSource]
    ContextType: Optional[String256]
    Description: Optional[ExperimentDescription]
    Properties: Optional[LineageEntityParameters]
    CreationTime: Optional[Timestamp]
    CreatedBy: Optional[UserContext]
    LastModifiedTime: Optional[Timestamp]
    LastModifiedBy: Optional[UserContext]
    LineageGroupArn: Optional[LineageGroupArn]


class DescribeDataQualityJobDefinitionRequest(ServiceRequest):
    JobDefinitionName: MonitoringJobDefinitionName


class DescribeDataQualityJobDefinitionResponse(TypedDict, total=False):
    JobDefinitionArn: MonitoringJobDefinitionArn
    JobDefinitionName: MonitoringJobDefinitionName
    CreationTime: Timestamp
    DataQualityBaselineConfig: Optional[DataQualityBaselineConfig]
    DataQualityAppSpecification: DataQualityAppSpecification
    DataQualityJobInput: DataQualityJobInput
    DataQualityJobOutputConfig: MonitoringOutputConfig
    JobResources: MonitoringResources
    NetworkConfig: Optional[MonitoringNetworkConfig]
    RoleArn: RoleArn
    StoppingCondition: Optional[MonitoringStoppingCondition]


class DescribeDeviceFleetRequest(ServiceRequest):
    DeviceFleetName: EntityName


class DescribeDeviceFleetResponse(TypedDict, total=False):
    DeviceFleetName: EntityName
    DeviceFleetArn: DeviceFleetArn
    OutputConfig: EdgeOutputConfig
    Description: Optional[DeviceFleetDescription]
    CreationTime: Timestamp
    LastModifiedTime: Timestamp
    RoleArn: Optional[RoleArn]
    IotRoleAlias: Optional[IotRoleAlias]


class DescribeDeviceRequest(ServiceRequest):
    NextToken: Optional[NextToken]
    DeviceName: EntityName
    DeviceFleetName: EntityName


class EdgeModel(TypedDict, total=False):
    """The model on the edge device."""

    ModelName: EntityName
    ModelVersion: EdgeVersion
    LatestSampleTime: Optional[Timestamp]
    LatestInference: Optional[Timestamp]


EdgeModels = List[EdgeModel]


class DescribeDeviceResponse(TypedDict, total=False):
    DeviceArn: Optional[DeviceArn]
    DeviceName: EntityName
    Description: Optional[DeviceDescription]
    DeviceFleetName: EntityName
    IotThingName: Optional[ThingName]
    RegistrationTime: Timestamp
    LatestHeartbeat: Optional[Timestamp]
    Models: Optional[EdgeModels]
    MaxModels: Optional[Integer]
    NextToken: Optional[NextToken]
    AgentVersion: Optional[EdgeVersion]


class DescribeDomainRequest(ServiceRequest):
    DomainId: DomainId


class DescribeDomainResponse(TypedDict, total=False):
    DomainArn: Optional[DomainArn]
    DomainId: Optional[DomainId]
    DomainName: Optional[DomainName]
    HomeEfsFileSystemId: Optional[ResourceId]
    SingleSignOnManagedApplicationInstanceId: Optional[String256]
    Status: Optional[DomainStatus]
    CreationTime: Optional[CreationTime]
    LastModifiedTime: Optional[LastModifiedTime]
    FailureReason: Optional[FailureReason]
    AuthMode: Optional[AuthMode]
    DefaultUserSettings: Optional[UserSettings]
    AppNetworkAccessType: Optional[AppNetworkAccessType]
    HomeEfsFileSystemKmsKeyId: Optional[KmsKeyId]
    SubnetIds: Optional[Subnets]
    Url: Optional[String1024]
    VpcId: Optional[VpcId]
    KmsKeyId: Optional[KmsKeyId]
    DomainSettings: Optional[DomainSettings]
    AppSecurityGroupManagement: Optional[AppSecurityGroupManagement]
    SecurityGroupIdForDomainBoundary: Optional[SecurityGroupId]


class DescribeEdgePackagingJobRequest(ServiceRequest):
    EdgePackagingJobName: EntityName


class EdgePresetDeploymentOutput(TypedDict, total=False):
    """The output of a SageMaker Edge Manager deployable resource."""

    Type: EdgePresetDeploymentType
    Artifact: Optional[EdgePresetDeploymentArtifact]
    Status: Optional[EdgePresetDeploymentStatus]
    StatusMessage: Optional[String]


class DescribeEdgePackagingJobResponse(TypedDict, total=False):
    EdgePackagingJobArn: EdgePackagingJobArn
    EdgePackagingJobName: EntityName
    CompilationJobName: Optional[EntityName]
    ModelName: Optional[EntityName]
    ModelVersion: Optional[EdgeVersion]
    RoleArn: Optional[RoleArn]
    OutputConfig: Optional[EdgeOutputConfig]
    ResourceKey: Optional[KmsKeyId]
    EdgePackagingJobStatus: EdgePackagingJobStatus
    EdgePackagingJobStatusMessage: Optional[String]
    CreationTime: Optional[Timestamp]
    LastModifiedTime: Optional[Timestamp]
    ModelArtifact: Optional[S3Uri]
    ModelSignature: Optional[String]
    PresetDeploymentOutput: Optional[EdgePresetDeploymentOutput]


class DescribeEndpointConfigInput(ServiceRequest):
    EndpointConfigName: EndpointConfigName


class DescribeEndpointConfigOutput(TypedDict, total=False):
    EndpointConfigName: EndpointConfigName
    EndpointConfigArn: EndpointConfigArn
    ProductionVariants: ProductionVariantList
    DataCaptureConfig: Optional[DataCaptureConfig]
    KmsKeyId: Optional[KmsKeyId]
    CreationTime: Timestamp
    AsyncInferenceConfig: Optional[AsyncInferenceConfig]


class DescribeEndpointInput(ServiceRequest):
    EndpointName: EndpointName


class ProductionVariantStatus(TypedDict, total=False):
    """Describes the status of the production variant."""

    Status: VariantStatus
    StatusMessage: Optional[VariantStatusMessage]
    StartTime: Optional[Timestamp]


ProductionVariantStatusList = List[ProductionVariantStatus]


class PendingProductionVariantSummary(TypedDict, total=False):
    """The production variant summary for a deployment when an endpoint is
    creating or updating with the ``CreateEndpoint`` or ``UpdateEndpoint``
    operations. Describes the ``VariantStatus``, weight and capacity for a
    production variant associated with an endpoint.
    """

    VariantName: VariantName
    DeployedImages: Optional[DeployedImages]
    CurrentWeight: Optional[VariantWeight]
    DesiredWeight: Optional[VariantWeight]
    CurrentInstanceCount: Optional[TaskCount]
    DesiredInstanceCount: Optional[TaskCount]
    InstanceType: Optional[ProductionVariantInstanceType]
    AcceleratorType: Optional[ProductionVariantAcceleratorType]
    VariantStatus: Optional[ProductionVariantStatusList]
    CurrentServerlessConfig: Optional[ProductionVariantServerlessConfig]
    DesiredServerlessConfig: Optional[ProductionVariantServerlessConfig]


PendingProductionVariantSummaryList = List[PendingProductionVariantSummary]


class PendingDeploymentSummary(TypedDict, total=False):
    """The summary of an in-progress deployment when an endpoint is creating or
    updating with a new endpoint configuration.
    """

    EndpointConfigName: EndpointConfigName
    ProductionVariants: Optional[PendingProductionVariantSummaryList]
    StartTime: Optional[Timestamp]


class ProductionVariantSummary(TypedDict, total=False):
    """Describes weight and capacities for a production variant associated with
    an endpoint. If you sent a request to the
    ``UpdateEndpointWeightsAndCapacities`` API and the endpoint status is
    ``Updating``, you get different desired and current values.
    """

    VariantName: VariantName
    DeployedImages: Optional[DeployedImages]
    CurrentWeight: Optional[VariantWeight]
    DesiredWeight: Optional[VariantWeight]
    CurrentInstanceCount: Optional[TaskCount]
    DesiredInstanceCount: Optional[TaskCount]
    VariantStatus: Optional[ProductionVariantStatusList]
    CurrentServerlessConfig: Optional[ProductionVariantServerlessConfig]
    DesiredServerlessConfig: Optional[ProductionVariantServerlessConfig]


ProductionVariantSummaryList = List[ProductionVariantSummary]


class DescribeEndpointOutput(TypedDict, total=False):
    EndpointName: EndpointName
    EndpointArn: EndpointArn
    EndpointConfigName: EndpointConfigName
    ProductionVariants: Optional[ProductionVariantSummaryList]
    DataCaptureConfig: Optional[DataCaptureConfigSummary]
    EndpointStatus: EndpointStatus
    FailureReason: Optional[FailureReason]
    CreationTime: Timestamp
    LastModifiedTime: Timestamp
    LastDeploymentConfig: Optional[DeploymentConfig]
    AsyncInferenceConfig: Optional[AsyncInferenceConfig]
    PendingDeploymentSummary: Optional[PendingDeploymentSummary]


class DescribeExperimentRequest(ServiceRequest):
    ExperimentName: ExperimentEntityName


class ExperimentSource(TypedDict, total=False):
    """The source of the experiment."""

    SourceArn: ExperimentSourceArn
    SourceType: Optional[SourceType]


class DescribeExperimentResponse(TypedDict, total=False):
    ExperimentName: Optional[ExperimentEntityName]
    ExperimentArn: Optional[ExperimentArn]
    DisplayName: Optional[ExperimentEntityName]
    Source: Optional[ExperimentSource]
    Description: Optional[ExperimentDescription]
    CreationTime: Optional[Timestamp]
    CreatedBy: Optional[UserContext]
    LastModifiedTime: Optional[Timestamp]
    LastModifiedBy: Optional[UserContext]


class DescribeFeatureGroupRequest(ServiceRequest):
    FeatureGroupName: FeatureGroupName
    NextToken: Optional[NextToken]


class OfflineStoreStatus(TypedDict, total=False):
    """The status of ``OfflineStore``."""

    Status: OfflineStoreStatusValue
    BlockedReason: Optional[BlockedReason]


class DescribeFeatureGroupResponse(TypedDict, total=False):
    FeatureGroupArn: FeatureGroupArn
    FeatureGroupName: FeatureGroupName
    RecordIdentifierFeatureName: FeatureName
    EventTimeFeatureName: FeatureName
    FeatureDefinitions: FeatureDefinitions
    CreationTime: CreationTime
    OnlineStoreConfig: Optional[OnlineStoreConfig]
    OfflineStoreConfig: Optional[OfflineStoreConfig]
    RoleArn: Optional[RoleArn]
    FeatureGroupStatus: Optional[FeatureGroupStatus]
    OfflineStoreStatus: Optional[OfflineStoreStatus]
    FailureReason: Optional[FailureReason]
    Description: Optional[Description]
    NextToken: NextToken


class DescribeFlowDefinitionRequest(ServiceRequest):
    FlowDefinitionName: FlowDefinitionName


class DescribeFlowDefinitionResponse(TypedDict, total=False):
    FlowDefinitionArn: FlowDefinitionArn
    FlowDefinitionName: FlowDefinitionName
    FlowDefinitionStatus: FlowDefinitionStatus
    CreationTime: Timestamp
    HumanLoopRequestSource: Optional[HumanLoopRequestSource]
    HumanLoopActivationConfig: Optional[HumanLoopActivationConfig]
    HumanLoopConfig: HumanLoopConfig
    OutputConfig: FlowDefinitionOutputConfig
    RoleArn: RoleArn
    FailureReason: Optional[FailureReason]


class DescribeHumanTaskUiRequest(ServiceRequest):
    HumanTaskUiName: HumanTaskUiName


class UiTemplateInfo(TypedDict, total=False):
    """Container for user interface template information."""

    Url: Optional[TemplateUrl]
    ContentSha256: Optional[TemplateContentSha256]


class DescribeHumanTaskUiResponse(TypedDict, total=False):
    HumanTaskUiArn: HumanTaskUiArn
    HumanTaskUiName: HumanTaskUiName
    HumanTaskUiStatus: Optional[HumanTaskUiStatus]
    CreationTime: Timestamp
    UiTemplate: UiTemplateInfo


class DescribeHyperParameterTuningJobRequest(ServiceRequest):
    HyperParameterTuningJobName: HyperParameterTuningJobName


class FinalHyperParameterTuningJobObjectiveMetric(TypedDict, total=False):
    """Shows the final value for the objective metric for a training job that
    was launched by a hyperparameter tuning job. You define the objective
    metric in the ``HyperParameterTuningJobObjective`` parameter of
    HyperParameterTuningJobConfig.
    """

    Type: Optional[HyperParameterTuningJobObjectiveType]
    MetricName: MetricName
    Value: MetricValue


class HyperParameterTrainingJobSummary(TypedDict, total=False):
    """The container for the summary information about a training job."""

    TrainingJobDefinitionName: Optional[HyperParameterTrainingJobDefinitionName]
    TrainingJobName: TrainingJobName
    TrainingJobArn: TrainingJobArn
    TuningJobName: Optional[HyperParameterTuningJobName]
    CreationTime: Timestamp
    TrainingStartTime: Optional[Timestamp]
    TrainingEndTime: Optional[Timestamp]
    TrainingJobStatus: TrainingJobStatus
    TunedHyperParameters: HyperParameters
    FailureReason: Optional[FailureReason]
    FinalHyperParameterTuningJobObjectiveMetric: Optional[
        FinalHyperParameterTuningJobObjectiveMetric
    ]
    ObjectiveStatus: Optional[ObjectiveStatus]


class ObjectiveStatusCounters(TypedDict, total=False):
    """Specifies the number of training jobs that this hyperparameter tuning
    job launched, categorized by the status of their objective metric. The
    objective metric status shows whether the final objective metric for the
    training job has been evaluated by the tuning job and used in the
    hyperparameter tuning process.
    """

    Succeeded: Optional[ObjectiveStatusCounter]
    Pending: Optional[ObjectiveStatusCounter]
    Failed: Optional[ObjectiveStatusCounter]


class TrainingJobStatusCounters(TypedDict, total=False):
    """The numbers of training jobs launched by a hyperparameter tuning job,
    categorized by status.
    """

    Completed: Optional[TrainingJobStatusCounter]
    InProgress: Optional[TrainingJobStatusCounter]
    RetryableError: Optional[TrainingJobStatusCounter]
    NonRetryableError: Optional[TrainingJobStatusCounter]
    Stopped: Optional[TrainingJobStatusCounter]


class DescribeHyperParameterTuningJobResponse(TypedDict, total=False):
    HyperParameterTuningJobName: HyperParameterTuningJobName
    HyperParameterTuningJobArn: HyperParameterTuningJobArn
    HyperParameterTuningJobConfig: HyperParameterTuningJobConfig
    TrainingJobDefinition: Optional[HyperParameterTrainingJobDefinition]
    TrainingJobDefinitions: Optional[HyperParameterTrainingJobDefinitions]
    HyperParameterTuningJobStatus: HyperParameterTuningJobStatus
    CreationTime: Timestamp
    HyperParameterTuningEndTime: Optional[Timestamp]
    LastModifiedTime: Optional[Timestamp]
    TrainingJobStatusCounters: TrainingJobStatusCounters
    ObjectiveStatusCounters: ObjectiveStatusCounters
    BestTrainingJob: Optional[HyperParameterTrainingJobSummary]
    OverallBestTrainingJob: Optional[HyperParameterTrainingJobSummary]
    WarmStartConfig: Optional[HyperParameterTuningJobWarmStartConfig]
    FailureReason: Optional[FailureReason]


class DescribeImageRequest(ServiceRequest):
    ImageName: ImageName


class DescribeImageResponse(TypedDict, total=False):
    CreationTime: Optional[Timestamp]
    Description: Optional[ImageDescription]
    DisplayName: Optional[ImageDisplayName]
    FailureReason: Optional[FailureReason]
    ImageArn: Optional[ImageArn]
    ImageName: Optional[ImageName]
    ImageStatus: Optional[ImageStatus]
    LastModifiedTime: Optional[Timestamp]
    RoleArn: Optional[RoleArn]


class DescribeImageVersionRequest(ServiceRequest):
    ImageName: ImageName
    Version: Optional[ImageVersionNumber]


class DescribeImageVersionResponse(TypedDict, total=False):
    BaseImage: Optional[ImageBaseImage]
    ContainerImage: Optional[ImageContainerImage]
    CreationTime: Optional[Timestamp]
    FailureReason: Optional[FailureReason]
    ImageArn: Optional[ImageArn]
    ImageVersionArn: Optional[ImageVersionArn]
    ImageVersionStatus: Optional[ImageVersionStatus]
    LastModifiedTime: Optional[Timestamp]
    Version: Optional[ImageVersionNumber]


class DescribeInferenceRecommendationsJobRequest(ServiceRequest):
    JobName: RecommendationJobName


class EnvironmentParameter(TypedDict, total=False):
    """A list of environment parameters suggested by the Amazon SageMaker
    Inference Recommender.
    """

    Key: String
    ValueType: String
    Value: String


EnvironmentParameters = List[EnvironmentParameter]


class ModelConfiguration(TypedDict, total=False):
    """Defines the model configuration. Includes the specification name and
    environment parameters.
    """

    InferenceSpecificationName: Optional[InferenceSpecificationName]
    EnvironmentParameters: Optional[EnvironmentParameters]


class EndpointOutputConfiguration(TypedDict, total=False):
    """The endpoint configuration made by Inference Recommender during a
    recommendation job.
    """

    EndpointName: String
    VariantName: String
    InstanceType: ProductionVariantInstanceType
    InitialInstanceCount: Integer


class RecommendationMetrics(TypedDict, total=False):
    """The metrics of recommendations."""

    CostPerHour: Float
    CostPerInference: Float
    MaxInvocations: Integer
    ModelLatency: Integer


class InferenceRecommendation(TypedDict, total=False):
    """A list of recommendations made by Amazon SageMaker Inference
    Recommender.
    """

    Metrics: RecommendationMetrics
    EndpointConfiguration: EndpointOutputConfiguration
    ModelConfiguration: ModelConfiguration


InferenceRecommendations = List[InferenceRecommendation]


class DescribeInferenceRecommendationsJobResponse(TypedDict, total=False):
    JobName: RecommendationJobName
    JobDescription: Optional[RecommendationJobDescription]
    JobType: RecommendationJobType
    JobArn: RecommendationJobArn
    RoleArn: RoleArn
    Status: RecommendationJobStatus
    CreationTime: CreationTime
    CompletionTime: Optional[Timestamp]
    LastModifiedTime: LastModifiedTime
    FailureReason: Optional[FailureReason]
    InputConfig: RecommendationJobInputConfig
    StoppingConditions: Optional[RecommendationJobStoppingConditions]
    InferenceRecommendations: Optional[InferenceRecommendations]


class DescribeLabelingJobRequest(ServiceRequest):
    LabelingJobName: LabelingJobName


class LabelingJobOutput(TypedDict, total=False):
    """Specifies the location of the output produced by the labeling job."""

    OutputDatasetS3Uri: S3Uri
    FinalActiveLearningModelArn: Optional[ModelArn]


class LabelCounters(TypedDict, total=False):
    """Provides a breakdown of the number of objects labeled."""

    TotalLabeled: Optional[LabelCounter]
    HumanLabeled: Optional[LabelCounter]
    MachineLabeled: Optional[LabelCounter]
    FailedNonRetryableError: Optional[LabelCounter]
    Unlabeled: Optional[LabelCounter]


class DescribeLabelingJobResponse(TypedDict, total=False):
    LabelingJobStatus: LabelingJobStatus
    LabelCounters: LabelCounters
    FailureReason: Optional[FailureReason]
    CreationTime: Timestamp
    LastModifiedTime: Timestamp
    JobReferenceCode: JobReferenceCode
    LabelingJobName: LabelingJobName
    LabelingJobArn: LabelingJobArn
    LabelAttributeName: Optional[LabelAttributeName]
    InputConfig: LabelingJobInputConfig
    OutputConfig: LabelingJobOutputConfig
    RoleArn: RoleArn
    LabelCategoryConfigS3Uri: Optional[S3Uri]
    StoppingConditions: Optional[LabelingJobStoppingConditions]
    LabelingJobAlgorithmsConfig: Optional[LabelingJobAlgorithmsConfig]
    HumanTaskConfig: HumanTaskConfig
    Tags: Optional[TagList]
    LabelingJobOutput: Optional[LabelingJobOutput]


class DescribeLineageGroupRequest(ServiceRequest):
    LineageGroupName: ExperimentEntityName


class DescribeLineageGroupResponse(TypedDict, total=False):
    LineageGroupName: Optional[ExperimentEntityName]
    LineageGroupArn: Optional[LineageGroupArn]
    DisplayName: Optional[ExperimentEntityName]
    Description: Optional[ExperimentDescription]
    CreationTime: Optional[Timestamp]
    CreatedBy: Optional[UserContext]
    LastModifiedTime: Optional[Timestamp]
    LastModifiedBy: Optional[UserContext]


class DescribeModelBiasJobDefinitionRequest(ServiceRequest):
    JobDefinitionName: MonitoringJobDefinitionName


class DescribeModelBiasJobDefinitionResponse(TypedDict, total=False):
    JobDefinitionArn: MonitoringJobDefinitionArn
    JobDefinitionName: MonitoringJobDefinitionName
    CreationTime: Timestamp
    ModelBiasBaselineConfig: Optional[ModelBiasBaselineConfig]
    ModelBiasAppSpecification: ModelBiasAppSpecification
    ModelBiasJobInput: ModelBiasJobInput
    ModelBiasJobOutputConfig: MonitoringOutputConfig
    JobResources: MonitoringResources
    NetworkConfig: Optional[MonitoringNetworkConfig]
    RoleArn: RoleArn
    StoppingCondition: Optional[MonitoringStoppingCondition]


class DescribeModelExplainabilityJobDefinitionRequest(ServiceRequest):
    JobDefinitionName: MonitoringJobDefinitionName


class DescribeModelExplainabilityJobDefinitionResponse(TypedDict, total=False):
    JobDefinitionArn: MonitoringJobDefinitionArn
    JobDefinitionName: MonitoringJobDefinitionName
    CreationTime: Timestamp
    ModelExplainabilityBaselineConfig: Optional[ModelExplainabilityBaselineConfig]
    ModelExplainabilityAppSpecification: ModelExplainabilityAppSpecification
    ModelExplainabilityJobInput: ModelExplainabilityJobInput
    ModelExplainabilityJobOutputConfig: MonitoringOutputConfig
    JobResources: MonitoringResources
    NetworkConfig: Optional[MonitoringNetworkConfig]
    RoleArn: RoleArn
    StoppingCondition: Optional[MonitoringStoppingCondition]


class DescribeModelInput(ServiceRequest):
    ModelName: ModelName


class DescribeModelOutput(TypedDict, total=False):
    ModelName: ModelName
    PrimaryContainer: Optional[ContainerDefinition]
    Containers: Optional[ContainerDefinitionList]
    InferenceExecutionConfig: Optional[InferenceExecutionConfig]
    ExecutionRoleArn: RoleArn
    VpcConfig: Optional[VpcConfig]
    CreationTime: Timestamp
    ModelArn: ModelArn
    EnableNetworkIsolation: Optional[Boolean]


class DescribeModelPackageGroupInput(ServiceRequest):
    ModelPackageGroupName: ArnOrName


class DescribeModelPackageGroupOutput(TypedDict, total=False):
    ModelPackageGroupName: EntityName
    ModelPackageGroupArn: ModelPackageGroupArn
    ModelPackageGroupDescription: Optional[EntityDescription]
    CreationTime: CreationTime
    CreatedBy: UserContext
    ModelPackageGroupStatus: ModelPackageGroupStatus


class DescribeModelPackageInput(ServiceRequest):
    ModelPackageName: VersionedArnOrName


class ModelPackageStatusItem(TypedDict, total=False):
    """Represents the overall status of a model package."""

    Name: EntityName
    Status: DetailedModelPackageStatus
    FailureReason: Optional[String]


ModelPackageStatusItemList = List[ModelPackageStatusItem]


class ModelPackageStatusDetails(TypedDict, total=False):
    """Specifies the validation and image scan statuses of the model package."""

    ValidationStatuses: ModelPackageStatusItemList
    ImageScanStatuses: Optional[ModelPackageStatusItemList]


class DescribeModelPackageOutput(TypedDict, total=False):
    ModelPackageName: EntityName
    ModelPackageGroupName: Optional[EntityName]
    ModelPackageVersion: Optional[ModelPackageVersion]
    ModelPackageArn: ModelPackageArn
    ModelPackageDescription: Optional[EntityDescription]
    CreationTime: CreationTime
    InferenceSpecification: Optional[InferenceSpecification]
    SourceAlgorithmSpecification: Optional[SourceAlgorithmSpecification]
    ValidationSpecification: Optional[ModelPackageValidationSpecification]
    ModelPackageStatus: ModelPackageStatus
    ModelPackageStatusDetails: ModelPackageStatusDetails
    CertifyForMarketplace: Optional[CertifyForMarketplace]
    ModelApprovalStatus: Optional[ModelApprovalStatus]
    CreatedBy: Optional[UserContext]
    MetadataProperties: Optional[MetadataProperties]
    ModelMetrics: Optional[ModelMetrics]
    LastModifiedTime: Optional[Timestamp]
    LastModifiedBy: Optional[UserContext]
    ApprovalDescription: Optional[ApprovalDescription]
    CustomerMetadataProperties: Optional[CustomerMetadataMap]
    DriftCheckBaselines: Optional[DriftCheckBaselines]
    Domain: Optional[String]
    Task: Optional[String]
    SamplePayloadUrl: Optional[String]
    AdditionalInferenceSpecifications: Optional[AdditionalInferenceSpecifications]


class DescribeModelQualityJobDefinitionRequest(ServiceRequest):
    JobDefinitionName: MonitoringJobDefinitionName


class DescribeModelQualityJobDefinitionResponse(TypedDict, total=False):
    JobDefinitionArn: MonitoringJobDefinitionArn
    JobDefinitionName: MonitoringJobDefinitionName
    CreationTime: Timestamp
    ModelQualityBaselineConfig: Optional[ModelQualityBaselineConfig]
    ModelQualityAppSpecification: ModelQualityAppSpecification
    ModelQualityJobInput: ModelQualityJobInput
    ModelQualityJobOutputConfig: MonitoringOutputConfig
    JobResources: MonitoringResources
    NetworkConfig: Optional[MonitoringNetworkConfig]
    RoleArn: RoleArn
    StoppingCondition: Optional[MonitoringStoppingCondition]


class DescribeMonitoringScheduleRequest(ServiceRequest):
    MonitoringScheduleName: MonitoringScheduleName


class MonitoringExecutionSummary(TypedDict, total=False):
    """Summary of information about the last monitoring job to run."""

    MonitoringScheduleName: MonitoringScheduleName
    ScheduledTime: Timestamp
    CreationTime: Timestamp
    LastModifiedTime: Timestamp
    MonitoringExecutionStatus: ExecutionStatus
    ProcessingJobArn: Optional[ProcessingJobArn]
    EndpointName: Optional[EndpointName]
    FailureReason: Optional[FailureReason]
    MonitoringJobDefinitionName: Optional[MonitoringJobDefinitionName]
    MonitoringType: Optional[MonitoringType]


class DescribeMonitoringScheduleResponse(TypedDict, total=False):
    MonitoringScheduleArn: MonitoringScheduleArn
    MonitoringScheduleName: MonitoringScheduleName
    MonitoringScheduleStatus: ScheduleStatus
    MonitoringType: Optional[MonitoringType]
    FailureReason: Optional[FailureReason]
    CreationTime: Timestamp
    LastModifiedTime: Timestamp
    MonitoringScheduleConfig: MonitoringScheduleConfig
    EndpointName: Optional[EndpointName]
    LastMonitoringExecutionSummary: Optional[MonitoringExecutionSummary]


class DescribeNotebookInstanceInput(ServiceRequest):
    NotebookInstanceName: NotebookInstanceName


class DescribeNotebookInstanceLifecycleConfigInput(ServiceRequest):
    NotebookInstanceLifecycleConfigName: NotebookInstanceLifecycleConfigName


class DescribeNotebookInstanceLifecycleConfigOutput(TypedDict, total=False):
    NotebookInstanceLifecycleConfigArn: Optional[NotebookInstanceLifecycleConfigArn]
    NotebookInstanceLifecycleConfigName: Optional[NotebookInstanceLifecycleConfigName]
    OnCreate: Optional[NotebookInstanceLifecycleConfigList]
    OnStart: Optional[NotebookInstanceLifecycleConfigList]
    LastModifiedTime: Optional[LastModifiedTime]
    CreationTime: Optional[CreationTime]


class DescribeNotebookInstanceOutput(TypedDict, total=False):
    NotebookInstanceArn: Optional[NotebookInstanceArn]
    NotebookInstanceName: Optional[NotebookInstanceName]
    NotebookInstanceStatus: Optional[NotebookInstanceStatus]
    FailureReason: Optional[FailureReason]
    Url: Optional[NotebookInstanceUrl]
    InstanceType: Optional[InstanceType]
    SubnetId: Optional[SubnetId]
    SecurityGroups: Optional[SecurityGroupIds]
    RoleArn: Optional[RoleArn]
    KmsKeyId: Optional[KmsKeyId]
    NetworkInterfaceId: Optional[NetworkInterfaceId]
    LastModifiedTime: Optional[LastModifiedTime]
    CreationTime: Optional[CreationTime]
    NotebookInstanceLifecycleConfigName: Optional[NotebookInstanceLifecycleConfigName]
    DirectInternetAccess: Optional[DirectInternetAccess]
    VolumeSizeInGB: Optional[NotebookInstanceVolumeSizeInGB]
    AcceleratorTypes: Optional[NotebookInstanceAcceleratorTypes]
    DefaultCodeRepository: Optional[CodeRepositoryNameOrUrl]
    AdditionalCodeRepositories: Optional[AdditionalCodeRepositoryNamesOrUrls]
    RootAccess: Optional[RootAccess]
    PlatformIdentifier: Optional[PlatformIdentifier]


class DescribePipelineDefinitionForExecutionRequest(ServiceRequest):
    PipelineExecutionArn: PipelineExecutionArn


class DescribePipelineDefinitionForExecutionResponse(TypedDict, total=False):
    PipelineDefinition: Optional[PipelineDefinition]
    CreationTime: Optional[Timestamp]


class DescribePipelineExecutionRequest(ServiceRequest):
    PipelineExecutionArn: PipelineExecutionArn


class PipelineExperimentConfig(TypedDict, total=False):
    """Specifies the names of the experiment and trial created by a pipeline."""

    ExperimentName: Optional[ExperimentEntityName]
    TrialName: Optional[ExperimentEntityName]


class DescribePipelineExecutionResponse(TypedDict, total=False):
    PipelineArn: Optional[PipelineArn]
    PipelineExecutionArn: Optional[PipelineExecutionArn]
    PipelineExecutionDisplayName: Optional[PipelineExecutionName]
    PipelineExecutionStatus: Optional[PipelineExecutionStatus]
    PipelineExecutionDescription: Optional[PipelineExecutionDescription]
    PipelineExperimentConfig: Optional[PipelineExperimentConfig]
    FailureReason: Optional[PipelineExecutionFailureReason]
    CreationTime: Optional[Timestamp]
    LastModifiedTime: Optional[Timestamp]
    CreatedBy: Optional[UserContext]
    LastModifiedBy: Optional[UserContext]
    ParallelismConfiguration: Optional[ParallelismConfiguration]


class DescribePipelineRequest(ServiceRequest):
    PipelineName: PipelineName


class DescribePipelineResponse(TypedDict, total=False):
    PipelineArn: Optional[PipelineArn]
    PipelineName: Optional[PipelineName]
    PipelineDisplayName: Optional[PipelineName]
    PipelineDefinition: Optional[PipelineDefinition]
    PipelineDescription: Optional[PipelineDescription]
    RoleArn: Optional[RoleArn]
    PipelineStatus: Optional[PipelineStatus]
    CreationTime: Optional[Timestamp]
    LastModifiedTime: Optional[Timestamp]
    LastRunTime: Optional[Timestamp]
    CreatedBy: Optional[UserContext]
    LastModifiedBy: Optional[UserContext]
    ParallelismConfiguration: Optional[ParallelismConfiguration]


class DescribeProcessingJobRequest(ServiceRequest):
    ProcessingJobName: ProcessingJobName


class DescribeProcessingJobResponse(TypedDict, total=False):
    ProcessingInputs: Optional[ProcessingInputs]
    ProcessingOutputConfig: Optional[ProcessingOutputConfig]
    ProcessingJobName: ProcessingJobName
    ProcessingResources: ProcessingResources
    StoppingCondition: Optional[ProcessingStoppingCondition]
    AppSpecification: AppSpecification
    Environment: Optional[ProcessingEnvironmentMap]
    NetworkConfig: Optional[NetworkConfig]
    RoleArn: Optional[RoleArn]
    ExperimentConfig: Optional[ExperimentConfig]
    ProcessingJobArn: ProcessingJobArn
    ProcessingJobStatus: ProcessingJobStatus
    ExitMessage: Optional[ExitMessage]
    FailureReason: Optional[FailureReason]
    ProcessingEndTime: Optional[Timestamp]
    ProcessingStartTime: Optional[Timestamp]
    LastModifiedTime: Optional[Timestamp]
    CreationTime: Timestamp
    MonitoringScheduleArn: Optional[MonitoringScheduleArn]
    AutoMLJobArn: Optional[AutoMLJobArn]
    TrainingJobArn: Optional[TrainingJobArn]


class DescribeProjectInput(ServiceRequest):
    ProjectName: ProjectEntityName


class ServiceCatalogProvisionedProductDetails(TypedDict, total=False):
    """Details of a provisioned service catalog product. For information about
    service catalog, see `What is Amazon Web Services Service
    Catalog <https://docs.aws.amazon.com/servicecatalog/latest/adminguide/introduction.html>`__.
    """

    ProvisionedProductId: Optional[ServiceCatalogEntityId]
    ProvisionedProductStatusMessage: Optional[ProvisionedProductStatusMessage]


class DescribeProjectOutput(TypedDict, total=False):
    ProjectArn: ProjectArn
    ProjectName: ProjectEntityName
    ProjectId: ProjectId
    ProjectDescription: Optional[EntityDescription]
    ServiceCatalogProvisioningDetails: ServiceCatalogProvisioningDetails
    ServiceCatalogProvisionedProductDetails: Optional[ServiceCatalogProvisionedProductDetails]
    ProjectStatus: ProjectStatus
    CreatedBy: Optional[UserContext]
    CreationTime: Timestamp
    LastModifiedTime: Optional[Timestamp]
    LastModifiedBy: Optional[UserContext]


class DescribeStudioLifecycleConfigRequest(ServiceRequest):
    StudioLifecycleConfigName: StudioLifecycleConfigName


class DescribeStudioLifecycleConfigResponse(TypedDict, total=False):
    StudioLifecycleConfigArn: Optional[StudioLifecycleConfigArn]
    StudioLifecycleConfigName: Optional[StudioLifecycleConfigName]
    CreationTime: Optional[Timestamp]
    LastModifiedTime: Optional[Timestamp]
    StudioLifecycleConfigContent: Optional[StudioLifecycleConfigContent]
    StudioLifecycleConfigAppType: Optional[StudioLifecycleConfigAppType]


class DescribeSubscribedWorkteamRequest(ServiceRequest):
    WorkteamArn: WorkteamArn


class SubscribedWorkteam(TypedDict, total=False):
    """Describes a work team of a vendor that does the a labelling job."""

    WorkteamArn: WorkteamArn
    MarketplaceTitle: Optional[String200]
    SellerName: Optional[String]
    MarketplaceDescription: Optional[String200]
    ListingId: Optional[String]


class DescribeSubscribedWorkteamResponse(TypedDict, total=False):
    SubscribedWorkteam: SubscribedWorkteam


class DescribeTrainingJobRequest(ServiceRequest):
    TrainingJobName: TrainingJobName


class ProfilerRuleEvaluationStatus(TypedDict, total=False):
    """Information about the status of the rule evaluation."""

    RuleConfigurationName: Optional[RuleConfigurationName]
    RuleEvaluationJobArn: Optional[ProcessingJobArn]
    RuleEvaluationStatus: Optional[RuleEvaluationStatus]
    StatusDetails: Optional[StatusDetails]
    LastModifiedTime: Optional[Timestamp]


ProfilerRuleEvaluationStatuses = List[ProfilerRuleEvaluationStatus]


class MetricData(TypedDict, total=False):
    """The name, value, and date and time of a metric that was emitted to
    Amazon CloudWatch.
    """

    MetricName: Optional[MetricName]
    Value: Optional[Float]
    Timestamp: Optional[Timestamp]


FinalMetricDataList = List[MetricData]


class SecondaryStatusTransition(TypedDict, total=False):
    """An array element of
    DescribeTrainingJobResponse$SecondaryStatusTransitions. It provides
    additional details about a status that the training job has transitioned
    through. A training job can be in one of several states, for example,
    starting, downloading, training, or uploading. Within each state, there
    are a number of intermediate states. For example, within the starting
    state, SageMaker could be starting the training job or launching the ML
    instances. These transitional states are referred to as the job's
    secondary status.
    """

    Status: SecondaryStatus
    StartTime: Timestamp
    EndTime: Optional[Timestamp]
    StatusMessage: Optional[StatusMessage]


SecondaryStatusTransitions = List[SecondaryStatusTransition]


class DescribeTrainingJobResponse(TypedDict, total=False):
    TrainingJobName: TrainingJobName
    TrainingJobArn: TrainingJobArn
    TuningJobArn: Optional[HyperParameterTuningJobArn]
    LabelingJobArn: Optional[LabelingJobArn]
    AutoMLJobArn: Optional[AutoMLJobArn]
    ModelArtifacts: ModelArtifacts
    TrainingJobStatus: TrainingJobStatus
    SecondaryStatus: SecondaryStatus
    FailureReason: Optional[FailureReason]
    HyperParameters: Optional[HyperParameters]
    AlgorithmSpecification: AlgorithmSpecification
    RoleArn: Optional[RoleArn]
    InputDataConfig: Optional[InputDataConfig]
    OutputDataConfig: Optional[OutputDataConfig]
    ResourceConfig: ResourceConfig
    VpcConfig: Optional[VpcConfig]
    StoppingCondition: StoppingCondition
    CreationTime: Timestamp
    TrainingStartTime: Optional[Timestamp]
    TrainingEndTime: Optional[Timestamp]
    LastModifiedTime: Optional[Timestamp]
    SecondaryStatusTransitions: Optional[SecondaryStatusTransitions]
    FinalMetricDataList: Optional[FinalMetricDataList]
    EnableNetworkIsolation: Optional[Boolean]
    EnableInterContainerTrafficEncryption: Optional[Boolean]
    EnableManagedSpotTraining: Optional[Boolean]
    CheckpointConfig: Optional[CheckpointConfig]
    TrainingTimeInSeconds: Optional[TrainingTimeInSeconds]
    BillableTimeInSeconds: Optional[BillableTimeInSeconds]
    DebugHookConfig: Optional[DebugHookConfig]
    ExperimentConfig: Optional[ExperimentConfig]
    DebugRuleConfigurations: Optional[DebugRuleConfigurations]
    TensorBoardOutputConfig: Optional[TensorBoardOutputConfig]
    DebugRuleEvaluationStatuses: Optional[DebugRuleEvaluationStatuses]
    ProfilerConfig: Optional[ProfilerConfig]
    ProfilerRuleConfigurations: Optional[ProfilerRuleConfigurations]
    ProfilerRuleEvaluationStatuses: Optional[ProfilerRuleEvaluationStatuses]
    ProfilingStatus: Optional[ProfilingStatus]
    RetryStrategy: Optional[RetryStrategy]
    Environment: Optional[TrainingEnvironmentMap]


class DescribeTransformJobRequest(ServiceRequest):
    TransformJobName: TransformJobName


class DescribeTransformJobResponse(TypedDict, total=False):
    TransformJobName: TransformJobName
    TransformJobArn: TransformJobArn
    TransformJobStatus: TransformJobStatus
    FailureReason: Optional[FailureReason]
    ModelName: ModelName
    MaxConcurrentTransforms: Optional[MaxConcurrentTransforms]
    ModelClientConfig: Optional[ModelClientConfig]
    MaxPayloadInMB: Optional[MaxPayloadInMB]
    BatchStrategy: Optional[BatchStrategy]
    Environment: Optional[TransformEnvironmentMap]
    TransformInput: TransformInput
    TransformOutput: Optional[TransformOutput]
    TransformResources: TransformResources
    CreationTime: Timestamp
    TransformStartTime: Optional[Timestamp]
    TransformEndTime: Optional[Timestamp]
    LabelingJobArn: Optional[LabelingJobArn]
    AutoMLJobArn: Optional[AutoMLJobArn]
    DataProcessing: Optional[DataProcessing]
    ExperimentConfig: Optional[ExperimentConfig]


class DescribeTrialComponentRequest(ServiceRequest):
    TrialComponentName: ExperimentEntityNameOrArn


class TrialComponentMetricSummary(TypedDict, total=False):
    """A summary of the metrics of a trial component."""

    MetricName: Optional[MetricName]
    SourceArn: Optional[TrialComponentSourceArn]
    TimeStamp: Optional[Timestamp]
    Max: Optional[OptionalDouble]
    Min: Optional[OptionalDouble]
    Last: Optional[OptionalDouble]
    Count: Optional[OptionalInteger]
    Avg: Optional[OptionalDouble]
    StdDev: Optional[OptionalDouble]


TrialComponentMetricSummaries = List[TrialComponentMetricSummary]


class TrialComponentSource(TypedDict, total=False):
    """The Amazon Resource Name (ARN) and job type of the source of a trial
    component.
    """

    SourceArn: TrialComponentSourceArn
    SourceType: Optional[SourceType]


class DescribeTrialComponentResponse(TypedDict, total=False):
    TrialComponentName: Optional[ExperimentEntityName]
    TrialComponentArn: Optional[TrialComponentArn]
    DisplayName: Optional[ExperimentEntityName]
    Source: Optional[TrialComponentSource]
    Status: Optional[TrialComponentStatus]
    StartTime: Optional[Timestamp]
    EndTime: Optional[Timestamp]
    CreationTime: Optional[Timestamp]
    CreatedBy: Optional[UserContext]
    LastModifiedTime: Optional[Timestamp]
    LastModifiedBy: Optional[UserContext]
    Parameters: Optional[TrialComponentParameters]
    InputArtifacts: Optional[TrialComponentArtifacts]
    OutputArtifacts: Optional[TrialComponentArtifacts]
    MetadataProperties: Optional[MetadataProperties]
    Metrics: Optional[TrialComponentMetricSummaries]
    LineageGroupArn: Optional[LineageGroupArn]


class DescribeTrialRequest(ServiceRequest):
    TrialName: ExperimentEntityName


class TrialSource(TypedDict, total=False):
    """The source of the trial."""

    SourceArn: TrialSourceArn
    SourceType: Optional[SourceType]


class DescribeTrialResponse(TypedDict, total=False):
    TrialName: Optional[ExperimentEntityName]
    TrialArn: Optional[TrialArn]
    DisplayName: Optional[ExperimentEntityName]
    ExperimentName: Optional[ExperimentEntityName]
    Source: Optional[TrialSource]
    CreationTime: Optional[Timestamp]
    CreatedBy: Optional[UserContext]
    LastModifiedTime: Optional[Timestamp]
    LastModifiedBy: Optional[UserContext]
    MetadataProperties: Optional[MetadataProperties]


class DescribeUserProfileRequest(ServiceRequest):
    DomainId: DomainId
    UserProfileName: UserProfileName


class DescribeUserProfileResponse(TypedDict, total=False):
    DomainId: Optional[DomainId]
    UserProfileArn: Optional[UserProfileArn]
    UserProfileName: Optional[UserProfileName]
    HomeEfsFileSystemUid: Optional[EfsUid]
    Status: Optional[UserProfileStatus]
    LastModifiedTime: Optional[LastModifiedTime]
    CreationTime: Optional[CreationTime]
    FailureReason: Optional[FailureReason]
    SingleSignOnUserIdentifier: Optional[SingleSignOnUserIdentifier]
    SingleSignOnUserValue: Optional[String256]
    UserSettings: Optional[UserSettings]


class DescribeWorkforceRequest(ServiceRequest):
    WorkforceName: WorkforceName


class OidcConfigForResponse(TypedDict, total=False):
    """Your OIDC IdP workforce configuration."""

    ClientId: Optional[ClientId]
    Issuer: Optional[OidcEndpoint]
    AuthorizationEndpoint: Optional[OidcEndpoint]
    TokenEndpoint: Optional[OidcEndpoint]
    UserInfoEndpoint: Optional[OidcEndpoint]
    LogoutEndpoint: Optional[OidcEndpoint]
    JwksUri: Optional[OidcEndpoint]


class Workforce(TypedDict, total=False):
    """A single private workforce, which is automatically created when you
    create your first private work team. You can create one private work
    force in each Amazon Web Services Region. By default, any
    workforce-related API operation used in a specific region will apply to
    the workforce created in that region. To learn how to create a private
    workforce, see `Create a Private
    Workforce <https://docs.aws.amazon.com/sagemaker/latest/dg/sms-workforce-create-private.html>`__.
    """

    WorkforceName: WorkforceName
    WorkforceArn: WorkforceArn
    LastUpdatedDate: Optional[Timestamp]
    SourceIpConfig: Optional[SourceIpConfig]
    SubDomain: Optional[String]
    CognitoConfig: Optional[CognitoConfig]
    OidcConfig: Optional[OidcConfigForResponse]
    CreateDate: Optional[Timestamp]


class DescribeWorkforceResponse(TypedDict, total=False):
    Workforce: Workforce


class DescribeWorkteamRequest(ServiceRequest):
    WorkteamName: WorkteamName


ProductListings = List[String]


class Workteam(TypedDict, total=False):
    """Provides details about a labeling work team."""

    WorkteamName: WorkteamName
    MemberDefinitions: MemberDefinitions
    WorkteamArn: WorkteamArn
    WorkforceArn: Optional[WorkforceArn]
    ProductListingIds: Optional[ProductListings]
    Description: String200
    SubDomain: Optional[String]
    CreateDate: Optional[Timestamp]
    LastUpdatedDate: Optional[Timestamp]
    NotificationConfiguration: Optional[NotificationConfiguration]


class DescribeWorkteamResponse(TypedDict, total=False):
    Workteam: Workteam


class DesiredWeightAndCapacity(TypedDict, total=False):
    """Specifies weight and capacity values for a production variant."""

    VariantName: VariantName
    DesiredWeight: Optional[VariantWeight]
    DesiredInstanceCount: Optional[TaskCount]


DesiredWeightAndCapacityList = List[DesiredWeightAndCapacity]


class Device(TypedDict, total=False):
    """Information of a particular device."""

    DeviceName: DeviceName
    Description: Optional[DeviceDescription]
    IotThingName: Optional[ThingName]


class DeviceFleetSummary(TypedDict, total=False):
    """Summary of the device fleet."""

    DeviceFleetArn: DeviceFleetArn
    DeviceFleetName: EntityName
    CreationTime: Optional[Timestamp]
    LastModifiedTime: Optional[Timestamp]


DeviceFleetSummaries = List[DeviceFleetSummary]


class DeviceStats(TypedDict, total=False):
    """Status of devices."""

    ConnectedDeviceCount: Long
    RegisteredDeviceCount: Long


class EdgeModelSummary(TypedDict, total=False):
    """Summary of model on edge device."""

    ModelName: EntityName
    ModelVersion: EdgeVersion


EdgeModelSummaries = List[EdgeModelSummary]


class DeviceSummary(TypedDict, total=False):
    """Summary of the device."""

    DeviceName: EntityName
    DeviceArn: DeviceArn
    Description: Optional[DeviceDescription]
    DeviceFleetName: Optional[EntityName]
    IotThingName: Optional[ThingName]
    RegistrationTime: Optional[Timestamp]
    LatestHeartbeat: Optional[Timestamp]
    Models: Optional[EdgeModelSummaries]
    AgentVersion: Optional[EdgeVersion]


DeviceSummaries = List[DeviceSummary]
Devices = List[Device]


class DisableSagemakerServicecatalogPortfolioInput(ServiceRequest):
    pass


class DisableSagemakerServicecatalogPortfolioOutput(TypedDict, total=False):
    pass


class DisassociateTrialComponentRequest(ServiceRequest):
    TrialComponentName: ExperimentEntityName
    TrialName: ExperimentEntityName


class DisassociateTrialComponentResponse(TypedDict, total=False):
    TrialComponentArn: Optional[TrialComponentArn]
    TrialArn: Optional[TrialArn]


class DomainDetails(TypedDict, total=False):
    """The domain's details."""

    DomainArn: Optional[DomainArn]
    DomainId: Optional[DomainId]
    DomainName: Optional[DomainName]
    Status: Optional[DomainStatus]
    CreationTime: Optional[CreationTime]
    LastModifiedTime: Optional[LastModifiedTime]
    Url: Optional[String1024]


DomainList = List[DomainDetails]


class RStudioServerProDomainSettingsForUpdate(TypedDict, total=False):
    """A collection of settings that update the current configuration for the
    ``RStudioServerPro`` Domain-level app.
    """

    DomainExecutionRoleArn: RoleArn
    DefaultResourceSpec: Optional[ResourceSpec]


class DomainSettingsForUpdate(TypedDict, total=False):
    """A collection of ``Domain`` configuration settings to update."""

    RStudioServerProDomainSettingsForUpdate: Optional[RStudioServerProDomainSettingsForUpdate]


class EMRStepMetadata(TypedDict, total=False):
    """The configurations and outcomes of an Amazon EMR step execution."""

    ClusterId: Optional[String256]
    StepId: Optional[String256]
    StepName: Optional[String256]
    LogFilePath: Optional[String1024]


class Edge(TypedDict, total=False):
    """A directed edge connecting two lineage entities."""

    SourceArn: Optional[AssociationEntityArn]
    DestinationArn: Optional[AssociationEntityArn]
    AssociationType: Optional[AssociationEdgeType]


class EdgeModelStat(TypedDict, total=False):
    """Status of edge devices with this model."""

    ModelName: EntityName
    ModelVersion: EdgeVersion
    OfflineDeviceCount: Long
    ConnectedDeviceCount: Long
    ActiveDeviceCount: Long
    SamplingDeviceCount: Long


EdgeModelStats = List[EdgeModelStat]


class EdgePackagingJobSummary(TypedDict, total=False):
    """Summary of edge packaging job."""

    EdgePackagingJobArn: EdgePackagingJobArn
    EdgePackagingJobName: EntityName
    EdgePackagingJobStatus: EdgePackagingJobStatus
    CompilationJobName: Optional[EntityName]
    ModelName: Optional[EntityName]
    ModelVersion: Optional[EdgeVersion]
    CreationTime: Optional[Timestamp]
    LastModifiedTime: Optional[Timestamp]


EdgePackagingJobSummaries = List[EdgePackagingJobSummary]
Edges = List[Edge]


class EnableSagemakerServicecatalogPortfolioInput(ServiceRequest):
    pass


class EnableSagemakerServicecatalogPortfolioOutput(TypedDict, total=False):
    pass


class MonitoringSchedule(TypedDict, total=False):
    """A schedule for a model monitoring job. For information about model
    monitor, see `Amazon SageMaker Model
    Monitor <https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html>`__.
    """

    MonitoringScheduleArn: Optional[MonitoringScheduleArn]
    MonitoringScheduleName: Optional[MonitoringScheduleName]
    MonitoringScheduleStatus: Optional[ScheduleStatus]
    MonitoringType: Optional[MonitoringType]
    FailureReason: Optional[FailureReason]
    CreationTime: Optional[Timestamp]
    LastModifiedTime: Optional[Timestamp]
    MonitoringScheduleConfig: Optional[MonitoringScheduleConfig]
    EndpointName: Optional[EndpointName]
    LastMonitoringExecutionSummary: Optional[MonitoringExecutionSummary]
    Tags: Optional[TagList]


MonitoringScheduleList = List[MonitoringSchedule]


class Endpoint(TypedDict, total=False):
    """A hosted endpoint for real-time inference."""

    EndpointName: EndpointName
    EndpointArn: EndpointArn
    EndpointConfigName: EndpointConfigName
    ProductionVariants: Optional[ProductionVariantSummaryList]
    DataCaptureConfig: Optional[DataCaptureConfigSummary]
    EndpointStatus: EndpointStatus
    FailureReason: Optional[FailureReason]
    CreationTime: Timestamp
    LastModifiedTime: Timestamp
    MonitoringSchedules: Optional[MonitoringScheduleList]
    Tags: Optional[TagList]


class EndpointConfigSummary(TypedDict, total=False):
    """Provides summary information for an endpoint configuration."""

    EndpointConfigName: EndpointConfigName
    EndpointConfigArn: EndpointConfigArn
    CreationTime: Timestamp


EndpointConfigSummaryList = List[EndpointConfigSummary]


class EndpointSummary(TypedDict, total=False):
    """Provides summary information for an endpoint."""

    EndpointName: EndpointName
    EndpointArn: EndpointArn
    CreationTime: Timestamp
    LastModifiedTime: Timestamp
    EndpointStatus: EndpointStatus


EndpointSummaryList = List[EndpointSummary]


class Experiment(TypedDict, total=False):
    """The properties of an experiment as returned by the Search API."""

    ExperimentName: Optional[ExperimentEntityName]
    ExperimentArn: Optional[ExperimentArn]
    DisplayName: Optional[ExperimentEntityName]
    Source: Optional[ExperimentSource]
    Description: Optional[ExperimentDescription]
    CreationTime: Optional[Timestamp]
    CreatedBy: Optional[UserContext]
    LastModifiedTime: Optional[Timestamp]
    LastModifiedBy: Optional[UserContext]
    Tags: Optional[TagList]


class ExperimentSummary(TypedDict, total=False):
    """A summary of the properties of an experiment. To get the complete set of
    properties, call the DescribeExperiment API and provide the
    ``ExperimentName``.
    """

    ExperimentArn: Optional[ExperimentArn]
    ExperimentName: Optional[ExperimentEntityName]
    DisplayName: Optional[ExperimentEntityName]
    ExperimentSource: Optional[ExperimentSource]
    CreationTime: Optional[Timestamp]
    LastModifiedTime: Optional[Timestamp]


ExperimentSummaries = List[ExperimentSummary]


class FailStepMetadata(TypedDict, total=False):
    """The container for the metadata for Fail step."""

    ErrorMessage: Optional[String3072]


class FeatureGroup(TypedDict, total=False):
    """Amazon SageMaker Feature Store stores features in a collection called
    Feature Group. A Feature Group can be visualized as a table which has
    rows, with a unique identifier for each row where each column in the
    table is a feature. In principle, a Feature Group is composed of
    features and values per features.
    """

    FeatureGroupArn: Optional[FeatureGroupArn]
    FeatureGroupName: Optional[FeatureGroupName]
    RecordIdentifierFeatureName: Optional[FeatureName]
    EventTimeFeatureName: Optional[FeatureName]
    FeatureDefinitions: Optional[FeatureDefinitions]
    CreationTime: Optional[CreationTime]
    OnlineStoreConfig: Optional[OnlineStoreConfig]
    OfflineStoreConfig: Optional[OfflineStoreConfig]
    RoleArn: Optional[RoleArn]
    FeatureGroupStatus: Optional[FeatureGroupStatus]
    OfflineStoreStatus: Optional[OfflineStoreStatus]
    FailureReason: Optional[FailureReason]
    Description: Optional[Description]
    Tags: Optional[TagList]


class FeatureGroupSummary(TypedDict, total=False):
    """The name, Arn, ``CreationTime``, ``FeatureGroup`` values,
    ``LastUpdatedTime`` and ``EnableOnlineStorage`` status of a
    ``FeatureGroup``.
    """

    FeatureGroupName: FeatureGroupName
    FeatureGroupArn: FeatureGroupArn
    CreationTime: Timestamp
    FeatureGroupStatus: Optional[FeatureGroupStatus]
    OfflineStoreStatus: Optional[OfflineStoreStatus]


FeatureGroupSummaries = List[FeatureGroupSummary]


class Filter(TypedDict, total=False):
    """A conditional statement for a search expression that includes a resource
    property, a Boolean operator, and a value. Resources that match the
    statement are returned in the results from the Search API.

    If you specify a ``Value``, but not an ``Operator``, Amazon SageMaker
    uses the equals operator.

    In search, there are several property types:

    Metrics
       To define a metric filter, enter a value using the form
       ``"Metrics.<name>"``, where ``<name>`` is a metric name. For example,
       the following filter searches for training jobs with an
       ``"accuracy"`` metric greater than ``"0.9"``:

       ``{``

       ``"Name": "Metrics.accuracy",``

       ``"Operator": "GreaterThan",``

       ``"Value": "0.9"``

       ``}``

    HyperParameters
       To define a hyperparameter filter, enter a value with the form
       ``"HyperParameters.<name>"``. Decimal hyperparameter values are
       treated as a decimal in a comparison if the specified ``Value`` is
       also a decimal value. If the specified ``Value`` is an integer, the
       decimal hyperparameter values are treated as integers. For example,
       the following filter is satisfied by training jobs with a
       ``"learning_rate"`` hyperparameter that is less than ``"0.5"``:

       ``{``

       ``"Name": "HyperParameters.learning_rate",``

       ``"Operator": "LessThan",``

       ``"Value": "0.5"``

       ``}``

    Tags
       To define a tag filter, enter a value with the form ``Tags.<key>``.
    """

    Name: ResourcePropertyName
    Operator: Optional[Operator]
    Value: Optional[FilterValue]


FilterList = List[Filter]


class FlowDefinitionSummary(TypedDict, total=False):
    """Contains summary information about the flow definition."""

    FlowDefinitionName: FlowDefinitionName
    FlowDefinitionArn: FlowDefinitionArn
    FlowDefinitionStatus: FlowDefinitionStatus
    CreationTime: Timestamp
    FailureReason: Optional[FailureReason]


FlowDefinitionSummaries = List[FlowDefinitionSummary]


class GetDeviceFleetReportRequest(ServiceRequest):
    DeviceFleetName: EntityName


class GetDeviceFleetReportResponse(TypedDict, total=False):
    DeviceFleetArn: DeviceFleetArn
    DeviceFleetName: EntityName
    OutputConfig: Optional[EdgeOutputConfig]
    Description: Optional[DeviceFleetDescription]
    ReportGenerated: Optional[Timestamp]
    DeviceStats: Optional[DeviceStats]
    AgentVersions: Optional[AgentVersions]
    ModelStats: Optional[EdgeModelStats]


class GetLineageGroupPolicyRequest(ServiceRequest):
    LineageGroupName: LineageGroupNameOrArn


class GetLineageGroupPolicyResponse(TypedDict, total=False):
    LineageGroupArn: Optional[LineageGroupArn]
    ResourcePolicy: Optional[ResourcePolicyString]


class GetModelPackageGroupPolicyInput(ServiceRequest):
    ModelPackageGroupName: EntityName


class GetModelPackageGroupPolicyOutput(TypedDict, total=False):
    ResourcePolicy: PolicyString


class GetSagemakerServicecatalogPortfolioStatusInput(ServiceRequest):
    pass


class GetSagemakerServicecatalogPortfolioStatusOutput(TypedDict, total=False):
    Status: Optional[SagemakerServicecatalogStatus]


class PropertyNameQuery(TypedDict, total=False):
    """Part of the ``SuggestionQuery`` type. Specifies a hint for retrieving
    property names that begin with the specified text.
    """

    PropertyNameHint: PropertyNameHint


class SuggestionQuery(TypedDict, total=False):
    """Specified in the GetSearchSuggestions request. Limits the property names
    that are included in the response.
    """

    PropertyNameQuery: Optional[PropertyNameQuery]


class GetSearchSuggestionsRequest(ServiceRequest):
    Resource: ResourceType
    SuggestionQuery: Optional[SuggestionQuery]


class PropertyNameSuggestion(TypedDict, total=False):
    """A property name returned from a ``GetSearchSuggestions`` call that
    specifies a value in the ``PropertyNameQuery`` field.
    """

    PropertyName: Optional[ResourcePropertyName]


PropertyNameSuggestionList = List[PropertyNameSuggestion]


class GetSearchSuggestionsResponse(TypedDict, total=False):
    PropertyNameSuggestions: Optional[PropertyNameSuggestionList]


class GitConfigForUpdate(TypedDict, total=False):
    """Specifies configuration details for a Git repository when the repository
    is updated.
    """

    SecretArn: Optional[SecretArn]


class HumanTaskUiSummary(TypedDict, total=False):
    """Container for human task user interface information."""

    HumanTaskUiName: HumanTaskUiName
    HumanTaskUiArn: HumanTaskUiArn
    CreationTime: Timestamp


HumanTaskUiSummaries = List[HumanTaskUiSummary]
HyperParameterTrainingJobSummaries = List[HyperParameterTrainingJobSummary]


class HyperParameterTuningJobSummary(TypedDict, total=False):
    """Provides summary information about a hyperparameter tuning job."""

    HyperParameterTuningJobName: HyperParameterTuningJobName
    HyperParameterTuningJobArn: HyperParameterTuningJobArn
    HyperParameterTuningJobStatus: HyperParameterTuningJobStatus
    Strategy: HyperParameterTuningJobStrategyType
    CreationTime: Timestamp
    HyperParameterTuningEndTime: Optional[Timestamp]
    LastModifiedTime: Optional[Timestamp]
    TrainingJobStatusCounters: TrainingJobStatusCounters
    ObjectiveStatusCounters: ObjectiveStatusCounters
    ResourceLimits: Optional[ResourceLimits]


HyperParameterTuningJobSummaries = List[HyperParameterTuningJobSummary]


class Image(TypedDict, total=False):
    """A SageMaker image. A SageMaker image represents a set of container
    images that are derived from a common base container image. Each of
    these container images is represented by a SageMaker ``ImageVersion``.
    """

    CreationTime: Timestamp
    Description: Optional[ImageDescription]
    DisplayName: Optional[ImageDisplayName]
    FailureReason: Optional[FailureReason]
    ImageArn: ImageArn
    ImageName: ImageName
    ImageStatus: ImageStatus
    LastModifiedTime: Timestamp


ImageDeletePropertyList = List[ImageDeleteProperty]


class ImageVersion(TypedDict, total=False):
    """A version of a SageMaker ``Image``. A version represents an existing
    container image.
    """

    CreationTime: Timestamp
    FailureReason: Optional[FailureReason]
    ImageArn: ImageArn
    ImageVersionArn: ImageVersionArn
    ImageVersionStatus: ImageVersionStatus
    LastModifiedTime: Timestamp
    Version: ImageVersionNumber


ImageVersions = List[ImageVersion]
Images = List[Image]


class InferenceRecommendationsJob(TypedDict, total=False):
    """A structure that contains a list of recommendation jobs."""

    JobName: RecommendationJobName
    JobDescription: RecommendationJobDescription
    JobType: RecommendationJobType
    JobArn: RecommendationJobArn
    Status: RecommendationJobStatus
    CreationTime: CreationTime
    CompletionTime: Optional[Timestamp]
    RoleArn: RoleArn
    LastModifiedTime: LastModifiedTime
    FailureReason: Optional[FailureReason]


InferenceRecommendationsJobs = List[InferenceRecommendationsJob]


class LabelCountersForWorkteam(TypedDict, total=False):
    """Provides counts for human-labeled tasks in the labeling job."""

    HumanLabeled: Optional[LabelCounter]
    PendingHuman: Optional[LabelCounter]
    Total: Optional[LabelCounter]


class LabelingJobForWorkteamSummary(TypedDict, total=False):
    """Provides summary information for a work team."""

    LabelingJobName: Optional[LabelingJobName]
    JobReferenceCode: JobReferenceCode
    WorkRequesterAccountId: AccountId
    CreationTime: Timestamp
    LabelCounters: Optional[LabelCountersForWorkteam]
    NumberOfHumanWorkersPerDataObject: Optional[NumberOfHumanWorkersPerDataObject]


LabelingJobForWorkteamSummaryList = List[LabelingJobForWorkteamSummary]


class LabelingJobSummary(TypedDict, total=False):
    """Provides summary information about a labeling job."""

    LabelingJobName: LabelingJobName
    LabelingJobArn: LabelingJobArn
    CreationTime: Timestamp
    LastModifiedTime: Timestamp
    LabelingJobStatus: LabelingJobStatus
    LabelCounters: LabelCounters
    WorkteamArn: WorkteamArn
    PreHumanTaskLambdaArn: LambdaFunctionArn
    AnnotationConsolidationLambdaArn: Optional[LambdaFunctionArn]
    FailureReason: Optional[FailureReason]
    LabelingJobOutput: Optional[LabelingJobOutput]
    InputConfig: Optional[LabelingJobInputConfig]


LabelingJobSummaryList = List[LabelingJobSummary]


class LambdaStepMetadata(TypedDict, total=False):
    """Metadata for a Lambda step."""

    Arn: Optional[String256]
    OutputParameters: Optional[OutputParameterList]


class LineageGroupSummary(TypedDict, total=False):
    """Lists a summary of the properties of a lineage group. A lineage group
    provides a group of shareable lineage entity resources.
    """

    LineageGroupArn: Optional[LineageGroupArn]
    LineageGroupName: Optional[ExperimentEntityName]
    DisplayName: Optional[ExperimentEntityName]
    CreationTime: Optional[Timestamp]
    LastModifiedTime: Optional[Timestamp]


LineageGroupSummaries = List[LineageGroupSummary]


class ListActionsRequest(ServiceRequest):
    SourceUri: Optional[SourceUri]
    ActionType: Optional[String256]
    CreatedAfter: Optional[Timestamp]
    CreatedBefore: Optional[Timestamp]
    SortBy: Optional[SortActionsBy]
    SortOrder: Optional[SortOrder]
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]


class ListActionsResponse(TypedDict, total=False):
    ActionSummaries: Optional[ActionSummaries]
    NextToken: Optional[NextToken]


class ListAlgorithmsInput(ServiceRequest):
    CreationTimeAfter: Optional[CreationTime]
    CreationTimeBefore: Optional[CreationTime]
    MaxResults: Optional[MaxResults]
    NameContains: Optional[NameContains]
    NextToken: Optional[NextToken]
    SortBy: Optional[AlgorithmSortBy]
    SortOrder: Optional[SortOrder]


class ListAlgorithmsOutput(TypedDict, total=False):
    AlgorithmSummaryList: AlgorithmSummaryList
    NextToken: Optional[NextToken]


class ListAppImageConfigsRequest(ServiceRequest):
    MaxResults: Optional[MaxResults]
    NextToken: Optional[NextToken]
    NameContains: Optional[AppImageConfigName]
    CreationTimeBefore: Optional[Timestamp]
    CreationTimeAfter: Optional[Timestamp]
    ModifiedTimeBefore: Optional[Timestamp]
    ModifiedTimeAfter: Optional[Timestamp]
    SortBy: Optional[AppImageConfigSortKey]
    SortOrder: Optional[SortOrder]


class ListAppImageConfigsResponse(TypedDict, total=False):
    NextToken: Optional[NextToken]
    AppImageConfigs: Optional[AppImageConfigList]


class ListAppsRequest(ServiceRequest):
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]
    SortOrder: Optional[SortOrder]
    SortBy: Optional[AppSortKey]
    DomainIdEquals: Optional[DomainId]
    UserProfileNameEquals: Optional[UserProfileName]


class ListAppsResponse(TypedDict, total=False):
    Apps: Optional[AppList]
    NextToken: Optional[NextToken]


class ListArtifactsRequest(ServiceRequest):
    SourceUri: Optional[SourceUri]
    ArtifactType: Optional[String256]
    CreatedAfter: Optional[Timestamp]
    CreatedBefore: Optional[Timestamp]
    SortBy: Optional[SortArtifactsBy]
    SortOrder: Optional[SortOrder]
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]


class ListArtifactsResponse(TypedDict, total=False):
    ArtifactSummaries: Optional[ArtifactSummaries]
    NextToken: Optional[NextToken]


class ListAssociationsRequest(ServiceRequest):
    SourceArn: Optional[AssociationEntityArn]
    DestinationArn: Optional[AssociationEntityArn]
    SourceType: Optional[String256]
    DestinationType: Optional[String256]
    AssociationType: Optional[AssociationEdgeType]
    CreatedAfter: Optional[Timestamp]
    CreatedBefore: Optional[Timestamp]
    SortBy: Optional[SortAssociationsBy]
    SortOrder: Optional[SortOrder]
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]


class ListAssociationsResponse(TypedDict, total=False):
    AssociationSummaries: Optional[AssociationSummaries]
    NextToken: Optional[NextToken]


class ListAutoMLJobsRequest(ServiceRequest):
    CreationTimeAfter: Optional[Timestamp]
    CreationTimeBefore: Optional[Timestamp]
    LastModifiedTimeAfter: Optional[Timestamp]
    LastModifiedTimeBefore: Optional[Timestamp]
    NameContains: Optional[AutoMLNameContains]
    StatusEquals: Optional[AutoMLJobStatus]
    SortOrder: Optional[AutoMLSortOrder]
    SortBy: Optional[AutoMLSortBy]
    MaxResults: Optional[AutoMLMaxResults]
    NextToken: Optional[NextToken]


class ListAutoMLJobsResponse(TypedDict, total=False):
    AutoMLJobSummaries: AutoMLJobSummaries
    NextToken: Optional[NextToken]


class ListCandidatesForAutoMLJobRequest(ServiceRequest):
    AutoMLJobName: AutoMLJobName
    StatusEquals: Optional[CandidateStatus]
    CandidateNameEquals: Optional[CandidateName]
    SortOrder: Optional[AutoMLSortOrder]
    SortBy: Optional[CandidateSortBy]
    MaxResults: Optional[AutoMLMaxResults]
    NextToken: Optional[NextToken]


class ListCandidatesForAutoMLJobResponse(TypedDict, total=False):
    Candidates: AutoMLCandidates
    NextToken: Optional[NextToken]


class ListCodeRepositoriesInput(ServiceRequest):
    CreationTimeAfter: Optional[CreationTime]
    CreationTimeBefore: Optional[CreationTime]
    LastModifiedTimeAfter: Optional[Timestamp]
    LastModifiedTimeBefore: Optional[Timestamp]
    MaxResults: Optional[MaxResults]
    NameContains: Optional[CodeRepositoryNameContains]
    NextToken: Optional[NextToken]
    SortBy: Optional[CodeRepositorySortBy]
    SortOrder: Optional[CodeRepositorySortOrder]


class ListCodeRepositoriesOutput(TypedDict, total=False):
    CodeRepositorySummaryList: CodeRepositorySummaryList
    NextToken: Optional[NextToken]


class ListCompilationJobsRequest(ServiceRequest):
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]
    CreationTimeAfter: Optional[CreationTime]
    CreationTimeBefore: Optional[CreationTime]
    LastModifiedTimeAfter: Optional[LastModifiedTime]
    LastModifiedTimeBefore: Optional[LastModifiedTime]
    NameContains: Optional[NameContains]
    StatusEquals: Optional[CompilationJobStatus]
    SortBy: Optional[ListCompilationJobsSortBy]
    SortOrder: Optional[SortOrder]


class ListCompilationJobsResponse(TypedDict, total=False):
    CompilationJobSummaries: CompilationJobSummaries
    NextToken: Optional[NextToken]


class ListContextsRequest(ServiceRequest):
    SourceUri: Optional[SourceUri]
    ContextType: Optional[String256]
    CreatedAfter: Optional[Timestamp]
    CreatedBefore: Optional[Timestamp]
    SortBy: Optional[SortContextsBy]
    SortOrder: Optional[SortOrder]
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]


class ListContextsResponse(TypedDict, total=False):
    ContextSummaries: Optional[ContextSummaries]
    NextToken: Optional[NextToken]


class ListDataQualityJobDefinitionsRequest(ServiceRequest):
    EndpointName: Optional[EndpointName]
    SortBy: Optional[MonitoringJobDefinitionSortKey]
    SortOrder: Optional[SortOrder]
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]
    NameContains: Optional[NameContains]
    CreationTimeBefore: Optional[Timestamp]
    CreationTimeAfter: Optional[Timestamp]


class MonitoringJobDefinitionSummary(TypedDict, total=False):
    """Summary information about a monitoring job."""

    MonitoringJobDefinitionName: MonitoringJobDefinitionName
    MonitoringJobDefinitionArn: MonitoringJobDefinitionArn
    CreationTime: Timestamp
    EndpointName: EndpointName


MonitoringJobDefinitionSummaryList = List[MonitoringJobDefinitionSummary]


class ListDataQualityJobDefinitionsResponse(TypedDict, total=False):
    JobDefinitionSummaries: MonitoringJobDefinitionSummaryList
    NextToken: Optional[NextToken]


class ListDeviceFleetsRequest(ServiceRequest):
    NextToken: Optional[NextToken]
    MaxResults: Optional[ListMaxResults]
    CreationTimeAfter: Optional[Timestamp]
    CreationTimeBefore: Optional[Timestamp]
    LastModifiedTimeAfter: Optional[Timestamp]
    LastModifiedTimeBefore: Optional[Timestamp]
    NameContains: Optional[NameContains]
    SortBy: Optional[ListDeviceFleetsSortBy]
    SortOrder: Optional[SortOrder]


class ListDeviceFleetsResponse(TypedDict, total=False):
    DeviceFleetSummaries: DeviceFleetSummaries
    NextToken: Optional[NextToken]


class ListDevicesRequest(ServiceRequest):
    NextToken: Optional[NextToken]
    MaxResults: Optional[ListMaxResults]
    LatestHeartbeatAfter: Optional[Timestamp]
    ModelName: Optional[EntityName]
    DeviceFleetName: Optional[EntityName]


class ListDevicesResponse(TypedDict, total=False):
    DeviceSummaries: DeviceSummaries
    NextToken: Optional[NextToken]


class ListDomainsRequest(ServiceRequest):
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]


class ListDomainsResponse(TypedDict, total=False):
    Domains: Optional[DomainList]
    NextToken: Optional[NextToken]


class ListEdgePackagingJobsRequest(ServiceRequest):
    NextToken: Optional[NextToken]
    MaxResults: Optional[ListMaxResults]
    CreationTimeAfter: Optional[Timestamp]
    CreationTimeBefore: Optional[Timestamp]
    LastModifiedTimeAfter: Optional[Timestamp]
    LastModifiedTimeBefore: Optional[Timestamp]
    NameContains: Optional[NameContains]
    ModelNameContains: Optional[NameContains]
    StatusEquals: Optional[EdgePackagingJobStatus]
    SortBy: Optional[ListEdgePackagingJobsSortBy]
    SortOrder: Optional[SortOrder]


class ListEdgePackagingJobsResponse(TypedDict, total=False):
    EdgePackagingJobSummaries: EdgePackagingJobSummaries
    NextToken: Optional[NextToken]


class ListEndpointConfigsInput(ServiceRequest):
    SortBy: Optional[EndpointConfigSortKey]
    SortOrder: Optional[OrderKey]
    NextToken: Optional[PaginationToken]
    MaxResults: Optional[MaxResults]
    NameContains: Optional[EndpointConfigNameContains]
    CreationTimeBefore: Optional[Timestamp]
    CreationTimeAfter: Optional[Timestamp]


class ListEndpointConfigsOutput(TypedDict, total=False):
    EndpointConfigs: EndpointConfigSummaryList
    NextToken: Optional[PaginationToken]


class ListEndpointsInput(ServiceRequest):
    SortBy: Optional[EndpointSortKey]
    SortOrder: Optional[OrderKey]
    NextToken: Optional[PaginationToken]
    MaxResults: Optional[MaxResults]
    NameContains: Optional[EndpointNameContains]
    CreationTimeBefore: Optional[Timestamp]
    CreationTimeAfter: Optional[Timestamp]
    LastModifiedTimeBefore: Optional[Timestamp]
    LastModifiedTimeAfter: Optional[Timestamp]
    StatusEquals: Optional[EndpointStatus]


class ListEndpointsOutput(TypedDict, total=False):
    Endpoints: EndpointSummaryList
    NextToken: Optional[PaginationToken]


class ListExperimentsRequest(ServiceRequest):
    CreatedAfter: Optional[Timestamp]
    CreatedBefore: Optional[Timestamp]
    SortBy: Optional[SortExperimentsBy]
    SortOrder: Optional[SortOrder]
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]


class ListExperimentsResponse(TypedDict, total=False):
    ExperimentSummaries: Optional[ExperimentSummaries]
    NextToken: Optional[NextToken]


class ListFeatureGroupsRequest(ServiceRequest):
    NameContains: Optional[FeatureGroupNameContains]
    FeatureGroupStatusEquals: Optional[FeatureGroupStatus]
    OfflineStoreStatusEquals: Optional[OfflineStoreStatusValue]
    CreationTimeAfter: Optional[CreationTime]
    CreationTimeBefore: Optional[CreationTime]
    SortOrder: Optional[FeatureGroupSortOrder]
    SortBy: Optional[FeatureGroupSortBy]
    MaxResults: Optional[FeatureGroupMaxResults]
    NextToken: Optional[NextToken]


class ListFeatureGroupsResponse(TypedDict, total=False):
    FeatureGroupSummaries: FeatureGroupSummaries
    NextToken: NextToken


class ListFlowDefinitionsRequest(ServiceRequest):
    CreationTimeAfter: Optional[Timestamp]
    CreationTimeBefore: Optional[Timestamp]
    SortOrder: Optional[SortOrder]
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]


class ListFlowDefinitionsResponse(TypedDict, total=False):
    FlowDefinitionSummaries: FlowDefinitionSummaries
    NextToken: Optional[NextToken]


class ListHumanTaskUisRequest(ServiceRequest):
    CreationTimeAfter: Optional[Timestamp]
    CreationTimeBefore: Optional[Timestamp]
    SortOrder: Optional[SortOrder]
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]


class ListHumanTaskUisResponse(TypedDict, total=False):
    HumanTaskUiSummaries: HumanTaskUiSummaries
    NextToken: Optional[NextToken]


class ListHyperParameterTuningJobsRequest(ServiceRequest):
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]
    SortBy: Optional[HyperParameterTuningJobSortByOptions]
    SortOrder: Optional[SortOrder]
    NameContains: Optional[NameContains]
    CreationTimeAfter: Optional[Timestamp]
    CreationTimeBefore: Optional[Timestamp]
    LastModifiedTimeAfter: Optional[Timestamp]
    LastModifiedTimeBefore: Optional[Timestamp]
    StatusEquals: Optional[HyperParameterTuningJobStatus]


class ListHyperParameterTuningJobsResponse(TypedDict, total=False):
    HyperParameterTuningJobSummaries: HyperParameterTuningJobSummaries
    NextToken: Optional[NextToken]


class ListImageVersionsRequest(ServiceRequest):
    CreationTimeAfter: Optional[Timestamp]
    CreationTimeBefore: Optional[Timestamp]
    ImageName: ImageName
    LastModifiedTimeAfter: Optional[Timestamp]
    LastModifiedTimeBefore: Optional[Timestamp]
    MaxResults: Optional[MaxResults]
    NextToken: Optional[NextToken]
    SortBy: Optional[ImageVersionSortBy]
    SortOrder: Optional[ImageVersionSortOrder]


class ListImageVersionsResponse(TypedDict, total=False):
    ImageVersions: Optional[ImageVersions]
    NextToken: Optional[NextToken]


class ListImagesRequest(ServiceRequest):
    CreationTimeAfter: Optional[Timestamp]
    CreationTimeBefore: Optional[Timestamp]
    LastModifiedTimeAfter: Optional[Timestamp]
    LastModifiedTimeBefore: Optional[Timestamp]
    MaxResults: Optional[MaxResults]
    NameContains: Optional[ImageNameContains]
    NextToken: Optional[NextToken]
    SortBy: Optional[ImageSortBy]
    SortOrder: Optional[ImageSortOrder]


class ListImagesResponse(TypedDict, total=False):
    Images: Optional[Images]
    NextToken: Optional[NextToken]


class ListInferenceRecommendationsJobsRequest(ServiceRequest):
    CreationTimeAfter: Optional[CreationTime]
    CreationTimeBefore: Optional[CreationTime]
    LastModifiedTimeAfter: Optional[LastModifiedTime]
    LastModifiedTimeBefore: Optional[LastModifiedTime]
    NameContains: Optional[NameContains]
    StatusEquals: Optional[RecommendationJobStatus]
    SortBy: Optional[ListInferenceRecommendationsJobsSortBy]
    SortOrder: Optional[SortOrder]
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]


class ListInferenceRecommendationsJobsResponse(TypedDict, total=False):
    InferenceRecommendationsJobs: InferenceRecommendationsJobs
    NextToken: Optional[NextToken]


class ListLabelingJobsForWorkteamRequest(ServiceRequest):
    WorkteamArn: WorkteamArn
    MaxResults: Optional[MaxResults]
    NextToken: Optional[NextToken]
    CreationTimeAfter: Optional[Timestamp]
    CreationTimeBefore: Optional[Timestamp]
    JobReferenceCodeContains: Optional[JobReferenceCodeContains]
    SortBy: Optional[ListLabelingJobsForWorkteamSortByOptions]
    SortOrder: Optional[SortOrder]


class ListLabelingJobsForWorkteamResponse(TypedDict, total=False):
    LabelingJobSummaryList: LabelingJobForWorkteamSummaryList
    NextToken: Optional[NextToken]


class ListLabelingJobsRequest(ServiceRequest):
    CreationTimeAfter: Optional[Timestamp]
    CreationTimeBefore: Optional[Timestamp]
    LastModifiedTimeAfter: Optional[Timestamp]
    LastModifiedTimeBefore: Optional[Timestamp]
    MaxResults: Optional[MaxResults]
    NextToken: Optional[NextToken]
    NameContains: Optional[NameContains]
    SortBy: Optional[SortBy]
    SortOrder: Optional[SortOrder]
    StatusEquals: Optional[LabelingJobStatus]


class ListLabelingJobsResponse(TypedDict, total=False):
    LabelingJobSummaryList: Optional[LabelingJobSummaryList]
    NextToken: Optional[NextToken]


ListLineageEntityParameterKey = List[StringParameterValue]


class ListLineageGroupsRequest(ServiceRequest):
    CreatedAfter: Optional[Timestamp]
    CreatedBefore: Optional[Timestamp]
    SortBy: Optional[SortLineageGroupsBy]
    SortOrder: Optional[SortOrder]
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]


class ListLineageGroupsResponse(TypedDict, total=False):
    LineageGroupSummaries: Optional[LineageGroupSummaries]
    NextToken: Optional[NextToken]


class ListModelBiasJobDefinitionsRequest(ServiceRequest):
    EndpointName: Optional[EndpointName]
    SortBy: Optional[MonitoringJobDefinitionSortKey]
    SortOrder: Optional[SortOrder]
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]
    NameContains: Optional[NameContains]
    CreationTimeBefore: Optional[Timestamp]
    CreationTimeAfter: Optional[Timestamp]


class ListModelBiasJobDefinitionsResponse(TypedDict, total=False):
    JobDefinitionSummaries: MonitoringJobDefinitionSummaryList
    NextToken: Optional[NextToken]


class ListModelExplainabilityJobDefinitionsRequest(ServiceRequest):
    EndpointName: Optional[EndpointName]
    SortBy: Optional[MonitoringJobDefinitionSortKey]
    SortOrder: Optional[SortOrder]
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]
    NameContains: Optional[NameContains]
    CreationTimeBefore: Optional[Timestamp]
    CreationTimeAfter: Optional[Timestamp]


class ListModelExplainabilityJobDefinitionsResponse(TypedDict, total=False):
    JobDefinitionSummaries: MonitoringJobDefinitionSummaryList
    NextToken: Optional[NextToken]


class ModelMetadataFilter(TypedDict, total=False):
    """Part of the search expression. You can specify the name and value
    (domain, task, framework, framework version, task, and model).
    """

    Name: ModelMetadataFilterType
    Value: String256


ModelMetadataFilters = List[ModelMetadataFilter]


class ModelMetadataSearchExpression(TypedDict, total=False):
    """One or more filters that searches for the specified resource or
    resources in a search. All resource objects that satisfy the
    expression's condition are included in the search results
    """

    Filters: Optional[ModelMetadataFilters]


class ListModelMetadataRequest(ServiceRequest):
    SearchExpression: Optional[ModelMetadataSearchExpression]
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]


class ModelMetadataSummary(TypedDict, total=False):
    """A summary of the model metadata."""

    Domain: String
    Framework: String
    Task: String
    Model: String
    FrameworkVersion: String


ModelMetadataSummaries = List[ModelMetadataSummary]


class ListModelMetadataResponse(TypedDict, total=False):
    ModelMetadataSummaries: ModelMetadataSummaries
    NextToken: Optional[NextToken]


class ListModelPackageGroupsInput(ServiceRequest):
    CreationTimeAfter: Optional[CreationTime]
    CreationTimeBefore: Optional[CreationTime]
    MaxResults: Optional[MaxResults]
    NameContains: Optional[NameContains]
    NextToken: Optional[NextToken]
    SortBy: Optional[ModelPackageGroupSortBy]
    SortOrder: Optional[SortOrder]


class ModelPackageGroupSummary(TypedDict, total=False):
    """Summary information about a model group."""

    ModelPackageGroupName: EntityName
    ModelPackageGroupArn: ModelPackageGroupArn
    ModelPackageGroupDescription: Optional[EntityDescription]
    CreationTime: CreationTime
    ModelPackageGroupStatus: ModelPackageGroupStatus


ModelPackageGroupSummaryList = List[ModelPackageGroupSummary]


class ListModelPackageGroupsOutput(TypedDict, total=False):
    ModelPackageGroupSummaryList: ModelPackageGroupSummaryList
    NextToken: Optional[NextToken]


class ListModelPackagesInput(ServiceRequest):
    CreationTimeAfter: Optional[CreationTime]
    CreationTimeBefore: Optional[CreationTime]
    MaxResults: Optional[MaxResults]
    NameContains: Optional[NameContains]
    ModelApprovalStatus: Optional[ModelApprovalStatus]
    ModelPackageGroupName: Optional[ArnOrName]
    ModelPackageType: Optional[ModelPackageType]
    NextToken: Optional[NextToken]
    SortBy: Optional[ModelPackageSortBy]
    SortOrder: Optional[SortOrder]


class ModelPackageSummary(TypedDict, total=False):
    """Provides summary information about a model package."""

    ModelPackageName: EntityName
    ModelPackageGroupName: Optional[EntityName]
    ModelPackageVersion: Optional[ModelPackageVersion]
    ModelPackageArn: ModelPackageArn
    ModelPackageDescription: Optional[EntityDescription]
    CreationTime: CreationTime
    ModelPackageStatus: ModelPackageStatus
    ModelApprovalStatus: Optional[ModelApprovalStatus]


ModelPackageSummaryList = List[ModelPackageSummary]


class ListModelPackagesOutput(TypedDict, total=False):
    ModelPackageSummaryList: ModelPackageSummaryList
    NextToken: Optional[NextToken]


class ListModelQualityJobDefinitionsRequest(ServiceRequest):
    EndpointName: Optional[EndpointName]
    SortBy: Optional[MonitoringJobDefinitionSortKey]
    SortOrder: Optional[SortOrder]
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]
    NameContains: Optional[NameContains]
    CreationTimeBefore: Optional[Timestamp]
    CreationTimeAfter: Optional[Timestamp]


class ListModelQualityJobDefinitionsResponse(TypedDict, total=False):
    JobDefinitionSummaries: MonitoringJobDefinitionSummaryList
    NextToken: Optional[NextToken]


class ListModelsInput(ServiceRequest):
    SortBy: Optional[ModelSortKey]
    SortOrder: Optional[OrderKey]
    NextToken: Optional[PaginationToken]
    MaxResults: Optional[MaxResults]
    NameContains: Optional[ModelNameContains]
    CreationTimeBefore: Optional[Timestamp]
    CreationTimeAfter: Optional[Timestamp]


class ModelSummary(TypedDict, total=False):
    """Provides summary information about a model."""

    ModelName: ModelName
    ModelArn: ModelArn
    CreationTime: Timestamp


ModelSummaryList = List[ModelSummary]


class ListModelsOutput(TypedDict, total=False):
    Models: ModelSummaryList
    NextToken: Optional[PaginationToken]


class ListMonitoringExecutionsRequest(ServiceRequest):
    MonitoringScheduleName: Optional[MonitoringScheduleName]
    EndpointName: Optional[EndpointName]
    SortBy: Optional[MonitoringExecutionSortKey]
    SortOrder: Optional[SortOrder]
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]
    ScheduledTimeBefore: Optional[Timestamp]
    ScheduledTimeAfter: Optional[Timestamp]
    CreationTimeBefore: Optional[Timestamp]
    CreationTimeAfter: Optional[Timestamp]
    LastModifiedTimeBefore: Optional[Timestamp]
    LastModifiedTimeAfter: Optional[Timestamp]
    StatusEquals: Optional[ExecutionStatus]
    MonitoringJobDefinitionName: Optional[MonitoringJobDefinitionName]
    MonitoringTypeEquals: Optional[MonitoringType]


MonitoringExecutionSummaryList = List[MonitoringExecutionSummary]


class ListMonitoringExecutionsResponse(TypedDict, total=False):
    MonitoringExecutionSummaries: MonitoringExecutionSummaryList
    NextToken: Optional[NextToken]


class ListMonitoringSchedulesRequest(ServiceRequest):
    EndpointName: Optional[EndpointName]
    SortBy: Optional[MonitoringScheduleSortKey]
    SortOrder: Optional[SortOrder]
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]
    NameContains: Optional[NameContains]
    CreationTimeBefore: Optional[Timestamp]
    CreationTimeAfter: Optional[Timestamp]
    LastModifiedTimeBefore: Optional[Timestamp]
    LastModifiedTimeAfter: Optional[Timestamp]
    StatusEquals: Optional[ScheduleStatus]
    MonitoringJobDefinitionName: Optional[MonitoringJobDefinitionName]
    MonitoringTypeEquals: Optional[MonitoringType]


class MonitoringScheduleSummary(TypedDict, total=False):
    """Summarizes the monitoring schedule."""

    MonitoringScheduleName: MonitoringScheduleName
    MonitoringScheduleArn: MonitoringScheduleArn
    CreationTime: Timestamp
    LastModifiedTime: Timestamp
    MonitoringScheduleStatus: ScheduleStatus
    EndpointName: Optional[EndpointName]
    MonitoringJobDefinitionName: Optional[MonitoringJobDefinitionName]
    MonitoringType: Optional[MonitoringType]


MonitoringScheduleSummaryList = List[MonitoringScheduleSummary]


class ListMonitoringSchedulesResponse(TypedDict, total=False):
    MonitoringScheduleSummaries: MonitoringScheduleSummaryList
    NextToken: Optional[NextToken]


class ListNotebookInstanceLifecycleConfigsInput(ServiceRequest):
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]
    SortBy: Optional[NotebookInstanceLifecycleConfigSortKey]
    SortOrder: Optional[NotebookInstanceLifecycleConfigSortOrder]
    NameContains: Optional[NotebookInstanceLifecycleConfigNameContains]
    CreationTimeBefore: Optional[CreationTime]
    CreationTimeAfter: Optional[CreationTime]
    LastModifiedTimeBefore: Optional[LastModifiedTime]
    LastModifiedTimeAfter: Optional[LastModifiedTime]


class NotebookInstanceLifecycleConfigSummary(TypedDict, total=False):
    """Provides a summary of a notebook instance lifecycle configuration."""

    NotebookInstanceLifecycleConfigName: NotebookInstanceLifecycleConfigName
    NotebookInstanceLifecycleConfigArn: NotebookInstanceLifecycleConfigArn
    CreationTime: Optional[CreationTime]
    LastModifiedTime: Optional[LastModifiedTime]


NotebookInstanceLifecycleConfigSummaryList = List[NotebookInstanceLifecycleConfigSummary]


class ListNotebookInstanceLifecycleConfigsOutput(TypedDict, total=False):
    NextToken: Optional[NextToken]
    NotebookInstanceLifecycleConfigs: Optional[NotebookInstanceLifecycleConfigSummaryList]


class ListNotebookInstancesInput(ServiceRequest):
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]
    SortBy: Optional[NotebookInstanceSortKey]
    SortOrder: Optional[NotebookInstanceSortOrder]
    NameContains: Optional[NotebookInstanceNameContains]
    CreationTimeBefore: Optional[CreationTime]
    CreationTimeAfter: Optional[CreationTime]
    LastModifiedTimeBefore: Optional[LastModifiedTime]
    LastModifiedTimeAfter: Optional[LastModifiedTime]
    StatusEquals: Optional[NotebookInstanceStatus]
    NotebookInstanceLifecycleConfigNameContains: Optional[NotebookInstanceLifecycleConfigName]
    DefaultCodeRepositoryContains: Optional[CodeRepositoryContains]
    AdditionalCodeRepositoryEquals: Optional[CodeRepositoryNameOrUrl]


class NotebookInstanceSummary(TypedDict, total=False):
    """Provides summary information for an SageMaker notebook instance."""

    NotebookInstanceName: NotebookInstanceName
    NotebookInstanceArn: NotebookInstanceArn
    NotebookInstanceStatus: Optional[NotebookInstanceStatus]
    Url: Optional[NotebookInstanceUrl]
    InstanceType: Optional[InstanceType]
    CreationTime: Optional[CreationTime]
    LastModifiedTime: Optional[LastModifiedTime]
    NotebookInstanceLifecycleConfigName: Optional[NotebookInstanceLifecycleConfigName]
    DefaultCodeRepository: Optional[CodeRepositoryNameOrUrl]
    AdditionalCodeRepositories: Optional[AdditionalCodeRepositoryNamesOrUrls]


NotebookInstanceSummaryList = List[NotebookInstanceSummary]


class ListNotebookInstancesOutput(TypedDict, total=False):
    NextToken: Optional[NextToken]
    NotebookInstances: Optional[NotebookInstanceSummaryList]


class ListPipelineExecutionStepsRequest(ServiceRequest):
    PipelineExecutionArn: Optional[PipelineExecutionArn]
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]
    SortOrder: Optional[SortOrder]


class QualityCheckStepMetadata(TypedDict, total=False):
    """Container for the metadata for a Quality check step. For more
    information, see the topic on `QualityCheck
    step <https://docs.aws.amazon.com/sagemaker/latest/dg/build-and-manage-steps.html#step-type-quality-check>`__
    in the *Amazon SageMaker Developer Guide*.
    """

    CheckType: Optional[String256]
    BaselineUsedForDriftCheckStatistics: Optional[String1024]
    BaselineUsedForDriftCheckConstraints: Optional[String1024]
    CalculatedBaselineStatistics: Optional[String1024]
    CalculatedBaselineConstraints: Optional[String1024]
    ModelPackageGroupName: Optional[String256]
    ViolationReport: Optional[String1024]
    CheckJobArn: Optional[String256]
    SkipCheck: Optional[Boolean]
    RegisterNewBaseline: Optional[Boolean]


class RegisterModelStepMetadata(TypedDict, total=False):
    """Metadata for a register model job step."""

    Arn: Optional[String256]


class ModelStepMetadata(TypedDict, total=False):
    """Metadata for Model steps."""

    Arn: Optional[String256]


class TuningJobStepMetaData(TypedDict, total=False):
    """Metadata for a tuning step."""

    Arn: Optional[HyperParameterTuningJobArn]


class TransformJobStepMetadata(TypedDict, total=False):
    """Metadata for a transform job step."""

    Arn: Optional[TransformJobArn]


class ProcessingJobStepMetadata(TypedDict, total=False):
    """Metadata for a processing job step."""

    Arn: Optional[ProcessingJobArn]


class TrainingJobStepMetadata(TypedDict, total=False):
    """Metadata for a training job step."""

    Arn: Optional[TrainingJobArn]


class PipelineExecutionStepMetadata(TypedDict, total=False):
    """Metadata for a step execution."""

    TrainingJob: Optional[TrainingJobStepMetadata]
    ProcessingJob: Optional[ProcessingJobStepMetadata]
    TransformJob: Optional[TransformJobStepMetadata]
    TuningJob: Optional[TuningJobStepMetaData]
    Model: Optional[ModelStepMetadata]
    RegisterModel: Optional[RegisterModelStepMetadata]
    Condition: Optional[ConditionStepMetadata]
    Callback: Optional[CallbackStepMetadata]
    Lambda: Optional[LambdaStepMetadata]
    QualityCheck: Optional[QualityCheckStepMetadata]
    ClarifyCheck: Optional[ClarifyCheckStepMetadata]
    EMR: Optional[EMRStepMetadata]
    Fail: Optional[FailStepMetadata]


class PipelineExecutionStep(TypedDict, total=False):
    """An execution of a step in a pipeline."""

    StepName: Optional[StepName]
    StepDisplayName: Optional[StepDisplayName]
    StepDescription: Optional[StepDescription]
    StartTime: Optional[Timestamp]
    EndTime: Optional[Timestamp]
    StepStatus: Optional[StepStatus]
    CacheHitResult: Optional[CacheHitResult]
    AttemptCount: Optional[IntegerValue]
    FailureReason: Optional[FailureReason]
    Metadata: Optional[PipelineExecutionStepMetadata]


PipelineExecutionStepList = List[PipelineExecutionStep]


class ListPipelineExecutionStepsResponse(TypedDict, total=False):
    PipelineExecutionSteps: Optional[PipelineExecutionStepList]
    NextToken: Optional[NextToken]


class ListPipelineExecutionsRequest(ServiceRequest):
    PipelineName: PipelineName
    CreatedAfter: Optional[Timestamp]
    CreatedBefore: Optional[Timestamp]
    SortBy: Optional[SortPipelineExecutionsBy]
    SortOrder: Optional[SortOrder]
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]


class PipelineExecutionSummary(TypedDict, total=False):
    """A pipeline execution summary."""

    PipelineExecutionArn: Optional[PipelineExecutionArn]
    StartTime: Optional[Timestamp]
    PipelineExecutionStatus: Optional[PipelineExecutionStatus]
    PipelineExecutionDescription: Optional[PipelineExecutionDescription]
    PipelineExecutionDisplayName: Optional[PipelineExecutionName]
    PipelineExecutionFailureReason: Optional[String3072]


PipelineExecutionSummaryList = List[PipelineExecutionSummary]


class ListPipelineExecutionsResponse(TypedDict, total=False):
    PipelineExecutionSummaries: Optional[PipelineExecutionSummaryList]
    NextToken: Optional[NextToken]


class ListPipelineParametersForExecutionRequest(ServiceRequest):
    PipelineExecutionArn: PipelineExecutionArn
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]


class Parameter(TypedDict, total=False):
    """Assigns a value to a named Pipeline parameter."""

    Name: PipelineParameterName
    Value: String1024


ParameterList = List[Parameter]


class ListPipelineParametersForExecutionResponse(TypedDict, total=False):
    PipelineParameters: Optional[ParameterList]
    NextToken: Optional[NextToken]


class ListPipelinesRequest(ServiceRequest):
    PipelineNamePrefix: Optional[PipelineName]
    CreatedAfter: Optional[Timestamp]
    CreatedBefore: Optional[Timestamp]
    SortBy: Optional[SortPipelinesBy]
    SortOrder: Optional[SortOrder]
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]


class PipelineSummary(TypedDict, total=False):
    """A summary of a pipeline."""

    PipelineArn: Optional[PipelineArn]
    PipelineName: Optional[PipelineName]
    PipelineDisplayName: Optional[PipelineName]
    PipelineDescription: Optional[PipelineDescription]
    RoleArn: Optional[RoleArn]
    CreationTime: Optional[Timestamp]
    LastModifiedTime: Optional[Timestamp]
    LastExecutionTime: Optional[Timestamp]


PipelineSummaryList = List[PipelineSummary]


class ListPipelinesResponse(TypedDict, total=False):
    PipelineSummaries: Optional[PipelineSummaryList]
    NextToken: Optional[NextToken]


class ListProcessingJobsRequest(ServiceRequest):
    CreationTimeAfter: Optional[Timestamp]
    CreationTimeBefore: Optional[Timestamp]
    LastModifiedTimeAfter: Optional[Timestamp]
    LastModifiedTimeBefore: Optional[Timestamp]
    NameContains: Optional[String]
    StatusEquals: Optional[ProcessingJobStatus]
    SortBy: Optional[SortBy]
    SortOrder: Optional[SortOrder]
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]


class ProcessingJobSummary(TypedDict, total=False):
    """Summary of information about a processing job."""

    ProcessingJobName: ProcessingJobName
    ProcessingJobArn: ProcessingJobArn
    CreationTime: Timestamp
    ProcessingEndTime: Optional[Timestamp]
    LastModifiedTime: Optional[Timestamp]
    ProcessingJobStatus: ProcessingJobStatus
    FailureReason: Optional[FailureReason]
    ExitMessage: Optional[ExitMessage]


ProcessingJobSummaries = List[ProcessingJobSummary]


class ListProcessingJobsResponse(TypedDict, total=False):
    ProcessingJobSummaries: ProcessingJobSummaries
    NextToken: Optional[NextToken]


class ListProjectsInput(ServiceRequest):
    CreationTimeAfter: Optional[Timestamp]
    CreationTimeBefore: Optional[Timestamp]
    MaxResults: Optional[MaxResults]
    NameContains: Optional[ProjectEntityName]
    NextToken: Optional[NextToken]
    SortBy: Optional[ProjectSortBy]
    SortOrder: Optional[ProjectSortOrder]


class ProjectSummary(TypedDict, total=False):
    """Information about a project."""

    ProjectName: ProjectEntityName
    ProjectDescription: Optional[EntityDescription]
    ProjectArn: ProjectArn
    ProjectId: ProjectId
    CreationTime: Timestamp
    ProjectStatus: ProjectStatus


ProjectSummaryList = List[ProjectSummary]


class ListProjectsOutput(TypedDict, total=False):
    ProjectSummaryList: ProjectSummaryList
    NextToken: Optional[NextToken]


class ListStudioLifecycleConfigsRequest(ServiceRequest):
    MaxResults: Optional[MaxResults]
    NextToken: Optional[NextToken]
    NameContains: Optional[StudioLifecycleConfigName]
    AppTypeEquals: Optional[StudioLifecycleConfigAppType]
    CreationTimeBefore: Optional[Timestamp]
    CreationTimeAfter: Optional[Timestamp]
    ModifiedTimeBefore: Optional[Timestamp]
    ModifiedTimeAfter: Optional[Timestamp]
    SortBy: Optional[StudioLifecycleConfigSortKey]
    SortOrder: Optional[SortOrder]


class StudioLifecycleConfigDetails(TypedDict, total=False):
    """Details of the Studio Lifecycle Configuration."""

    StudioLifecycleConfigArn: Optional[StudioLifecycleConfigArn]
    StudioLifecycleConfigName: Optional[StudioLifecycleConfigName]
    CreationTime: Optional[Timestamp]
    LastModifiedTime: Optional[Timestamp]
    StudioLifecycleConfigAppType: Optional[StudioLifecycleConfigAppType]


StudioLifecycleConfigsList = List[StudioLifecycleConfigDetails]


class ListStudioLifecycleConfigsResponse(TypedDict, total=False):
    NextToken: Optional[NextToken]
    StudioLifecycleConfigs: Optional[StudioLifecycleConfigsList]


class ListSubscribedWorkteamsRequest(ServiceRequest):
    NameContains: Optional[WorkteamName]
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]


SubscribedWorkteams = List[SubscribedWorkteam]


class ListSubscribedWorkteamsResponse(TypedDict, total=False):
    SubscribedWorkteams: SubscribedWorkteams
    NextToken: Optional[NextToken]


class ListTagsInput(ServiceRequest):
    ResourceArn: ResourceArn
    NextToken: Optional[NextToken]
    MaxResults: Optional[ListTagsMaxResults]


class ListTagsOutput(TypedDict, total=False):
    Tags: Optional[TagList]
    NextToken: Optional[NextToken]


class ListTrainingJobsForHyperParameterTuningJobRequest(ServiceRequest):
    HyperParameterTuningJobName: HyperParameterTuningJobName
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]
    StatusEquals: Optional[TrainingJobStatus]
    SortBy: Optional[TrainingJobSortByOptions]
    SortOrder: Optional[SortOrder]


class ListTrainingJobsForHyperParameterTuningJobResponse(TypedDict, total=False):
    TrainingJobSummaries: HyperParameterTrainingJobSummaries
    NextToken: Optional[NextToken]


class ListTrainingJobsRequest(ServiceRequest):
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]
    CreationTimeAfter: Optional[Timestamp]
    CreationTimeBefore: Optional[Timestamp]
    LastModifiedTimeAfter: Optional[Timestamp]
    LastModifiedTimeBefore: Optional[Timestamp]
    NameContains: Optional[NameContains]
    StatusEquals: Optional[TrainingJobStatus]
    SortBy: Optional[SortBy]
    SortOrder: Optional[SortOrder]


class TrainingJobSummary(TypedDict, total=False):
    """Provides summary information about a training job."""

    TrainingJobName: TrainingJobName
    TrainingJobArn: TrainingJobArn
    CreationTime: Timestamp
    TrainingEndTime: Optional[Timestamp]
    LastModifiedTime: Optional[Timestamp]
    TrainingJobStatus: TrainingJobStatus


TrainingJobSummaries = List[TrainingJobSummary]


class ListTrainingJobsResponse(TypedDict, total=False):
    TrainingJobSummaries: TrainingJobSummaries
    NextToken: Optional[NextToken]


class ListTransformJobsRequest(ServiceRequest):
    CreationTimeAfter: Optional[Timestamp]
    CreationTimeBefore: Optional[Timestamp]
    LastModifiedTimeAfter: Optional[Timestamp]
    LastModifiedTimeBefore: Optional[Timestamp]
    NameContains: Optional[NameContains]
    StatusEquals: Optional[TransformJobStatus]
    SortBy: Optional[SortBy]
    SortOrder: Optional[SortOrder]
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]


class TransformJobSummary(TypedDict, total=False):
    """Provides a summary of a transform job. Multiple ``TransformJobSummary``
    objects are returned as a list after in response to a ListTransformJobs
    call.
    """

    TransformJobName: TransformJobName
    TransformJobArn: TransformJobArn
    CreationTime: Timestamp
    TransformEndTime: Optional[Timestamp]
    LastModifiedTime: Optional[Timestamp]
    TransformJobStatus: TransformJobStatus
    FailureReason: Optional[FailureReason]


TransformJobSummaries = List[TransformJobSummary]


class ListTransformJobsResponse(TypedDict, total=False):
    TransformJobSummaries: TransformJobSummaries
    NextToken: Optional[NextToken]


ListTrialComponentKey256 = List[TrialComponentKey256]


class ListTrialComponentsRequest(ServiceRequest):
    ExperimentName: Optional[ExperimentEntityName]
    TrialName: Optional[ExperimentEntityName]
    SourceArn: Optional[String256]
    CreatedAfter: Optional[Timestamp]
    CreatedBefore: Optional[Timestamp]
    SortBy: Optional[SortTrialComponentsBy]
    SortOrder: Optional[SortOrder]
    MaxResults: Optional[MaxResults]
    NextToken: Optional[NextToken]


class TrialComponentSummary(TypedDict, total=False):
    """A summary of the properties of a trial component. To get all the
    properties, call the DescribeTrialComponent API and provide the
    ``TrialComponentName``.
    """

    TrialComponentName: Optional[ExperimentEntityName]
    TrialComponentArn: Optional[TrialComponentArn]
    DisplayName: Optional[ExperimentEntityName]
    TrialComponentSource: Optional[TrialComponentSource]
    Status: Optional[TrialComponentStatus]
    StartTime: Optional[Timestamp]
    EndTime: Optional[Timestamp]
    CreationTime: Optional[Timestamp]
    CreatedBy: Optional[UserContext]
    LastModifiedTime: Optional[Timestamp]
    LastModifiedBy: Optional[UserContext]


TrialComponentSummaries = List[TrialComponentSummary]


class ListTrialComponentsResponse(TypedDict, total=False):
    TrialComponentSummaries: Optional[TrialComponentSummaries]
    NextToken: Optional[NextToken]


class ListTrialsRequest(ServiceRequest):
    ExperimentName: Optional[ExperimentEntityName]
    TrialComponentName: Optional[ExperimentEntityName]
    CreatedAfter: Optional[Timestamp]
    CreatedBefore: Optional[Timestamp]
    SortBy: Optional[SortTrialsBy]
    SortOrder: Optional[SortOrder]
    MaxResults: Optional[MaxResults]
    NextToken: Optional[NextToken]


class TrialSummary(TypedDict, total=False):
    """A summary of the properties of a trial. To get the complete set of
    properties, call the DescribeTrial API and provide the ``TrialName``.
    """

    TrialArn: Optional[TrialArn]
    TrialName: Optional[ExperimentEntityName]
    DisplayName: Optional[ExperimentEntityName]
    TrialSource: Optional[TrialSource]
    CreationTime: Optional[Timestamp]
    LastModifiedTime: Optional[Timestamp]


TrialSummaries = List[TrialSummary]


class ListTrialsResponse(TypedDict, total=False):
    TrialSummaries: Optional[TrialSummaries]
    NextToken: Optional[NextToken]


class ListUserProfilesRequest(ServiceRequest):
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]
    SortOrder: Optional[SortOrder]
    SortBy: Optional[UserProfileSortKey]
    DomainIdEquals: Optional[DomainId]
    UserProfileNameContains: Optional[UserProfileName]


class UserProfileDetails(TypedDict, total=False):
    """The user profile details."""

    DomainId: Optional[DomainId]
    UserProfileName: Optional[UserProfileName]
    Status: Optional[UserProfileStatus]
    CreationTime: Optional[CreationTime]
    LastModifiedTime: Optional[LastModifiedTime]


UserProfileList = List[UserProfileDetails]


class ListUserProfilesResponse(TypedDict, total=False):
    UserProfiles: Optional[UserProfileList]
    NextToken: Optional[NextToken]


class ListWorkforcesRequest(ServiceRequest):
    SortBy: Optional[ListWorkforcesSortByOptions]
    SortOrder: Optional[SortOrder]
    NameContains: Optional[WorkforceName]
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]


Workforces = List[Workforce]


class ListWorkforcesResponse(TypedDict, total=False):
    Workforces: Workforces
    NextToken: Optional[NextToken]


class ListWorkteamsRequest(ServiceRequest):
    SortBy: Optional[ListWorkteamsSortByOptions]
    SortOrder: Optional[SortOrder]
    NameContains: Optional[WorkteamName]
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]


Workteams = List[Workteam]


class ListWorkteamsResponse(TypedDict, total=False):
    Workteams: Workteams
    NextToken: Optional[NextToken]


class ModelPackage(TypedDict, total=False):
    """A versioned model that can be deployed for SageMaker inference."""

    ModelPackageName: Optional[EntityName]
    ModelPackageGroupName: Optional[EntityName]
    ModelPackageVersion: Optional[ModelPackageVersion]
    ModelPackageArn: Optional[ModelPackageArn]
    ModelPackageDescription: Optional[EntityDescription]
    CreationTime: Optional[CreationTime]
    InferenceSpecification: Optional[InferenceSpecification]
    SourceAlgorithmSpecification: Optional[SourceAlgorithmSpecification]
    ValidationSpecification: Optional[ModelPackageValidationSpecification]
    ModelPackageStatus: Optional[ModelPackageStatus]
    ModelPackageStatusDetails: Optional[ModelPackageStatusDetails]
    CertifyForMarketplace: Optional[CertifyForMarketplace]
    ModelApprovalStatus: Optional[ModelApprovalStatus]
    CreatedBy: Optional[UserContext]
    MetadataProperties: Optional[MetadataProperties]
    ModelMetrics: Optional[ModelMetrics]
    LastModifiedTime: Optional[Timestamp]
    LastModifiedBy: Optional[UserContext]
    ApprovalDescription: Optional[ApprovalDescription]
    Domain: Optional[String]
    Task: Optional[String]
    SamplePayloadUrl: Optional[String]
    AdditionalInferenceSpecifications: Optional[AdditionalInferenceSpecifications]
    Tags: Optional[TagList]
    CustomerMetadataProperties: Optional[CustomerMetadataMap]
    DriftCheckBaselines: Optional[DriftCheckBaselines]


class ModelPackageGroup(TypedDict, total=False):
    """A group of versioned models in the model registry."""

    ModelPackageGroupName: Optional[EntityName]
    ModelPackageGroupArn: Optional[ModelPackageGroupArn]
    ModelPackageGroupDescription: Optional[EntityDescription]
    CreationTime: Optional[CreationTime]
    CreatedBy: Optional[UserContext]
    ModelPackageGroupStatus: Optional[ModelPackageGroupStatus]
    Tags: Optional[TagList]


class NestedFilters(TypedDict, total=False):
    """A list of nested Filter objects. A resource must satisfy the conditions
    of all filters to be included in the results returned from the Search
    API.

    For example, to filter on a training job's ``InputDataConfig`` property
    with a specific channel name and ``S3Uri`` prefix, define the following
    filters:

    -  ``'{Name:"InputDataConfig.ChannelName", "Operator":"Equals", "Value":"train"}',``

    -  ``'{Name:"InputDataConfig.DataSource.S3DataSource.S3Uri", "Operator":"Contains", "Value":"mybucket/catdata"}'``
    """

    NestedPropertyName: ResourcePropertyName
    Filters: FilterList


NestedFiltersList = List[NestedFilters]


class Parent(TypedDict, total=False):
    """The trial that a trial component is associated with and the experiment
    the trial is part of. A component might not be associated with a trial.
    A component can be associated with multiple trials.
    """

    TrialName: Optional[ExperimentEntityName]
    ExperimentName: Optional[ExperimentEntityName]


Parents = List[Parent]


class Pipeline(TypedDict, total=False):
    """A SageMaker Model Building Pipeline instance."""

    PipelineArn: Optional[PipelineArn]
    PipelineName: Optional[PipelineName]
    PipelineDisplayName: Optional[PipelineName]
    PipelineDescription: Optional[PipelineDescription]
    RoleArn: Optional[RoleArn]
    PipelineStatus: Optional[PipelineStatus]
    CreationTime: Optional[Timestamp]
    LastModifiedTime: Optional[Timestamp]
    LastRunTime: Optional[Timestamp]
    CreatedBy: Optional[UserContext]
    LastModifiedBy: Optional[UserContext]
    ParallelismConfiguration: Optional[ParallelismConfiguration]
    Tags: Optional[TagList]


class PipelineExecution(TypedDict, total=False):
    """An execution of a pipeline."""

    PipelineArn: Optional[PipelineArn]
    PipelineExecutionArn: Optional[PipelineExecutionArn]
    PipelineExecutionDisplayName: Optional[PipelineExecutionName]
    PipelineExecutionStatus: Optional[PipelineExecutionStatus]
    PipelineExecutionDescription: Optional[PipelineExecutionDescription]
    PipelineExperimentConfig: Optional[PipelineExperimentConfig]
    FailureReason: Optional[PipelineExecutionFailureReason]
    CreationTime: Optional[Timestamp]
    LastModifiedTime: Optional[Timestamp]
    CreatedBy: Optional[UserContext]
    LastModifiedBy: Optional[UserContext]
    ParallelismConfiguration: Optional[ParallelismConfiguration]
    PipelineParameters: Optional[ParameterList]


class ProcessingJob(TypedDict, total=False):
    """An Amazon SageMaker processing job that is used to analyze data and
    evaluate models. For more information, see `Process Data and Evaluate
    Models <https://docs.aws.amazon.com/sagemaker/latest/dg/processing-job.html>`__.
    """

    ProcessingInputs: Optional[ProcessingInputs]
    ProcessingOutputConfig: Optional[ProcessingOutputConfig]
    ProcessingJobName: Optional[ProcessingJobName]
    ProcessingResources: Optional[ProcessingResources]
    StoppingCondition: Optional[ProcessingStoppingCondition]
    AppSpecification: Optional[AppSpecification]
    Environment: Optional[ProcessingEnvironmentMap]
    NetworkConfig: Optional[NetworkConfig]
    RoleArn: Optional[RoleArn]
    ExperimentConfig: Optional[ExperimentConfig]
    ProcessingJobArn: Optional[ProcessingJobArn]
    ProcessingJobStatus: Optional[ProcessingJobStatus]
    ExitMessage: Optional[ExitMessage]
    FailureReason: Optional[FailureReason]
    ProcessingEndTime: Optional[Timestamp]
    ProcessingStartTime: Optional[Timestamp]
    LastModifiedTime: Optional[Timestamp]
    CreationTime: Optional[Timestamp]
    MonitoringScheduleArn: Optional[MonitoringScheduleArn]
    AutoMLJobArn: Optional[AutoMLJobArn]
    TrainingJobArn: Optional[TrainingJobArn]
    Tags: Optional[TagList]


class ProfilerConfigForUpdate(TypedDict, total=False):
    """Configuration information for updating the Debugger profile parameters,
    system and framework metrics configurations, and storage paths.
    """

    S3OutputPath: Optional[S3Uri]
    ProfilingIntervalInMilliseconds: Optional[ProfilingIntervalInMilliseconds]
    ProfilingParameters: Optional[ProfilingParameters]
    DisableProfiler: Optional[DisableProfiler]


class Project(TypedDict, total=False):
    """The properties of a project as returned by the Search API."""

    ProjectArn: Optional[ProjectArn]
    ProjectName: Optional[ProjectEntityName]
    ProjectId: Optional[ProjectId]
    ProjectDescription: Optional[EntityDescription]
    ServiceCatalogProvisioningDetails: Optional[ServiceCatalogProvisioningDetails]
    ServiceCatalogProvisionedProductDetails: Optional[ServiceCatalogProvisionedProductDetails]
    ProjectStatus: Optional[ProjectStatus]
    CreatedBy: Optional[UserContext]
    CreationTime: Optional[Timestamp]
    Tags: Optional[TagList]
    LastModifiedTime: Optional[Timestamp]
    LastModifiedBy: Optional[UserContext]


class PutModelPackageGroupPolicyInput(ServiceRequest):
    ModelPackageGroupName: EntityName
    ResourcePolicy: PolicyString


class PutModelPackageGroupPolicyOutput(TypedDict, total=False):
    ModelPackageGroupArn: ModelPackageGroupArn


QueryProperties = Dict[String256, String256]
QueryLineageTypes = List[LineageType]
QueryTypes = List[String40]


class QueryFilters(TypedDict, total=False):
    """A set of filters to narrow the set of lineage entities connected to the
    ``StartArn`` (s) returned by the ``QueryLineage`` API action.
    """

    Types: Optional[QueryTypes]
    LineageTypes: Optional[QueryLineageTypes]
    CreatedBefore: Optional[Timestamp]
    CreatedAfter: Optional[Timestamp]
    ModifiedBefore: Optional[Timestamp]
    ModifiedAfter: Optional[Timestamp]
    Properties: Optional[QueryProperties]


QueryLineageStartArns = List[AssociationEntityArn]


class QueryLineageRequest(ServiceRequest):
    StartArns: QueryLineageStartArns
    Direction: Optional[Direction]
    IncludeEdges: Optional[Boolean]
    Filters: Optional[QueryFilters]
    MaxDepth: Optional[QueryLineageMaxDepth]
    MaxResults: Optional[QueryLineageMaxResults]
    NextToken: Optional[String8192]


class Vertex(TypedDict, total=False):
    """A lineage entity connected to the starting entity(ies)."""

    Arn: Optional[AssociationEntityArn]
    Type: Optional[String40]
    LineageType: Optional[LineageType]


Vertices = List[Vertex]


class QueryLineageResponse(TypedDict, total=False):
    Vertices: Optional[Vertices]
    Edges: Optional[Edges]
    NextToken: Optional[String8192]


class RegisterDevicesRequest(ServiceRequest):
    DeviceFleetName: EntityName
    Devices: Devices
    Tags: Optional[TagList]


class RenderableTask(TypedDict, total=False):
    """Contains input values for a task."""

    Input: TaskInput


class RenderUiTemplateRequest(ServiceRequest):
    UiTemplate: Optional[UiTemplate]
    Task: RenderableTask
    RoleArn: RoleArn
    HumanTaskUiArn: Optional[HumanTaskUiArn]


class RenderingError(TypedDict, total=False):
    """A description of an error that occurred while rendering the template."""

    Code: String
    Message: String


RenderingErrorList = List[RenderingError]


class RenderUiTemplateResponse(TypedDict, total=False):
    RenderedContent: String
    Errors: RenderingErrorList


class RetryPipelineExecutionRequest(ServiceRequest):
    PipelineExecutionArn: PipelineExecutionArn
    ClientRequestToken: IdempotencyToken
    ParallelismConfiguration: Optional[ParallelismConfiguration]


class RetryPipelineExecutionResponse(TypedDict, total=False):
    PipelineExecutionArn: Optional[PipelineExecutionArn]


class SearchExpression(TypedDict, total=False):
    """A multi-expression that searches for the specified resource or resources
    in a search. All resource objects that satisfy the expression's
    condition are included in the search results. You must specify at least
    one subexpression, filter, or nested filter. A ``SearchExpression`` can
    contain up to twenty elements.

    A ``SearchExpression`` contains the following components:

    -  A list of ``Filter`` objects. Each filter defines a simple Boolean
       expression comprised of a resource property name, Boolean operator,
       and value.

    -  A list of ``NestedFilter`` objects. Each nested filter defines a list
       of Boolean expressions using a list of resource properties. A nested
       filter is satisfied if a single object in the list satisfies all
       Boolean expressions.

    -  A list of ``SearchExpression`` objects. A search expression object
       can be nested in a list of search expression objects.

    -  A Boolean operator: ``And`` or ``Or``.
    """

    Filters: Optional["FilterList"]
    NestedFilters: Optional["NestedFiltersList"]
    SubExpressions: Optional["SearchExpressionList"]
    Operator: Optional["BooleanOperator"]


SearchExpressionList = List[SearchExpression]


class TransformJob(TypedDict, total=False):
    """A batch transform job. For information about SageMaker batch transform,
    see `Use Batch
    Transform <https://docs.aws.amazon.com/sagemaker/latest/dg/batch-transform.html>`__.
    """

    TransformJobName: Optional[TransformJobName]
    TransformJobArn: Optional[TransformJobArn]
    TransformJobStatus: Optional[TransformJobStatus]
    FailureReason: Optional[FailureReason]
    ModelName: Optional[ModelName]
    MaxConcurrentTransforms: Optional[MaxConcurrentTransforms]
    ModelClientConfig: Optional[ModelClientConfig]
    MaxPayloadInMB: Optional[MaxPayloadInMB]
    BatchStrategy: Optional[BatchStrategy]
    Environment: Optional[TransformEnvironmentMap]
    TransformInput: Optional[TransformInput]
    TransformOutput: Optional[TransformOutput]
    TransformResources: Optional[TransformResources]
    CreationTime: Optional[Timestamp]
    TransformStartTime: Optional[Timestamp]
    TransformEndTime: Optional[Timestamp]
    LabelingJobArn: Optional[LabelingJobArn]
    AutoMLJobArn: Optional[AutoMLJobArn]
    DataProcessing: Optional[DataProcessing]
    ExperimentConfig: Optional[ExperimentConfig]
    Tags: Optional[TagList]


class TrainingJob(TypedDict, total=False):
    """Contains information about a training job."""

    TrainingJobName: Optional[TrainingJobName]
    TrainingJobArn: Optional[TrainingJobArn]
    TuningJobArn: Optional[HyperParameterTuningJobArn]
    LabelingJobArn: Optional[LabelingJobArn]
    AutoMLJobArn: Optional[AutoMLJobArn]
    ModelArtifacts: Optional[ModelArtifacts]
    TrainingJobStatus: Optional[TrainingJobStatus]
    SecondaryStatus: Optional[SecondaryStatus]
    FailureReason: Optional[FailureReason]
    HyperParameters: Optional[HyperParameters]
    AlgorithmSpecification: Optional[AlgorithmSpecification]
    RoleArn: Optional[RoleArn]
    InputDataConfig: Optional[InputDataConfig]
    OutputDataConfig: Optional[OutputDataConfig]
    ResourceConfig: Optional[ResourceConfig]
    VpcConfig: Optional[VpcConfig]
    StoppingCondition: Optional[StoppingCondition]
    CreationTime: Optional[Timestamp]
    TrainingStartTime: Optional[Timestamp]
    TrainingEndTime: Optional[Timestamp]
    LastModifiedTime: Optional[Timestamp]
    SecondaryStatusTransitions: Optional[SecondaryStatusTransitions]
    FinalMetricDataList: Optional[FinalMetricDataList]
    EnableNetworkIsolation: Optional[Boolean]
    EnableInterContainerTrafficEncryption: Optional[Boolean]
    EnableManagedSpotTraining: Optional[Boolean]
    CheckpointConfig: Optional[CheckpointConfig]
    TrainingTimeInSeconds: Optional[TrainingTimeInSeconds]
    BillableTimeInSeconds: Optional[BillableTimeInSeconds]
    DebugHookConfig: Optional[DebugHookConfig]
    ExperimentConfig: Optional[ExperimentConfig]
    DebugRuleConfigurations: Optional[DebugRuleConfigurations]
    TensorBoardOutputConfig: Optional[TensorBoardOutputConfig]
    DebugRuleEvaluationStatuses: Optional[DebugRuleEvaluationStatuses]
    Environment: Optional[TrainingEnvironmentMap]
    RetryStrategy: Optional[RetryStrategy]
    Tags: Optional[TagList]


class TrialComponentSourceDetail(TypedDict, total=False):
    """Detailed information about the source of a trial component. Either
    ``ProcessingJob`` or ``TrainingJob`` is returned.
    """

    SourceArn: Optional[TrialComponentSourceArn]
    TrainingJob: Optional[TrainingJob]
    ProcessingJob: Optional[ProcessingJob]
    TransformJob: Optional[TransformJob]


class TrialComponent(TypedDict, total=False):
    """The properties of a trial component as returned by the Search API."""

    TrialComponentName: Optional[ExperimentEntityName]
    DisplayName: Optional[ExperimentEntityName]
    TrialComponentArn: Optional[TrialComponentArn]
    Source: Optional[TrialComponentSource]
    Status: Optional[TrialComponentStatus]
    StartTime: Optional[Timestamp]
    EndTime: Optional[Timestamp]
    CreationTime: Optional[Timestamp]
    CreatedBy: Optional[UserContext]
    LastModifiedTime: Optional[Timestamp]
    LastModifiedBy: Optional[UserContext]
    Parameters: Optional[TrialComponentParameters]
    InputArtifacts: Optional[TrialComponentArtifacts]
    OutputArtifacts: Optional[TrialComponentArtifacts]
    Metrics: Optional[TrialComponentMetricSummaries]
    MetadataProperties: Optional[MetadataProperties]
    SourceDetail: Optional[TrialComponentSourceDetail]
    LineageGroupArn: Optional[LineageGroupArn]
    Tags: Optional[TagList]
    Parents: Optional[Parents]


class TrialComponentSimpleSummary(TypedDict, total=False):
    """A short summary of a trial component."""

    TrialComponentName: Optional[ExperimentEntityName]
    TrialComponentArn: Optional[TrialComponentArn]
    TrialComponentSource: Optional[TrialComponentSource]
    CreationTime: Optional[Timestamp]
    CreatedBy: Optional[UserContext]


TrialComponentSimpleSummaries = List[TrialComponentSimpleSummary]


class Trial(TypedDict, total=False):
    """The properties of a trial as returned by the Search API."""

    TrialName: Optional[ExperimentEntityName]
    TrialArn: Optional[TrialArn]
    DisplayName: Optional[ExperimentEntityName]
    ExperimentName: Optional[ExperimentEntityName]
    Source: Optional[TrialSource]
    CreationTime: Optional[Timestamp]
    CreatedBy: Optional[UserContext]
    LastModifiedTime: Optional[Timestamp]
    LastModifiedBy: Optional[UserContext]
    MetadataProperties: Optional[MetadataProperties]
    Tags: Optional[TagList]
    TrialComponentSummaries: Optional[TrialComponentSimpleSummaries]


class SearchRecord(TypedDict, total=False):
    """A single resource returned as part of the Search API response."""

    TrainingJob: Optional[TrainingJob]
    Experiment: Optional[Experiment]
    Trial: Optional[Trial]
    TrialComponent: Optional[TrialComponent]
    Endpoint: Optional[Endpoint]
    ModelPackage: Optional[ModelPackage]
    ModelPackageGroup: Optional[ModelPackageGroup]
    Pipeline: Optional[Pipeline]
    PipelineExecution: Optional[PipelineExecution]
    FeatureGroup: Optional[FeatureGroup]
    Project: Optional[Project]


class SearchRequest(ServiceRequest):
    Resource: ResourceType
    SearchExpression: Optional[SearchExpression]
    SortBy: Optional[ResourcePropertyName]
    SortOrder: Optional[SearchSortOrder]
    NextToken: Optional[NextToken]
    MaxResults: Optional[MaxResults]


SearchResultsList = List[SearchRecord]


class SearchResponse(TypedDict, total=False):
    Results: Optional[SearchResultsList]
    NextToken: Optional[NextToken]


class SendPipelineExecutionStepFailureRequest(ServiceRequest):
    CallbackToken: CallbackToken
    FailureReason: Optional[String256]
    ClientRequestToken: Optional[IdempotencyToken]


class SendPipelineExecutionStepFailureResponse(TypedDict, total=False):
    PipelineExecutionArn: Optional[PipelineExecutionArn]


class SendPipelineExecutionStepSuccessRequest(ServiceRequest):
    CallbackToken: CallbackToken
    OutputParameters: Optional[OutputParameterList]
    ClientRequestToken: Optional[IdempotencyToken]


class SendPipelineExecutionStepSuccessResponse(TypedDict, total=False):
    PipelineExecutionArn: Optional[PipelineExecutionArn]


class ServiceCatalogProvisioningUpdateDetails(TypedDict, total=False):
    """Details that you specify to provision a service catalog product. For
    information about service catalog, see `What is Amazon Web Services
    Service
    Catalog <https://docs.aws.amazon.com/servicecatalog/latest/adminguide/introduction.html>`__.
    """

    ProvisioningArtifactId: Optional[ServiceCatalogEntityId]
    ProvisioningParameters: Optional[ProvisioningParameters]


class StartMonitoringScheduleRequest(ServiceRequest):
    MonitoringScheduleName: MonitoringScheduleName


class StartNotebookInstanceInput(ServiceRequest):
    NotebookInstanceName: NotebookInstanceName


class StartPipelineExecutionRequest(ServiceRequest):
    PipelineName: PipelineName
    PipelineExecutionDisplayName: Optional[PipelineExecutionName]
    PipelineParameters: Optional[ParameterList]
    PipelineExecutionDescription: Optional[PipelineExecutionDescription]
    ClientRequestToken: IdempotencyToken
    ParallelismConfiguration: Optional[ParallelismConfiguration]


class StartPipelineExecutionResponse(TypedDict, total=False):
    PipelineExecutionArn: Optional[PipelineExecutionArn]


class StopAutoMLJobRequest(ServiceRequest):
    AutoMLJobName: AutoMLJobName


class StopCompilationJobRequest(ServiceRequest):
    CompilationJobName: EntityName


class StopEdgePackagingJobRequest(ServiceRequest):
    EdgePackagingJobName: EntityName


class StopHyperParameterTuningJobRequest(ServiceRequest):
    HyperParameterTuningJobName: HyperParameterTuningJobName


class StopInferenceRecommendationsJobRequest(ServiceRequest):
    JobName: RecommendationJobName


class StopLabelingJobRequest(ServiceRequest):
    LabelingJobName: LabelingJobName


class StopMonitoringScheduleRequest(ServiceRequest):
    MonitoringScheduleName: MonitoringScheduleName


class StopNotebookInstanceInput(ServiceRequest):
    NotebookInstanceName: NotebookInstanceName


class StopPipelineExecutionRequest(ServiceRequest):
    PipelineExecutionArn: PipelineExecutionArn
    ClientRequestToken: IdempotencyToken


class StopPipelineExecutionResponse(TypedDict, total=False):
    PipelineExecutionArn: Optional[PipelineExecutionArn]


class StopProcessingJobRequest(ServiceRequest):
    ProcessingJobName: ProcessingJobName


class StopTrainingJobRequest(ServiceRequest):
    TrainingJobName: TrainingJobName


class StopTransformJobRequest(ServiceRequest):
    TransformJobName: TransformJobName


class UpdateActionRequest(ServiceRequest):
    ActionName: ExperimentEntityName
    Description: Optional[ExperimentDescription]
    Status: Optional[ActionStatus]
    Properties: Optional[LineageEntityParameters]
    PropertiesToRemove: Optional[ListLineageEntityParameterKey]


class UpdateActionResponse(TypedDict, total=False):
    ActionArn: Optional[ActionArn]


class UpdateAppImageConfigRequest(ServiceRequest):
    AppImageConfigName: AppImageConfigName
    KernelGatewayImageConfig: Optional[KernelGatewayImageConfig]


class UpdateAppImageConfigResponse(TypedDict, total=False):
    AppImageConfigArn: Optional[AppImageConfigArn]


class UpdateArtifactRequest(ServiceRequest):
    ArtifactArn: ArtifactArn
    ArtifactName: Optional[ExperimentEntityName]
    Properties: Optional[LineageEntityParameters]
    PropertiesToRemove: Optional[ListLineageEntityParameterKey]


class UpdateArtifactResponse(TypedDict, total=False):
    ArtifactArn: Optional[ArtifactArn]


class UpdateCodeRepositoryInput(ServiceRequest):
    CodeRepositoryName: EntityName
    GitConfig: Optional[GitConfigForUpdate]


class UpdateCodeRepositoryOutput(TypedDict, total=False):
    CodeRepositoryArn: CodeRepositoryArn


class UpdateContextRequest(ServiceRequest):
    ContextName: ExperimentEntityName
    Description: Optional[ExperimentDescription]
    Properties: Optional[LineageEntityParameters]
    PropertiesToRemove: Optional[ListLineageEntityParameterKey]


class UpdateContextResponse(TypedDict, total=False):
    ContextArn: Optional[ContextArn]


class UpdateDeviceFleetRequest(ServiceRequest):
    DeviceFleetName: EntityName
    RoleArn: Optional[RoleArn]
    Description: Optional[DeviceFleetDescription]
    OutputConfig: EdgeOutputConfig
    EnableIotRoleAlias: Optional[EnableIotRoleAlias]


class UpdateDevicesRequest(ServiceRequest):
    DeviceFleetName: EntityName
    Devices: Devices


class UpdateDomainRequest(ServiceRequest):
    DomainId: DomainId
    DefaultUserSettings: Optional[UserSettings]
    DomainSettingsForUpdate: Optional[DomainSettingsForUpdate]


class UpdateDomainResponse(TypedDict, total=False):
    DomainArn: Optional[DomainArn]


class VariantProperty(TypedDict, total=False):
    """Specifies a production variant property type for an Endpoint.

    If you are updating an endpoint with the
    UpdateEndpointInput$RetainAllVariantProperties option set to ``true``,
    the ``VariantProperty`` objects listed in
    UpdateEndpointInput$ExcludeRetainedVariantProperties override the
    existing variant properties of the endpoint.
    """

    VariantPropertyType: VariantPropertyType


VariantPropertyList = List[VariantProperty]


class UpdateEndpointInput(ServiceRequest):
    EndpointName: EndpointName
    EndpointConfigName: EndpointConfigName
    RetainAllVariantProperties: Optional[Boolean]
    ExcludeRetainedVariantProperties: Optional[VariantPropertyList]
    DeploymentConfig: Optional[DeploymentConfig]
    RetainDeploymentConfig: Optional[Boolean]


class UpdateEndpointOutput(TypedDict, total=False):
    EndpointArn: EndpointArn


class UpdateEndpointWeightsAndCapacitiesInput(ServiceRequest):
    EndpointName: EndpointName
    DesiredWeightsAndCapacities: DesiredWeightAndCapacityList


class UpdateEndpointWeightsAndCapacitiesOutput(TypedDict, total=False):
    EndpointArn: EndpointArn


class UpdateExperimentRequest(ServiceRequest):
    ExperimentName: ExperimentEntityName
    DisplayName: Optional[ExperimentEntityName]
    Description: Optional[ExperimentDescription]


class UpdateExperimentResponse(TypedDict, total=False):
    ExperimentArn: Optional[ExperimentArn]


class UpdateImageRequest(ServiceRequest):
    DeleteProperties: Optional[ImageDeletePropertyList]
    Description: Optional[ImageDescription]
    DisplayName: Optional[ImageDisplayName]
    ImageName: ImageName
    RoleArn: Optional[RoleArn]


class UpdateImageResponse(TypedDict, total=False):
    ImageArn: Optional[ImageArn]


class UpdateModelPackageInput(ServiceRequest):
    ModelPackageArn: ModelPackageArn
    ModelApprovalStatus: Optional[ModelApprovalStatus]
    ApprovalDescription: Optional[ApprovalDescription]
    CustomerMetadataProperties: Optional[CustomerMetadataMap]
    CustomerMetadataPropertiesToRemove: Optional[CustomerMetadataKeyList]
    AdditionalInferenceSpecificationsToAdd: Optional[AdditionalInferenceSpecifications]


class UpdateModelPackageOutput(TypedDict, total=False):
    ModelPackageArn: ModelPackageArn


class UpdateMonitoringScheduleRequest(ServiceRequest):
    MonitoringScheduleName: MonitoringScheduleName
    MonitoringScheduleConfig: MonitoringScheduleConfig


class UpdateMonitoringScheduleResponse(TypedDict, total=False):
    MonitoringScheduleArn: MonitoringScheduleArn


class UpdateNotebookInstanceInput(ServiceRequest):
    NotebookInstanceName: NotebookInstanceName
    InstanceType: Optional[InstanceType]
    RoleArn: Optional[RoleArn]
    LifecycleConfigName: Optional[NotebookInstanceLifecycleConfigName]
    DisassociateLifecycleConfig: Optional[DisassociateNotebookInstanceLifecycleConfig]
    VolumeSizeInGB: Optional[NotebookInstanceVolumeSizeInGB]
    DefaultCodeRepository: Optional[CodeRepositoryNameOrUrl]
    AdditionalCodeRepositories: Optional[AdditionalCodeRepositoryNamesOrUrls]
    AcceleratorTypes: Optional[NotebookInstanceAcceleratorTypes]
    DisassociateAcceleratorTypes: Optional[DisassociateNotebookInstanceAcceleratorTypes]
    DisassociateDefaultCodeRepository: Optional[DisassociateDefaultCodeRepository]
    DisassociateAdditionalCodeRepositories: Optional[DisassociateAdditionalCodeRepositories]
    RootAccess: Optional[RootAccess]


class UpdateNotebookInstanceLifecycleConfigInput(ServiceRequest):
    NotebookInstanceLifecycleConfigName: NotebookInstanceLifecycleConfigName
    OnCreate: Optional[NotebookInstanceLifecycleConfigList]
    OnStart: Optional[NotebookInstanceLifecycleConfigList]


class UpdateNotebookInstanceLifecycleConfigOutput(TypedDict, total=False):
    pass


class UpdateNotebookInstanceOutput(TypedDict, total=False):
    pass


class UpdatePipelineExecutionRequest(ServiceRequest):
    PipelineExecutionArn: PipelineExecutionArn
    PipelineExecutionDescription: Optional[PipelineExecutionDescription]
    PipelineExecutionDisplayName: Optional[PipelineExecutionName]
    ParallelismConfiguration: Optional[ParallelismConfiguration]


class UpdatePipelineExecutionResponse(TypedDict, total=False):
    PipelineExecutionArn: Optional[PipelineExecutionArn]


class UpdatePipelineRequest(ServiceRequest):
    PipelineName: PipelineName
    PipelineDisplayName: Optional[PipelineName]
    PipelineDefinition: Optional[PipelineDefinition]
    PipelineDefinitionS3Location: Optional[PipelineDefinitionS3Location]
    PipelineDescription: Optional[PipelineDescription]
    RoleArn: Optional[RoleArn]
    ParallelismConfiguration: Optional[ParallelismConfiguration]


class UpdatePipelineResponse(TypedDict, total=False):
    PipelineArn: Optional[PipelineArn]


class UpdateProjectInput(ServiceRequest):
    ProjectName: ProjectEntityName
    ProjectDescription: Optional[EntityDescription]
    ServiceCatalogProvisioningUpdateDetails: Optional[ServiceCatalogProvisioningUpdateDetails]
    Tags: Optional[TagList]


class UpdateProjectOutput(TypedDict, total=False):
    ProjectArn: ProjectArn


class UpdateTrainingJobRequest(ServiceRequest):
    TrainingJobName: TrainingJobName
    ProfilerConfig: Optional[ProfilerConfigForUpdate]
    ProfilerRuleConfigurations: Optional[ProfilerRuleConfigurations]


class UpdateTrainingJobResponse(TypedDict, total=False):
    TrainingJobArn: TrainingJobArn


class UpdateTrialComponentRequest(ServiceRequest):
    TrialComponentName: ExperimentEntityName
    DisplayName: Optional[ExperimentEntityName]
    Status: Optional[TrialComponentStatus]
    StartTime: Optional[Timestamp]
    EndTime: Optional[Timestamp]
    Parameters: Optional[TrialComponentParameters]
    ParametersToRemove: Optional[ListTrialComponentKey256]
    InputArtifacts: Optional[TrialComponentArtifacts]
    InputArtifactsToRemove: Optional[ListTrialComponentKey256]
    OutputArtifacts: Optional[TrialComponentArtifacts]
    OutputArtifactsToRemove: Optional[ListTrialComponentKey256]


class UpdateTrialComponentResponse(TypedDict, total=False):
    TrialComponentArn: Optional[TrialComponentArn]


class UpdateTrialRequest(ServiceRequest):
    TrialName: ExperimentEntityName
    DisplayName: Optional[ExperimentEntityName]


class UpdateTrialResponse(TypedDict, total=False):
    TrialArn: Optional[TrialArn]


class UpdateUserProfileRequest(ServiceRequest):
    DomainId: DomainId
    UserProfileName: UserProfileName
    UserSettings: Optional[UserSettings]


class UpdateUserProfileResponse(TypedDict, total=False):
    UserProfileArn: Optional[UserProfileArn]


class UpdateWorkforceRequest(ServiceRequest):
    WorkforceName: WorkforceName
    SourceIpConfig: Optional[SourceIpConfig]
    OidcConfig: Optional[OidcConfig]


class UpdateWorkforceResponse(TypedDict, total=False):
    Workforce: Workforce


class UpdateWorkteamRequest(ServiceRequest):
    WorkteamName: WorkteamName
    MemberDefinitions: Optional[MemberDefinitions]
    Description: Optional[String200]
    NotificationConfiguration: Optional[NotificationConfiguration]


class UpdateWorkteamResponse(TypedDict, total=False):
    Workteam: Workteam


class SagemakerApi:

    service = "sagemaker"
    version = "2017-07-24"

    @handler("AddAssociation")
    def add_association(
        self,
        context: RequestContext,
        source_arn: AssociationEntityArn,
        destination_arn: AssociationEntityArn,
        association_type: AssociationEdgeType = None,
    ) -> AddAssociationResponse:
        """Creates an *association* between the source and the destination. A
        source can be associated with multiple destinations, and a destination
        can be associated with multiple sources. An association is a lineage
        tracking entity. For more information, see `Amazon SageMaker ML Lineage
        Tracking <https://docs.aws.amazon.com/sagemaker/latest/dg/lineage-tracking.html>`__.

        :param source_arn: The ARN of the source.
        :param destination_arn: The Amazon Resource Name (ARN) of the destination.
        :param association_type: The type of association.
        :returns: AddAssociationResponse
        :raises ResourceNotFound:
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("AddTags")
    def add_tags(
        self, context: RequestContext, resource_arn: ResourceArn, tags: TagList
    ) -> AddTagsOutput:
        """Adds or overwrites one or more tags for the specified SageMaker
        resource. You can add tags to notebook instances, training jobs,
        hyperparameter tuning jobs, batch transform jobs, models, labeling jobs,
        work teams, endpoint configurations, and endpoints.

        Each tag consists of a key and an optional value. Tag keys must be
        unique per resource. For more information about tags, see For more
        information, see `Amazon Web Services Tagging
        Strategies <https://aws.amazon.com/answers/account-management/aws-tagging-strategies/>`__.

        Tags that you add to a hyperparameter tuning job by calling this API are
        also added to any training jobs that the hyperparameter tuning job
        launches after you call this API, but not to training jobs that the
        hyperparameter tuning job launched before you called this API. To make
        sure that the tags associated with a hyperparameter tuning job are also
        added to all training jobs that the hyperparameter tuning job launches,
        add the tags when you first create the tuning job by specifying them in
        the ``Tags`` parameter of CreateHyperParameterTuningJob

        Tags that you add to a SageMaker Studio Domain or User Profile by
        calling this API are also added to any Apps that the Domain or User
        Profile launches after you call this API, but not to Apps that the
        Domain or User Profile launched before you called this API. To make sure
        that the tags associated with a Domain or User Profile are also added to
        all Apps that the Domain or User Profile launches, add the tags when you
        first create the Domain or User Profile by specifying them in the
        ``Tags`` parameter of CreateDomain or CreateUserProfile.

        :param resource_arn: The Amazon Resource Name (ARN) of the resource that you want to tag.
        :param tags: An array of key-value pairs.
        :returns: AddTagsOutput
        """
        raise NotImplementedError

    @handler("AssociateTrialComponent")
    def associate_trial_component(
        self,
        context: RequestContext,
        trial_component_name: ExperimentEntityName,
        trial_name: ExperimentEntityName,
    ) -> AssociateTrialComponentResponse:
        """Associates a trial component with a trial. A trial component can be
        associated with multiple trials. To disassociate a trial component from
        a trial, call the DisassociateTrialComponent API.

        :param trial_component_name: The name of the component to associated with the trial.
        :param trial_name: The name of the trial to associate with.
        :returns: AssociateTrialComponentResponse
        :raises ResourceNotFound:
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("BatchDescribeModelPackage")
    def batch_describe_model_package(
        self, context: RequestContext, model_package_arn_list: ModelPackageArnList
    ) -> BatchDescribeModelPackageOutput:
        """This action batch describes a list of versioned model packages

        :param model_package_arn_list: The list of Amazon Resource Name (ARN) of the model package groups.
        :returns: BatchDescribeModelPackageOutput
        """
        raise NotImplementedError

    @handler("CreateAction")
    def create_action(
        self,
        context: RequestContext,
        action_name: ExperimentEntityName,
        source: ActionSource,
        action_type: String256,
        description: ExperimentDescription = None,
        status: ActionStatus = None,
        properties: LineageEntityParameters = None,
        metadata_properties: MetadataProperties = None,
        tags: TagList = None,
    ) -> CreateActionResponse:
        """Creates an *action*. An action is a lineage tracking entity that
        represents an action or activity. For example, a model deployment or an
        HPO job. Generally, an action involves at least one input or output
        artifact. For more information, see `Amazon SageMaker ML Lineage
        Tracking <https://docs.aws.amazon.com/sagemaker/latest/dg/lineage-tracking.html>`__.

        :param action_name: The name of the action.
        :param source: The source type, ID, and URI.
        :param action_type: The action type.
        :param description: The description of the action.
        :param status: The status of the action.
        :param properties: A list of properties to add to the action.
        :param metadata_properties: Metadata properties of the tracking entity, trial, or trial component.
        :param tags: A list of tags to apply to the action.
        :returns: CreateActionResponse
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("CreateAlgorithm")
    def create_algorithm(
        self,
        context: RequestContext,
        algorithm_name: EntityName,
        training_specification: TrainingSpecification,
        algorithm_description: EntityDescription = None,
        inference_specification: InferenceSpecification = None,
        validation_specification: AlgorithmValidationSpecification = None,
        certify_for_marketplace: CertifyForMarketplace = None,
        tags: TagList = None,
    ) -> CreateAlgorithmOutput:
        """Create a machine learning algorithm that you can use in SageMaker and
        list in the Amazon Web Services Marketplace.

        :param algorithm_name: The name of the algorithm.
        :param training_specification: Specifies details about training jobs run by this algorithm, including
        the following:

        -  The Amazon ECR path of the container and the version digest of the
           algorithm.
        :param algorithm_description: A description of the algorithm.
        :param inference_specification: Specifies details about inference jobs that the algorithm runs,
        including the following:

        -  The Amazon ECR paths of containers that contain the inference code
           and model artifacts.
        :param validation_specification: Specifies configurations for one or more training jobs and that
        SageMaker runs to test the algorithm's training code and, optionally,
        one or more batch transform jobs that SageMaker runs to test the
        algorithm's inference code.
        :param certify_for_marketplace: Whether to certify the algorithm so that it can be listed in Amazon Web
        Services Marketplace.
        :param tags: An array of key-value pairs.
        :returns: CreateAlgorithmOutput
        """
        raise NotImplementedError

    @handler("CreateApp")
    def create_app(
        self,
        context: RequestContext,
        domain_id: DomainId,
        user_profile_name: UserProfileName,
        app_type: AppType,
        app_name: AppName,
        tags: TagList = None,
        resource_spec: ResourceSpec = None,
    ) -> CreateAppResponse:
        """Creates a running app for the specified UserProfile. Supported apps are
        ``JupyterServer`` and ``KernelGateway``. This operation is automatically
        invoked by Amazon SageMaker Studio upon access to the associated Domain,
        and when new kernel configurations are selected by the user. A user may
        have multiple Apps active simultaneously.

        :param domain_id: The domain ID.
        :param user_profile_name: The user profile name.
        :param app_type: The type of app.
        :param app_name: The name of the app.
        :param tags: Each tag consists of a key and an optional value.
        :param resource_spec: The instance type and the Amazon Resource Name (ARN) of the SageMaker
        image created on the instance.
        :returns: CreateAppResponse
        :raises ResourceLimitExceeded:
        :raises ResourceInUse:
        """
        raise NotImplementedError

    @handler("CreateAppImageConfig")
    def create_app_image_config(
        self,
        context: RequestContext,
        app_image_config_name: AppImageConfigName,
        tags: TagList = None,
        kernel_gateway_image_config: KernelGatewayImageConfig = None,
    ) -> CreateAppImageConfigResponse:
        """Creates a configuration for running a SageMaker image as a KernelGateway
        app. The configuration specifies the Amazon Elastic File System (EFS)
        storage volume on the image, and a list of the kernels in the image.

        :param app_image_config_name: The name of the AppImageConfig.
        :param tags: A list of tags to apply to the AppImageConfig.
        :param kernel_gateway_image_config: The KernelGatewayImageConfig.
        :returns: CreateAppImageConfigResponse
        :raises ResourceInUse:
        """
        raise NotImplementedError

    @handler("CreateArtifact")
    def create_artifact(
        self,
        context: RequestContext,
        source: ArtifactSource,
        artifact_type: String256,
        artifact_name: ExperimentEntityName = None,
        properties: LineageEntityParameters = None,
        metadata_properties: MetadataProperties = None,
        tags: TagList = None,
    ) -> CreateArtifactResponse:
        """Creates an *artifact*. An artifact is a lineage tracking entity that
        represents a URI addressable object or data. Some examples are the S3
        URI of a dataset and the ECR registry path of an image. For more
        information, see `Amazon SageMaker ML Lineage
        Tracking <https://docs.aws.amazon.com/sagemaker/latest/dg/lineage-tracking.html>`__.

        :param source: The ID, ID type, and URI of the source.
        :param artifact_type: The artifact type.
        :param artifact_name: The name of the artifact.
        :param properties: A list of properties to add to the artifact.
        :param metadata_properties: Metadata properties of the tracking entity, trial, or trial component.
        :param tags: A list of tags to apply to the artifact.
        :returns: CreateArtifactResponse
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("CreateAutoMLJob")
    def create_auto_ml_job(
        self,
        context: RequestContext,
        auto_ml_job_name: AutoMLJobName,
        input_data_config: AutoMLInputDataConfig,
        output_data_config: AutoMLOutputDataConfig,
        role_arn: RoleArn,
        problem_type: ProblemType = None,
        auto_ml_job_objective: AutoMLJobObjective = None,
        auto_ml_job_config: AutoMLJobConfig = None,
        generate_candidate_definitions_only: GenerateCandidateDefinitionsOnly = None,
        tags: TagList = None,
        model_deploy_config: ModelDeployConfig = None,
    ) -> CreateAutoMLJobResponse:
        """Creates an Autopilot job.

        Find the best-performing model after you run an Autopilot job by calling
        .

        For information about how to use Autopilot, see `Automate Model
        Development with Amazon SageMaker
        Autopilot <https://docs.aws.amazon.com/sagemaker/latest/dg/autopilot-automate-model-development.html>`__.

        :param auto_ml_job_name: Identifies an Autopilot job.
        :param input_data_config: An array of channel objects that describes the input data and its
        location.
        :param output_data_config: Provides information about encryption and the Amazon S3 output path
        needed to store artifacts from an AutoML job.
        :param role_arn: The ARN of the role that is used to access the data.
        :param problem_type: Defines the type of supervised learning available for the candidates.
        :param auto_ml_job_objective: Defines the objective metric used to measure the predictive quality of
        an AutoML job.
        :param auto_ml_job_config: Contains ``CompletionCriteria`` and ``SecurityConfig`` settings for the
        AutoML job.
        :param generate_candidate_definitions_only: Generates possible candidates without training the models.
        :param tags: Each tag consists of a key and an optional value.
        :param model_deploy_config: Specifies how to generate the endpoint name for an automatic one-click
        Autopilot model deployment.
        :returns: CreateAutoMLJobResponse
        :raises ResourceInUse:
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("CreateCodeRepository")
    def create_code_repository(
        self,
        context: RequestContext,
        code_repository_name: EntityName,
        git_config: GitConfig,
        tags: TagList = None,
    ) -> CreateCodeRepositoryOutput:
        """Creates a Git repository as a resource in your SageMaker account. You
        can associate the repository with notebook instances so that you can use
        Git source control for the notebooks you create. The Git repository is a
        resource in your SageMaker account, so it can be associated with more
        than one notebook instance, and it persists independently from the
        lifecycle of any notebook instances it is associated with.

        The repository can be hosted either in `Amazon Web Services
        CodeCommit <https://docs.aws.amazon.com/codecommit/latest/userguide/welcome.html>`__
        or in any other Git repository.

        :param code_repository_name: The name of the Git repository.
        :param git_config: Specifies details about the repository, including the URL where the
        repository is located, the default branch, and credentials to use to
        access the repository.
        :param tags: An array of key-value pairs.
        :returns: CreateCodeRepositoryOutput
        """
        raise NotImplementedError

    @handler("CreateCompilationJob")
    def create_compilation_job(
        self,
        context: RequestContext,
        compilation_job_name: EntityName,
        role_arn: RoleArn,
        output_config: OutputConfig,
        stopping_condition: StoppingCondition,
        model_package_version_arn: ModelPackageArn = None,
        input_config: InputConfig = None,
        vpc_config: NeoVpcConfig = None,
        tags: TagList = None,
    ) -> CreateCompilationJobResponse:
        """Starts a model compilation job. After the model has been compiled,
        Amazon SageMaker saves the resulting model artifacts to an Amazon Simple
        Storage Service (Amazon S3) bucket that you specify.

        If you choose to host your model using Amazon SageMaker hosting
        services, you can use the resulting model artifacts as part of the
        model. You can also use the artifacts with Amazon Web Services IoT
        Greengrass. In that case, deploy them as an ML resource.

        In the request body, you provide the following:

        -  A name for the compilation job

        -  Information about the input model artifacts

        -  The output location for the compiled model and the device (target)
           that the model runs on

        -  The Amazon Resource Name (ARN) of the IAM role that Amazon SageMaker
           assumes to perform the model compilation job.

        You can also provide a ``Tag`` to track the model compilation job's
        resource use and costs. The response body contains the
        ``CompilationJobArn`` for the compiled job.

        To stop a model compilation job, use StopCompilationJob. To get
        information about a particular model compilation job, use
        DescribeCompilationJob. To get information about multiple model
        compilation jobs, use ListCompilationJobs.

        :param compilation_job_name: A name for the model compilation job.
        :param role_arn: The Amazon Resource Name (ARN) of an IAM role that enables Amazon
        SageMaker to perform tasks on your behalf.
        :param output_config: Provides information about the output location for the compiled model
        and the target device the model runs on.
        :param stopping_condition: Specifies a limit to how long a model compilation job can run.
        :param model_package_version_arn: The Amazon Resource Name (ARN) of a versioned model package.
        :param input_config: Provides information about the location of input model artifacts, the
        name and shape of the expected data inputs, and the framework in which
        the model was trained.
        :param vpc_config: A VpcConfig object that specifies the VPC that you want your compilation
        job to connect to.
        :param tags: An array of key-value pairs.
        :returns: CreateCompilationJobResponse
        :raises ResourceInUse:
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("CreateContext")
    def create_context(
        self,
        context: RequestContext,
        context_name: ExperimentEntityName,
        source: ContextSource,
        context_type: String256,
        description: ExperimentDescription = None,
        properties: LineageEntityParameters = None,
        tags: TagList = None,
    ) -> CreateContextResponse:
        """Creates a *context*. A context is a lineage tracking entity that
        represents a logical grouping of other tracking or experiment entities.
        Some examples are an endpoint and a model package. For more information,
        see `Amazon SageMaker ML Lineage
        Tracking <https://docs.aws.amazon.com/sagemaker/latest/dg/lineage-tracking.html>`__.

        :param context_name: The name of the context.
        :param source: The source type, ID, and URI.
        :param context_type: The context type.
        :param description: The description of the context.
        :param properties: A list of properties to add to the context.
        :param tags: A list of tags to apply to the context.
        :returns: CreateContextResponse
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("CreateDataQualityJobDefinition")
    def create_data_quality_job_definition(
        self,
        context: RequestContext,
        job_definition_name: MonitoringJobDefinitionName,
        data_quality_app_specification: DataQualityAppSpecification,
        data_quality_job_input: DataQualityJobInput,
        data_quality_job_output_config: MonitoringOutputConfig,
        job_resources: MonitoringResources,
        role_arn: RoleArn,
        data_quality_baseline_config: DataQualityBaselineConfig = None,
        network_config: MonitoringNetworkConfig = None,
        stopping_condition: MonitoringStoppingCondition = None,
        tags: TagList = None,
    ) -> CreateDataQualityJobDefinitionResponse:
        """Creates a definition for a job that monitors data quality and drift. For
        information about model monitor, see `Amazon SageMaker Model
        Monitor <https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html>`__.

        :param job_definition_name: The name for the monitoring job definition.
        :param data_quality_app_specification: Specifies the container that runs the monitoring job.
        :param data_quality_job_input: A list of inputs for the monitoring job.
        :param data_quality_job_output_config: The output configuration for monitoring jobs.
        :param job_resources: Identifies the resources to deploy for a monitoring job.
        :param role_arn: The Amazon Resource Name (ARN) of an IAM role that Amazon SageMaker can
        assume to perform tasks on your behalf.
        :param data_quality_baseline_config: Configures the constraints and baselines for the monitoring job.
        :param network_config: Specifies networking configuration for the monitoring job.
        :param stopping_condition: A time limit for how long the monitoring job is allowed to run before
        stopping.
        :param tags: (Optional) An array of key-value pairs.
        :returns: CreateDataQualityJobDefinitionResponse
        :raises ResourceLimitExceeded:
        :raises ResourceInUse:
        """
        raise NotImplementedError

    @handler("CreateDeviceFleet")
    def create_device_fleet(
        self,
        context: RequestContext,
        device_fleet_name: EntityName,
        output_config: EdgeOutputConfig,
        role_arn: RoleArn = None,
        description: DeviceFleetDescription = None,
        tags: TagList = None,
        enable_iot_role_alias: EnableIotRoleAlias = None,
    ) -> None:
        """Creates a device fleet.

        :param device_fleet_name: The name of the fleet that the device belongs to.
        :param output_config: The output configuration for storing sample data collected by the fleet.
        :param role_arn: The Amazon Resource Name (ARN) that has access to Amazon Web Services
        Internet of Things (IoT).
        :param description: A description of the fleet.
        :param tags: Creates tags for the specified fleet.
        :param enable_iot_role_alias: Whether to create an Amazon Web Services IoT Role Alias during device
        fleet creation.
        :raises ResourceInUse:
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("CreateDomain")
    def create_domain(
        self,
        context: RequestContext,
        domain_name: DomainName,
        auth_mode: AuthMode,
        default_user_settings: UserSettings,
        subnet_ids: Subnets,
        vpc_id: VpcId,
        tags: TagList = None,
        app_network_access_type: AppNetworkAccessType = None,
        home_efs_file_system_kms_key_id: KmsKeyId = None,
        kms_key_id: KmsKeyId = None,
        app_security_group_management: AppSecurityGroupManagement = None,
        domain_settings: DomainSettings = None,
    ) -> CreateDomainResponse:
        """Creates a ``Domain`` used by Amazon SageMaker Studio. A domain consists
        of an associated Amazon Elastic File System (EFS) volume, a list of
        authorized users, and a variety of security, application, policy, and
        Amazon Virtual Private Cloud (VPC) configurations. An Amazon Web
        Services account is limited to one domain per region. Users within a
        domain can share notebook files and other artifacts with each other.

        **EFS storage**

        When a domain is created, an EFS volume is created for use by all of the
        users within the domain. Each user receives a private home directory
        within the EFS volume for notebooks, Git repositories, and data files.

        SageMaker uses the Amazon Web Services Key Management Service (Amazon
        Web Services KMS) to encrypt the EFS volume attached to the domain with
        an Amazon Web Services managed key by default. For more control, you can
        specify a customer managed key. For more information, see `Protect Data
        at Rest Using
        Encryption <https://docs.aws.amazon.com/sagemaker/latest/dg/encryption-at-rest.html>`__.

        **VPC configuration**

        All SageMaker Studio traffic between the domain and the EFS volume is
        through the specified VPC and subnets. For other Studio traffic, you can
        specify the ``AppNetworkAccessType`` parameter. ``AppNetworkAccessType``
        corresponds to the network access type that you choose when you onboard
        to Studio. The following options are available:

        -  ``PublicInternetOnly`` - Non-EFS traffic goes through a VPC managed
           by Amazon SageMaker, which allows internet access. This is the
           default value.

        -  ``VpcOnly`` - All Studio traffic is through the specified VPC and
           subnets. Internet access is disabled by default. To allow internet
           access, you must specify a NAT gateway.

           When internet access is disabled, you won't be able to run a Studio
           notebook or to train or host models unless your VPC has an interface
           endpoint to the SageMaker API and runtime or a NAT gateway and your
           security groups allow outbound connections.

        NFS traffic over TCP on port 2049 needs to be allowed in both inbound
        and outbound rules in order to launch a SageMaker Studio app
        successfully.

        For more information, see `Connect SageMaker Studio Notebooks to
        Resources in a
        VPC <https://docs.aws.amazon.com/sagemaker/latest/dg/studio-notebooks-and-internet-access.html>`__.

        :param domain_name: A name for the domain.
        :param auth_mode: The mode of authentication that members use to access the domain.
        :param default_user_settings: The default settings to use to create a user profile when
        ``UserSettings`` isn't specified in the call to the
        ``CreateUserProfile`` API.
        :param subnet_ids: The VPC subnets that Studio uses for communication.
        :param vpc_id: The ID of the Amazon Virtual Private Cloud (VPC) that Studio uses for
        communication.
        :param tags: Tags to associated with the Domain.
        :param app_network_access_type: Specifies the VPC used for non-EFS traffic.
        :param home_efs_file_system_kms_key_id: Use ``KmsKeyId``.
        :param kms_key_id: SageMaker uses Amazon Web Services KMS to encrypt the EFS volume
        attached to the domain with an Amazon Web Services managed key by
        default.
        :param app_security_group_management: The entity that creates and manages the required security groups for
        inter-app communication in ``VPCOnly`` mode.
        :param domain_settings: A collection of ``Domain`` settings.
        :returns: CreateDomainResponse
        :raises ResourceLimitExceeded:
        :raises ResourceInUse:
        """
        raise NotImplementedError

    @handler("CreateEdgePackagingJob")
    def create_edge_packaging_job(
        self,
        context: RequestContext,
        edge_packaging_job_name: EntityName,
        compilation_job_name: EntityName,
        model_name: EntityName,
        model_version: EdgeVersion,
        role_arn: RoleArn,
        output_config: EdgeOutputConfig,
        resource_key: KmsKeyId = None,
        tags: TagList = None,
    ) -> None:
        """Starts a SageMaker Edge Manager model packaging job. Edge Manager will
        use the model artifacts from the Amazon Simple Storage Service bucket
        that you specify. After the model has been packaged, Amazon SageMaker
        saves the resulting artifacts to an S3 bucket that you specify.

        :param edge_packaging_job_name: The name of the edge packaging job.
        :param compilation_job_name: The name of the SageMaker Neo compilation job that will be used to
        locate model artifacts for packaging.
        :param model_name: The name of the model.
        :param model_version: The version of the model.
        :param role_arn: The Amazon Resource Name (ARN) of an IAM role that enables Amazon
        SageMaker to download and upload the model, and to contact SageMaker
        Neo.
        :param output_config: Provides information about the output location for the packaged model.
        :param resource_key: The Amazon Web Services KMS key to use when encrypting the EBS volume
        the edge packaging job runs on.
        :param tags: Creates tags for the packaging job.
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("CreateEndpoint")
    def create_endpoint(
        self,
        context: RequestContext,
        endpoint_name: EndpointName,
        endpoint_config_name: EndpointConfigName,
        deployment_config: DeploymentConfig = None,
        tags: TagList = None,
    ) -> CreateEndpointOutput:
        """Creates an endpoint using the endpoint configuration specified in the
        request. SageMaker uses the endpoint to provision resources and deploy
        models. You create the endpoint configuration with the
        CreateEndpointConfig API.

        Use this API to deploy models using SageMaker hosting services.

        For an example that calls this method when deploying a model to
        SageMaker hosting services, see the `Create Endpoint example
        notebook. <https://github.com/aws/amazon-sagemaker-examples/blob/master/sagemaker-fundamentals/create-endpoint/create_endpoint.ipynb>`__

        You must not delete an ``EndpointConfig`` that is in use by an endpoint
        that is live or while the ``UpdateEndpoint`` or ``CreateEndpoint``
        operations are being performed on the endpoint. To update an endpoint,
        you must create a new ``EndpointConfig``.

        The endpoint name must be unique within an Amazon Web Services Region in
        your Amazon Web Services account.

        When it receives the request, SageMaker creates the endpoint, launches
        the resources (ML compute instances), and deploys the model(s) on them.

        When you call CreateEndpoint, a load call is made to DynamoDB to verify
        that your endpoint configuration exists. When you read data from a
        DynamoDB table supporting
        ```Eventually Consistent Reads`` <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html>`__
        , the response might not reflect the results of a recently completed
        write operation. The response might include some stale data. If the
        dependent entities are not yet in DynamoDB, this causes a validation
        error. If you repeat your read request after a short time, the response
        should return the latest data. So retry logic is recommended to handle
        these possible issues. We also recommend that customers call
        DescribeEndpointConfig before calling CreateEndpoint to minimize the
        potential impact of a DynamoDB eventually consistent read.

        When SageMaker receives the request, it sets the endpoint status to
        ``Creating``. After it creates the endpoint, it sets the status to
        ``InService``. SageMaker can then process incoming requests for
        inferences. To check the status of an endpoint, use the DescribeEndpoint
        API.

        If any of the models hosted at this endpoint get model data from an
        Amazon S3 location, SageMaker uses Amazon Web Services Security Token
        Service to download model artifacts from the S3 path you provided.
        Amazon Web Services STS is activated in your IAM user account by
        default. If you previously deactivated Amazon Web Services STS for a
        region, you need to reactivate Amazon Web Services STS for that region.
        For more information, see `Activating and Deactivating Amazon Web
        Services STS in an Amazon Web Services
        Region <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_enable-regions.html>`__
        in the *Amazon Web Services Identity and Access Management User Guide*.

        To add the IAM role policies for using this API operation, go to the
        `IAM console <https://console.aws.amazon.com/iam/>`__, and choose Roles
        in the left navigation pane. Search the IAM role that you want to grant
        access to use the CreateEndpoint and CreateEndpointConfig API
        operations, add the following policies to the role.

        -  Option 1: For a full SageMaker access, search and attach the
           ``AmazonSageMakerFullAccess`` policy.

        -  Option 2: For granting a limited access to an IAM role, paste the
           following Action elements manually into the JSON file of the IAM
           role:

           ``"Action": ["sagemaker:CreateEndpoint", "sagemaker:CreateEndpointConfig"]``

           ``"Resource": [``

           ``"arn:aws:sagemaker:region:account-id:endpoint/endpointName"``

           ``"arn:aws:sagemaker:region:account-id:endpoint-config/endpointConfigName"``

           ``]``

           For more information, see `SageMaker API Permissions: Actions,
           Permissions, and Resources
           Reference <https://docs.aws.amazon.com/sagemaker/latest/dg/api-permissions-reference.html>`__.

        :param endpoint_name: The name of the endpoint.
        :param endpoint_config_name: The name of an endpoint configuration.
        :param deployment_config: The deployment configuration for an endpoint, which contains the desired
        deployment strategy and rollback configurations.
        :param tags: An array of key-value pairs.
        :returns: CreateEndpointOutput
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("CreateEndpointConfig")
    def create_endpoint_config(
        self,
        context: RequestContext,
        endpoint_config_name: EndpointConfigName,
        production_variants: ProductionVariantList,
        data_capture_config: DataCaptureConfig = None,
        tags: TagList = None,
        kms_key_id: KmsKeyId = None,
        async_inference_config: AsyncInferenceConfig = None,
    ) -> CreateEndpointConfigOutput:
        """Creates an endpoint configuration that SageMaker hosting services uses
        to deploy models. In the configuration, you identify one or more models,
        created using the ``CreateModel`` API, to deploy and the resources that
        you want SageMaker to provision. Then you call the CreateEndpoint API.

        Use this API if you want to use SageMaker hosting services to deploy
        models into production.

        In the request, you define a ``ProductionVariant``, for each model that
        you want to deploy. Each ``ProductionVariant`` parameter also describes
        the resources that you want SageMaker to provision. This includes the
        number and type of ML compute instances to deploy.

        If you are hosting multiple models, you also assign a ``VariantWeight``
        to specify how much traffic you want to allocate to each model. For
        example, suppose that you want to host two models, A and B, and you
        assign traffic weight 2 for model A and 1 for model B. SageMaker
        distributes two-thirds of the traffic to Model A, and one-third to model
        B.

        When you call CreateEndpoint, a load call is made to DynamoDB to verify
        that your endpoint configuration exists. When you read data from a
        DynamoDB table supporting
        ```Eventually Consistent Reads`` <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html>`__
        , the response might not reflect the results of a recently completed
        write operation. The response might include some stale data. If the
        dependent entities are not yet in DynamoDB, this causes a validation
        error. If you repeat your read request after a short time, the response
        should return the latest data. So retry logic is recommended to handle
        these possible issues. We also recommend that customers call
        DescribeEndpointConfig before calling CreateEndpoint to minimize the
        potential impact of a DynamoDB eventually consistent read.

        :param endpoint_config_name: The name of the endpoint configuration.
        :param production_variants: An list of ``ProductionVariant`` objects, one for each model that you
        want to host at this endpoint.
        :param data_capture_config: .
        :param tags: An array of key-value pairs.
        :param kms_key_id: The Amazon Resource Name (ARN) of a Amazon Web Services Key Management
        Service key that SageMaker uses to encrypt data on the storage volume
        attached to the ML compute instance that hosts the endpoint.
        :param async_inference_config: Specifies configuration for how an endpoint performs asynchronous
        inference.
        :returns: CreateEndpointConfigOutput
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("CreateExperiment")
    def create_experiment(
        self,
        context: RequestContext,
        experiment_name: ExperimentEntityName,
        display_name: ExperimentEntityName = None,
        description: ExperimentDescription = None,
        tags: TagList = None,
    ) -> CreateExperimentResponse:
        """Creates an SageMaker *experiment*. An experiment is a collection of
        *trials* that are observed, compared and evaluated as a group. A trial
        is a set of steps, called *trial components*, that produce a machine
        learning model.

        The goal of an experiment is to determine the components that produce
        the best model. Multiple trials are performed, each one isolating and
        measuring the impact of a change to one or more inputs, while keeping
        the remaining inputs constant.

        When you use SageMaker Studio or the SageMaker Python SDK, all
        experiments, trials, and trial components are automatically tracked,
        logged, and indexed. When you use the Amazon Web Services SDK for Python
        (Boto), you must use the logging APIs provided by the SDK.

        You can add tags to experiments, trials, trial components and then use
        the Search API to search for the tags.

        To add a description to an experiment, specify the optional
        ``Description`` parameter. To add a description later, or to change the
        description, call the UpdateExperiment API.

        To get a list of all your experiments, call the ListExperiments API. To
        view an experiment's properties, call the DescribeExperiment API. To get
        a list of all the trials associated with an experiment, call the
        ListTrials API. To create a trial call the CreateTrial API.

        :param experiment_name: The name of the experiment.
        :param display_name: The name of the experiment as displayed.
        :param description: The description of the experiment.
        :param tags: A list of tags to associate with the experiment.
        :returns: CreateExperimentResponse
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("CreateFeatureGroup")
    def create_feature_group(
        self,
        context: RequestContext,
        feature_group_name: FeatureGroupName,
        record_identifier_feature_name: FeatureName,
        event_time_feature_name: FeatureName,
        feature_definitions: FeatureDefinitions,
        online_store_config: OnlineStoreConfig = None,
        offline_store_config: OfflineStoreConfig = None,
        role_arn: RoleArn = None,
        description: Description = None,
        tags: TagList = None,
    ) -> CreateFeatureGroupResponse:
        """Create a new ``FeatureGroup``. A ``FeatureGroup`` is a group of
        ``Features`` defined in the ``FeatureStore`` to describe a ``Record``.

        The ``FeatureGroup`` defines the schema and features contained in the
        FeatureGroup. A ``FeatureGroup`` definition is composed of a list of
        ``Features``, a ``RecordIdentifierFeatureName``, an
        ``EventTimeFeatureName`` and configurations for its ``OnlineStore`` and
        ``OfflineStore``. Check `Amazon Web Services service
        quotas <https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html>`__
        to see the ``FeatureGroup`` s quota for your Amazon Web Services
        account.

        You must include at least one of ``OnlineStoreConfig`` and
        ``OfflineStoreConfig`` to create a ``FeatureGroup``.

        :param feature_group_name: The name of the ``FeatureGroup``.
        :param record_identifier_feature_name: The name of the ``Feature`` whose value uniquely identifies a ``Record``
        defined in the ``FeatureStore``.
        :param event_time_feature_name: The name of the feature that stores the ``EventTime`` of a ``Record`` in
        a ``FeatureGroup``.
        :param feature_definitions: A list of ``Feature`` names and types.
        :param online_store_config: You can turn the ``OnlineStore`` on or off by specifying ``True`` for
        the ``EnableOnlineStore`` flag in ``OnlineStoreConfig``; the default
        value is ``False``.
        :param offline_store_config: Use this to configure an ``OfflineFeatureStore``.
        :param role_arn: The Amazon Resource Name (ARN) of the IAM execution role used to persist
        data into the ``OfflineStore`` if an ``OfflineStoreConfig`` is provided.
        :param description: A free-form description of a ``FeatureGroup``.
        :param tags: Tags used to identify ``Features`` in each ``FeatureGroup``.
        :returns: CreateFeatureGroupResponse
        :raises ResourceInUse:
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("CreateFlowDefinition")
    def create_flow_definition(
        self,
        context: RequestContext,
        flow_definition_name: FlowDefinitionName,
        human_loop_config: HumanLoopConfig,
        output_config: FlowDefinitionOutputConfig,
        role_arn: RoleArn,
        human_loop_request_source: HumanLoopRequestSource = None,
        human_loop_activation_config: HumanLoopActivationConfig = None,
        tags: TagList = None,
    ) -> CreateFlowDefinitionResponse:
        """Creates a flow definition.

        :param flow_definition_name: The name of your flow definition.
        :param human_loop_config: An object containing information about the tasks the human reviewers
        will perform.
        :param output_config: An object containing information about where the human review results
        will be uploaded.
        :param role_arn: The Amazon Resource Name (ARN) of the role needed to call other services
        on your behalf.
        :param human_loop_request_source: Container for configuring the source of human task requests.
        :param human_loop_activation_config: An object containing information about the events that trigger a human
        workflow.
        :param tags: An array of key-value pairs that contain metadata to help you categorize
        and organize a flow definition.
        :returns: CreateFlowDefinitionResponse
        :raises ResourceLimitExceeded:
        :raises ResourceInUse:
        """
        raise NotImplementedError

    @handler("CreateHumanTaskUi")
    def create_human_task_ui(
        self,
        context: RequestContext,
        human_task_ui_name: HumanTaskUiName,
        ui_template: UiTemplate,
        tags: TagList = None,
    ) -> CreateHumanTaskUiResponse:
        """Defines the settings you will use for the human review workflow user
        interface. Reviewers will see a three-panel interface with an
        instruction area, the item to review, and an input area.

        :param human_task_ui_name: The name of the user interface you are creating.
        :param ui_template: The Liquid template for the worker user interface.
        :param tags: An array of key-value pairs that contain metadata to help you categorize
        and organize a human review workflow user interface.
        :returns: CreateHumanTaskUiResponse
        :raises ResourceLimitExceeded:
        :raises ResourceInUse:
        """
        raise NotImplementedError

    @handler("CreateHyperParameterTuningJob")
    def create_hyper_parameter_tuning_job(
        self,
        context: RequestContext,
        hyper_parameter_tuning_job_name: HyperParameterTuningJobName,
        hyper_parameter_tuning_job_config: HyperParameterTuningJobConfig,
        training_job_definition: HyperParameterTrainingJobDefinition = None,
        training_job_definitions: HyperParameterTrainingJobDefinitions = None,
        warm_start_config: HyperParameterTuningJobWarmStartConfig = None,
        tags: TagList = None,
    ) -> CreateHyperParameterTuningJobResponse:
        """Starts a hyperparameter tuning job. A hyperparameter tuning job finds
        the best version of a model by running many training jobs on your
        dataset using the algorithm you choose and values for hyperparameters
        within ranges that you specify. It then chooses the hyperparameter
        values that result in a model that performs the best, as measured by an
        objective metric that you choose.

        :param hyper_parameter_tuning_job_name: The name of the tuning job.
        :param hyper_parameter_tuning_job_config: The HyperParameterTuningJobConfig object that describes the tuning job,
        including the search strategy, the objective metric used to evaluate
        training jobs, ranges of parameters to search, and resource limits for
        the tuning job.
        :param training_job_definition: The HyperParameterTrainingJobDefinition object that describes the
        training jobs that this tuning job launches, including static
        hyperparameters, input data configuration, output data configuration,
        resource configuration, and stopping condition.
        :param training_job_definitions: A list of the HyperParameterTrainingJobDefinition objects launched for
        this tuning job.
        :param warm_start_config: Specifies the configuration for starting the hyperparameter tuning job
        using one or more previous tuning jobs as a starting point.
        :param tags: An array of key-value pairs.
        :returns: CreateHyperParameterTuningJobResponse
        :raises ResourceInUse:
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("CreateImage")
    def create_image(
        self,
        context: RequestContext,
        image_name: ImageName,
        role_arn: RoleArn,
        description: ImageDescription = None,
        display_name: ImageDisplayName = None,
        tags: TagList = None,
    ) -> CreateImageResponse:
        """Creates a custom SageMaker image. A SageMaker image is a set of image
        versions. Each image version represents a container image stored in
        Amazon Elastic Container Registry (ECR). For more information, see
        `Bring your own SageMaker
        image <https://docs.aws.amazon.com/sagemaker/latest/dg/studio-byoi.html>`__.

        :param image_name: The name of the image.
        :param role_arn: The Amazon Resource Name (ARN) of an IAM role that enables Amazon
        SageMaker to perform tasks on your behalf.
        :param description: The description of the image.
        :param display_name: The display name of the image.
        :param tags: A list of tags to apply to the image.
        :returns: CreateImageResponse
        :raises ResourceInUse:
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("CreateImageVersion")
    def create_image_version(
        self,
        context: RequestContext,
        base_image: ImageBaseImage,
        client_token: ClientToken,
        image_name: ImageName,
    ) -> CreateImageVersionResponse:
        """Creates a version of the SageMaker image specified by ``ImageName``. The
        version represents the Amazon Elastic Container Registry (ECR) container
        image specified by ``BaseImage``.

        :param base_image: The registry path of the container image to use as the starting point
        for this version.
        :param client_token: A unique ID.
        :param image_name: The ``ImageName`` of the ``Image`` to create a version of.
        :returns: CreateImageVersionResponse
        :raises ResourceInUse:
        :raises ResourceLimitExceeded:
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("CreateInferenceRecommendationsJob")
    def create_inference_recommendations_job(
        self,
        context: RequestContext,
        job_name: RecommendationJobName,
        job_type: RecommendationJobType,
        role_arn: RoleArn,
        input_config: RecommendationJobInputConfig,
        job_description: RecommendationJobDescription = None,
        stopping_conditions: RecommendationJobStoppingConditions = None,
        output_config: RecommendationJobOutputConfig = None,
        tags: TagList = None,
    ) -> CreateInferenceRecommendationsJobResponse:
        """Starts a recommendation job. You can create either an instance
        recommendation or load test job.

        :param job_name: A name for the recommendation job.
        :param job_type: Defines the type of recommendation job.
        :param role_arn: The Amazon Resource Name (ARN) of an IAM role that enables Amazon
        SageMaker to perform tasks on your behalf.
        :param input_config: Provides information about the versioned model package Amazon Resource
        Name (ARN), the traffic pattern, and endpoint configurations.
        :param job_description: Description of the recommendation job.
        :param stopping_conditions: A set of conditions for stopping a recommendation job.
        :param output_config: Provides information about the output artifacts and the KMS key to use
        for Amazon S3 server-side encryption.
        :param tags: The metadata that you apply to Amazon Web Services resources to help you
        categorize and organize them.
        :returns: CreateInferenceRecommendationsJobResponse
        :raises ResourceInUse:
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("CreateLabelingJob")
    def create_labeling_job(
        self,
        context: RequestContext,
        labeling_job_name: LabelingJobName,
        label_attribute_name: LabelAttributeName,
        input_config: LabelingJobInputConfig,
        output_config: LabelingJobOutputConfig,
        role_arn: RoleArn,
        human_task_config: HumanTaskConfig,
        label_category_config_s3_uri: S3Uri = None,
        stopping_conditions: LabelingJobStoppingConditions = None,
        labeling_job_algorithms_config: LabelingJobAlgorithmsConfig = None,
        tags: TagList = None,
    ) -> CreateLabelingJobResponse:
        """Creates a job that uses workers to label the data objects in your input
        dataset. You can use the labeled data to train machine learning models.

        You can select your workforce from one of three providers:

        -  A private workforce that you create. It can include employees,
           contractors, and outside experts. Use a private workforce when want
           the data to stay within your organization or when a specific set of
           skills is required.

        -  One or more vendors that you select from the Amazon Web Services
           Marketplace. Vendors provide expertise in specific areas.

        -  The Amazon Mechanical Turk workforce. This is the largest workforce,
           but it should only be used for public data or data that has been
           stripped of any personally identifiable information.

        You can also use *automated data labeling* to reduce the number of data
        objects that need to be labeled by a human. Automated data labeling uses
        *active learning* to determine if a data object can be labeled by
        machine or if it needs to be sent to a human worker. For more
        information, see `Using Automated Data
        Labeling <https://docs.aws.amazon.com/sagemaker/latest/dg/sms-automated-labeling.html>`__.

        The data objects to be labeled are contained in an Amazon S3 bucket. You
        create a *manifest file* that describes the location of each object. For
        more information, see `Using Input and Output
        Data <https://docs.aws.amazon.com/sagemaker/latest/dg/sms-data.html>`__.

        The output can be used as the manifest file for another labeling job or
        as training data for your machine learning models.

        You can use this operation to create a static labeling job or a
        streaming labeling job. A static labeling job stops if all data objects
        in the input manifest file identified in ``ManifestS3Uri`` have been
        labeled. A streaming labeling job runs perpetually until it is manually
        stopped, or remains idle for 10 days. You can send new data objects to
        an active (``InProgress``) streaming labeling job in real time. To learn
        how to create a static labeling job, see `Create a Labeling Job
        (API) <https://docs.aws.amazon.com/sagemaker/latest/dg/sms-create-labeling-job-api.html>`__
        in the Amazon SageMaker Developer Guide. To learn how to create a
        streaming labeling job, see `Create a Streaming Labeling
        Job <https://docs.aws.amazon.com/sagemaker/latest/dg/sms-streaming-create-job.html>`__.

        :param labeling_job_name: The name of the labeling job.
        :param label_attribute_name: The attribute name to use for the label in the output manifest file.
        :param input_config: Input data for the labeling job, such as the Amazon S3 location of the
        data objects and the location of the manifest file that describes the
        data objects.
        :param output_config: The location of the output data and the Amazon Web Services Key
        Management Service key ID for the key used to encrypt the output data,
        if any.
        :param role_arn: The Amazon Resource Number (ARN) that Amazon SageMaker assumes to
        perform tasks on your behalf during data labeling.
        :param human_task_config: Configures the labeling task and how it is presented to workers;
        including, but not limited to price, keywords, and batch size (task
        count).
        :param label_category_config_s3_uri: The S3 URI of the file, referred to as a *label category configuration
        file*, that defines the categories used to label the data objects.
        :param stopping_conditions: A set of conditions for stopping the labeling job.
        :param labeling_job_algorithms_config: Configures the information required to perform automated data labeling.
        :param tags: An array of key/value pairs.
        :returns: CreateLabelingJobResponse
        :raises ResourceInUse:
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("CreateModel")
    def create_model(
        self,
        context: RequestContext,
        model_name: ModelName,
        execution_role_arn: RoleArn,
        primary_container: ContainerDefinition = None,
        containers: ContainerDefinitionList = None,
        inference_execution_config: InferenceExecutionConfig = None,
        tags: TagList = None,
        vpc_config: VpcConfig = None,
        enable_network_isolation: Boolean = None,
    ) -> CreateModelOutput:
        """Creates a model in SageMaker. In the request, you name the model and
        describe a primary container. For the primary container, you specify the
        Docker image that contains inference code, artifacts (from prior
        training), and a custom environment map that the inference code uses
        when you deploy the model for predictions.

        Use this API to create a model if you want to use SageMaker hosting
        services or run a batch transform job.

        To host your model, you create an endpoint configuration with the
        ``CreateEndpointConfig`` API, and then create an endpoint with the
        ``CreateEndpoint`` API. SageMaker then deploys all of the containers
        that you defined for the model in the hosting environment.

        For an example that calls this method when deploying a model to
        SageMaker hosting services, see `Deploy the Model to Amazon SageMaker
        Hosting Services (Amazon Web Services SDK for Python (Boto
        3)). <https://docs.aws.amazon.com/sagemaker/latest/dg/ex1-deploy-model.html#ex1-deploy-model-boto>`__

        To run a batch transform using your model, you start a job with the
        ``CreateTransformJob`` API. SageMaker uses your model and your dataset
        to get inferences which are then saved to a specified S3 location.

        In the request, you also provide an IAM role that SageMaker can assume
        to access model artifacts and docker image for deployment on ML compute
        hosting instances or for batch transform jobs. In addition, you also use
        the IAM role to manage permissions the inference code needs. For
        example, if the inference code access any other Amazon Web Services
        resources, you grant necessary permissions via this role.

        :param model_name: The name of the new model.
        :param execution_role_arn: The Amazon Resource Name (ARN) of the IAM role that SageMaker can assume
        to access model artifacts and docker image for deployment on ML compute
        instances or for batch transform jobs.
        :param primary_container: The location of the primary docker image containing inference code,
        associated artifacts, and custom environment map that the inference code
        uses when the model is deployed for predictions.
        :param containers: Specifies the containers in the inference pipeline.
        :param inference_execution_config: Specifies details of how containers in a multi-container endpoint are
        called.
        :param tags: An array of key-value pairs.
        :param vpc_config: A VpcConfig object that specifies the VPC that you want your model to
        connect to.
        :param enable_network_isolation: Isolates the model container.
        :returns: CreateModelOutput
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("CreateModelBiasJobDefinition")
    def create_model_bias_job_definition(
        self,
        context: RequestContext,
        job_definition_name: MonitoringJobDefinitionName,
        model_bias_app_specification: ModelBiasAppSpecification,
        model_bias_job_input: ModelBiasJobInput,
        model_bias_job_output_config: MonitoringOutputConfig,
        job_resources: MonitoringResources,
        role_arn: RoleArn,
        model_bias_baseline_config: ModelBiasBaselineConfig = None,
        network_config: MonitoringNetworkConfig = None,
        stopping_condition: MonitoringStoppingCondition = None,
        tags: TagList = None,
    ) -> CreateModelBiasJobDefinitionResponse:
        """Creates the definition for a model bias job.

        :param job_definition_name: The name of the bias job definition.
        :param model_bias_app_specification: Configures the model bias job to run a specified Docker container image.
        :param model_bias_job_input: Inputs for the model bias job.
        :param model_bias_job_output_config: The output configuration for monitoring jobs.
        :param job_resources: Identifies the resources to deploy for a monitoring job.
        :param role_arn: The Amazon Resource Name (ARN) of an IAM role that Amazon SageMaker can
        assume to perform tasks on your behalf.
        :param model_bias_baseline_config: The baseline configuration for a model bias job.
        :param network_config: Networking options for a model bias job.
        :param stopping_condition: A time limit for how long the monitoring job is allowed to run before
        stopping.
        :param tags: (Optional) An array of key-value pairs.
        :returns: CreateModelBiasJobDefinitionResponse
        :raises ResourceLimitExceeded:
        :raises ResourceInUse:
        """
        raise NotImplementedError

    @handler("CreateModelExplainabilityJobDefinition")
    def create_model_explainability_job_definition(
        self,
        context: RequestContext,
        job_definition_name: MonitoringJobDefinitionName,
        model_explainability_app_specification: ModelExplainabilityAppSpecification,
        model_explainability_job_input: ModelExplainabilityJobInput,
        model_explainability_job_output_config: MonitoringOutputConfig,
        job_resources: MonitoringResources,
        role_arn: RoleArn,
        model_explainability_baseline_config: ModelExplainabilityBaselineConfig = None,
        network_config: MonitoringNetworkConfig = None,
        stopping_condition: MonitoringStoppingCondition = None,
        tags: TagList = None,
    ) -> CreateModelExplainabilityJobDefinitionResponse:
        """Creates the definition for a model explainability job.

        :param job_definition_name: The name of the model explainability job definition.
        :param model_explainability_app_specification: Configures the model explainability job to run a specified Docker
        container image.
        :param model_explainability_job_input: Inputs for the model explainability job.
        :param model_explainability_job_output_config: The output configuration for monitoring jobs.
        :param job_resources: Identifies the resources to deploy for a monitoring job.
        :param role_arn: The Amazon Resource Name (ARN) of an IAM role that Amazon SageMaker can
        assume to perform tasks on your behalf.
        :param model_explainability_baseline_config: The baseline configuration for a model explainability job.
        :param network_config: Networking options for a model explainability job.
        :param stopping_condition: A time limit for how long the monitoring job is allowed to run before
        stopping.
        :param tags: (Optional) An array of key-value pairs.
        :returns: CreateModelExplainabilityJobDefinitionResponse
        :raises ResourceLimitExceeded:
        :raises ResourceInUse:
        """
        raise NotImplementedError

    @handler("CreateModelPackage")
    def create_model_package(
        self,
        context: RequestContext,
        model_package_name: EntityName = None,
        model_package_group_name: ArnOrName = None,
        model_package_description: EntityDescription = None,
        inference_specification: InferenceSpecification = None,
        validation_specification: ModelPackageValidationSpecification = None,
        source_algorithm_specification: SourceAlgorithmSpecification = None,
        certify_for_marketplace: CertifyForMarketplace = None,
        tags: TagList = None,
        model_approval_status: ModelApprovalStatus = None,
        metadata_properties: MetadataProperties = None,
        model_metrics: ModelMetrics = None,
        client_token: ClientToken = None,
        customer_metadata_properties: CustomerMetadataMap = None,
        drift_check_baselines: DriftCheckBaselines = None,
        domain: String = None,
        task: String = None,
        sample_payload_url: S3Uri = None,
        additional_inference_specifications: AdditionalInferenceSpecifications = None,
    ) -> CreateModelPackageOutput:
        """Creates a model package that you can use to create SageMaker models or
        list on Amazon Web Services Marketplace, or a versioned model that is
        part of a model group. Buyers can subscribe to model packages listed on
        Amazon Web Services Marketplace to create models in SageMaker.

        To create a model package by specifying a Docker container that contains
        your inference code and the Amazon S3 location of your model artifacts,
        provide values for ``InferenceSpecification``. To create a model from an
        algorithm resource that you created or subscribed to in Amazon Web
        Services Marketplace, provide a value for
        ``SourceAlgorithmSpecification``.

        There are two types of model packages:

        -  Versioned - a model that is part of a model group in the model
           registry.

        -  Unversioned - a model package that is not part of a model group.

        :param model_package_name: The name of the model package.
        :param model_package_group_name: The name or Amazon Resource Name (ARN) of the model package group that
        this model version belongs to.
        :param model_package_description: A description of the model package.
        :param inference_specification: Specifies details about inference jobs that can be run with models based
        on this model package, including the following:

        -  The Amazon ECR paths of containers that contain the inference code
           and model artifacts.
        :param validation_specification: Specifies configurations for one or more transform jobs that SageMaker
        runs to test the model package.
        :param source_algorithm_specification: Details about the algorithm that was used to create the model package.
        :param certify_for_marketplace: Whether to certify the model package for listing on Amazon Web Services
        Marketplace.
        :param tags: A list of key value pairs associated with the model.
        :param model_approval_status: Whether the model is approved for deployment.
        :param metadata_properties: Metadata properties of the tracking entity, trial, or trial component.
        :param model_metrics: A structure that contains model metrics reports.
        :param client_token: A unique token that guarantees that the call to this API is idempotent.
        :param customer_metadata_properties: The metadata properties associated with the model package versions.
        :param drift_check_baselines: Represents the drift check baselines that can be used when the model
        monitor is set using the model package.
        :param domain: The machine learning domain of your model package and its components.
        :param task: The machine learning task your model package accomplishes.
        :param sample_payload_url: The Amazon Simple Storage Service (Amazon S3) path where the sample
        payload are stored.
        :param additional_inference_specifications: An array of additional Inference Specification objects.
        :returns: CreateModelPackageOutput
        :raises ConflictException:
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("CreateModelPackageGroup")
    def create_model_package_group(
        self,
        context: RequestContext,
        model_package_group_name: EntityName,
        model_package_group_description: EntityDescription = None,
        tags: TagList = None,
    ) -> CreateModelPackageGroupOutput:
        """Creates a model group. A model group contains a group of model versions.

        :param model_package_group_name: The name of the model group.
        :param model_package_group_description: A description for the model group.
        :param tags: A list of key value pairs associated with the model group.
        :returns: CreateModelPackageGroupOutput
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("CreateModelQualityJobDefinition")
    def create_model_quality_job_definition(
        self,
        context: RequestContext,
        job_definition_name: MonitoringJobDefinitionName,
        model_quality_app_specification: ModelQualityAppSpecification,
        model_quality_job_input: ModelQualityJobInput,
        model_quality_job_output_config: MonitoringOutputConfig,
        job_resources: MonitoringResources,
        role_arn: RoleArn,
        model_quality_baseline_config: ModelQualityBaselineConfig = None,
        network_config: MonitoringNetworkConfig = None,
        stopping_condition: MonitoringStoppingCondition = None,
        tags: TagList = None,
    ) -> CreateModelQualityJobDefinitionResponse:
        """Creates a definition for a job that monitors model quality and drift.
        For information about model monitor, see `Amazon SageMaker Model
        Monitor <https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html>`__.

        :param job_definition_name: The name of the monitoring job definition.
        :param model_quality_app_specification: The container that runs the monitoring job.
        :param model_quality_job_input: A list of the inputs that are monitored.
        :param model_quality_job_output_config: The output configuration for monitoring jobs.
        :param job_resources: Identifies the resources to deploy for a monitoring job.
        :param role_arn: The Amazon Resource Name (ARN) of an IAM role that Amazon SageMaker can
        assume to perform tasks on your behalf.
        :param model_quality_baseline_config: Specifies the constraints and baselines for the monitoring job.
        :param network_config: Specifies the network configuration for the monitoring job.
        :param stopping_condition: A time limit for how long the monitoring job is allowed to run before
        stopping.
        :param tags: (Optional) An array of key-value pairs.
        :returns: CreateModelQualityJobDefinitionResponse
        :raises ResourceLimitExceeded:
        :raises ResourceInUse:
        """
        raise NotImplementedError

    @handler("CreateMonitoringSchedule")
    def create_monitoring_schedule(
        self,
        context: RequestContext,
        monitoring_schedule_name: MonitoringScheduleName,
        monitoring_schedule_config: MonitoringScheduleConfig,
        tags: TagList = None,
    ) -> CreateMonitoringScheduleResponse:
        """Creates a schedule that regularly starts Amazon SageMaker Processing
        Jobs to monitor the data captured for an Amazon SageMaker Endoint.

        :param monitoring_schedule_name: The name of the monitoring schedule.
        :param monitoring_schedule_config: The configuration object that specifies the monitoring schedule and
        defines the monitoring job.
        :param tags: (Optional) An array of key-value pairs.
        :returns: CreateMonitoringScheduleResponse
        :raises ResourceLimitExceeded:
        :raises ResourceInUse:
        """
        raise NotImplementedError

    @handler("CreateNotebookInstance")
    def create_notebook_instance(
        self,
        context: RequestContext,
        notebook_instance_name: NotebookInstanceName,
        instance_type: InstanceType,
        role_arn: RoleArn,
        subnet_id: SubnetId = None,
        security_group_ids: SecurityGroupIds = None,
        kms_key_id: KmsKeyId = None,
        tags: TagList = None,
        lifecycle_config_name: NotebookInstanceLifecycleConfigName = None,
        direct_internet_access: DirectInternetAccess = None,
        volume_size_in_gb: NotebookInstanceVolumeSizeInGB = None,
        accelerator_types: NotebookInstanceAcceleratorTypes = None,
        default_code_repository: CodeRepositoryNameOrUrl = None,
        additional_code_repositories: AdditionalCodeRepositoryNamesOrUrls = None,
        root_access: RootAccess = None,
        platform_identifier: PlatformIdentifier = None,
    ) -> CreateNotebookInstanceOutput:
        """Creates an SageMaker notebook instance. A notebook instance is a machine
        learning (ML) compute instance running on a Jupyter notebook.

        In a ``CreateNotebookInstance`` request, specify the type of ML compute
        instance that you want to run. SageMaker launches the instance, installs
        common libraries that you can use to explore datasets for model
        training, and attaches an ML storage volume to the notebook instance.

        SageMaker also provides a set of example notebooks. Each notebook
        demonstrates how to use SageMaker with a specific algorithm or with a
        machine learning framework.

        After receiving the request, SageMaker does the following:

        #. Creates a network interface in the SageMaker VPC.

        #. (Option) If you specified ``SubnetId``, SageMaker creates a network
           interface in your own VPC, which is inferred from the subnet ID that
           you provide in the input. When creating this network interface,
           SageMaker attaches the security group that you specified in the
           request to the network interface that it creates in your VPC.

        #. Launches an EC2 instance of the type specified in the request in the
           SageMaker VPC. If you specified ``SubnetId`` of your VPC, SageMaker
           specifies both network interfaces when launching this instance. This
           enables inbound traffic from your own VPC to the notebook instance,
           assuming that the security groups allow it.

        After creating the notebook instance, SageMaker returns its Amazon
        Resource Name (ARN). You can't change the name of a notebook instance
        after you create it.

        After SageMaker creates the notebook instance, you can connect to the
        Jupyter server and work in Jupyter notebooks. For example, you can write
        code to explore a dataset that you can use for model training, train a
        model, host models by creating SageMaker endpoints, and validate hosted
        models.

        For more information, see `How It
        Works <https://docs.aws.amazon.com/sagemaker/latest/dg/how-it-works.html>`__.

        :param notebook_instance_name: The name of the new notebook instance.
        :param instance_type: The type of ML compute instance to launch for the notebook instance.
        :param role_arn: When you send any requests to Amazon Web Services resources from the
        notebook instance, SageMaker assumes this role to perform tasks on your
        behalf.
        :param subnet_id: The ID of the subnet in a VPC to which you would like to have a
        connectivity from your ML compute instance.
        :param security_group_ids: The VPC security group IDs, in the form sg-xxxxxxxx.
        :param kms_key_id: The Amazon Resource Name (ARN) of a Amazon Web Services Key Management
        Service key that SageMaker uses to encrypt data on the storage volume
        attached to your notebook instance.
        :param tags: An array of key-value pairs.
        :param lifecycle_config_name: The name of a lifecycle configuration to associate with the notebook
        instance.
        :param direct_internet_access: Sets whether SageMaker provides internet access to the notebook
        instance.
        :param volume_size_in_gb: The size, in GB, of the ML storage volume to attach to the notebook
        instance.
        :param accelerator_types: A list of Elastic Inference (EI) instance types to associate with this
        notebook instance.
        :param default_code_repository: A Git repository to associate with the notebook instance as its default
        code repository.
        :param additional_code_repositories: An array of up to three Git repositories to associate with the notebook
        instance.
        :param root_access: Whether root access is enabled or disabled for users of the notebook
        instance.
        :param platform_identifier: The platform identifier of the notebook instance runtime environment.
        :returns: CreateNotebookInstanceOutput
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("CreateNotebookInstanceLifecycleConfig")
    def create_notebook_instance_lifecycle_config(
        self,
        context: RequestContext,
        notebook_instance_lifecycle_config_name: NotebookInstanceLifecycleConfigName,
        on_create: NotebookInstanceLifecycleConfigList = None,
        on_start: NotebookInstanceLifecycleConfigList = None,
    ) -> CreateNotebookInstanceLifecycleConfigOutput:
        """Creates a lifecycle configuration that you can associate with a notebook
        instance. A *lifecycle configuration* is a collection of shell scripts
        that run when you create or start a notebook instance.

        Each lifecycle configuration script has a limit of 16384 characters.

        The value of the ``$PATH`` environment variable that is available to
        both scripts is ``/sbin:bin:/usr/sbin:/usr/bin``.

        View CloudWatch Logs for notebook instance lifecycle configurations in
        log group ``/aws/sagemaker/NotebookInstances`` in log stream
        ``[notebook-instance-name]/[LifecycleConfigHook]``.

        Lifecycle configuration scripts cannot run for longer than 5 minutes. If
        a script runs for longer than 5 minutes, it fails and the notebook
        instance is not created or started.

        For information about notebook instance lifestyle configurations, see
        `Step 2.1: (Optional) Customize a Notebook
        Instance <https://docs.aws.amazon.com/sagemaker/latest/dg/notebook-lifecycle-config.html>`__.

        :param notebook_instance_lifecycle_config_name: The name of the lifecycle configuration.
        :param on_create: A shell script that runs only once, when you create a notebook instance.
        :param on_start: A shell script that runs every time you start a notebook instance,
        including when you create the notebook instance.
        :returns: CreateNotebookInstanceLifecycleConfigOutput
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("CreatePipeline")
    def create_pipeline(
        self,
        context: RequestContext,
        pipeline_name: PipelineName,
        client_request_token: IdempotencyToken,
        role_arn: RoleArn,
        pipeline_display_name: PipelineName = None,
        pipeline_definition: PipelineDefinition = None,
        pipeline_definition_s3_location: PipelineDefinitionS3Location = None,
        pipeline_description: PipelineDescription = None,
        tags: TagList = None,
        parallelism_configuration: ParallelismConfiguration = None,
    ) -> CreatePipelineResponse:
        """Creates a pipeline using a JSON pipeline definition.

        :param pipeline_name: The name of the pipeline.
        :param client_request_token: A unique, case-sensitive identifier that you provide to ensure the
        idempotency of the operation.
        :param role_arn: The Amazon Resource Name (ARN) of the role used by the pipeline to
        access and create resources.
        :param pipeline_display_name: The display name of the pipeline.
        :param pipeline_definition: The JSON pipeline definition of the pipeline.
        :param pipeline_definition_s3_location: The location of the pipeline definition stored in Amazon S3.
        :param pipeline_description: A description of the pipeline.
        :param tags: A list of tags to apply to the created pipeline.
        :param parallelism_configuration: This is the configuration that controls the parallelism of the pipeline.
        :returns: CreatePipelineResponse
        :raises ResourceNotFound:
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("CreatePresignedDomainUrl")
    def create_presigned_domain_url(
        self,
        context: RequestContext,
        domain_id: DomainId,
        user_profile_name: UserProfileName,
        session_expiration_duration_in_seconds: SessionExpirationDurationInSeconds = None,
        expires_in_seconds: ExpiresInSeconds = None,
    ) -> CreatePresignedDomainUrlResponse:
        """Creates a URL for a specified UserProfile in a Domain. When accessed in
        a web browser, the user will be automatically signed in to Amazon
        SageMaker Studio, and granted access to all of the Apps and files
        associated with the Domain's Amazon Elastic File System (EFS) volume.
        This operation can only be called when the authentication mode equals
        IAM.

        The IAM role or user used to call this API defines the permissions to
        access the app. Once the presigned URL is created, no additional
        permission is required to access this URL. IAM authorization policies
        for this API are also enforced for every HTTP request and WebSocket
        frame that attempts to connect to the app.

        You can restrict access to this API and to the URL that it returns to a
        list of IP addresses, Amazon VPCs or Amazon VPC Endpoints that you
        specify. For more information, see `Connect to SageMaker Studio Through
        an Interface VPC
        Endpoint <https://docs.aws.amazon.com/sagemaker/latest/dg/studio-interface-endpoint.html>`__
        .

        The URL that you get from a call to ``CreatePresignedDomainUrl`` has a
        default timeout of 5 minutes. You can configure this value using
        ``ExpiresInSeconds``. If you try to use the URL after the timeout limit
        expires, you are directed to the Amazon Web Services console sign-in
        page.

        :param domain_id: The domain ID.
        :param user_profile_name: The name of the UserProfile to sign-in as.
        :param session_expiration_duration_in_seconds: The session expiration duration in seconds.
        :param expires_in_seconds: The number of seconds until the pre-signed URL expires.
        :returns: CreatePresignedDomainUrlResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("CreatePresignedNotebookInstanceUrl")
    def create_presigned_notebook_instance_url(
        self,
        context: RequestContext,
        notebook_instance_name: NotebookInstanceName,
        session_expiration_duration_in_seconds: SessionExpirationDurationInSeconds = None,
    ) -> CreatePresignedNotebookInstanceUrlOutput:
        """Returns a URL that you can use to connect to the Jupyter server from a
        notebook instance. In the SageMaker console, when you choose ``Open``
        next to a notebook instance, SageMaker opens a new tab showing the
        Jupyter server home page from the notebook instance. The console uses
        this API to get the URL and show the page.

        The IAM role or user used to call this API defines the permissions to
        access the notebook instance. Once the presigned URL is created, no
        additional permission is required to access this URL. IAM authorization
        policies for this API are also enforced for every HTTP request and
        WebSocket frame that attempts to connect to the notebook instance.

        You can restrict access to this API and to the URL that it returns to a
        list of IP addresses that you specify. Use the ``NotIpAddress``
        condition operator and the ``aws:SourceIP`` condition context key to
        specify the list of IP addresses that you want to have access to the
        notebook instance. For more information, see `Limit Access to a Notebook
        Instance by IP
        Address <https://docs.aws.amazon.com/sagemaker/latest/dg/security_iam_id-based-policy-examples.html#nbi-ip-filter>`__.

        The URL that you get from a call to CreatePresignedNotebookInstanceUrl
        is valid only for 5 minutes. If you try to use the URL after the
        5-minute limit expires, you are directed to the Amazon Web Services
        console sign-in page.

        :param notebook_instance_name: The name of the notebook instance.
        :param session_expiration_duration_in_seconds: The duration of the session, in seconds.
        :returns: CreatePresignedNotebookInstanceUrlOutput
        """
        raise NotImplementedError

    @handler("CreateProcessingJob")
    def create_processing_job(
        self,
        context: RequestContext,
        processing_job_name: ProcessingJobName,
        processing_resources: ProcessingResources,
        app_specification: AppSpecification,
        role_arn: RoleArn,
        processing_inputs: ProcessingInputs = None,
        processing_output_config: ProcessingOutputConfig = None,
        stopping_condition: ProcessingStoppingCondition = None,
        environment: ProcessingEnvironmentMap = None,
        network_config: NetworkConfig = None,
        tags: TagList = None,
        experiment_config: ExperimentConfig = None,
    ) -> CreateProcessingJobResponse:
        """Creates a processing job.

        :param processing_job_name: The name of the processing job.
        :param processing_resources: Identifies the resources, ML compute instances, and ML storage volumes
        to deploy for a processing job.
        :param app_specification: Configures the processing job to run a specified Docker container image.
        :param role_arn: The Amazon Resource Name (ARN) of an IAM role that Amazon SageMaker can
        assume to perform tasks on your behalf.
        :param processing_inputs: An array of inputs configuring the data to download into the processing
        container.
        :param processing_output_config: Output configuration for the processing job.
        :param stopping_condition: The time limit for how long the processing job is allowed to run.
        :param environment: The environment variables to set in the Docker container.
        :param network_config: Networking options for a processing job, such as whether to allow
        inbound and outbound network calls to and from processing containers,
        and the VPC subnets and security groups to use for VPC-enabled
        processing jobs.
        :param tags: (Optional) An array of key-value pairs.
        :param experiment_config: Associates a SageMaker job as a trial component with an experiment and
        trial.
        :returns: CreateProcessingJobResponse
        :raises ResourceInUse:
        :raises ResourceLimitExceeded:
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("CreateProject")
    def create_project(
        self,
        context: RequestContext,
        project_name: ProjectEntityName,
        service_catalog_provisioning_details: ServiceCatalogProvisioningDetails,
        project_description: EntityDescription = None,
        tags: TagList = None,
    ) -> CreateProjectOutput:
        """Creates a machine learning (ML) project that can contain one or more
        templates that set up an ML pipeline from training to deploying an
        approved model.

        :param project_name: The name of the project.
        :param service_catalog_provisioning_details: The product ID and provisioning artifact ID to provision a service
        catalog.
        :param project_description: A description for the project.
        :param tags: An array of key-value pairs that you want to use to organize and track
        your Amazon Web Services resource costs.
        :returns: CreateProjectOutput
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("CreateStudioLifecycleConfig")
    def create_studio_lifecycle_config(
        self,
        context: RequestContext,
        studio_lifecycle_config_name: StudioLifecycleConfigName,
        studio_lifecycle_config_content: StudioLifecycleConfigContent,
        studio_lifecycle_config_app_type: StudioLifecycleConfigAppType,
        tags: TagList = None,
    ) -> CreateStudioLifecycleConfigResponse:
        """Creates a new Studio Lifecycle Configuration.

        :param studio_lifecycle_config_name: The name of the Studio Lifecycle Configuration to create.
        :param studio_lifecycle_config_content: The content of your Studio Lifecycle Configuration script.
        :param studio_lifecycle_config_app_type: The App type that the Lifecycle Configuration is attached to.
        :param tags: Tags to be associated with the Lifecycle Configuration.
        :returns: CreateStudioLifecycleConfigResponse
        :raises ResourceInUse:
        """
        raise NotImplementedError

    @handler("CreateTrainingJob")
    def create_training_job(
        self,
        context: RequestContext,
        training_job_name: TrainingJobName,
        algorithm_specification: AlgorithmSpecification,
        role_arn: RoleArn,
        output_data_config: OutputDataConfig,
        resource_config: ResourceConfig,
        stopping_condition: StoppingCondition,
        hyper_parameters: HyperParameters = None,
        input_data_config: InputDataConfig = None,
        vpc_config: VpcConfig = None,
        tags: TagList = None,
        enable_network_isolation: Boolean = None,
        enable_inter_container_traffic_encryption: Boolean = None,
        enable_managed_spot_training: Boolean = None,
        checkpoint_config: CheckpointConfig = None,
        debug_hook_config: DebugHookConfig = None,
        debug_rule_configurations: DebugRuleConfigurations = None,
        tensor_board_output_config: TensorBoardOutputConfig = None,
        experiment_config: ExperimentConfig = None,
        profiler_config: ProfilerConfig = None,
        profiler_rule_configurations: ProfilerRuleConfigurations = None,
        environment: TrainingEnvironmentMap = None,
        retry_strategy: RetryStrategy = None,
    ) -> CreateTrainingJobResponse:
        """Starts a model training job. After training completes, SageMaker saves
        the resulting model artifacts to an Amazon S3 location that you specify.

        If you choose to host your model using SageMaker hosting services, you
        can use the resulting model artifacts as part of the model. You can also
        use the artifacts in a machine learning service other than SageMaker,
        provided that you know how to use them for inference.

        In the request body, you provide the following:

        -  ``AlgorithmSpecification`` - Identifies the training algorithm to
           use.

        -  ``HyperParameters`` - Specify these algorithm-specific parameters to
           enable the estimation of model parameters during training.
           Hyperparameters can be tuned to optimize this learning process. For a
           list of hyperparameters for each training algorithm provided by
           SageMaker, see
           `Algorithms <https://docs.aws.amazon.com/sagemaker/latest/dg/algos.html>`__.

        -  ``InputDataConfig`` - Describes the training dataset and the Amazon
           S3, EFS, or FSx location where it is stored.

        -  ``OutputDataConfig`` - Identifies the Amazon S3 bucket where you want
           SageMaker to save the results of model training.

        -  ``ResourceConfig`` - Identifies the resources, ML compute instances,
           and ML storage volumes to deploy for model training. In distributed
           training, you specify more than one instance.

        -  ``EnableManagedSpotTraining`` - Optimize the cost of training machine
           learning models by up to 80% by using Amazon EC2 Spot instances. For
           more information, see `Managed Spot
           Training <https://docs.aws.amazon.com/sagemaker/latest/dg/model-managed-spot-training.html>`__.

        -  ``RoleArn`` - The Amazon Resource Name (ARN) that SageMaker assumes
           to perform tasks on your behalf during model training. You must grant
           this role the necessary permissions so that SageMaker can
           successfully complete model training.

        -  ``StoppingCondition`` - To help cap training costs, use
           ``MaxRuntimeInSeconds`` to set a time limit for training. Use
           ``MaxWaitTimeInSeconds`` to specify how long a managed spot training
           job has to complete.

        -  ``Environment`` - The environment variables to set in the Docker
           container.

        -  ``RetryStrategy`` - The number of times to retry the job when the job
           fails due to an ``InternalServerError``.

        For more information about SageMaker, see `How It
        Works <https://docs.aws.amazon.com/sagemaker/latest/dg/how-it-works.html>`__.

        :param training_job_name: The name of the training job.
        :param algorithm_specification: The registry path of the Docker image that contains the training
        algorithm and algorithm-specific metadata, including the input mode.
        :param role_arn: The Amazon Resource Name (ARN) of an IAM role that SageMaker can assume
        to perform tasks on your behalf.
        :param output_data_config: Specifies the path to the S3 location where you want to store model
        artifacts.
        :param resource_config: The resources, including the ML compute instances and ML storage
        volumes, to use for model training.
        :param stopping_condition: Specifies a limit to how long a model training job can run.
        :param hyper_parameters: Algorithm-specific parameters that influence the quality of the model.
        :param input_data_config: An array of ``Channel`` objects.
        :param vpc_config: A VpcConfig object that specifies the VPC that you want your training
        job to connect to.
        :param tags: An array of key-value pairs.
        :param enable_network_isolation: Isolates the training container.
        :param enable_inter_container_traffic_encryption: To encrypt all communications between ML compute instances in
        distributed training, choose ``True``.
        :param enable_managed_spot_training: To train models using managed spot training, choose ``True``.
        :param checkpoint_config: Contains information about the output location for managed spot training
        checkpoint data.
        :param debug_hook_config: Configuration information for the Debugger hook parameters, metric and
        tensor collections, and storage paths.
        :param debug_rule_configurations: Configuration information for Debugger rules for debugging output
        tensors.
        :param tensor_board_output_config: Configuration of storage locations for the Debugger TensorBoard output
        data.
        :param experiment_config: Associates a SageMaker job as a trial component with an experiment and
        trial.
        :param profiler_config: Configuration information for Debugger system monitoring, framework
        profiling, and storage paths.
        :param profiler_rule_configurations: Configuration information for Debugger rules for profiling system and
        framework metrics.
        :param environment: The environment variables to set in the Docker container.
        :param retry_strategy: The number of times to retry the job when the job fails due to an
        ``InternalServerError``.
        :returns: CreateTrainingJobResponse
        :raises ResourceInUse:
        :raises ResourceLimitExceeded:
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("CreateTransformJob")
    def create_transform_job(
        self,
        context: RequestContext,
        transform_job_name: TransformJobName,
        model_name: ModelName,
        transform_input: TransformInput,
        transform_output: TransformOutput,
        transform_resources: TransformResources,
        max_concurrent_transforms: MaxConcurrentTransforms = None,
        model_client_config: ModelClientConfig = None,
        max_payload_in_mb: MaxPayloadInMB = None,
        batch_strategy: BatchStrategy = None,
        environment: TransformEnvironmentMap = None,
        data_processing: DataProcessing = None,
        tags: TagList = None,
        experiment_config: ExperimentConfig = None,
    ) -> CreateTransformJobResponse:
        """Starts a transform job. A transform job uses a trained model to get
        inferences on a dataset and saves these results to an Amazon S3 location
        that you specify.

        To perform batch transformations, you create a transform job and use the
        data that you have readily available.

        In the request body, you provide the following:

        -  ``TransformJobName`` - Identifies the transform job. The name must be
           unique within an Amazon Web Services Region in an Amazon Web Services
           account.

        -  ``ModelName`` - Identifies the model to use. ``ModelName`` must be
           the name of an existing Amazon SageMaker model in the same Amazon Web
           Services Region and Amazon Web Services account. For information on
           creating a model, see CreateModel.

        -  ``TransformInput`` - Describes the dataset to be transformed and the
           Amazon S3 location where it is stored.

        -  ``TransformOutput`` - Identifies the Amazon S3 location where you
           want Amazon SageMaker to save the results from the transform job.

        -  ``TransformResources`` - Identifies the ML compute instances for the
           transform job.

        For more information about how batch transformation works, see `Batch
        Transform <https://docs.aws.amazon.com/sagemaker/latest/dg/batch-transform.html>`__.

        :param transform_job_name: The name of the transform job.
        :param model_name: The name of the model that you want to use for the transform job.
        :param transform_input: Describes the input source and the way the transform job consumes it.
        :param transform_output: Describes the results of the transform job.
        :param transform_resources: Describes the resources, including ML instance types and ML instance
        count, to use for the transform job.
        :param max_concurrent_transforms: The maximum number of parallel requests that can be sent to each
        instance in a transform job.
        :param model_client_config: Configures the timeout and maximum number of retries for processing a
        transform job invocation.
        :param max_payload_in_mb: The maximum allowed size of the payload, in MB.
        :param batch_strategy: Specifies the number of records to include in a mini-batch for an HTTP
        inference request.
        :param environment: The environment variables to set in the Docker container.
        :param data_processing: The data structure used to specify the data to be used for inference in
        a batch transform job and to associate the data that is relevant to the
        prediction results in the output.
        :param tags: (Optional) An array of key-value pairs.
        :param experiment_config: Associates a SageMaker job as a trial component with an experiment and
        trial.
        :returns: CreateTransformJobResponse
        :raises ResourceInUse:
        :raises ResourceLimitExceeded:
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("CreateTrial")
    def create_trial(
        self,
        context: RequestContext,
        trial_name: ExperimentEntityName,
        experiment_name: ExperimentEntityName,
        display_name: ExperimentEntityName = None,
        metadata_properties: MetadataProperties = None,
        tags: TagList = None,
    ) -> CreateTrialResponse:
        """Creates an SageMaker *trial*. A trial is a set of steps called *trial
        components* that produce a machine learning model. A trial is part of a
        single SageMaker *experiment*.

        When you use SageMaker Studio or the SageMaker Python SDK, all
        experiments, trials, and trial components are automatically tracked,
        logged, and indexed. When you use the Amazon Web Services SDK for Python
        (Boto), you must use the logging APIs provided by the SDK.

        You can add tags to a trial and then use the Search API to search for
        the tags.

        To get a list of all your trials, call the ListTrials API. To view a
        trial's properties, call the DescribeTrial API. To create a trial
        component, call the CreateTrialComponent API.

        :param trial_name: The name of the trial.
        :param experiment_name: The name of the experiment to associate the trial with.
        :param display_name: The name of the trial as displayed.
        :param metadata_properties: Metadata properties of the tracking entity, trial, or trial component.
        :param tags: A list of tags to associate with the trial.
        :returns: CreateTrialResponse
        :raises ResourceNotFound:
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("CreateTrialComponent")
    def create_trial_component(
        self,
        context: RequestContext,
        trial_component_name: ExperimentEntityName,
        display_name: ExperimentEntityName = None,
        status: TrialComponentStatus = None,
        start_time: Timestamp = None,
        end_time: Timestamp = None,
        parameters: TrialComponentParameters = None,
        input_artifacts: TrialComponentArtifacts = None,
        output_artifacts: TrialComponentArtifacts = None,
        metadata_properties: MetadataProperties = None,
        tags: TagList = None,
    ) -> CreateTrialComponentResponse:
        """Creates a *trial component*, which is a stage of a machine learning
        *trial*. A trial is composed of one or more trial components. A trial
        component can be used in multiple trials.

        Trial components include pre-processing jobs, training jobs, and batch
        transform jobs.

        When you use SageMaker Studio or the SageMaker Python SDK, all
        experiments, trials, and trial components are automatically tracked,
        logged, and indexed. When you use the Amazon Web Services SDK for Python
        (Boto), you must use the logging APIs provided by the SDK.

        You can add tags to a trial component and then use the Search API to
        search for the tags.

        :param trial_component_name: The name of the component.
        :param display_name: The name of the component as displayed.
        :param status: The status of the component.
        :param start_time: When the component started.
        :param end_time: When the component ended.
        :param parameters: The hyperparameters for the component.
        :param input_artifacts: The input artifacts for the component.
        :param output_artifacts: The output artifacts for the component.
        :param metadata_properties: Metadata properties of the tracking entity, trial, or trial component.
        :param tags: A list of tags to associate with the component.
        :returns: CreateTrialComponentResponse
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("CreateUserProfile")
    def create_user_profile(
        self,
        context: RequestContext,
        domain_id: DomainId,
        user_profile_name: UserProfileName,
        single_sign_on_user_identifier: SingleSignOnUserIdentifier = None,
        single_sign_on_user_value: String256 = None,
        tags: TagList = None,
        user_settings: UserSettings = None,
    ) -> CreateUserProfileResponse:
        """Creates a user profile. A user profile represents a single user within a
        domain, and is the main way to reference a "person" for the purposes of
        sharing, reporting, and other user-oriented features. This entity is
        created when a user onboards to Amazon SageMaker Studio. If an
        administrator invites a person by email or imports them from SSO, a user
        profile is automatically created. A user profile is the primary holder
        of settings for an individual user and has a reference to the user's
        private Amazon Elastic File System (EFS) home directory.

        :param domain_id: The ID of the associated Domain.
        :param user_profile_name: A name for the UserProfile.
        :param single_sign_on_user_identifier: A specifier for the type of value specified in SingleSignOnUserValue.
        :param single_sign_on_user_value: The username of the associated Amazon Web Services Single Sign-On User
        for this UserProfile.
        :param tags: Each tag consists of a key and an optional value.
        :param user_settings: A collection of settings.
        :returns: CreateUserProfileResponse
        :raises ResourceLimitExceeded:
        :raises ResourceInUse:
        """
        raise NotImplementedError

    @handler("CreateWorkforce")
    def create_workforce(
        self,
        context: RequestContext,
        workforce_name: WorkforceName,
        cognito_config: CognitoConfig = None,
        oidc_config: OidcConfig = None,
        source_ip_config: SourceIpConfig = None,
        tags: TagList = None,
    ) -> CreateWorkforceResponse:
        """Use this operation to create a workforce. This operation will return an
        error if a workforce already exists in the Amazon Web Services Region
        that you specify. You can only create one workforce in each Amazon Web
        Services Region per Amazon Web Services account.

        If you want to create a new workforce in an Amazon Web Services Region
        where a workforce already exists, use the API operation to delete the
        existing workforce and then use ``CreateWorkforce`` to create a new
        workforce.

        To create a private workforce using Amazon Cognito, you must specify a
        Cognito user pool in ``CognitoConfig``. You can also create an Amazon
        Cognito workforce using the Amazon SageMaker console. For more
        information, see `Create a Private Workforce (Amazon
        Cognito) <https://docs.aws.amazon.com/sagemaker/latest/dg/sms-workforce-create-private.html>`__.

        To create a private workforce using your own OIDC Identity Provider
        (IdP), specify your IdP configuration in ``OidcConfig``. Your OIDC IdP
        must support *groups* because groups are used by Ground Truth and Amazon
        A2I to create work teams. For more information, see `Create a Private
        Workforce (OIDC
        IdP) <https://docs.aws.amazon.com/sagemaker/latest/dg/sms-workforce-create-private-oidc.html>`__.

        :param workforce_name: The name of the private workforce.
        :param cognito_config: Use this parameter to configure an Amazon Cognito private workforce.
        :param oidc_config: Use this parameter to configure a private workforce using your own OIDC
        Identity Provider.
        :param source_ip_config: A list of IP address ranges
        (`CIDRs <https://docs.
        :param tags: An array of key-value pairs that contain metadata to help you categorize
        and organize our workforce.
        :returns: CreateWorkforceResponse
        """
        raise NotImplementedError

    @handler("CreateWorkteam")
    def create_workteam(
        self,
        context: RequestContext,
        workteam_name: WorkteamName,
        member_definitions: MemberDefinitions,
        description: String200,
        workforce_name: WorkforceName = None,
        notification_configuration: NotificationConfiguration = None,
        tags: TagList = None,
    ) -> CreateWorkteamResponse:
        """Creates a new work team for labeling your data. A work team is defined
        by one or more Amazon Cognito user pools. You must first create the user
        pools before you can create a work team.

        You cannot create more than 25 work teams in an account and region.

        :param workteam_name: The name of the work team.
        :param member_definitions: A list of ``MemberDefinition`` objects that contains objects that
        identify the workers that make up the work team.
        :param description: A description of the work team.
        :param workforce_name: The name of the workforce.
        :param notification_configuration: Configures notification of workers regarding available or expiring work
        items.
        :param tags: An array of key-value pairs.
        :returns: CreateWorkteamResponse
        :raises ResourceInUse:
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("DeleteAction")
    def delete_action(
        self, context: RequestContext, action_name: ExperimentEntityName
    ) -> DeleteActionResponse:
        """Deletes an action.

        :param action_name: The name of the action to delete.
        :returns: DeleteActionResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DeleteAlgorithm")
    def delete_algorithm(self, context: RequestContext, algorithm_name: EntityName) -> None:
        """Removes the specified algorithm from your account.

        :param algorithm_name: The name of the algorithm to delete.
        """
        raise NotImplementedError

    @handler("DeleteApp")
    def delete_app(
        self,
        context: RequestContext,
        domain_id: DomainId,
        user_profile_name: UserProfileName,
        app_type: AppType,
        app_name: AppName,
    ) -> None:
        """Used to stop and delete an app.

        :param domain_id: The domain ID.
        :param user_profile_name: The user profile name.
        :param app_type: The type of app.
        :param app_name: The name of the app.
        :raises ResourceInUse:
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DeleteAppImageConfig")
    def delete_app_image_config(
        self, context: RequestContext, app_image_config_name: AppImageConfigName
    ) -> None:
        """Deletes an AppImageConfig.

        :param app_image_config_name: The name of the AppImageConfig to delete.
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DeleteArtifact")
    def delete_artifact(
        self,
        context: RequestContext,
        artifact_arn: ArtifactArn = None,
        source: ArtifactSource = None,
    ) -> DeleteArtifactResponse:
        """Deletes an artifact. Either ``ArtifactArn`` or ``Source`` must be
        specified.

        :param artifact_arn: The Amazon Resource Name (ARN) of the artifact to delete.
        :param source: The URI of the source.
        :returns: DeleteArtifactResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DeleteAssociation")
    def delete_association(
        self,
        context: RequestContext,
        source_arn: AssociationEntityArn,
        destination_arn: AssociationEntityArn,
    ) -> DeleteAssociationResponse:
        """Deletes an association.

        :param source_arn: The ARN of the source.
        :param destination_arn: The Amazon Resource Name (ARN) of the destination.
        :returns: DeleteAssociationResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DeleteCodeRepository")
    def delete_code_repository(
        self, context: RequestContext, code_repository_name: EntityName
    ) -> None:
        """Deletes the specified Git repository from your account.

        :param code_repository_name: The name of the Git repository to delete.
        """
        raise NotImplementedError

    @handler("DeleteContext")
    def delete_context(
        self, context: RequestContext, context_name: ExperimentEntityName
    ) -> DeleteContextResponse:
        """Deletes an context.

        :param context_name: The name of the context to delete.
        :returns: DeleteContextResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DeleteDataQualityJobDefinition")
    def delete_data_quality_job_definition(
        self, context: RequestContext, job_definition_name: MonitoringJobDefinitionName
    ) -> None:
        """Deletes a data quality monitoring job definition.

        :param job_definition_name: The name of the data quality monitoring job definition to delete.
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DeleteDeviceFleet")
    def delete_device_fleet(self, context: RequestContext, device_fleet_name: EntityName) -> None:
        """Deletes a fleet.

        :param device_fleet_name: The name of the fleet to delete.
        :raises ResourceInUse:
        """
        raise NotImplementedError

    @handler("DeleteDomain")
    def delete_domain(
        self, context: RequestContext, domain_id: DomainId, retention_policy: RetentionPolicy = None
    ) -> None:
        """Used to delete a domain. If you onboarded with IAM mode, you will need
        to delete your domain to onboard again using SSO. Use with caution. All
        of the members of the domain will lose access to their EFS volume,
        including data, notebooks, and other artifacts.

        :param domain_id: The domain ID.
        :param retention_policy: The retention policy for this domain, which specifies whether resources
        will be retained after the Domain is deleted.
        :raises ResourceInUse:
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DeleteEndpoint")
    def delete_endpoint(self, context: RequestContext, endpoint_name: EndpointName) -> None:
        """Deletes an endpoint. SageMaker frees up all of the resources that were
        deployed when the endpoint was created.

        SageMaker retires any custom KMS key grants associated with the
        endpoint, meaning you don't need to use the
        `RevokeGrant <http://docs.aws.amazon.com/kms/latest/APIReference/API_RevokeGrant.html>`__
        API call.

        When you delete your endpoint, SageMaker asynchronously deletes
        associated endpoint resources such as KMS key grants. You might still
        see these resources in your account for a few minutes after deleting
        your endpoint. Do not delete or revoke the permissions for your
        ``ExecutionRoleArn``, otherwise SageMaker cannot delete these resources.

        :param endpoint_name: The name of the endpoint that you want to delete.
        """
        raise NotImplementedError

    @handler("DeleteEndpointConfig")
    def delete_endpoint_config(
        self, context: RequestContext, endpoint_config_name: EndpointConfigName
    ) -> None:
        """Deletes an endpoint configuration. The ``DeleteEndpointConfig`` API
        deletes only the specified configuration. It does not delete endpoints
        created using the configuration.

        You must not delete an ``EndpointConfig`` in use by an endpoint that is
        live or while the ``UpdateEndpoint`` or ``CreateEndpoint`` operations
        are being performed on the endpoint. If you delete the
        ``EndpointConfig`` of an endpoint that is active or being created or
        updated you may lose visibility into the instance type the endpoint is
        using. The endpoint must be deleted in order to stop incurring charges.

        :param endpoint_config_name: The name of the endpoint configuration that you want to delete.
        """
        raise NotImplementedError

    @handler("DeleteExperiment")
    def delete_experiment(
        self, context: RequestContext, experiment_name: ExperimentEntityName
    ) -> DeleteExperimentResponse:
        """Deletes an SageMaker experiment. All trials associated with the
        experiment must be deleted first. Use the ListTrials API to get a list
        of the trials associated with the experiment.

        :param experiment_name: The name of the experiment to delete.
        :returns: DeleteExperimentResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DeleteFeatureGroup")
    def delete_feature_group(
        self, context: RequestContext, feature_group_name: FeatureGroupName
    ) -> None:
        """Delete the ``FeatureGroup`` and any data that was written to the
        ``OnlineStore`` of the ``FeatureGroup``. Data cannot be accessed from
        the ``OnlineStore`` immediately after ``DeleteFeatureGroup`` is called.

        Data written into the ``OfflineStore`` will not be deleted. The Amazon
        Web Services Glue database and tables that are automatically created for
        your ``OfflineStore`` are not deleted.

        :param feature_group_name: The name of the ``FeatureGroup`` you want to delete.
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DeleteFlowDefinition")
    def delete_flow_definition(
        self, context: RequestContext, flow_definition_name: FlowDefinitionName
    ) -> DeleteFlowDefinitionResponse:
        """Deletes the specified flow definition.

        :param flow_definition_name: The name of the flow definition you are deleting.
        :returns: DeleteFlowDefinitionResponse
        :raises ResourceInUse:
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DeleteHumanTaskUi")
    def delete_human_task_ui(
        self, context: RequestContext, human_task_ui_name: HumanTaskUiName
    ) -> DeleteHumanTaskUiResponse:
        """Use this operation to delete a human task user interface (worker task
        template).

        To see a list of human task user interfaces (work task templates) in
        your account, use . When you delete a worker task template, it no longer
        appears when you call ``ListHumanTaskUis``.

        :param human_task_ui_name: The name of the human task user interface (work task template) you want
        to delete.
        :returns: DeleteHumanTaskUiResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DeleteImage")
    def delete_image(self, context: RequestContext, image_name: ImageName) -> DeleteImageResponse:
        """Deletes a SageMaker image and all versions of the image. The container
        images aren't deleted.

        :param image_name: The name of the image to delete.
        :returns: DeleteImageResponse
        :raises ResourceInUse:
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DeleteImageVersion")
    def delete_image_version(
        self, context: RequestContext, image_name: ImageName, version: ImageVersionNumber
    ) -> DeleteImageVersionResponse:
        """Deletes a version of a SageMaker image. The container image the version
        represents isn't deleted.

        :param image_name: The name of the image.
        :param version: The version to delete.
        :returns: DeleteImageVersionResponse
        :raises ResourceInUse:
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DeleteModel")
    def delete_model(self, context: RequestContext, model_name: ModelName) -> None:
        """Deletes a model. The ``DeleteModel`` API deletes only the model entry
        that was created in SageMaker when you called the ``CreateModel`` API.
        It does not delete model artifacts, inference code, or the IAM role that
        you specified when creating the model.

        :param model_name: The name of the model to delete.
        """
        raise NotImplementedError

    @handler("DeleteModelBiasJobDefinition")
    def delete_model_bias_job_definition(
        self, context: RequestContext, job_definition_name: MonitoringJobDefinitionName
    ) -> None:
        """Deletes an Amazon SageMaker model bias job definition.

        :param job_definition_name: The name of the model bias job definition to delete.
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DeleteModelExplainabilityJobDefinition")
    def delete_model_explainability_job_definition(
        self, context: RequestContext, job_definition_name: MonitoringJobDefinitionName
    ) -> None:
        """Deletes an Amazon SageMaker model explainability job definition.

        :param job_definition_name: The name of the model explainability job definition to delete.
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DeleteModelPackage")
    def delete_model_package(
        self, context: RequestContext, model_package_name: VersionedArnOrName
    ) -> None:
        """Deletes a model package.

        A model package is used to create SageMaker models or list on Amazon Web
        Services Marketplace. Buyers can subscribe to model packages listed on
        Amazon Web Services Marketplace to create models in SageMaker.

        :param model_package_name: The name or Amazon Resource Name (ARN) of the model package to delete.
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("DeleteModelPackageGroup")
    def delete_model_package_group(
        self, context: RequestContext, model_package_group_name: ArnOrName
    ) -> None:
        """Deletes the specified model group.

        :param model_package_group_name: The name of the model group to delete.
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("DeleteModelPackageGroupPolicy")
    def delete_model_package_group_policy(
        self, context: RequestContext, model_package_group_name: EntityName
    ) -> None:
        """Deletes a model group resource policy.

        :param model_package_group_name: The name of the model group for which to delete the policy.
        """
        raise NotImplementedError

    @handler("DeleteModelQualityJobDefinition")
    def delete_model_quality_job_definition(
        self, context: RequestContext, job_definition_name: MonitoringJobDefinitionName
    ) -> None:
        """Deletes the secified model quality monitoring job definition.

        :param job_definition_name: The name of the model quality monitoring job definition to delete.
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DeleteMonitoringSchedule")
    def delete_monitoring_schedule(
        self, context: RequestContext, monitoring_schedule_name: MonitoringScheduleName
    ) -> None:
        """Deletes a monitoring schedule. Also stops the schedule had not already
        been stopped. This does not delete the job execution history of the
        monitoring schedule.

        :param monitoring_schedule_name: The name of the monitoring schedule to delete.
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DeleteNotebookInstance")
    def delete_notebook_instance(
        self, context: RequestContext, notebook_instance_name: NotebookInstanceName
    ) -> None:
        """Deletes an SageMaker notebook instance. Before you can delete a notebook
        instance, you must call the ``StopNotebookInstance`` API.

        When you delete a notebook instance, you lose all of your data.
        SageMaker removes the ML compute instance, and deletes the ML storage
        volume and the network interface associated with the notebook instance.

        :param notebook_instance_name: The name of the SageMaker notebook instance to delete.
        """
        raise NotImplementedError

    @handler("DeleteNotebookInstanceLifecycleConfig")
    def delete_notebook_instance_lifecycle_config(
        self,
        context: RequestContext,
        notebook_instance_lifecycle_config_name: NotebookInstanceLifecycleConfigName,
    ) -> None:
        """Deletes a notebook instance lifecycle configuration.

        :param notebook_instance_lifecycle_config_name: The name of the lifecycle configuration to delete.
        """
        raise NotImplementedError

    @handler("DeletePipeline")
    def delete_pipeline(
        self,
        context: RequestContext,
        pipeline_name: PipelineName,
        client_request_token: IdempotencyToken,
    ) -> DeletePipelineResponse:
        """Deletes a pipeline if there are no running instances of the pipeline. To
        delete a pipeline, you must stop all running instances of the pipeline
        using the ``StopPipelineExecution`` API. When you delete a pipeline, all
        instances of the pipeline are deleted.

        :param pipeline_name: The name of the pipeline to delete.
        :param client_request_token: A unique, case-sensitive identifier that you provide to ensure the
        idempotency of the operation.
        :returns: DeletePipelineResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DeleteProject")
    def delete_project(self, context: RequestContext, project_name: ProjectEntityName) -> None:
        """Delete the specified project.

        :param project_name: The name of the project to delete.
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("DeleteStudioLifecycleConfig")
    def delete_studio_lifecycle_config(
        self, context: RequestContext, studio_lifecycle_config_name: StudioLifecycleConfigName
    ) -> None:
        """Deletes the Studio Lifecycle Configuration. In order to delete the
        Lifecycle Configuration, there must be no running apps using the
        Lifecycle Configuration. You must also remove the Lifecycle
        Configuration from UserSettings in all Domains and UserProfiles.

        :param studio_lifecycle_config_name: The name of the Studio Lifecycle Configuration to delete.
        :raises ResourceNotFound:
        :raises ResourceInUse:
        """
        raise NotImplementedError

    @handler("DeleteTags")
    def delete_tags(
        self, context: RequestContext, resource_arn: ResourceArn, tag_keys: TagKeyList
    ) -> DeleteTagsOutput:
        """Deletes the specified tags from an SageMaker resource.

        To list a resource's tags, use the ``ListTags`` API.

        When you call this API to delete tags from a hyperparameter tuning job,
        the deleted tags are not removed from training jobs that the
        hyperparameter tuning job launched before you called this API.

        When you call this API to delete tags from a SageMaker Studio Domain or
        User Profile, the deleted tags are not removed from Apps that the
        SageMaker Studio Domain or User Profile launched before you called this
        API.

        :param resource_arn: The Amazon Resource Name (ARN) of the resource whose tags you want to
        delete.
        :param tag_keys: An array or one or more tag keys to delete.
        :returns: DeleteTagsOutput
        """
        raise NotImplementedError

    @handler("DeleteTrial")
    def delete_trial(
        self, context: RequestContext, trial_name: ExperimentEntityName
    ) -> DeleteTrialResponse:
        """Deletes the specified trial. All trial components that make up the trial
        must be deleted first. Use the DescribeTrialComponent API to get the
        list of trial components.

        :param trial_name: The name of the trial to delete.
        :returns: DeleteTrialResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DeleteTrialComponent")
    def delete_trial_component(
        self, context: RequestContext, trial_component_name: ExperimentEntityName
    ) -> DeleteTrialComponentResponse:
        """Deletes the specified trial component. A trial component must be
        disassociated from all trials before the trial component can be deleted.
        To disassociate a trial component from a trial, call the
        DisassociateTrialComponent API.

        :param trial_component_name: The name of the component to delete.
        :returns: DeleteTrialComponentResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DeleteUserProfile")
    def delete_user_profile(
        self, context: RequestContext, domain_id: DomainId, user_profile_name: UserProfileName
    ) -> None:
        """Deletes a user profile. When a user profile is deleted, the user loses
        access to their EFS volume, including data, notebooks, and other
        artifacts.

        :param domain_id: The domain ID.
        :param user_profile_name: The user profile name.
        :raises ResourceInUse:
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DeleteWorkforce")
    def delete_workforce(
        self, context: RequestContext, workforce_name: WorkforceName
    ) -> DeleteWorkforceResponse:
        """Use this operation to delete a workforce.

        If you want to create a new workforce in an Amazon Web Services Region
        where a workforce already exists, use this operation to delete the
        existing workforce and then use to create a new workforce.

        If a private workforce contains one or more work teams, you must use the
        operation to delete all work teams before you delete the workforce. If
        you try to delete a workforce that contains one or more work teams, you
        will recieve a ``ResourceInUse`` error.

        :param workforce_name: The name of the workforce.
        :returns: DeleteWorkforceResponse
        """
        raise NotImplementedError

    @handler("DeleteWorkteam")
    def delete_workteam(
        self, context: RequestContext, workteam_name: WorkteamName
    ) -> DeleteWorkteamResponse:
        """Deletes an existing work team. This operation can't be undone.

        :param workteam_name: The name of the work team to delete.
        :returns: DeleteWorkteamResponse
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("DeregisterDevices")
    def deregister_devices(
        self, context: RequestContext, device_fleet_name: EntityName, device_names: DeviceNames
    ) -> None:
        """Deregisters the specified devices. After you deregister a device, you
        will need to re-register the devices.

        :param device_fleet_name: The name of the fleet the devices belong to.
        :param device_names: The unique IDs of the devices.
        """
        raise NotImplementedError

    @handler("DescribeAction")
    def describe_action(
        self, context: RequestContext, action_name: ExperimentEntityName
    ) -> DescribeActionResponse:
        """Describes an action.

        :param action_name: The name of the action to describe.
        :returns: DescribeActionResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeAlgorithm")
    def describe_algorithm(
        self, context: RequestContext, algorithm_name: ArnOrName
    ) -> DescribeAlgorithmOutput:
        """Returns a description of the specified algorithm that is in your
        account.

        :param algorithm_name: The name of the algorithm to describe.
        :returns: DescribeAlgorithmOutput
        """
        raise NotImplementedError

    @handler("DescribeApp")
    def describe_app(
        self,
        context: RequestContext,
        domain_id: DomainId,
        user_profile_name: UserProfileName,
        app_type: AppType,
        app_name: AppName,
    ) -> DescribeAppResponse:
        """Describes the app.

        :param domain_id: The domain ID.
        :param user_profile_name: The user profile name.
        :param app_type: The type of app.
        :param app_name: The name of the app.
        :returns: DescribeAppResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeAppImageConfig")
    def describe_app_image_config(
        self, context: RequestContext, app_image_config_name: AppImageConfigName
    ) -> DescribeAppImageConfigResponse:
        """Describes an AppImageConfig.

        :param app_image_config_name: The name of the AppImageConfig to describe.
        :returns: DescribeAppImageConfigResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeArtifact")
    def describe_artifact(
        self, context: RequestContext, artifact_arn: ArtifactArn
    ) -> DescribeArtifactResponse:
        """Describes an artifact.

        :param artifact_arn: The Amazon Resource Name (ARN) of the artifact to describe.
        :returns: DescribeArtifactResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeAutoMLJob")
    def describe_auto_ml_job(
        self, context: RequestContext, auto_ml_job_name: AutoMLJobName
    ) -> DescribeAutoMLJobResponse:
        """Returns information about an Amazon SageMaker AutoML job.

        :param auto_ml_job_name: Requests information about an AutoML job using its unique name.
        :returns: DescribeAutoMLJobResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeCodeRepository")
    def describe_code_repository(
        self, context: RequestContext, code_repository_name: EntityName
    ) -> DescribeCodeRepositoryOutput:
        """Gets details about the specified Git repository.

        :param code_repository_name: The name of the Git repository to describe.
        :returns: DescribeCodeRepositoryOutput
        """
        raise NotImplementedError

    @handler("DescribeCompilationJob")
    def describe_compilation_job(
        self, context: RequestContext, compilation_job_name: EntityName
    ) -> DescribeCompilationJobResponse:
        """Returns information about a model compilation job.

        To create a model compilation job, use CreateCompilationJob. To get
        information about multiple model compilation jobs, use
        ListCompilationJobs.

        :param compilation_job_name: The name of the model compilation job that you want information about.
        :returns: DescribeCompilationJobResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeContext")
    def describe_context(
        self, context: RequestContext, context_name: ExperimentEntityNameOrArn
    ) -> DescribeContextResponse:
        """Describes a context.

        :param context_name: The name of the context to describe.
        :returns: DescribeContextResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeDataQualityJobDefinition")
    def describe_data_quality_job_definition(
        self, context: RequestContext, job_definition_name: MonitoringJobDefinitionName
    ) -> DescribeDataQualityJobDefinitionResponse:
        """Gets the details of a data quality monitoring job definition.

        :param job_definition_name: The name of the data quality monitoring job definition to describe.
        :returns: DescribeDataQualityJobDefinitionResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeDevice")
    def describe_device(
        self,
        context: RequestContext,
        device_name: EntityName,
        device_fleet_name: EntityName,
        next_token: NextToken = None,
    ) -> DescribeDeviceResponse:
        """Describes the device.

        :param device_name: The unique ID of the device.
        :param device_fleet_name: The name of the fleet the devices belong to.
        :param next_token: Next token of device description.
        :returns: DescribeDeviceResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeDeviceFleet")
    def describe_device_fleet(
        self, context: RequestContext, device_fleet_name: EntityName
    ) -> DescribeDeviceFleetResponse:
        """A description of the fleet the device belongs to.

        :param device_fleet_name: The name of the fleet.
        :returns: DescribeDeviceFleetResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeDomain")
    def describe_domain(
        self, context: RequestContext, domain_id: DomainId
    ) -> DescribeDomainResponse:
        """The description of the domain.

        :param domain_id: The domain ID.
        :returns: DescribeDomainResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeEdgePackagingJob")
    def describe_edge_packaging_job(
        self, context: RequestContext, edge_packaging_job_name: EntityName
    ) -> DescribeEdgePackagingJobResponse:
        """A description of edge packaging jobs.

        :param edge_packaging_job_name: The name of the edge packaging job.
        :returns: DescribeEdgePackagingJobResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeEndpoint")
    def describe_endpoint(
        self, context: RequestContext, endpoint_name: EndpointName
    ) -> DescribeEndpointOutput:
        """Returns the description of an endpoint.

        :param endpoint_name: The name of the endpoint.
        :returns: DescribeEndpointOutput
        """
        raise NotImplementedError

    @handler("DescribeEndpointConfig")
    def describe_endpoint_config(
        self, context: RequestContext, endpoint_config_name: EndpointConfigName
    ) -> DescribeEndpointConfigOutput:
        """Returns the description of an endpoint configuration created using the
        ``CreateEndpointConfig`` API.

        :param endpoint_config_name: The name of the endpoint configuration.
        :returns: DescribeEndpointConfigOutput
        """
        raise NotImplementedError

    @handler("DescribeExperiment")
    def describe_experiment(
        self, context: RequestContext, experiment_name: ExperimentEntityName
    ) -> DescribeExperimentResponse:
        """Provides a list of an experiment's properties.

        :param experiment_name: The name of the experiment to describe.
        :returns: DescribeExperimentResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeFeatureGroup")
    def describe_feature_group(
        self,
        context: RequestContext,
        feature_group_name: FeatureGroupName,
        next_token: NextToken = None,
    ) -> DescribeFeatureGroupResponse:
        """Use this operation to describe a ``FeatureGroup``. The response includes
        information on the creation time, ``FeatureGroup`` name, the unique
        identifier for each ``FeatureGroup``, and more.

        :param feature_group_name: The name of the ``FeatureGroup`` you want described.
        :param next_token: A token to resume pagination of the list of ``Features``
        (``FeatureDefinitions``).
        :returns: DescribeFeatureGroupResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeFlowDefinition")
    def describe_flow_definition(
        self, context: RequestContext, flow_definition_name: FlowDefinitionName
    ) -> DescribeFlowDefinitionResponse:
        """Returns information about the specified flow definition.

        :param flow_definition_name: The name of the flow definition.
        :returns: DescribeFlowDefinitionResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeHumanTaskUi")
    def describe_human_task_ui(
        self, context: RequestContext, human_task_ui_name: HumanTaskUiName
    ) -> DescribeHumanTaskUiResponse:
        """Returns information about the requested human task user interface
        (worker task template).

        :param human_task_ui_name: The name of the human task user interface (worker task template) you
        want information about.
        :returns: DescribeHumanTaskUiResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeHyperParameterTuningJob")
    def describe_hyper_parameter_tuning_job(
        self, context: RequestContext, hyper_parameter_tuning_job_name: HyperParameterTuningJobName
    ) -> DescribeHyperParameterTuningJobResponse:
        """Gets a description of a hyperparameter tuning job.

        :param hyper_parameter_tuning_job_name: The name of the tuning job.
        :returns: DescribeHyperParameterTuningJobResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeImage")
    def describe_image(
        self, context: RequestContext, image_name: ImageName
    ) -> DescribeImageResponse:
        """Describes a SageMaker image.

        :param image_name: The name of the image to describe.
        :returns: DescribeImageResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeImageVersion")
    def describe_image_version(
        self, context: RequestContext, image_name: ImageName, version: ImageVersionNumber = None
    ) -> DescribeImageVersionResponse:
        """Describes a version of a SageMaker image.

        :param image_name: The name of the image.
        :param version: The version of the image.
        :returns: DescribeImageVersionResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeInferenceRecommendationsJob")
    def describe_inference_recommendations_job(
        self, context: RequestContext, job_name: RecommendationJobName
    ) -> DescribeInferenceRecommendationsJobResponse:
        """Provides the results of the Inference Recommender job. One or more
        recommendation jobs are returned.

        :param job_name: The name of the job.
        :returns: DescribeInferenceRecommendationsJobResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeLabelingJob")
    def describe_labeling_job(
        self, context: RequestContext, labeling_job_name: LabelingJobName
    ) -> DescribeLabelingJobResponse:
        """Gets information about a labeling job.

        :param labeling_job_name: The name of the labeling job to return information for.
        :returns: DescribeLabelingJobResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeLineageGroup")
    def describe_lineage_group(
        self, context: RequestContext, lineage_group_name: ExperimentEntityName
    ) -> DescribeLineageGroupResponse:
        """Provides a list of properties for the requested lineage group. For more
        information, see `Cross-Account Lineage
        Tracking <https://docs.aws.amazon.com/sagemaker/latest/dg/xaccount-lineage-tracking.html>`__
        in the *Amazon SageMaker Developer Guide*.

        :param lineage_group_name: The name of the lineage group.
        :returns: DescribeLineageGroupResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeModel")
    def describe_model(self, context: RequestContext, model_name: ModelName) -> DescribeModelOutput:
        """Describes a model that you created using the ``CreateModel`` API.

        :param model_name: The name of the model.
        :returns: DescribeModelOutput
        """
        raise NotImplementedError

    @handler("DescribeModelBiasJobDefinition")
    def describe_model_bias_job_definition(
        self, context: RequestContext, job_definition_name: MonitoringJobDefinitionName
    ) -> DescribeModelBiasJobDefinitionResponse:
        """Returns a description of a model bias job definition.

        :param job_definition_name: The name of the model bias job definition.
        :returns: DescribeModelBiasJobDefinitionResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeModelExplainabilityJobDefinition")
    def describe_model_explainability_job_definition(
        self, context: RequestContext, job_definition_name: MonitoringJobDefinitionName
    ) -> DescribeModelExplainabilityJobDefinitionResponse:
        """Returns a description of a model explainability job definition.

        :param job_definition_name: The name of the model explainability job definition.
        :returns: DescribeModelExplainabilityJobDefinitionResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeModelPackage")
    def describe_model_package(
        self, context: RequestContext, model_package_name: VersionedArnOrName
    ) -> DescribeModelPackageOutput:
        """Returns a description of the specified model package, which is used to
        create SageMaker models or list them on Amazon Web Services Marketplace.

        To create models in SageMaker, buyers can subscribe to model packages
        listed on Amazon Web Services Marketplace.

        :param model_package_name: The name or Amazon Resource Name (ARN) of the model package to describe.
        :returns: DescribeModelPackageOutput
        """
        raise NotImplementedError

    @handler("DescribeModelPackageGroup")
    def describe_model_package_group(
        self, context: RequestContext, model_package_group_name: ArnOrName
    ) -> DescribeModelPackageGroupOutput:
        """Gets a description for the specified model group.

        :param model_package_group_name: The name of gthe model group to describe.
        :returns: DescribeModelPackageGroupOutput
        """
        raise NotImplementedError

    @handler("DescribeModelQualityJobDefinition")
    def describe_model_quality_job_definition(
        self, context: RequestContext, job_definition_name: MonitoringJobDefinitionName
    ) -> DescribeModelQualityJobDefinitionResponse:
        """Returns a description of a model quality job definition.

        :param job_definition_name: The name of the model quality job.
        :returns: DescribeModelQualityJobDefinitionResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeMonitoringSchedule")
    def describe_monitoring_schedule(
        self, context: RequestContext, monitoring_schedule_name: MonitoringScheduleName
    ) -> DescribeMonitoringScheduleResponse:
        """Describes the schedule for a monitoring job.

        :param monitoring_schedule_name: Name of a previously created monitoring schedule.
        :returns: DescribeMonitoringScheduleResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeNotebookInstance")
    def describe_notebook_instance(
        self, context: RequestContext, notebook_instance_name: NotebookInstanceName
    ) -> DescribeNotebookInstanceOutput:
        """Returns information about a notebook instance.

        :param notebook_instance_name: The name of the notebook instance that you want information about.
        :returns: DescribeNotebookInstanceOutput
        """
        raise NotImplementedError

    @handler("DescribeNotebookInstanceLifecycleConfig")
    def describe_notebook_instance_lifecycle_config(
        self,
        context: RequestContext,
        notebook_instance_lifecycle_config_name: NotebookInstanceLifecycleConfigName,
    ) -> DescribeNotebookInstanceLifecycleConfigOutput:
        """Returns a description of a notebook instance lifecycle configuration.

        For information about notebook instance lifestyle configurations, see
        `Step 2.1: (Optional) Customize a Notebook
        Instance <https://docs.aws.amazon.com/sagemaker/latest/dg/notebook-lifecycle-config.html>`__.

        :param notebook_instance_lifecycle_config_name: The name of the lifecycle configuration to describe.
        :returns: DescribeNotebookInstanceLifecycleConfigOutput
        """
        raise NotImplementedError

    @handler("DescribePipeline")
    def describe_pipeline(
        self, context: RequestContext, pipeline_name: PipelineName
    ) -> DescribePipelineResponse:
        """Describes the details of a pipeline.

        :param pipeline_name: The name of the pipeline to describe.
        :returns: DescribePipelineResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribePipelineDefinitionForExecution")
    def describe_pipeline_definition_for_execution(
        self, context: RequestContext, pipeline_execution_arn: PipelineExecutionArn
    ) -> DescribePipelineDefinitionForExecutionResponse:
        """Describes the details of an execution's pipeline definition.

        :param pipeline_execution_arn: The Amazon Resource Name (ARN) of the pipeline execution.
        :returns: DescribePipelineDefinitionForExecutionResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribePipelineExecution")
    def describe_pipeline_execution(
        self, context: RequestContext, pipeline_execution_arn: PipelineExecutionArn
    ) -> DescribePipelineExecutionResponse:
        """Describes the details of a pipeline execution.

        :param pipeline_execution_arn: The Amazon Resource Name (ARN) of the pipeline execution.
        :returns: DescribePipelineExecutionResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeProcessingJob")
    def describe_processing_job(
        self, context: RequestContext, processing_job_name: ProcessingJobName
    ) -> DescribeProcessingJobResponse:
        """Returns a description of a processing job.

        :param processing_job_name: The name of the processing job.
        :returns: DescribeProcessingJobResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeProject")
    def describe_project(
        self, context: RequestContext, project_name: ProjectEntityName
    ) -> DescribeProjectOutput:
        """Describes the details of a project.

        :param project_name: The name of the project to describe.
        :returns: DescribeProjectOutput
        """
        raise NotImplementedError

    @handler("DescribeStudioLifecycleConfig")
    def describe_studio_lifecycle_config(
        self, context: RequestContext, studio_lifecycle_config_name: StudioLifecycleConfigName
    ) -> DescribeStudioLifecycleConfigResponse:
        """Describes the Studio Lifecycle Configuration.

        :param studio_lifecycle_config_name: The name of the Studio Lifecycle Configuration to describe.
        :returns: DescribeStudioLifecycleConfigResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeSubscribedWorkteam")
    def describe_subscribed_workteam(
        self, context: RequestContext, workteam_arn: WorkteamArn
    ) -> DescribeSubscribedWorkteamResponse:
        """Gets information about a work team provided by a vendor. It returns
        details about the subscription with a vendor in the Amazon Web Services
        Marketplace.

        :param workteam_arn: The Amazon Resource Name (ARN) of the subscribed work team to describe.
        :returns: DescribeSubscribedWorkteamResponse
        """
        raise NotImplementedError

    @handler("DescribeTrainingJob")
    def describe_training_job(
        self, context: RequestContext, training_job_name: TrainingJobName
    ) -> DescribeTrainingJobResponse:
        """Returns information about a training job.

        Some of the attributes below only appear if the training job
        successfully starts. If the training job fails, ``TrainingJobStatus`` is
        ``Failed`` and, depending on the ``FailureReason``, attributes like
        ``TrainingStartTime``, ``TrainingTimeInSeconds``, ``TrainingEndTime``,
        and ``BillableTimeInSeconds`` may not be present in the response.

        :param training_job_name: The name of the training job.
        :returns: DescribeTrainingJobResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeTransformJob")
    def describe_transform_job(
        self, context: RequestContext, transform_job_name: TransformJobName
    ) -> DescribeTransformJobResponse:
        """Returns information about a transform job.

        :param transform_job_name: The name of the transform job that you want to view details of.
        :returns: DescribeTransformJobResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeTrial")
    def describe_trial(
        self, context: RequestContext, trial_name: ExperimentEntityName
    ) -> DescribeTrialResponse:
        """Provides a list of a trial's properties.

        :param trial_name: The name of the trial to describe.
        :returns: DescribeTrialResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeTrialComponent")
    def describe_trial_component(
        self, context: RequestContext, trial_component_name: ExperimentEntityNameOrArn
    ) -> DescribeTrialComponentResponse:
        """Provides a list of a trials component's properties.

        :param trial_component_name: The name of the trial component to describe.
        :returns: DescribeTrialComponentResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeUserProfile")
    def describe_user_profile(
        self, context: RequestContext, domain_id: DomainId, user_profile_name: UserProfileName
    ) -> DescribeUserProfileResponse:
        """Describes a user profile. For more information, see
        ``CreateUserProfile``.

        :param domain_id: The domain ID.
        :param user_profile_name: The user profile name.
        :returns: DescribeUserProfileResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("DescribeWorkforce")
    def describe_workforce(
        self, context: RequestContext, workforce_name: WorkforceName
    ) -> DescribeWorkforceResponse:
        """Lists private workforce information, including workforce name, Amazon
        Resource Name (ARN), and, if applicable, allowed IP address ranges
        (`CIDRs <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html>`__).
        Allowable IP address ranges are the IP addresses that workers can use to
        access tasks.

        This operation applies only to private workforces.

        :param workforce_name: The name of the private workforce whose access you want to restrict.
        :returns: DescribeWorkforceResponse
        """
        raise NotImplementedError

    @handler("DescribeWorkteam")
    def describe_workteam(
        self, context: RequestContext, workteam_name: WorkteamName
    ) -> DescribeWorkteamResponse:
        """Gets information about a specific work team. You can see information
        such as the create date, the last updated date, membership information,
        and the work team's Amazon Resource Name (ARN).

        :param workteam_name: The name of the work team to return a description of.
        :returns: DescribeWorkteamResponse
        """
        raise NotImplementedError

    @handler("DisableSagemakerServicecatalogPortfolio")
    def disable_sagemaker_servicecatalog_portfolio(
        self,
        context: RequestContext,
    ) -> DisableSagemakerServicecatalogPortfolioOutput:
        """Disables using Service Catalog in SageMaker. Service Catalog is used to
        create SageMaker projects.

        :returns: DisableSagemakerServicecatalogPortfolioOutput
        """
        raise NotImplementedError

    @handler("DisassociateTrialComponent")
    def disassociate_trial_component(
        self,
        context: RequestContext,
        trial_component_name: ExperimentEntityName,
        trial_name: ExperimentEntityName,
    ) -> DisassociateTrialComponentResponse:
        """Disassociates a trial component from a trial. This doesn't effect other
        trials the component is associated with. Before you can delete a
        component, you must disassociate the component from all trials it is
        associated with. To associate a trial component with a trial, call the
        AssociateTrialComponent API.

        To get a list of the trials a component is associated with, use the
        Search API. Specify ``ExperimentTrialComponent`` for the ``Resource``
        parameter. The list appears in the response under
        ``Results.TrialComponent.Parents``.

        :param trial_component_name: The name of the component to disassociate from the trial.
        :param trial_name: The name of the trial to disassociate from.
        :returns: DisassociateTrialComponentResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("EnableSagemakerServicecatalogPortfolio")
    def enable_sagemaker_servicecatalog_portfolio(
        self,
        context: RequestContext,
    ) -> EnableSagemakerServicecatalogPortfolioOutput:
        """Enables using Service Catalog in SageMaker. Service Catalog is used to
        create SageMaker projects.

        :returns: EnableSagemakerServicecatalogPortfolioOutput
        """
        raise NotImplementedError

    @handler("GetDeviceFleetReport")
    def get_device_fleet_report(
        self, context: RequestContext, device_fleet_name: EntityName
    ) -> GetDeviceFleetReportResponse:
        """Describes a fleet.

        :param device_fleet_name: The name of the fleet.
        :returns: GetDeviceFleetReportResponse
        """
        raise NotImplementedError

    @handler("GetLineageGroupPolicy")
    def get_lineage_group_policy(
        self, context: RequestContext, lineage_group_name: LineageGroupNameOrArn
    ) -> GetLineageGroupPolicyResponse:
        """The resource policy for the lineage group.

        :param lineage_group_name: The name or Amazon Resource Name (ARN) of the lineage group.
        :returns: GetLineageGroupPolicyResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("GetModelPackageGroupPolicy")
    def get_model_package_group_policy(
        self, context: RequestContext, model_package_group_name: EntityName
    ) -> GetModelPackageGroupPolicyOutput:
        """Gets a resource policy that manages access for a model group. For
        information about resource policies, see `Identity-based policies and
        resource-based
        policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_identity-vs-resource.html>`__
        in the *Amazon Web Services Identity and Access Management User Guide.*.

        :param model_package_group_name: The name of the model group for which to get the resource policy.
        :returns: GetModelPackageGroupPolicyOutput
        """
        raise NotImplementedError

    @handler("GetSagemakerServicecatalogPortfolioStatus")
    def get_sagemaker_servicecatalog_portfolio_status(
        self,
        context: RequestContext,
    ) -> GetSagemakerServicecatalogPortfolioStatusOutput:
        """Gets the status of Service Catalog in SageMaker. Service Catalog is used
        to create SageMaker projects.

        :returns: GetSagemakerServicecatalogPortfolioStatusOutput
        """
        raise NotImplementedError

    @handler("GetSearchSuggestions")
    def get_search_suggestions(
        self,
        context: RequestContext,
        resource: ResourceType,
        suggestion_query: SuggestionQuery = None,
    ) -> GetSearchSuggestionsResponse:
        """An auto-complete API for the search functionality in the Amazon
        SageMaker console. It returns suggestions of possible matches for the
        property name to use in ``Search`` queries. Provides suggestions for
        ``HyperParameters``, ``Tags``, and ``Metrics``.

        :param resource: The name of the Amazon SageMaker resource to search for.
        :param suggestion_query: Limits the property names that are included in the response.
        :returns: GetSearchSuggestionsResponse
        """
        raise NotImplementedError

    @handler("ListActions")
    def list_actions(
        self,
        context: RequestContext,
        source_uri: SourceUri = None,
        action_type: String256 = None,
        created_after: Timestamp = None,
        created_before: Timestamp = None,
        sort_by: SortActionsBy = None,
        sort_order: SortOrder = None,
        next_token: NextToken = None,
        max_results: MaxResults = None,
    ) -> ListActionsResponse:
        """Lists the actions in your account and their properties.

        :param source_uri: A filter that returns only actions with the specified source URI.
        :param action_type: A filter that returns only actions of the specified type.
        :param created_after: A filter that returns only actions created on or after the specified
        time.
        :param created_before: A filter that returns only actions created on or before the specified
        time.
        :param sort_by: The property used to sort results.
        :param sort_order: The sort order.
        :param next_token: If the previous call to ``ListActions`` didn't return the full set of
        actions, the call returns a token for getting the next set of actions.
        :param max_results: The maximum number of actions to return in the response.
        :returns: ListActionsResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("ListAlgorithms")
    def list_algorithms(
        self,
        context: RequestContext,
        creation_time_after: CreationTime = None,
        creation_time_before: CreationTime = None,
        max_results: MaxResults = None,
        name_contains: NameContains = None,
        next_token: NextToken = None,
        sort_by: AlgorithmSortBy = None,
        sort_order: SortOrder = None,
    ) -> ListAlgorithmsOutput:
        """Lists the machine learning algorithms that have been created.

        :param creation_time_after: A filter that returns only algorithms created after the specified time
        (timestamp).
        :param creation_time_before: A filter that returns only algorithms created before the specified time
        (timestamp).
        :param max_results: The maximum number of algorithms to return in the response.
        :param name_contains: A string in the algorithm name.
        :param next_token: If the response to a previous ``ListAlgorithms`` request was truncated,
        the response includes a ``NextToken``.
        :param sort_by: The parameter by which to sort the results.
        :param sort_order: The sort order for the results.
        :returns: ListAlgorithmsOutput
        """
        raise NotImplementedError

    @handler("ListAppImageConfigs")
    def list_app_image_configs(
        self,
        context: RequestContext,
        max_results: MaxResults = None,
        next_token: NextToken = None,
        name_contains: AppImageConfigName = None,
        creation_time_before: Timestamp = None,
        creation_time_after: Timestamp = None,
        modified_time_before: Timestamp = None,
        modified_time_after: Timestamp = None,
        sort_by: AppImageConfigSortKey = None,
        sort_order: SortOrder = None,
    ) -> ListAppImageConfigsResponse:
        """Lists the AppImageConfigs in your account and their properties. The list
        can be filtered by creation time or modified time, and whether the
        AppImageConfig name contains a specified string.

        :param max_results: The maximum number of AppImageConfigs to return in the response.
        :param next_token: If the previous call to ``ListImages`` didn't return the full set of
        AppImageConfigs, the call returns a token for getting the next set of
        AppImageConfigs.
        :param name_contains: A filter that returns only AppImageConfigs whose name contains the
        specified string.
        :param creation_time_before: A filter that returns only AppImageConfigs created on or before the
        specified time.
        :param creation_time_after: A filter that returns only AppImageConfigs created on or after the
        specified time.
        :param modified_time_before: A filter that returns only AppImageConfigs modified on or before the
        specified time.
        :param modified_time_after: A filter that returns only AppImageConfigs modified on or after the
        specified time.
        :param sort_by: The property used to sort results.
        :param sort_order: The sort order.
        :returns: ListAppImageConfigsResponse
        """
        raise NotImplementedError

    @handler("ListApps")
    def list_apps(
        self,
        context: RequestContext,
        next_token: NextToken = None,
        max_results: MaxResults = None,
        sort_order: SortOrder = None,
        sort_by: AppSortKey = None,
        domain_id_equals: DomainId = None,
        user_profile_name_equals: UserProfileName = None,
    ) -> ListAppsResponse:
        """Lists apps.

        :param next_token: If the previous response was truncated, you will receive this token.
        :param max_results: Returns a list up to a specified limit.
        :param sort_order: The sort order for the results.
        :param sort_by: The parameter by which to sort the results.
        :param domain_id_equals: A parameter to search for the domain ID.
        :param user_profile_name_equals: A parameter to search by user profile name.
        :returns: ListAppsResponse
        """
        raise NotImplementedError

    @handler("ListArtifacts")
    def list_artifacts(
        self,
        context: RequestContext,
        source_uri: SourceUri = None,
        artifact_type: String256 = None,
        created_after: Timestamp = None,
        created_before: Timestamp = None,
        sort_by: SortArtifactsBy = None,
        sort_order: SortOrder = None,
        next_token: NextToken = None,
        max_results: MaxResults = None,
    ) -> ListArtifactsResponse:
        """Lists the artifacts in your account and their properties.

        :param source_uri: A filter that returns only artifacts with the specified source URI.
        :param artifact_type: A filter that returns only artifacts of the specified type.
        :param created_after: A filter that returns only artifacts created on or after the specified
        time.
        :param created_before: A filter that returns only artifacts created on or before the specified
        time.
        :param sort_by: The property used to sort results.
        :param sort_order: The sort order.
        :param next_token: If the previous call to ``ListArtifacts`` didn't return the full set of
        artifacts, the call returns a token for getting the next set of
        artifacts.
        :param max_results: The maximum number of artifacts to return in the response.
        :returns: ListArtifactsResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("ListAssociations")
    def list_associations(
        self,
        context: RequestContext,
        source_arn: AssociationEntityArn = None,
        destination_arn: AssociationEntityArn = None,
        source_type: String256 = None,
        destination_type: String256 = None,
        association_type: AssociationEdgeType = None,
        created_after: Timestamp = None,
        created_before: Timestamp = None,
        sort_by: SortAssociationsBy = None,
        sort_order: SortOrder = None,
        next_token: NextToken = None,
        max_results: MaxResults = None,
    ) -> ListAssociationsResponse:
        """Lists the associations in your account and their properties.

        :param source_arn: A filter that returns only associations with the specified source ARN.
        :param destination_arn: A filter that returns only associations with the specified destination
        Amazon Resource Name (ARN).
        :param source_type: A filter that returns only associations with the specified source type.
        :param destination_type: A filter that returns only associations with the specified destination
        type.
        :param association_type: A filter that returns only associations of the specified type.
        :param created_after: A filter that returns only associations created on or after the
        specified time.
        :param created_before: A filter that returns only associations created on or before the
        specified time.
        :param sort_by: The property used to sort results.
        :param sort_order: The sort order.
        :param next_token: If the previous call to ``ListAssociations`` didn't return the full set
        of associations, the call returns a token for getting the next set of
        associations.
        :param max_results: The maximum number of associations to return in the response.
        :returns: ListAssociationsResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("ListAutoMLJobs")
    def list_auto_ml_jobs(
        self,
        context: RequestContext,
        creation_time_after: Timestamp = None,
        creation_time_before: Timestamp = None,
        last_modified_time_after: Timestamp = None,
        last_modified_time_before: Timestamp = None,
        name_contains: AutoMLNameContains = None,
        status_equals: AutoMLJobStatus = None,
        sort_order: AutoMLSortOrder = None,
        sort_by: AutoMLSortBy = None,
        max_results: AutoMLMaxResults = None,
        next_token: NextToken = None,
    ) -> ListAutoMLJobsResponse:
        """Request a list of jobs.

        :param creation_time_after: Request a list of jobs, using a filter for time.
        :param creation_time_before: Request a list of jobs, using a filter for time.
        :param last_modified_time_after: Request a list of jobs, using a filter for time.
        :param last_modified_time_before: Request a list of jobs, using a filter for time.
        :param name_contains: Request a list of jobs, using a search filter for name.
        :param status_equals: Request a list of jobs, using a filter for status.
        :param sort_order: The sort order for the results.
        :param sort_by: The parameter by which to sort the results.
        :param max_results: Request a list of jobs up to a specified limit.
        :param next_token: If the previous response was truncated, you receive this token.
        :returns: ListAutoMLJobsResponse
        """
        raise NotImplementedError

    @handler("ListCandidatesForAutoMLJob")
    def list_candidates_for_auto_ml_job(
        self,
        context: RequestContext,
        auto_ml_job_name: AutoMLJobName,
        status_equals: CandidateStatus = None,
        candidate_name_equals: CandidateName = None,
        sort_order: AutoMLSortOrder = None,
        sort_by: CandidateSortBy = None,
        max_results: AutoMLMaxResults = None,
        next_token: NextToken = None,
    ) -> ListCandidatesForAutoMLJobResponse:
        """List the candidates created for the job.

        :param auto_ml_job_name: List the candidates created for the job by providing the job's name.
        :param status_equals: List the candidates for the job and filter by status.
        :param candidate_name_equals: List the candidates for the job and filter by candidate name.
        :param sort_order: The sort order for the results.
        :param sort_by: The parameter by which to sort the results.
        :param max_results: List the job's candidates up to a specified limit.
        :param next_token: If the previous response was truncated, you receive this token.
        :returns: ListCandidatesForAutoMLJobResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("ListCodeRepositories")
    def list_code_repositories(
        self,
        context: RequestContext,
        creation_time_after: CreationTime = None,
        creation_time_before: CreationTime = None,
        last_modified_time_after: Timestamp = None,
        last_modified_time_before: Timestamp = None,
        max_results: MaxResults = None,
        name_contains: CodeRepositoryNameContains = None,
        next_token: NextToken = None,
        sort_by: CodeRepositorySortBy = None,
        sort_order: CodeRepositorySortOrder = None,
    ) -> ListCodeRepositoriesOutput:
        """Gets a list of the Git repositories in your account.

        :param creation_time_after: A filter that returns only Git repositories that were created after the
        specified time.
        :param creation_time_before: A filter that returns only Git repositories that were created before the
        specified time.
        :param last_modified_time_after: A filter that returns only Git repositories that were last modified
        after the specified time.
        :param last_modified_time_before: A filter that returns only Git repositories that were last modified
        before the specified time.
        :param max_results: The maximum number of Git repositories to return in the response.
        :param name_contains: A string in the Git repositories name.
        :param next_token: If the result of a ``ListCodeRepositoriesOutput`` request was truncated,
        the response includes a ``NextToken``.
        :param sort_by: The field to sort results by.
        :param sort_order: The sort order for results.
        :returns: ListCodeRepositoriesOutput
        """
        raise NotImplementedError

    @handler("ListCompilationJobs")
    def list_compilation_jobs(
        self,
        context: RequestContext,
        next_token: NextToken = None,
        max_results: MaxResults = None,
        creation_time_after: CreationTime = None,
        creation_time_before: CreationTime = None,
        last_modified_time_after: LastModifiedTime = None,
        last_modified_time_before: LastModifiedTime = None,
        name_contains: NameContains = None,
        status_equals: CompilationJobStatus = None,
        sort_by: ListCompilationJobsSortBy = None,
        sort_order: SortOrder = None,
    ) -> ListCompilationJobsResponse:
        """Lists model compilation jobs that satisfy various filters.

        To create a model compilation job, use CreateCompilationJob. To get
        information about a particular model compilation job you have created,
        use DescribeCompilationJob.

        :param next_token: If the result of the previous ``ListCompilationJobs`` request was
        truncated, the response includes a ``NextToken``.
        :param max_results: The maximum number of model compilation jobs to return in the response.
        :param creation_time_after: A filter that returns the model compilation jobs that were created after
        a specified time.
        :param creation_time_before: A filter that returns the model compilation jobs that were created
        before a specified time.
        :param last_modified_time_after: A filter that returns the model compilation jobs that were modified
        after a specified time.
        :param last_modified_time_before: A filter that returns the model compilation jobs that were modified
        before a specified time.
        :param name_contains: A filter that returns the model compilation jobs whose name contains a
        specified string.
        :param status_equals: A filter that retrieves model compilation jobs with a specific
        DescribeCompilationJobResponse$CompilationJobStatus status.
        :param sort_by: The field by which to sort results.
        :param sort_order: The sort order for results.
        :returns: ListCompilationJobsResponse
        """
        raise NotImplementedError

    @handler("ListContexts")
    def list_contexts(
        self,
        context: RequestContext,
        source_uri: SourceUri = None,
        context_type: String256 = None,
        created_after: Timestamp = None,
        created_before: Timestamp = None,
        sort_by: SortContextsBy = None,
        sort_order: SortOrder = None,
        next_token: NextToken = None,
        max_results: MaxResults = None,
    ) -> ListContextsResponse:
        """Lists the contexts in your account and their properties.

        :param source_uri: A filter that returns only contexts with the specified source URI.
        :param context_type: A filter that returns only contexts of the specified type.
        :param created_after: A filter that returns only contexts created on or after the specified
        time.
        :param created_before: A filter that returns only contexts created on or before the specified
        time.
        :param sort_by: The property used to sort results.
        :param sort_order: The sort order.
        :param next_token: If the previous call to ``ListContexts`` didn't return the full set of
        contexts, the call returns a token for getting the next set of contexts.
        :param max_results: The maximum number of contexts to return in the response.
        :returns: ListContextsResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("ListDataQualityJobDefinitions")
    def list_data_quality_job_definitions(
        self,
        context: RequestContext,
        endpoint_name: EndpointName = None,
        sort_by: MonitoringJobDefinitionSortKey = None,
        sort_order: SortOrder = None,
        next_token: NextToken = None,
        max_results: MaxResults = None,
        name_contains: NameContains = None,
        creation_time_before: Timestamp = None,
        creation_time_after: Timestamp = None,
    ) -> ListDataQualityJobDefinitionsResponse:
        """Lists the data quality job definitions in your account.

        :param endpoint_name: A filter that lists the data quality job definitions associated with the
        specified endpoint.
        :param sort_by: The field to sort results by.
        :param sort_order: The sort order for results.
        :param next_token: If the result of the previous ``ListDataQualityJobDefinitions`` request
        was truncated, the response includes a ``NextToken``.
        :param max_results: The maximum number of data quality monitoring job definitions to return
        in the response.
        :param name_contains: A string in the data quality monitoring job definition name.
        :param creation_time_before: A filter that returns only data quality monitoring job definitions
        created before the specified time.
        :param creation_time_after: A filter that returns only data quality monitoring job definitions
        created after the specified time.
        :returns: ListDataQualityJobDefinitionsResponse
        """
        raise NotImplementedError

    @handler("ListDeviceFleets")
    def list_device_fleets(
        self,
        context: RequestContext,
        next_token: NextToken = None,
        max_results: ListMaxResults = None,
        creation_time_after: Timestamp = None,
        creation_time_before: Timestamp = None,
        last_modified_time_after: Timestamp = None,
        last_modified_time_before: Timestamp = None,
        name_contains: NameContains = None,
        sort_by: ListDeviceFleetsSortBy = None,
        sort_order: SortOrder = None,
    ) -> ListDeviceFleetsResponse:
        """Returns a list of devices in the fleet.

        :param next_token: The response from the last list when returning a list large enough to
        need tokening.
        :param max_results: The maximum number of results to select.
        :param creation_time_after: Filter fleets where packaging job was created after specified time.
        :param creation_time_before: Filter fleets where the edge packaging job was created before specified
        time.
        :param last_modified_time_after: Select fleets where the job was updated after X.
        :param last_modified_time_before: Select fleets where the job was updated before X.
        :param name_contains: Filter for fleets containing this name in their fleet device name.
        :param sort_by: The column to sort by.
        :param sort_order: What direction to sort in.
        :returns: ListDeviceFleetsResponse
        """
        raise NotImplementedError

    @handler("ListDevices")
    def list_devices(
        self,
        context: RequestContext,
        next_token: NextToken = None,
        max_results: ListMaxResults = None,
        latest_heartbeat_after: Timestamp = None,
        model_name: EntityName = None,
        device_fleet_name: EntityName = None,
    ) -> ListDevicesResponse:
        """A list of devices.

        :param next_token: The response from the last list when returning a list large enough to
        need tokening.
        :param max_results: Maximum number of results to select.
        :param latest_heartbeat_after: Select fleets where the job was updated after X.
        :param model_name: A filter that searches devices that contains this name in any of their
        models.
        :param device_fleet_name: Filter for fleets containing this name in their device fleet name.
        :returns: ListDevicesResponse
        """
        raise NotImplementedError

    @handler("ListDomains")
    def list_domains(
        self, context: RequestContext, next_token: NextToken = None, max_results: MaxResults = None
    ) -> ListDomainsResponse:
        """Lists the domains.

        :param next_token: If the previous response was truncated, you will receive this token.
        :param max_results: Returns a list up to a specified limit.
        :returns: ListDomainsResponse
        """
        raise NotImplementedError

    @handler("ListEdgePackagingJobs")
    def list_edge_packaging_jobs(
        self,
        context: RequestContext,
        next_token: NextToken = None,
        max_results: ListMaxResults = None,
        creation_time_after: Timestamp = None,
        creation_time_before: Timestamp = None,
        last_modified_time_after: Timestamp = None,
        last_modified_time_before: Timestamp = None,
        name_contains: NameContains = None,
        model_name_contains: NameContains = None,
        status_equals: EdgePackagingJobStatus = None,
        sort_by: ListEdgePackagingJobsSortBy = None,
        sort_order: SortOrder = None,
    ) -> ListEdgePackagingJobsResponse:
        """Returns a list of edge packaging jobs.

        :param next_token: The response from the last list when returning a list large enough to
        need tokening.
        :param max_results: Maximum number of results to select.
        :param creation_time_after: Select jobs where the job was created after specified time.
        :param creation_time_before: Select jobs where the job was created before specified time.
        :param last_modified_time_after: Select jobs where the job was updated after specified time.
        :param last_modified_time_before: Select jobs where the job was updated before specified time.
        :param name_contains: Filter for jobs containing this name in their packaging job name.
        :param model_name_contains: Filter for jobs where the model name contains this string.
        :param status_equals: The job status to filter for.
        :param sort_by: Use to specify what column to sort by.
        :param sort_order: What direction to sort by.
        :returns: ListEdgePackagingJobsResponse
        """
        raise NotImplementedError

    @handler("ListEndpointConfigs")
    def list_endpoint_configs(
        self,
        context: RequestContext,
        sort_by: EndpointConfigSortKey = None,
        sort_order: OrderKey = None,
        next_token: PaginationToken = None,
        max_results: MaxResults = None,
        name_contains: EndpointConfigNameContains = None,
        creation_time_before: Timestamp = None,
        creation_time_after: Timestamp = None,
    ) -> ListEndpointConfigsOutput:
        """Lists endpoint configurations.

        :param sort_by: The field to sort results by.
        :param sort_order: The sort order for results.
        :param next_token: If the result of the previous ``ListEndpointConfig`` request was
        truncated, the response includes a ``NextToken``.
        :param max_results: The maximum number of training jobs to return in the response.
        :param name_contains: A string in the endpoint configuration name.
        :param creation_time_before: A filter that returns only endpoint configurations created before the
        specified time (timestamp).
        :param creation_time_after: A filter that returns only endpoint configurations with a creation time
        greater than or equal to the specified time (timestamp).
        :returns: ListEndpointConfigsOutput
        """
        raise NotImplementedError

    @handler("ListEndpoints")
    def list_endpoints(
        self,
        context: RequestContext,
        sort_by: EndpointSortKey = None,
        sort_order: OrderKey = None,
        next_token: PaginationToken = None,
        max_results: MaxResults = None,
        name_contains: EndpointNameContains = None,
        creation_time_before: Timestamp = None,
        creation_time_after: Timestamp = None,
        last_modified_time_before: Timestamp = None,
        last_modified_time_after: Timestamp = None,
        status_equals: EndpointStatus = None,
    ) -> ListEndpointsOutput:
        """Lists endpoints.

        :param sort_by: Sorts the list of results.
        :param sort_order: The sort order for results.
        :param next_token: If the result of a ``ListEndpoints`` request was truncated, the response
        includes a ``NextToken``.
        :param max_results: The maximum number of endpoints to return in the response.
        :param name_contains: A string in endpoint names.
        :param creation_time_before: A filter that returns only endpoints that were created before the
        specified time (timestamp).
        :param creation_time_after: A filter that returns only endpoints with a creation time greater than
        or equal to the specified time (timestamp).
        :param last_modified_time_before: A filter that returns only endpoints that were modified before the
        specified timestamp.
        :param last_modified_time_after: A filter that returns only endpoints that were modified after the
        specified timestamp.
        :param status_equals: A filter that returns only endpoints with the specified status.
        :returns: ListEndpointsOutput
        """
        raise NotImplementedError

    @handler("ListExperiments")
    def list_experiments(
        self,
        context: RequestContext,
        created_after: Timestamp = None,
        created_before: Timestamp = None,
        sort_by: SortExperimentsBy = None,
        sort_order: SortOrder = None,
        next_token: NextToken = None,
        max_results: MaxResults = None,
    ) -> ListExperimentsResponse:
        """Lists all the experiments in your account. The list can be filtered to
        show only experiments that were created in a specific time range. The
        list can be sorted by experiment name or creation time.

        :param created_after: A filter that returns only experiments created after the specified time.
        :param created_before: A filter that returns only experiments created before the specified
        time.
        :param sort_by: The property used to sort results.
        :param sort_order: The sort order.
        :param next_token: If the previous call to ``ListExperiments`` didn't return the full set
        of experiments, the call returns a token for getting the next set of
        experiments.
        :param max_results: The maximum number of experiments to return in the response.
        :returns: ListExperimentsResponse
        """
        raise NotImplementedError

    @handler("ListFeatureGroups")
    def list_feature_groups(
        self,
        context: RequestContext,
        name_contains: FeatureGroupNameContains = None,
        feature_group_status_equals: FeatureGroupStatus = None,
        offline_store_status_equals: OfflineStoreStatusValue = None,
        creation_time_after: CreationTime = None,
        creation_time_before: CreationTime = None,
        sort_order: FeatureGroupSortOrder = None,
        sort_by: FeatureGroupSortBy = None,
        max_results: FeatureGroupMaxResults = None,
        next_token: NextToken = None,
    ) -> ListFeatureGroupsResponse:
        """List ``FeatureGroup`` s based on given filter and order.

        :param name_contains: A string that partially matches one or more ``FeatureGroup`` s names.
        :param feature_group_status_equals: A ``FeatureGroup`` status.
        :param offline_store_status_equals: An ``OfflineStore`` status.
        :param creation_time_after: Use this parameter to search for ``FeatureGroups`` s created after a
        specific date and time.
        :param creation_time_before: Use this parameter to search for ``FeatureGroups`` s created before a
        specific date and time.
        :param sort_order: The order in which feature groups are listed.
        :param sort_by: The value on which the feature group list is sorted.
        :param max_results: The maximum number of results returned by ``ListFeatureGroups``.
        :param next_token: A token to resume pagination of ``ListFeatureGroups`` results.
        :returns: ListFeatureGroupsResponse
        """
        raise NotImplementedError

    @handler("ListFlowDefinitions")
    def list_flow_definitions(
        self,
        context: RequestContext,
        creation_time_after: Timestamp = None,
        creation_time_before: Timestamp = None,
        sort_order: SortOrder = None,
        next_token: NextToken = None,
        max_results: MaxResults = None,
    ) -> ListFlowDefinitionsResponse:
        """Returns information about the flow definitions in your account.

        :param creation_time_after: A filter that returns only flow definitions with a creation time greater
        than or equal to the specified timestamp.
        :param creation_time_before: A filter that returns only flow definitions that were created before the
        specified timestamp.
        :param sort_order: An optional value that specifies whether you want the results sorted in
        ``Ascending`` or ``Descending`` order.
        :param next_token: A token to resume pagination.
        :param max_results: The total number of items to return.
        :returns: ListFlowDefinitionsResponse
        """
        raise NotImplementedError

    @handler("ListHumanTaskUis")
    def list_human_task_uis(
        self,
        context: RequestContext,
        creation_time_after: Timestamp = None,
        creation_time_before: Timestamp = None,
        sort_order: SortOrder = None,
        next_token: NextToken = None,
        max_results: MaxResults = None,
    ) -> ListHumanTaskUisResponse:
        """Returns information about the human task user interfaces in your
        account.

        :param creation_time_after: A filter that returns only human task user interfaces with a creation
        time greater than or equal to the specified timestamp.
        :param creation_time_before: A filter that returns only human task user interfaces that were created
        before the specified timestamp.
        :param sort_order: An optional value that specifies whether you want the results sorted in
        ``Ascending`` or ``Descending`` order.
        :param next_token: A token to resume pagination.
        :param max_results: The total number of items to return.
        :returns: ListHumanTaskUisResponse
        """
        raise NotImplementedError

    @handler("ListHyperParameterTuningJobs")
    def list_hyper_parameter_tuning_jobs(
        self,
        context: RequestContext,
        next_token: NextToken = None,
        max_results: MaxResults = None,
        sort_by: HyperParameterTuningJobSortByOptions = None,
        sort_order: SortOrder = None,
        name_contains: NameContains = None,
        creation_time_after: Timestamp = None,
        creation_time_before: Timestamp = None,
        last_modified_time_after: Timestamp = None,
        last_modified_time_before: Timestamp = None,
        status_equals: HyperParameterTuningJobStatus = None,
    ) -> ListHyperParameterTuningJobsResponse:
        """Gets a list of HyperParameterTuningJobSummary objects that describe the
        hyperparameter tuning jobs launched in your account.

        :param next_token: If the result of the previous ``ListHyperParameterTuningJobs`` request
        was truncated, the response includes a ``NextToken``.
        :param max_results: The maximum number of tuning jobs to return.
        :param sort_by: The field to sort results by.
        :param sort_order: The sort order for results.
        :param name_contains: A string in the tuning job name.
        :param creation_time_after: A filter that returns only tuning jobs that were created after the
        specified time.
        :param creation_time_before: A filter that returns only tuning jobs that were created before the
        specified time.
        :param last_modified_time_after: A filter that returns only tuning jobs that were modified after the
        specified time.
        :param last_modified_time_before: A filter that returns only tuning jobs that were modified before the
        specified time.
        :param status_equals: A filter that returns only tuning jobs with the specified status.
        :returns: ListHyperParameterTuningJobsResponse
        """
        raise NotImplementedError

    @handler("ListImageVersions")
    def list_image_versions(
        self,
        context: RequestContext,
        image_name: ImageName,
        creation_time_after: Timestamp = None,
        creation_time_before: Timestamp = None,
        last_modified_time_after: Timestamp = None,
        last_modified_time_before: Timestamp = None,
        max_results: MaxResults = None,
        next_token: NextToken = None,
        sort_by: ImageVersionSortBy = None,
        sort_order: ImageVersionSortOrder = None,
    ) -> ListImageVersionsResponse:
        """Lists the versions of a specified image and their properties. The list
        can be filtered by creation time or modified time.

        :param image_name: The name of the image to list the versions of.
        :param creation_time_after: A filter that returns only versions created on or after the specified
        time.
        :param creation_time_before: A filter that returns only versions created on or before the specified
        time.
        :param last_modified_time_after: A filter that returns only versions modified on or after the specified
        time.
        :param last_modified_time_before: A filter that returns only versions modified on or before the specified
        time.
        :param max_results: The maximum number of versions to return in the response.
        :param next_token: If the previous call to ``ListImageVersions`` didn't return the full set
        of versions, the call returns a token for getting the next set of
        versions.
        :param sort_by: The property used to sort results.
        :param sort_order: The sort order.
        :returns: ListImageVersionsResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("ListImages")
    def list_images(
        self,
        context: RequestContext,
        creation_time_after: Timestamp = None,
        creation_time_before: Timestamp = None,
        last_modified_time_after: Timestamp = None,
        last_modified_time_before: Timestamp = None,
        max_results: MaxResults = None,
        name_contains: ImageNameContains = None,
        next_token: NextToken = None,
        sort_by: ImageSortBy = None,
        sort_order: ImageSortOrder = None,
    ) -> ListImagesResponse:
        """Lists the images in your account and their properties. The list can be
        filtered by creation time or modified time, and whether the image name
        contains a specified string.

        :param creation_time_after: A filter that returns only images created on or after the specified
        time.
        :param creation_time_before: A filter that returns only images created on or before the specified
        time.
        :param last_modified_time_after: A filter that returns only images modified on or after the specified
        time.
        :param last_modified_time_before: A filter that returns only images modified on or before the specified
        time.
        :param max_results: The maximum number of images to return in the response.
        :param name_contains: A filter that returns only images whose name contains the specified
        string.
        :param next_token: If the previous call to ``ListImages`` didn't return the full set of
        images, the call returns a token for getting the next set of images.
        :param sort_by: The property used to sort results.
        :param sort_order: The sort order.
        :returns: ListImagesResponse
        """
        raise NotImplementedError

    @handler("ListInferenceRecommendationsJobs")
    def list_inference_recommendations_jobs(
        self,
        context: RequestContext,
        creation_time_after: CreationTime = None,
        creation_time_before: CreationTime = None,
        last_modified_time_after: LastModifiedTime = None,
        last_modified_time_before: LastModifiedTime = None,
        name_contains: NameContains = None,
        status_equals: RecommendationJobStatus = None,
        sort_by: ListInferenceRecommendationsJobsSortBy = None,
        sort_order: SortOrder = None,
        next_token: NextToken = None,
        max_results: MaxResults = None,
    ) -> ListInferenceRecommendationsJobsResponse:
        """Lists recommendation jobs that satisfy various filters.

        :param creation_time_after: A filter that returns only jobs created after the specified time
        (timestamp).
        :param creation_time_before: A filter that returns only jobs created before the specified time
        (timestamp).
        :param last_modified_time_after: A filter that returns only jobs that were last modified after the
        specified time (timestamp).
        :param last_modified_time_before: A filter that returns only jobs that were last modified before the
        specified time (timestamp).
        :param name_contains: A string in the job name.
        :param status_equals: A filter that retrieves only inference recommendations jobs with a
        specific status.
        :param sort_by: The parameter by which to sort the results.
        :param sort_order: The sort order for the results.
        :param next_token: If the response to a previous
        ``ListInferenceRecommendationsJobsRequest`` request was truncated, the
        response includes a ``NextToken``.
        :param max_results: The maximum number of recommendations to return in the response.
        :returns: ListInferenceRecommendationsJobsResponse
        """
        raise NotImplementedError

    @handler("ListLabelingJobs")
    def list_labeling_jobs(
        self,
        context: RequestContext,
        creation_time_after: Timestamp = None,
        creation_time_before: Timestamp = None,
        last_modified_time_after: Timestamp = None,
        last_modified_time_before: Timestamp = None,
        max_results: MaxResults = None,
        next_token: NextToken = None,
        name_contains: NameContains = None,
        sort_by: SortBy = None,
        sort_order: SortOrder = None,
        status_equals: LabelingJobStatus = None,
    ) -> ListLabelingJobsResponse:
        """Gets a list of labeling jobs.

        :param creation_time_after: A filter that returns only labeling jobs created after the specified
        time (timestamp).
        :param creation_time_before: A filter that returns only labeling jobs created before the specified
        time (timestamp).
        :param last_modified_time_after: A filter that returns only labeling jobs modified after the specified
        time (timestamp).
        :param last_modified_time_before: A filter that returns only labeling jobs modified before the specified
        time (timestamp).
        :param max_results: The maximum number of labeling jobs to return in each page of the
        response.
        :param next_token: If the result of the previous ``ListLabelingJobs`` request was
        truncated, the response includes a ``NextToken``.
        :param name_contains: A string in the labeling job name.
        :param sort_by: The field to sort results by.
        :param sort_order: The sort order for results.
        :param status_equals: A filter that retrieves only labeling jobs with a specific status.
        :returns: ListLabelingJobsResponse
        """
        raise NotImplementedError

    @handler("ListLabelingJobsForWorkteam")
    def list_labeling_jobs_for_workteam(
        self,
        context: RequestContext,
        workteam_arn: WorkteamArn,
        max_results: MaxResults = None,
        next_token: NextToken = None,
        creation_time_after: Timestamp = None,
        creation_time_before: Timestamp = None,
        job_reference_code_contains: JobReferenceCodeContains = None,
        sort_by: ListLabelingJobsForWorkteamSortByOptions = None,
        sort_order: SortOrder = None,
    ) -> ListLabelingJobsForWorkteamResponse:
        """Gets a list of labeling jobs assigned to a specified work team.

        :param workteam_arn: The Amazon Resource Name (ARN) of the work team for which you want to
        see labeling jobs for.
        :param max_results: The maximum number of labeling jobs to return in each page of the
        response.
        :param next_token: If the result of the previous ``ListLabelingJobsForWorkteam`` request
        was truncated, the response includes a ``NextToken``.
        :param creation_time_after: A filter that returns only labeling jobs created after the specified
        time (timestamp).
        :param creation_time_before: A filter that returns only labeling jobs created before the specified
        time (timestamp).
        :param job_reference_code_contains: A filter the limits jobs to only the ones whose job reference code
        contains the specified string.
        :param sort_by: The field to sort results by.
        :param sort_order: The sort order for results.
        :returns: ListLabelingJobsForWorkteamResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("ListLineageGroups")
    def list_lineage_groups(
        self,
        context: RequestContext,
        created_after: Timestamp = None,
        created_before: Timestamp = None,
        sort_by: SortLineageGroupsBy = None,
        sort_order: SortOrder = None,
        next_token: NextToken = None,
        max_results: MaxResults = None,
    ) -> ListLineageGroupsResponse:
        """A list of lineage groups shared with your Amazon Web Services account.
        For more information, see `Cross-Account Lineage
        Tracking <https://docs.aws.amazon.com/sagemaker/latest/dg/xaccount-lineage-tracking.html>`__
        in the *Amazon SageMaker Developer Guide*.

        :param created_after: A timestamp to filter against lineage groups created after a certain
        point in time.
        :param created_before: A timestamp to filter against lineage groups created before a certain
        point in time.
        :param sort_by: The parameter by which to sort the results.
        :param sort_order: The sort order for the results.
        :param next_token: If the response is truncated, SageMaker returns this token.
        :param max_results: The maximum number of endpoints to return in the response.
        :returns: ListLineageGroupsResponse
        """
        raise NotImplementedError

    @handler("ListModelBiasJobDefinitions")
    def list_model_bias_job_definitions(
        self,
        context: RequestContext,
        endpoint_name: EndpointName = None,
        sort_by: MonitoringJobDefinitionSortKey = None,
        sort_order: SortOrder = None,
        next_token: NextToken = None,
        max_results: MaxResults = None,
        name_contains: NameContains = None,
        creation_time_before: Timestamp = None,
        creation_time_after: Timestamp = None,
    ) -> ListModelBiasJobDefinitionsResponse:
        """Lists model bias jobs definitions that satisfy various filters.

        :param endpoint_name: Name of the endpoint to monitor for model bias.
        :param sort_by: Whether to sort results by the ``Name`` or ``CreationTime`` field.
        :param sort_order: Whether to sort the results in ``Ascending`` or ``Descending`` order.
        :param next_token: The token returned if the response is truncated.
        :param max_results: The maximum number of model bias jobs to return in the response.
        :param name_contains: Filter for model bias jobs whose name contains a specified string.
        :param creation_time_before: A filter that returns only model bias jobs created before a specified
        time.
        :param creation_time_after: A filter that returns only model bias jobs created after a specified
        time.
        :returns: ListModelBiasJobDefinitionsResponse
        """
        raise NotImplementedError

    @handler("ListModelExplainabilityJobDefinitions")
    def list_model_explainability_job_definitions(
        self,
        context: RequestContext,
        endpoint_name: EndpointName = None,
        sort_by: MonitoringJobDefinitionSortKey = None,
        sort_order: SortOrder = None,
        next_token: NextToken = None,
        max_results: MaxResults = None,
        name_contains: NameContains = None,
        creation_time_before: Timestamp = None,
        creation_time_after: Timestamp = None,
    ) -> ListModelExplainabilityJobDefinitionsResponse:
        """Lists model explainability job definitions that satisfy various filters.

        :param endpoint_name: Name of the endpoint to monitor for model explainability.
        :param sort_by: Whether to sort results by the ``Name`` or ``CreationTime`` field.
        :param sort_order: Whether to sort the results in ``Ascending`` or ``Descending`` order.
        :param next_token: The token returned if the response is truncated.
        :param max_results: The maximum number of jobs to return in the response.
        :param name_contains: Filter for model explainability jobs whose name contains a specified
        string.
        :param creation_time_before: A filter that returns only model explainability jobs created before a
        specified time.
        :param creation_time_after: A filter that returns only model explainability jobs created after a
        specified time.
        :returns: ListModelExplainabilityJobDefinitionsResponse
        """
        raise NotImplementedError

    @handler("ListModelMetadata")
    def list_model_metadata(
        self,
        context: RequestContext,
        search_expression: ModelMetadataSearchExpression = None,
        next_token: NextToken = None,
        max_results: MaxResults = None,
    ) -> ListModelMetadataResponse:
        """Lists the domain, framework, task, and model name of standard machine
        learning models found in common model zoos.

        :param search_expression: One or more filters that searches for the specified resource or
        resources in a search.
        :param next_token: If the response to a previous ``ListModelMetadataResponse`` request was
        truncated, the response includes a NextToken.
        :param max_results: The maximum number of models to return in the response.
        :returns: ListModelMetadataResponse
        """
        raise NotImplementedError

    @handler("ListModelPackageGroups")
    def list_model_package_groups(
        self,
        context: RequestContext,
        creation_time_after: CreationTime = None,
        creation_time_before: CreationTime = None,
        max_results: MaxResults = None,
        name_contains: NameContains = None,
        next_token: NextToken = None,
        sort_by: ModelPackageGroupSortBy = None,
        sort_order: SortOrder = None,
    ) -> ListModelPackageGroupsOutput:
        """Gets a list of the model groups in your Amazon Web Services account.

        :param creation_time_after: A filter that returns only model groups created after the specified
        time.
        :param creation_time_before: A filter that returns only model groups created before the specified
        time.
        :param max_results: The maximum number of results to return in the response.
        :param name_contains: A string in the model group name.
        :param next_token: If the result of the previous ``ListModelPackageGroups`` request was
        truncated, the response includes a ``NextToken``.
        :param sort_by: The field to sort results by.
        :param sort_order: The sort order for results.
        :returns: ListModelPackageGroupsOutput
        """
        raise NotImplementedError

    @handler("ListModelPackages")
    def list_model_packages(
        self,
        context: RequestContext,
        creation_time_after: CreationTime = None,
        creation_time_before: CreationTime = None,
        max_results: MaxResults = None,
        name_contains: NameContains = None,
        model_approval_status: ModelApprovalStatus = None,
        model_package_group_name: ArnOrName = None,
        model_package_type: ModelPackageType = None,
        next_token: NextToken = None,
        sort_by: ModelPackageSortBy = None,
        sort_order: SortOrder = None,
    ) -> ListModelPackagesOutput:
        """Lists the model packages that have been created.

        :param creation_time_after: A filter that returns only model packages created after the specified
        time (timestamp).
        :param creation_time_before: A filter that returns only model packages created before the specified
        time (timestamp).
        :param max_results: The maximum number of model packages to return in the response.
        :param name_contains: A string in the model package name.
        :param model_approval_status: A filter that returns only the model packages with the specified
        approval status.
        :param model_package_group_name: A filter that returns only model versions that belong to the specified
        model group.
        :param model_package_type: A filter that returns only the model packages of the specified type.
        :param next_token: If the response to a previous ``ListModelPackages`` request was
        truncated, the response includes a ``NextToken``.
        :param sort_by: The parameter by which to sort the results.
        :param sort_order: The sort order for the results.
        :returns: ListModelPackagesOutput
        """
        raise NotImplementedError

    @handler("ListModelQualityJobDefinitions")
    def list_model_quality_job_definitions(
        self,
        context: RequestContext,
        endpoint_name: EndpointName = None,
        sort_by: MonitoringJobDefinitionSortKey = None,
        sort_order: SortOrder = None,
        next_token: NextToken = None,
        max_results: MaxResults = None,
        name_contains: NameContains = None,
        creation_time_before: Timestamp = None,
        creation_time_after: Timestamp = None,
    ) -> ListModelQualityJobDefinitionsResponse:
        """Gets a list of model quality monitoring job definitions in your account.

        :param endpoint_name: A filter that returns only model quality monitoring job definitions that
        are associated with the specified endpoint.
        :param sort_by: The field to sort results by.
        :param sort_order: The sort order for results.
        :param next_token: If the result of the previous ``ListModelQualityJobDefinitions`` request
        was truncated, the response includes a ``NextToken``.
        :param max_results: The maximum number of results to return in a call to
        ``ListModelQualityJobDefinitions``.
        :param name_contains: A string in the transform job name.
        :param creation_time_before: A filter that returns only model quality monitoring job definitions
        created before the specified time.
        :param creation_time_after: A filter that returns only model quality monitoring job definitions
        created after the specified time.
        :returns: ListModelQualityJobDefinitionsResponse
        """
        raise NotImplementedError

    @handler("ListModels")
    def list_models(
        self,
        context: RequestContext,
        sort_by: ModelSortKey = None,
        sort_order: OrderKey = None,
        next_token: PaginationToken = None,
        max_results: MaxResults = None,
        name_contains: ModelNameContains = None,
        creation_time_before: Timestamp = None,
        creation_time_after: Timestamp = None,
    ) -> ListModelsOutput:
        """Lists models created with the ``CreateModel`` API.

        :param sort_by: Sorts the list of results.
        :param sort_order: The sort order for results.
        :param next_token: If the response to a previous ``ListModels`` request was truncated, the
        response includes a ``NextToken``.
        :param max_results: The maximum number of models to return in the response.
        :param name_contains: A string in the model name.
        :param creation_time_before: A filter that returns only models created before the specified time
        (timestamp).
        :param creation_time_after: A filter that returns only models with a creation time greater than or
        equal to the specified time (timestamp).
        :returns: ListModelsOutput
        """
        raise NotImplementedError

    @handler("ListMonitoringExecutions")
    def list_monitoring_executions(
        self,
        context: RequestContext,
        monitoring_schedule_name: MonitoringScheduleName = None,
        endpoint_name: EndpointName = None,
        sort_by: MonitoringExecutionSortKey = None,
        sort_order: SortOrder = None,
        next_token: NextToken = None,
        max_results: MaxResults = None,
        scheduled_time_before: Timestamp = None,
        scheduled_time_after: Timestamp = None,
        creation_time_before: Timestamp = None,
        creation_time_after: Timestamp = None,
        last_modified_time_before: Timestamp = None,
        last_modified_time_after: Timestamp = None,
        status_equals: ExecutionStatus = None,
        monitoring_job_definition_name: MonitoringJobDefinitionName = None,
        monitoring_type_equals: MonitoringType = None,
    ) -> ListMonitoringExecutionsResponse:
        """Returns list of all monitoring job executions.

        :param monitoring_schedule_name: Name of a specific schedule to fetch jobs for.
        :param endpoint_name: Name of a specific endpoint to fetch jobs for.
        :param sort_by: Whether to sort results by ``Status``, ``CreationTime``,
        ``ScheduledTime`` field.
        :param sort_order: Whether to sort the results in ``Ascending`` or ``Descending`` order.
        :param next_token: The token returned if the response is truncated.
        :param max_results: The maximum number of jobs to return in the response.
        :param scheduled_time_before: Filter for jobs scheduled before a specified time.
        :param scheduled_time_after: Filter for jobs scheduled after a specified time.
        :param creation_time_before: A filter that returns only jobs created before a specified time.
        :param creation_time_after: A filter that returns only jobs created after a specified time.
        :param last_modified_time_before: A filter that returns only jobs modified after a specified time.
        :param last_modified_time_after: A filter that returns only jobs modified before a specified time.
        :param status_equals: A filter that retrieves only jobs with a specific status.
        :param monitoring_job_definition_name: Gets a list of the monitoring job runs of the specified monitoring job
        definitions.
        :param monitoring_type_equals: A filter that returns only the monitoring job runs of the specified
        monitoring type.
        :returns: ListMonitoringExecutionsResponse
        """
        raise NotImplementedError

    @handler("ListMonitoringSchedules")
    def list_monitoring_schedules(
        self,
        context: RequestContext,
        endpoint_name: EndpointName = None,
        sort_by: MonitoringScheduleSortKey = None,
        sort_order: SortOrder = None,
        next_token: NextToken = None,
        max_results: MaxResults = None,
        name_contains: NameContains = None,
        creation_time_before: Timestamp = None,
        creation_time_after: Timestamp = None,
        last_modified_time_before: Timestamp = None,
        last_modified_time_after: Timestamp = None,
        status_equals: ScheduleStatus = None,
        monitoring_job_definition_name: MonitoringJobDefinitionName = None,
        monitoring_type_equals: MonitoringType = None,
    ) -> ListMonitoringSchedulesResponse:
        """Returns list of all monitoring schedules.

        :param endpoint_name: Name of a specific endpoint to fetch schedules for.
        :param sort_by: Whether to sort results by ``Status``, ``CreationTime``,
        ``ScheduledTime`` field.
        :param sort_order: Whether to sort the results in ``Ascending`` or ``Descending`` order.
        :param next_token: The token returned if the response is truncated.
        :param max_results: The maximum number of jobs to return in the response.
        :param name_contains: Filter for monitoring schedules whose name contains a specified string.
        :param creation_time_before: A filter that returns only monitoring schedules created before a
        specified time.
        :param creation_time_after: A filter that returns only monitoring schedules created after a
        specified time.
        :param last_modified_time_before: A filter that returns only monitoring schedules modified before a
        specified time.
        :param last_modified_time_after: A filter that returns only monitoring schedules modified after a
        specified time.
        :param status_equals: A filter that returns only monitoring schedules modified before a
        specified time.
        :param monitoring_job_definition_name: Gets a list of the monitoring schedules for the specified monitoring job
        definition.
        :param monitoring_type_equals: A filter that returns only the monitoring schedules for the specified
        monitoring type.
        :returns: ListMonitoringSchedulesResponse
        """
        raise NotImplementedError

    @handler("ListNotebookInstanceLifecycleConfigs")
    def list_notebook_instance_lifecycle_configs(
        self,
        context: RequestContext,
        next_token: NextToken = None,
        max_results: MaxResults = None,
        sort_by: NotebookInstanceLifecycleConfigSortKey = None,
        sort_order: NotebookInstanceLifecycleConfigSortOrder = None,
        name_contains: NotebookInstanceLifecycleConfigNameContains = None,
        creation_time_before: CreationTime = None,
        creation_time_after: CreationTime = None,
        last_modified_time_before: LastModifiedTime = None,
        last_modified_time_after: LastModifiedTime = None,
    ) -> ListNotebookInstanceLifecycleConfigsOutput:
        """Lists notebook instance lifestyle configurations created with the
        CreateNotebookInstanceLifecycleConfig API.

        :param next_token: If the result of a ``ListNotebookInstanceLifecycleConfigs`` request was
        truncated, the response includes a ``NextToken``.
        :param max_results: The maximum number of lifecycle configurations to return in the
        response.
        :param sort_by: Sorts the list of results.
        :param sort_order: The sort order for results.
        :param name_contains: A string in the lifecycle configuration name.
        :param creation_time_before: A filter that returns only lifecycle configurations that were created
        before the specified time (timestamp).
        :param creation_time_after: A filter that returns only lifecycle configurations that were created
        after the specified time (timestamp).
        :param last_modified_time_before: A filter that returns only lifecycle configurations that were modified
        before the specified time (timestamp).
        :param last_modified_time_after: A filter that returns only lifecycle configurations that were modified
        after the specified time (timestamp).
        :returns: ListNotebookInstanceLifecycleConfigsOutput
        """
        raise NotImplementedError

    @handler("ListNotebookInstances")
    def list_notebook_instances(
        self,
        context: RequestContext,
        next_token: NextToken = None,
        max_results: MaxResults = None,
        sort_by: NotebookInstanceSortKey = None,
        sort_order: NotebookInstanceSortOrder = None,
        name_contains: NotebookInstanceNameContains = None,
        creation_time_before: CreationTime = None,
        creation_time_after: CreationTime = None,
        last_modified_time_before: LastModifiedTime = None,
        last_modified_time_after: LastModifiedTime = None,
        status_equals: NotebookInstanceStatus = None,
        notebook_instance_lifecycle_config_name_contains: NotebookInstanceLifecycleConfigName = None,
        default_code_repository_contains: CodeRepositoryContains = None,
        additional_code_repository_equals: CodeRepositoryNameOrUrl = None,
    ) -> ListNotebookInstancesOutput:
        """Returns a list of the SageMaker notebook instances in the requester's
        account in an Amazon Web Services Region.

        :param next_token: If the previous call to the ``ListNotebookInstances`` is truncated, the
        response includes a ``NextToken``.
        :param max_results: The maximum number of notebook instances to return.
        :param sort_by: The field to sort results by.
        :param sort_order: The sort order for results.
        :param name_contains: A string in the notebook instances' name.
        :param creation_time_before: A filter that returns only notebook instances that were created before
        the specified time (timestamp).
        :param creation_time_after: A filter that returns only notebook instances that were created after
        the specified time (timestamp).
        :param last_modified_time_before: A filter that returns only notebook instances that were modified before
        the specified time (timestamp).
        :param last_modified_time_after: A filter that returns only notebook instances that were modified after
        the specified time (timestamp).
        :param status_equals: A filter that returns only notebook instances with the specified status.
        :param notebook_instance_lifecycle_config_name_contains: A string in the name of a notebook instances lifecycle configuration
        associated with this notebook instance.
        :param default_code_repository_contains: A string in the name or URL of a Git repository associated with this
        notebook instance.
        :param additional_code_repository_equals: A filter that returns only notebook instances with associated with the
        specified git repository.
        :returns: ListNotebookInstancesOutput
        """
        raise NotImplementedError

    @handler("ListPipelineExecutionSteps")
    def list_pipeline_execution_steps(
        self,
        context: RequestContext,
        pipeline_execution_arn: PipelineExecutionArn = None,
        next_token: NextToken = None,
        max_results: MaxResults = None,
        sort_order: SortOrder = None,
    ) -> ListPipelineExecutionStepsResponse:
        """Gets a list of ``PipeLineExecutionStep`` objects.

        :param pipeline_execution_arn: The Amazon Resource Name (ARN) of the pipeline execution.
        :param next_token: If the result of the previous ``ListPipelineExecutionSteps`` request was
        truncated, the response includes a ``NextToken``.
        :param max_results: The maximum number of pipeline execution steps to return in the
        response.
        :param sort_order: The field by which to sort results.
        :returns: ListPipelineExecutionStepsResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("ListPipelineExecutions")
    def list_pipeline_executions(
        self,
        context: RequestContext,
        pipeline_name: PipelineName,
        created_after: Timestamp = None,
        created_before: Timestamp = None,
        sort_by: SortPipelineExecutionsBy = None,
        sort_order: SortOrder = None,
        next_token: NextToken = None,
        max_results: MaxResults = None,
    ) -> ListPipelineExecutionsResponse:
        """Gets a list of the pipeline executions.

        :param pipeline_name: The name of the pipeline.
        :param created_after: A filter that returns the pipeline executions that were created after a
        specified time.
        :param created_before: A filter that returns the pipeline executions that were created before a
        specified time.
        :param sort_by: The field by which to sort results.
        :param sort_order: The sort order for results.
        :param next_token: If the result of the previous ``ListPipelineExecutions`` request was
        truncated, the response includes a ``NextToken``.
        :param max_results: The maximum number of pipeline executions to return in the response.
        :returns: ListPipelineExecutionsResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("ListPipelineParametersForExecution")
    def list_pipeline_parameters_for_execution(
        self,
        context: RequestContext,
        pipeline_execution_arn: PipelineExecutionArn,
        next_token: NextToken = None,
        max_results: MaxResults = None,
    ) -> ListPipelineParametersForExecutionResponse:
        """Gets a list of parameters for a pipeline execution.

        :param pipeline_execution_arn: The Amazon Resource Name (ARN) of the pipeline execution.
        :param next_token: If the result of the previous ``ListPipelineParametersForExecution``
        request was truncated, the response includes a ``NextToken``.
        :param max_results: The maximum number of parameters to return in the response.
        :returns: ListPipelineParametersForExecutionResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("ListPipelines")
    def list_pipelines(
        self,
        context: RequestContext,
        pipeline_name_prefix: PipelineName = None,
        created_after: Timestamp = None,
        created_before: Timestamp = None,
        sort_by: SortPipelinesBy = None,
        sort_order: SortOrder = None,
        next_token: NextToken = None,
        max_results: MaxResults = None,
    ) -> ListPipelinesResponse:
        """Gets a list of pipelines.

        :param pipeline_name_prefix: The prefix of the pipeline name.
        :param created_after: A filter that returns the pipelines that were created after a specified
        time.
        :param created_before: A filter that returns the pipelines that were created before a specified
        time.
        :param sort_by: The field by which to sort results.
        :param sort_order: The sort order for results.
        :param next_token: If the result of the previous ``ListPipelines`` request was truncated,
        the response includes a ``NextToken``.
        :param max_results: The maximum number of pipelines to return in the response.
        :returns: ListPipelinesResponse
        """
        raise NotImplementedError

    @handler("ListProcessingJobs")
    def list_processing_jobs(
        self,
        context: RequestContext,
        creation_time_after: Timestamp = None,
        creation_time_before: Timestamp = None,
        last_modified_time_after: Timestamp = None,
        last_modified_time_before: Timestamp = None,
        name_contains: String = None,
        status_equals: ProcessingJobStatus = None,
        sort_by: SortBy = None,
        sort_order: SortOrder = None,
        next_token: NextToken = None,
        max_results: MaxResults = None,
    ) -> ListProcessingJobsResponse:
        """Lists processing jobs that satisfy various filters.

        :param creation_time_after: A filter that returns only processing jobs created after the specified
        time.
        :param creation_time_before: A filter that returns only processing jobs created after the specified
        time.
        :param last_modified_time_after: A filter that returns only processing jobs modified after the specified
        time.
        :param last_modified_time_before: A filter that returns only processing jobs modified before the specified
        time.
        :param name_contains: A string in the processing job name.
        :param status_equals: A filter that retrieves only processing jobs with a specific status.
        :param sort_by: The field to sort results by.
        :param sort_order: The sort order for results.
        :param next_token: If the result of the previous ``ListProcessingJobs`` request was
        truncated, the response includes a ``NextToken``.
        :param max_results: The maximum number of processing jobs to return in the response.
        :returns: ListProcessingJobsResponse
        """
        raise NotImplementedError

    @handler("ListProjects")
    def list_projects(
        self,
        context: RequestContext,
        creation_time_after: Timestamp = None,
        creation_time_before: Timestamp = None,
        max_results: MaxResults = None,
        name_contains: ProjectEntityName = None,
        next_token: NextToken = None,
        sort_by: ProjectSortBy = None,
        sort_order: ProjectSortOrder = None,
    ) -> ListProjectsOutput:
        """Gets a list of the projects in an Amazon Web Services account.

        :param creation_time_after: A filter that returns the projects that were created after a specified
        time.
        :param creation_time_before: A filter that returns the projects that were created before a specified
        time.
        :param max_results: The maximum number of projects to return in the response.
        :param name_contains: A filter that returns the projects whose name contains a specified
        string.
        :param next_token: If the result of the previous ``ListProjects`` request was truncated,
        the response includes a ``NextToken``.
        :param sort_by: The field by which to sort results.
        :param sort_order: The sort order for results.
        :returns: ListProjectsOutput
        """
        raise NotImplementedError

    @handler("ListStudioLifecycleConfigs")
    def list_studio_lifecycle_configs(
        self,
        context: RequestContext,
        max_results: MaxResults = None,
        next_token: NextToken = None,
        name_contains: StudioLifecycleConfigName = None,
        app_type_equals: StudioLifecycleConfigAppType = None,
        creation_time_before: Timestamp = None,
        creation_time_after: Timestamp = None,
        modified_time_before: Timestamp = None,
        modified_time_after: Timestamp = None,
        sort_by: StudioLifecycleConfigSortKey = None,
        sort_order: SortOrder = None,
    ) -> ListStudioLifecycleConfigsResponse:
        """Lists the Studio Lifecycle Configurations in your Amazon Web Services
        Account.

        :param max_results: The maximum number of Studio Lifecycle Configurations to return in the
        response.
        :param next_token: If the previous call to ListStudioLifecycleConfigs didn't return the
        full set of Lifecycle Configurations, the call returns a token for
        getting the next set of Lifecycle Configurations.
        :param name_contains: A string in the Lifecycle Configuration name.
        :param app_type_equals: A parameter to search for the App Type to which the Lifecycle
        Configuration is attached.
        :param creation_time_before: A filter that returns only Lifecycle Configurations created on or before
        the specified time.
        :param creation_time_after: A filter that returns only Lifecycle Configurations created on or after
        the specified time.
        :param modified_time_before: A filter that returns only Lifecycle Configurations modified before the
        specified time.
        :param modified_time_after: A filter that returns only Lifecycle Configurations modified after the
        specified time.
        :param sort_by: The property used to sort results.
        :param sort_order: The sort order.
        :returns: ListStudioLifecycleConfigsResponse
        :raises ResourceInUse:
        """
        raise NotImplementedError

    @handler("ListSubscribedWorkteams")
    def list_subscribed_workteams(
        self,
        context: RequestContext,
        name_contains: WorkteamName = None,
        next_token: NextToken = None,
        max_results: MaxResults = None,
    ) -> ListSubscribedWorkteamsResponse:
        """Gets a list of the work teams that you are subscribed to in the Amazon
        Web Services Marketplace. The list may be empty if no work team
        satisfies the filter specified in the ``NameContains`` parameter.

        :param name_contains: A string in the work team name.
        :param next_token: If the result of the previous ``ListSubscribedWorkteams`` request was
        truncated, the response includes a ``NextToken``.
        :param max_results: The maximum number of work teams to return in each page of the response.
        :returns: ListSubscribedWorkteamsResponse
        """
        raise NotImplementedError

    @handler("ListTags")
    def list_tags(
        self,
        context: RequestContext,
        resource_arn: ResourceArn,
        next_token: NextToken = None,
        max_results: ListTagsMaxResults = None,
    ) -> ListTagsOutput:
        """Returns the tags for the specified SageMaker resource.

        :param resource_arn: The Amazon Resource Name (ARN) of the resource whose tags you want to
        retrieve.
        :param next_token: If the response to the previous ``ListTags`` request is truncated,
        SageMaker returns this token.
        :param max_results: Maximum number of tags to return.
        :returns: ListTagsOutput
        """
        raise NotImplementedError

    @handler("ListTrainingJobs")
    def list_training_jobs(
        self,
        context: RequestContext,
        next_token: NextToken = None,
        max_results: MaxResults = None,
        creation_time_after: Timestamp = None,
        creation_time_before: Timestamp = None,
        last_modified_time_after: Timestamp = None,
        last_modified_time_before: Timestamp = None,
        name_contains: NameContains = None,
        status_equals: TrainingJobStatus = None,
        sort_by: SortBy = None,
        sort_order: SortOrder = None,
    ) -> ListTrainingJobsResponse:
        """Lists training jobs.

        When ``StatusEquals`` and ``MaxResults`` are set at the same time, the
        ``MaxResults`` number of training jobs are first retrieved ignoring the
        ``StatusEquals`` parameter and then they are filtered by the
        ``StatusEquals`` parameter, which is returned as a response.

        For example, if ``ListTrainingJobs`` is invoked with the following
        parameters:

        ``{ ... MaxResults: 100, StatusEquals: InProgress ... }``

        First, 100 trainings jobs with any status, including those other than
        ``InProgress``, are selected (sorted according to the creation time,
        from the most current to the oldest). Next, those with a status of
        ``InProgress`` are returned.

        You can quickly test the API using the following Amazon Web Services CLI
        code.

        ``aws sagemaker list-training-jobs --max-results 100 --status-equals InProgress``

        :param next_token: If the result of the previous ``ListTrainingJobs`` request was
        truncated, the response includes a ``NextToken``.
        :param max_results: The maximum number of training jobs to return in the response.
        :param creation_time_after: A filter that returns only training jobs created after the specified
        time (timestamp).
        :param creation_time_before: A filter that returns only training jobs created before the specified
        time (timestamp).
        :param last_modified_time_after: A filter that returns only training jobs modified after the specified
        time (timestamp).
        :param last_modified_time_before: A filter that returns only training jobs modified before the specified
        time (timestamp).
        :param name_contains: A string in the training job name.
        :param status_equals: A filter that retrieves only training jobs with a specific status.
        :param sort_by: The field to sort results by.
        :param sort_order: The sort order for results.
        :returns: ListTrainingJobsResponse
        """
        raise NotImplementedError

    @handler("ListTrainingJobsForHyperParameterTuningJob")
    def list_training_jobs_for_hyper_parameter_tuning_job(
        self,
        context: RequestContext,
        hyper_parameter_tuning_job_name: HyperParameterTuningJobName,
        next_token: NextToken = None,
        max_results: MaxResults = None,
        status_equals: TrainingJobStatus = None,
        sort_by: TrainingJobSortByOptions = None,
        sort_order: SortOrder = None,
    ) -> ListTrainingJobsForHyperParameterTuningJobResponse:
        """Gets a list of TrainingJobSummary objects that describe the training
        jobs that a hyperparameter tuning job launched.

        :param hyper_parameter_tuning_job_name: The name of the tuning job whose training jobs you want to list.
        :param next_token: If the result of the previous
        ``ListTrainingJobsForHyperParameterTuningJob`` request was truncated,
        the response includes a ``NextToken``.
        :param max_results: The maximum number of training jobs to return.
        :param status_equals: A filter that returns only training jobs with the specified status.
        :param sort_by: The field to sort results by.
        :param sort_order: The sort order for results.
        :returns: ListTrainingJobsForHyperParameterTuningJobResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("ListTransformJobs")
    def list_transform_jobs(
        self,
        context: RequestContext,
        creation_time_after: Timestamp = None,
        creation_time_before: Timestamp = None,
        last_modified_time_after: Timestamp = None,
        last_modified_time_before: Timestamp = None,
        name_contains: NameContains = None,
        status_equals: TransformJobStatus = None,
        sort_by: SortBy = None,
        sort_order: SortOrder = None,
        next_token: NextToken = None,
        max_results: MaxResults = None,
    ) -> ListTransformJobsResponse:
        """Lists transform jobs.

        :param creation_time_after: A filter that returns only transform jobs created after the specified
        time.
        :param creation_time_before: A filter that returns only transform jobs created before the specified
        time.
        :param last_modified_time_after: A filter that returns only transform jobs modified after the specified
        time.
        :param last_modified_time_before: A filter that returns only transform jobs modified before the specified
        time.
        :param name_contains: A string in the transform job name.
        :param status_equals: A filter that retrieves only transform jobs with a specific status.
        :param sort_by: The field to sort results by.
        :param sort_order: The sort order for results.
        :param next_token: If the result of the previous ``ListTransformJobs`` request was
        truncated, the response includes a ``NextToken``.
        :param max_results: The maximum number of transform jobs to return in the response.
        :returns: ListTransformJobsResponse
        """
        raise NotImplementedError

    @handler("ListTrialComponents")
    def list_trial_components(
        self,
        context: RequestContext,
        experiment_name: ExperimentEntityName = None,
        trial_name: ExperimentEntityName = None,
        source_arn: String256 = None,
        created_after: Timestamp = None,
        created_before: Timestamp = None,
        sort_by: SortTrialComponentsBy = None,
        sort_order: SortOrder = None,
        max_results: MaxResults = None,
        next_token: NextToken = None,
    ) -> ListTrialComponentsResponse:
        """Lists the trial components in your account. You can sort the list by
        trial component name or creation time. You can filter the list to show
        only components that were created in a specific time range. You can also
        filter on one of the following:

        -  ``ExperimentName``

        -  ``SourceArn``

        -  ``TrialName``

        :param experiment_name: A filter that returns only components that are part of the specified
        experiment.
        :param trial_name: A filter that returns only components that are part of the specified
        trial.
        :param source_arn: A filter that returns only components that have the specified source
        Amazon Resource Name (ARN).
        :param created_after: A filter that returns only components created after the specified time.
        :param created_before: A filter that returns only components created before the specified time.
        :param sort_by: The property used to sort results.
        :param sort_order: The sort order.
        :param max_results: The maximum number of components to return in the response.
        :param next_token: If the previous call to ``ListTrialComponents`` didn't return the full
        set of components, the call returns a token for getting the next set of
        components.
        :returns: ListTrialComponentsResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("ListTrials")
    def list_trials(
        self,
        context: RequestContext,
        experiment_name: ExperimentEntityName = None,
        trial_component_name: ExperimentEntityName = None,
        created_after: Timestamp = None,
        created_before: Timestamp = None,
        sort_by: SortTrialsBy = None,
        sort_order: SortOrder = None,
        max_results: MaxResults = None,
        next_token: NextToken = None,
    ) -> ListTrialsResponse:
        """Lists the trials in your account. Specify an experiment name to limit
        the list to the trials that are part of that experiment. Specify a trial
        component name to limit the list to the trials that associated with that
        trial component. The list can be filtered to show only trials that were
        created in a specific time range. The list can be sorted by trial name
        or creation time.

        :param experiment_name: A filter that returns only trials that are part of the specified
        experiment.
        :param trial_component_name: A filter that returns only trials that are associated with the specified
        trial component.
        :param created_after: A filter that returns only trials created after the specified time.
        :param created_before: A filter that returns only trials created before the specified time.
        :param sort_by: The property used to sort results.
        :param sort_order: The sort order.
        :param max_results: The maximum number of trials to return in the response.
        :param next_token: If the previous call to ``ListTrials`` didn't return the full set of
        trials, the call returns a token for getting the next set of trials.
        :returns: ListTrialsResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("ListUserProfiles")
    def list_user_profiles(
        self,
        context: RequestContext,
        next_token: NextToken = None,
        max_results: MaxResults = None,
        sort_order: SortOrder = None,
        sort_by: UserProfileSortKey = None,
        domain_id_equals: DomainId = None,
        user_profile_name_contains: UserProfileName = None,
    ) -> ListUserProfilesResponse:
        """Lists user profiles.

        :param next_token: If the previous response was truncated, you will receive this token.
        :param max_results: Returns a list up to a specified limit.
        :param sort_order: The sort order for the results.
        :param sort_by: The parameter by which to sort the results.
        :param domain_id_equals: A parameter by which to filter the results.
        :param user_profile_name_contains: A parameter by which to filter the results.
        :returns: ListUserProfilesResponse
        """
        raise NotImplementedError

    @handler("ListWorkforces")
    def list_workforces(
        self,
        context: RequestContext,
        sort_by: ListWorkforcesSortByOptions = None,
        sort_order: SortOrder = None,
        name_contains: WorkforceName = None,
        next_token: NextToken = None,
        max_results: MaxResults = None,
    ) -> ListWorkforcesResponse:
        """Use this operation to list all private and vendor workforces in an
        Amazon Web Services Region. Note that you can only have one private
        workforce per Amazon Web Services Region.

        :param sort_by: Sort workforces using the workforce name or creation date.
        :param sort_order: Sort workforces in ascending or descending order.
        :param name_contains: A filter you can use to search for workforces using part of the
        workforce name.
        :param next_token: A token to resume pagination.
        :param max_results: The maximum number of workforces returned in the response.
        :returns: ListWorkforcesResponse
        """
        raise NotImplementedError

    @handler("ListWorkteams")
    def list_workteams(
        self,
        context: RequestContext,
        sort_by: ListWorkteamsSortByOptions = None,
        sort_order: SortOrder = None,
        name_contains: WorkteamName = None,
        next_token: NextToken = None,
        max_results: MaxResults = None,
    ) -> ListWorkteamsResponse:
        """Gets a list of private work teams that you have defined in a region. The
        list may be empty if no work team satisfies the filter specified in the
        ``NameContains`` parameter.

        :param sort_by: The field to sort results by.
        :param sort_order: The sort order for results.
        :param name_contains: A string in the work team's name.
        :param next_token: If the result of the previous ``ListWorkteams`` request was truncated,
        the response includes a ``NextToken``.
        :param max_results: The maximum number of work teams to return in each page of the response.
        :returns: ListWorkteamsResponse
        """
        raise NotImplementedError

    @handler("PutModelPackageGroupPolicy")
    def put_model_package_group_policy(
        self,
        context: RequestContext,
        model_package_group_name: EntityName,
        resource_policy: PolicyString,
    ) -> PutModelPackageGroupPolicyOutput:
        """Adds a resouce policy to control access to a model group. For
        information about resoure policies, see `Identity-based policies and
        resource-based
        policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_identity-vs-resource.html>`__
        in the *Amazon Web Services Identity and Access Management User Guide.*.

        :param model_package_group_name: The name of the model group to add a resource policy to.
        :param resource_policy: The resource policy for the model group.
        :returns: PutModelPackageGroupPolicyOutput
        """
        raise NotImplementedError

    @handler("QueryLineage")
    def query_lineage(
        self,
        context: RequestContext,
        start_arns: QueryLineageStartArns,
        direction: Direction = None,
        include_edges: Boolean = None,
        filters: QueryFilters = None,
        max_depth: QueryLineageMaxDepth = None,
        max_results: QueryLineageMaxResults = None,
        next_token: String8192 = None,
    ) -> QueryLineageResponse:
        """Use this action to inspect your lineage and discover relationships
        between entities. For more information, see `Querying Lineage
        Entities <https://docs.aws.amazon.com/sagemaker/latest/dg/querying-lineage-entities.html>`__
        in the *Amazon SageMaker Developer Guide*.

        :param start_arns: A list of resource Amazon Resource Name (ARN) that represent the
        starting point for your lineage query.
        :param direction: Associations between lineage entities have a direction.
        :param include_edges: Setting this value to ``True`` retrieves not only the entities of
        interest but also the
        `Associations <https://docs.
        :param filters: A set of filtering parameters that allow you to specify which entities
        should be returned.
        :param max_depth: The maximum depth in lineage relationships from the ``StartArns`` that
        are traversed.
        :param max_results: Limits the number of vertices in the results.
        :param next_token: Limits the number of vertices in the request.
        :returns: QueryLineageResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("RegisterDevices")
    def register_devices(
        self,
        context: RequestContext,
        device_fleet_name: EntityName,
        devices: Devices,
        tags: TagList = None,
    ) -> None:
        """Register devices.

        :param device_fleet_name: The name of the fleet.
        :param devices: A list of devices to register with SageMaker Edge Manager.
        :param tags: The tags associated with devices.
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("RenderUiTemplate")
    def render_ui_template(
        self,
        context: RequestContext,
        task: RenderableTask,
        role_arn: RoleArn,
        ui_template: UiTemplate = None,
        human_task_ui_arn: HumanTaskUiArn = None,
    ) -> RenderUiTemplateResponse:
        """Renders the UI template so that you can preview the worker's experience.

        :param task: A ``RenderableTask`` object containing a representative task to render.
        :param role_arn: The Amazon Resource Name (ARN) that has access to the S3 objects that
        are used by the template.
        :param ui_template: A ``Template`` object containing the worker UI template to render.
        :param human_task_ui_arn: The ``HumanTaskUiArn`` of the worker UI that you want to render.
        :returns: RenderUiTemplateResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("RetryPipelineExecution")
    def retry_pipeline_execution(
        self,
        context: RequestContext,
        pipeline_execution_arn: PipelineExecutionArn,
        client_request_token: IdempotencyToken,
        parallelism_configuration: ParallelismConfiguration = None,
    ) -> RetryPipelineExecutionResponse:
        """Retry the execution of the pipeline.

        :param pipeline_execution_arn: The Amazon Resource Name (ARN) of the pipeline execution.
        :param client_request_token: A unique, case-sensitive identifier that you provide to ensure the
        idempotency of the operation.
        :param parallelism_configuration: This configuration, if specified, overrides the parallelism
        configuration of the parent pipeline.
        :returns: RetryPipelineExecutionResponse
        :raises ResourceNotFound:
        :raises ResourceLimitExceeded:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("Search")
    def search(
        self,
        context: RequestContext,
        resource: ResourceType,
        search_expression: SearchExpression = None,
        sort_by: ResourcePropertyName = None,
        sort_order: SearchSortOrder = None,
        next_token: NextToken = None,
        max_results: MaxResults = None,
    ) -> SearchResponse:
        """Finds Amazon SageMaker resources that match a search query. Matching
        resources are returned as a list of ``SearchRecord`` objects in the
        response. You can sort the search results by any resource property in a
        ascending or descending order.

        You can query against the following value types: numeric, text, Boolean,
        and timestamp.

        :param resource: The name of the Amazon SageMaker resource to search for.
        :param search_expression: A Boolean conditional statement.
        :param sort_by: The name of the resource property used to sort the ``SearchResults``.
        :param sort_order: How ``SearchResults`` are ordered.
        :param next_token: If more than ``MaxResults`` resources match the specified
        ``SearchExpression``, the response includes a ``NextToken``.
        :param max_results: The maximum number of results to return.
        :returns: SearchResponse
        """
        raise NotImplementedError

    @handler("SendPipelineExecutionStepFailure")
    def send_pipeline_execution_step_failure(
        self,
        context: RequestContext,
        callback_token: CallbackToken,
        failure_reason: String256 = None,
        client_request_token: IdempotencyToken = None,
    ) -> SendPipelineExecutionStepFailureResponse:
        """Notifies the pipeline that the execution of a callback step failed,
        along with a message describing why. When a callback step is run, the
        pipeline generates a callback token and includes the token in a message
        sent to Amazon Simple Queue Service (Amazon SQS).

        :param callback_token: The pipeline generated token from the Amazon SQS queue.
        :param failure_reason: A message describing why the step failed.
        :param client_request_token: A unique, case-sensitive identifier that you provide to ensure the
        idempotency of the operation.
        :returns: SendPipelineExecutionStepFailureResponse
        :raises ResourceNotFound:
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("SendPipelineExecutionStepSuccess")
    def send_pipeline_execution_step_success(
        self,
        context: RequestContext,
        callback_token: CallbackToken,
        output_parameters: OutputParameterList = None,
        client_request_token: IdempotencyToken = None,
    ) -> SendPipelineExecutionStepSuccessResponse:
        """Notifies the pipeline that the execution of a callback step succeeded
        and provides a list of the step's output parameters. When a callback
        step is run, the pipeline generates a callback token and includes the
        token in a message sent to Amazon Simple Queue Service (Amazon SQS).

        :param callback_token: The pipeline generated token from the Amazon SQS queue.
        :param output_parameters: A list of the output parameters of the callback step.
        :param client_request_token: A unique, case-sensitive identifier that you provide to ensure the
        idempotency of the operation.
        :returns: SendPipelineExecutionStepSuccessResponse
        :raises ResourceNotFound:
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("StartMonitoringSchedule")
    def start_monitoring_schedule(
        self, context: RequestContext, monitoring_schedule_name: MonitoringScheduleName
    ) -> None:
        """Starts a previously stopped monitoring schedule.

        By default, when you successfully create a new schedule, the status of a
        monitoring schedule is ``scheduled``.

        :param monitoring_schedule_name: The name of the schedule to start.
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("StartNotebookInstance")
    def start_notebook_instance(
        self, context: RequestContext, notebook_instance_name: NotebookInstanceName
    ) -> None:
        """Launches an ML compute instance with the latest version of the libraries
        and attaches your ML storage volume. After configuring the notebook
        instance, SageMaker sets the notebook instance status to ``InService``.
        A notebook instance's status must be ``InService`` before you can
        connect to your Jupyter notebook.

        :param notebook_instance_name: The name of the notebook instance to start.
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("StartPipelineExecution")
    def start_pipeline_execution(
        self,
        context: RequestContext,
        pipeline_name: PipelineName,
        client_request_token: IdempotencyToken,
        pipeline_execution_display_name: PipelineExecutionName = None,
        pipeline_parameters: ParameterList = None,
        pipeline_execution_description: PipelineExecutionDescription = None,
        parallelism_configuration: ParallelismConfiguration = None,
    ) -> StartPipelineExecutionResponse:
        """Starts a pipeline execution.

        :param pipeline_name: The name of the pipeline.
        :param client_request_token: A unique, case-sensitive identifier that you provide to ensure the
        idempotency of the operation.
        :param pipeline_execution_display_name: The display name of the pipeline execution.
        :param pipeline_parameters: Contains a list of pipeline parameters.
        :param pipeline_execution_description: The description of the pipeline execution.
        :param parallelism_configuration: This configuration, if specified, overrides the parallelism
        configuration of the parent pipeline for this specific run.
        :returns: StartPipelineExecutionResponse
        :raises ResourceNotFound:
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("StopAutoMLJob")
    def stop_auto_ml_job(self, context: RequestContext, auto_ml_job_name: AutoMLJobName) -> None:
        """A method for forcing the termination of a running job.

        :param auto_ml_job_name: The name of the object you are requesting.
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("StopCompilationJob")
    def stop_compilation_job(
        self, context: RequestContext, compilation_job_name: EntityName
    ) -> None:
        """Stops a model compilation job.

        To stop a job, Amazon SageMaker sends the algorithm the SIGTERM signal.
        This gracefully shuts the job down. If the job hasn't stopped, it sends
        the SIGKILL signal.

        When it receives a ``StopCompilationJob`` request, Amazon SageMaker
        changes the CompilationJobSummary$CompilationJobStatus of the job to
        ``Stopping``. After Amazon SageMaker stops the job, it sets the
        CompilationJobSummary$CompilationJobStatus to ``Stopped``.

        :param compilation_job_name: The name of the model compilation job to stop.
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("StopEdgePackagingJob")
    def stop_edge_packaging_job(
        self, context: RequestContext, edge_packaging_job_name: EntityName
    ) -> None:
        """Request to stop an edge packaging job.

        :param edge_packaging_job_name: The name of the edge packaging job.
        """
        raise NotImplementedError

    @handler("StopHyperParameterTuningJob")
    def stop_hyper_parameter_tuning_job(
        self, context: RequestContext, hyper_parameter_tuning_job_name: HyperParameterTuningJobName
    ) -> None:
        """Stops a running hyperparameter tuning job and all running training jobs
        that the tuning job launched.

        All model artifacts output from the training jobs are stored in Amazon
        Simple Storage Service (Amazon S3). All data that the training jobs
        write to Amazon CloudWatch Logs are still available in CloudWatch. After
        the tuning job moves to the ``Stopped`` state, it releases all reserved
        resources for the tuning job.

        :param hyper_parameter_tuning_job_name: The name of the tuning job to stop.
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("StopInferenceRecommendationsJob")
    def stop_inference_recommendations_job(
        self, context: RequestContext, job_name: RecommendationJobName
    ) -> None:
        """Stops an Inference Recommender job.

        :param job_name: The name of the job you want to stop.
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("StopLabelingJob")
    def stop_labeling_job(
        self, context: RequestContext, labeling_job_name: LabelingJobName
    ) -> None:
        """Stops a running labeling job. A job that is stopped cannot be restarted.
        Any results obtained before the job is stopped are placed in the Amazon
        S3 output bucket.

        :param labeling_job_name: The name of the labeling job to stop.
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("StopMonitoringSchedule")
    def stop_monitoring_schedule(
        self, context: RequestContext, monitoring_schedule_name: MonitoringScheduleName
    ) -> None:
        """Stops a previously started monitoring schedule.

        :param monitoring_schedule_name: The name of the schedule to stop.
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("StopNotebookInstance")
    def stop_notebook_instance(
        self, context: RequestContext, notebook_instance_name: NotebookInstanceName
    ) -> None:
        """Terminates the ML compute instance. Before terminating the instance,
        SageMaker disconnects the ML storage volume from it. SageMaker preserves
        the ML storage volume. SageMaker stops charging you for the ML compute
        instance when you call ``StopNotebookInstance``.

        To access data on the ML storage volume for a notebook instance that has
        been terminated, call the ``StartNotebookInstance`` API.
        ``StartNotebookInstance`` launches another ML compute instance,
        configures it, and attaches the preserved ML storage volume so you can
        continue your work.

        :param notebook_instance_name: The name of the notebook instance to terminate.
        """
        raise NotImplementedError

    @handler("StopPipelineExecution")
    def stop_pipeline_execution(
        self,
        context: RequestContext,
        pipeline_execution_arn: PipelineExecutionArn,
        client_request_token: IdempotencyToken,
    ) -> StopPipelineExecutionResponse:
        """Stops a pipeline execution.

        **Callback Step**

        A pipeline execution won't stop while a callback step is running. When
        you call ``StopPipelineExecution`` on a pipeline execution with a
        running callback step, SageMaker Pipelines sends an additional Amazon
        SQS message to the specified SQS queue. The body of the SQS message
        contains a "Status" field which is set to "Stopping".

        You should add logic to your Amazon SQS message consumer to take any
        needed action (for example, resource cleanup) upon receipt of the
        message followed by a call to ``SendPipelineExecutionStepSuccess`` or
        ``SendPipelineExecutionStepFailure``.

        Only when SageMaker Pipelines receives one of these calls will it stop
        the pipeline execution.

        **Lambda Step**

        A pipeline execution can't be stopped while a lambda step is running
        because the Lambda function invoked by the lambda step can't be stopped.
        If you attempt to stop the execution while the Lambda function is
        running, the pipeline waits for the Lambda function to finish or until
        the timeout is hit, whichever occurs first, and then stops. If the
        Lambda function finishes, the pipeline execution status is ``Stopped``.
        If the timeout is hit the pipeline execution status is ``Failed``.

        :param pipeline_execution_arn: The Amazon Resource Name (ARN) of the pipeline execution.
        :param client_request_token: A unique, case-sensitive identifier that you provide to ensure the
        idempotency of the operation.
        :returns: StopPipelineExecutionResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("StopProcessingJob")
    def stop_processing_job(
        self, context: RequestContext, processing_job_name: ProcessingJobName
    ) -> None:
        """Stops a processing job.

        :param processing_job_name: The name of the processing job to stop.
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("StopTrainingJob")
    def stop_training_job(
        self, context: RequestContext, training_job_name: TrainingJobName
    ) -> None:
        """Stops a training job. To stop a job, SageMaker sends the algorithm the
        ``SIGTERM`` signal, which delays job termination for 120 seconds.
        Algorithms might use this 120-second window to save the model artifacts,
        so the results of the training is not lost.

        When it receives a ``StopTrainingJob`` request, SageMaker changes the
        status of the job to ``Stopping``. After SageMaker stops the job, it
        sets the status to ``Stopped``.

        :param training_job_name: The name of the training job to stop.
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("StopTransformJob")
    def stop_transform_job(
        self, context: RequestContext, transform_job_name: TransformJobName
    ) -> None:
        """Stops a batch transform job.

        When Amazon SageMaker receives a ``StopTransformJob`` request, the
        status of the job changes to ``Stopping``. After Amazon SageMaker stops
        the job, the status is set to ``Stopped``. When you stop a batch
        transform job before it is completed, Amazon SageMaker doesn't store the
        job's output in Amazon S3.

        :param transform_job_name: The name of the batch transform job to stop.
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("UpdateAction")
    def update_action(
        self,
        context: RequestContext,
        action_name: ExperimentEntityName,
        description: ExperimentDescription = None,
        status: ActionStatus = None,
        properties: LineageEntityParameters = None,
        properties_to_remove: ListLineageEntityParameterKey = None,
    ) -> UpdateActionResponse:
        """Updates an action.

        :param action_name: The name of the action to update.
        :param description: The new description for the action.
        :param status: The new status for the action.
        :param properties: The new list of properties.
        :param properties_to_remove: A list of properties to remove.
        :returns: UpdateActionResponse
        :raises ConflictException:
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("UpdateAppImageConfig")
    def update_app_image_config(
        self,
        context: RequestContext,
        app_image_config_name: AppImageConfigName,
        kernel_gateway_image_config: KernelGatewayImageConfig = None,
    ) -> UpdateAppImageConfigResponse:
        """Updates the properties of an AppImageConfig.

        :param app_image_config_name: The name of the AppImageConfig to update.
        :param kernel_gateway_image_config: The new KernelGateway app to run on the image.
        :returns: UpdateAppImageConfigResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("UpdateArtifact")
    def update_artifact(
        self,
        context: RequestContext,
        artifact_arn: ArtifactArn,
        artifact_name: ExperimentEntityName = None,
        properties: LineageEntityParameters = None,
        properties_to_remove: ListLineageEntityParameterKey = None,
    ) -> UpdateArtifactResponse:
        """Updates an artifact.

        :param artifact_arn: The Amazon Resource Name (ARN) of the artifact to update.
        :param artifact_name: The new name for the artifact.
        :param properties: The new list of properties.
        :param properties_to_remove: A list of properties to remove.
        :returns: UpdateArtifactResponse
        :raises ConflictException:
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("UpdateCodeRepository")
    def update_code_repository(
        self,
        context: RequestContext,
        code_repository_name: EntityName,
        git_config: GitConfigForUpdate = None,
    ) -> UpdateCodeRepositoryOutput:
        """Updates the specified Git repository with the specified values.

        :param code_repository_name: The name of the Git repository to update.
        :param git_config: The configuration of the git repository, including the URL and the
        Amazon Resource Name (ARN) of the Amazon Web Services Secrets Manager
        secret that contains the credentials used to access the repository.
        :returns: UpdateCodeRepositoryOutput
        """
        raise NotImplementedError

    @handler("UpdateContext")
    def update_context(
        self,
        context: RequestContext,
        context_name: ExperimentEntityName,
        description: ExperimentDescription = None,
        properties: LineageEntityParameters = None,
        properties_to_remove: ListLineageEntityParameterKey = None,
    ) -> UpdateContextResponse:
        """Updates a context.

        :param context_name: The name of the context to update.
        :param description: The new description for the context.
        :param properties: The new list of properties.
        :param properties_to_remove: A list of properties to remove.
        :returns: UpdateContextResponse
        :raises ConflictException:
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("UpdateDeviceFleet")
    def update_device_fleet(
        self,
        context: RequestContext,
        device_fleet_name: EntityName,
        output_config: EdgeOutputConfig,
        role_arn: RoleArn = None,
        description: DeviceFleetDescription = None,
        enable_iot_role_alias: EnableIotRoleAlias = None,
    ) -> None:
        """Updates a fleet of devices.

        :param device_fleet_name: The name of the fleet.
        :param output_config: Output configuration for storing sample data collected by the fleet.
        :param role_arn: The Amazon Resource Name (ARN) of the device.
        :param description: Description of the fleet.
        :param enable_iot_role_alias: Whether to create an Amazon Web Services IoT Role Alias during device
        fleet creation.
        :raises ResourceInUse:
        """
        raise NotImplementedError

    @handler("UpdateDevices")
    def update_devices(
        self, context: RequestContext, device_fleet_name: EntityName, devices: Devices
    ) -> None:
        """Updates one or more devices in a fleet.

        :param device_fleet_name: The name of the fleet the devices belong to.
        :param devices: List of devices to register with Edge Manager agent.
        """
        raise NotImplementedError

    @handler("UpdateDomain")
    def update_domain(
        self,
        context: RequestContext,
        domain_id: DomainId,
        default_user_settings: UserSettings = None,
        domain_settings_for_update: DomainSettingsForUpdate = None,
    ) -> UpdateDomainResponse:
        """Updates the default settings for new user profiles in the domain.

        :param domain_id: The ID of the domain to be updated.
        :param default_user_settings: A collection of settings.
        :param domain_settings_for_update: A collection of ``DomainSettings`` configuration values to update.
        :returns: UpdateDomainResponse
        :raises ResourceLimitExceeded:
        :raises ResourceInUse:
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("UpdateEndpoint")
    def update_endpoint(
        self,
        context: RequestContext,
        endpoint_name: EndpointName,
        endpoint_config_name: EndpointConfigName,
        retain_all_variant_properties: Boolean = None,
        exclude_retained_variant_properties: VariantPropertyList = None,
        deployment_config: DeploymentConfig = None,
        retain_deployment_config: Boolean = None,
    ) -> UpdateEndpointOutput:
        """Deploys the new ``EndpointConfig`` specified in the request, switches to
        using newly created endpoint, and then deletes resources provisioned for
        the endpoint using the previous ``EndpointConfig`` (there is no
        availability loss).

        When SageMaker receives the request, it sets the endpoint status to
        ``Updating``. After updating the endpoint, it sets the status to
        ``InService``. To check the status of an endpoint, use the
        DescribeEndpoint API.

        You must not delete an ``EndpointConfig`` in use by an endpoint that is
        live or while the ``UpdateEndpoint`` or ``CreateEndpoint`` operations
        are being performed on the endpoint. To update an endpoint, you must
        create a new ``EndpointConfig``.

        If you delete the ``EndpointConfig`` of an endpoint that is active or
        being created or updated you may lose visibility into the instance type
        the endpoint is using. The endpoint must be deleted in order to stop
        incurring charges.

        :param endpoint_name: The name of the endpoint whose configuration you want to update.
        :param endpoint_config_name: The name of the new endpoint configuration.
        :param retain_all_variant_properties: When updating endpoint resources, enables or disables the retention of
        `variant
        properties <https://docs.
        :param exclude_retained_variant_properties: When you are updating endpoint resources with
        UpdateEndpointInput$RetainAllVariantProperties, whose value is set to
        ``true``, ``ExcludeRetainedVariantProperties`` specifies the list of
        type VariantProperty to override with the values provided by
        ``EndpointConfig``.
        :param deployment_config: The deployment configuration for an endpoint, which contains the desired
        deployment strategy and rollback configurations.
        :param retain_deployment_config: Specifies whether to reuse the last deployment configuration.
        :returns: UpdateEndpointOutput
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("UpdateEndpointWeightsAndCapacities")
    def update_endpoint_weights_and_capacities(
        self,
        context: RequestContext,
        endpoint_name: EndpointName,
        desired_weights_and_capacities: DesiredWeightAndCapacityList,
    ) -> UpdateEndpointWeightsAndCapacitiesOutput:
        """Updates variant weight of one or more variants associated with an
        existing endpoint, or capacity of one variant associated with an
        existing endpoint. When it receives the request, SageMaker sets the
        endpoint status to ``Updating``. After updating the endpoint, it sets
        the status to ``InService``. To check the status of an endpoint, use the
        DescribeEndpoint API.

        :param endpoint_name: The name of an existing SageMaker endpoint.
        :param desired_weights_and_capacities: An object that provides new capacity and weight values for a variant.
        :returns: UpdateEndpointWeightsAndCapacitiesOutput
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("UpdateExperiment")
    def update_experiment(
        self,
        context: RequestContext,
        experiment_name: ExperimentEntityName,
        display_name: ExperimentEntityName = None,
        description: ExperimentDescription = None,
    ) -> UpdateExperimentResponse:
        """Adds, updates, or removes the description of an experiment. Updates the
        display name of an experiment.

        :param experiment_name: The name of the experiment to update.
        :param display_name: The name of the experiment as displayed.
        :param description: The description of the experiment.
        :returns: UpdateExperimentResponse
        :raises ConflictException:
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("UpdateImage")
    def update_image(
        self,
        context: RequestContext,
        image_name: ImageName,
        delete_properties: ImageDeletePropertyList = None,
        description: ImageDescription = None,
        display_name: ImageDisplayName = None,
        role_arn: RoleArn = None,
    ) -> UpdateImageResponse:
        """Updates the properties of a SageMaker image. To change the image's tags,
        use the AddTags and DeleteTags APIs.

        :param image_name: The name of the image to update.
        :param delete_properties: A list of properties to delete.
        :param description: The new description for the image.
        :param display_name: The new display name for the image.
        :param role_arn: The new Amazon Resource Name (ARN) for the IAM role that enables Amazon
        SageMaker to perform tasks on your behalf.
        :returns: UpdateImageResponse
        :raises ResourceInUse:
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("UpdateModelPackage")
    def update_model_package(
        self,
        context: RequestContext,
        model_package_arn: ModelPackageArn,
        model_approval_status: ModelApprovalStatus = None,
        approval_description: ApprovalDescription = None,
        customer_metadata_properties: CustomerMetadataMap = None,
        customer_metadata_properties_to_remove: CustomerMetadataKeyList = None,
        additional_inference_specifications_to_add: AdditionalInferenceSpecifications = None,
    ) -> UpdateModelPackageOutput:
        """Updates a versioned model.

        :param model_package_arn: The Amazon Resource Name (ARN) of the model package.
        :param model_approval_status: The approval status of the model.
        :param approval_description: A description for the approval status of the model.
        :param customer_metadata_properties: The metadata properties associated with the model package versions.
        :param customer_metadata_properties_to_remove: The metadata properties associated with the model package versions to
        remove.
        :param additional_inference_specifications_to_add: An array of additional Inference Specification objects to be added to
        the existing array additional Inference Specification.
        :returns: UpdateModelPackageOutput
        """
        raise NotImplementedError

    @handler("UpdateMonitoringSchedule")
    def update_monitoring_schedule(
        self,
        context: RequestContext,
        monitoring_schedule_name: MonitoringScheduleName,
        monitoring_schedule_config: MonitoringScheduleConfig,
    ) -> UpdateMonitoringScheduleResponse:
        """Updates a previously created schedule.

        :param monitoring_schedule_name: The name of the monitoring schedule.
        :param monitoring_schedule_config: The configuration object that specifies the monitoring schedule and
        defines the monitoring job.
        :returns: UpdateMonitoringScheduleResponse
        :raises ResourceLimitExceeded:
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("UpdateNotebookInstance")
    def update_notebook_instance(
        self,
        context: RequestContext,
        notebook_instance_name: NotebookInstanceName,
        instance_type: InstanceType = None,
        role_arn: RoleArn = None,
        lifecycle_config_name: NotebookInstanceLifecycleConfigName = None,
        disassociate_lifecycle_config: DisassociateNotebookInstanceLifecycleConfig = None,
        volume_size_in_gb: NotebookInstanceVolumeSizeInGB = None,
        default_code_repository: CodeRepositoryNameOrUrl = None,
        additional_code_repositories: AdditionalCodeRepositoryNamesOrUrls = None,
        accelerator_types: NotebookInstanceAcceleratorTypes = None,
        disassociate_accelerator_types: DisassociateNotebookInstanceAcceleratorTypes = None,
        disassociate_default_code_repository: DisassociateDefaultCodeRepository = None,
        disassociate_additional_code_repositories: DisassociateAdditionalCodeRepositories = None,
        root_access: RootAccess = None,
    ) -> UpdateNotebookInstanceOutput:
        """Updates a notebook instance. NotebookInstance updates include upgrading
        or downgrading the ML compute instance used for your notebook instance
        to accommodate changes in your workload requirements.

        :param notebook_instance_name: The name of the notebook instance to update.
        :param instance_type: The Amazon ML compute instance type.
        :param role_arn: The Amazon Resource Name (ARN) of the IAM role that SageMaker can assume
        to access the notebook instance.
        :param lifecycle_config_name: The name of a lifecycle configuration to associate with the notebook
        instance.
        :param disassociate_lifecycle_config: Set to ``true`` to remove the notebook instance lifecycle configuration
        currently associated with the notebook instance.
        :param volume_size_in_gb: The size, in GB, of the ML storage volume to attach to the notebook
        instance.
        :param default_code_repository: The Git repository to associate with the notebook instance as its
        default code repository.
        :param additional_code_repositories: An array of up to three Git repositories to associate with the notebook
        instance.
        :param accelerator_types: A list of the Elastic Inference (EI) instance types to associate with
        this notebook instance.
        :param disassociate_accelerator_types: A list of the Elastic Inference (EI) instance types to remove from this
        notebook instance.
        :param disassociate_default_code_repository: The name or URL of the default Git repository to remove from this
        notebook instance.
        :param disassociate_additional_code_repositories: A list of names or URLs of the default Git repositories to remove from
        this notebook instance.
        :param root_access: Whether root access is enabled or disabled for users of the notebook
        instance.
        :returns: UpdateNotebookInstanceOutput
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("UpdateNotebookInstanceLifecycleConfig")
    def update_notebook_instance_lifecycle_config(
        self,
        context: RequestContext,
        notebook_instance_lifecycle_config_name: NotebookInstanceLifecycleConfigName,
        on_create: NotebookInstanceLifecycleConfigList = None,
        on_start: NotebookInstanceLifecycleConfigList = None,
    ) -> UpdateNotebookInstanceLifecycleConfigOutput:
        """Updates a notebook instance lifecycle configuration created with the
        CreateNotebookInstanceLifecycleConfig API.

        :param notebook_instance_lifecycle_config_name: The name of the lifecycle configuration.
        :param on_create: The shell script that runs only once, when you create a notebook
        instance.
        :param on_start: The shell script that runs every time you start a notebook instance,
        including when you create the notebook instance.
        :returns: UpdateNotebookInstanceLifecycleConfigOutput
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError

    @handler("UpdatePipeline")
    def update_pipeline(
        self,
        context: RequestContext,
        pipeline_name: PipelineName,
        pipeline_display_name: PipelineName = None,
        pipeline_definition: PipelineDefinition = None,
        pipeline_definition_s3_location: PipelineDefinitionS3Location = None,
        pipeline_description: PipelineDescription = None,
        role_arn: RoleArn = None,
        parallelism_configuration: ParallelismConfiguration = None,
    ) -> UpdatePipelineResponse:
        """Updates a pipeline.

        :param pipeline_name: The name of the pipeline to update.
        :param pipeline_display_name: The display name of the pipeline.
        :param pipeline_definition: The JSON pipeline definition.
        :param pipeline_definition_s3_location: The location of the pipeline definition stored in Amazon S3.
        :param pipeline_description: The description of the pipeline.
        :param role_arn: The Amazon Resource Name (ARN) that the pipeline uses to execute.
        :param parallelism_configuration: If specified, it applies to all executions of this pipeline by default.
        :returns: UpdatePipelineResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("UpdatePipelineExecution")
    def update_pipeline_execution(
        self,
        context: RequestContext,
        pipeline_execution_arn: PipelineExecutionArn,
        pipeline_execution_description: PipelineExecutionDescription = None,
        pipeline_execution_display_name: PipelineExecutionName = None,
        parallelism_configuration: ParallelismConfiguration = None,
    ) -> UpdatePipelineExecutionResponse:
        """Updates a pipeline execution.

        :param pipeline_execution_arn: The Amazon Resource Name (ARN) of the pipeline execution.
        :param pipeline_execution_description: The description of the pipeline execution.
        :param pipeline_execution_display_name: The display name of the pipeline execution.
        :param parallelism_configuration: This configuration, if specified, overrides the parallelism
        configuration of the parent pipeline for this specific run.
        :returns: UpdatePipelineExecutionResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("UpdateProject")
    def update_project(
        self,
        context: RequestContext,
        project_name: ProjectEntityName,
        project_description: EntityDescription = None,
        service_catalog_provisioning_update_details: ServiceCatalogProvisioningUpdateDetails = None,
        tags: TagList = None,
    ) -> UpdateProjectOutput:
        """Updates a machine learning (ML) project that is created from a template
        that sets up an ML pipeline from training to deploying an approved
        model.

        You must not update a project that is in use. If you update the
        ``ServiceCatalogProvisioningUpdateDetails`` of a project that is active
        or being created, or updated, you may lose resources already created by
        the project.

        :param project_name: The name of the project.
        :param project_description: The description for the project.
        :param service_catalog_provisioning_update_details: The product ID and provisioning artifact ID to provision a service
        catalog.
        :param tags: An array of key-value pairs.
        :returns: UpdateProjectOutput
        """
        raise NotImplementedError

    @handler("UpdateTrainingJob")
    def update_training_job(
        self,
        context: RequestContext,
        training_job_name: TrainingJobName,
        profiler_config: ProfilerConfigForUpdate = None,
        profiler_rule_configurations: ProfilerRuleConfigurations = None,
    ) -> UpdateTrainingJobResponse:
        """Update a model training job to request a new Debugger profiling
        configuration.

        :param training_job_name: The name of a training job to update the Debugger profiling
        configuration.
        :param profiler_config: Configuration information for Debugger system monitoring, framework
        profiling, and storage paths.
        :param profiler_rule_configurations: Configuration information for Debugger rules for profiling system and
        framework metrics.
        :returns: UpdateTrainingJobResponse
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("UpdateTrial")
    def update_trial(
        self,
        context: RequestContext,
        trial_name: ExperimentEntityName,
        display_name: ExperimentEntityName = None,
    ) -> UpdateTrialResponse:
        """Updates the display name of a trial.

        :param trial_name: The name of the trial to update.
        :param display_name: The name of the trial as displayed.
        :returns: UpdateTrialResponse
        :raises ConflictException:
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("UpdateTrialComponent")
    def update_trial_component(
        self,
        context: RequestContext,
        trial_component_name: ExperimentEntityName,
        display_name: ExperimentEntityName = None,
        status: TrialComponentStatus = None,
        start_time: Timestamp = None,
        end_time: Timestamp = None,
        parameters: TrialComponentParameters = None,
        parameters_to_remove: ListTrialComponentKey256 = None,
        input_artifacts: TrialComponentArtifacts = None,
        input_artifacts_to_remove: ListTrialComponentKey256 = None,
        output_artifacts: TrialComponentArtifacts = None,
        output_artifacts_to_remove: ListTrialComponentKey256 = None,
    ) -> UpdateTrialComponentResponse:
        """Updates one or more properties of a trial component.

        :param trial_component_name: The name of the component to update.
        :param display_name: The name of the component as displayed.
        :param status: The new status of the component.
        :param start_time: When the component started.
        :param end_time: When the component ended.
        :param parameters: Replaces all of the component's hyperparameters with the specified
        hyperparameters.
        :param parameters_to_remove: The hyperparameters to remove from the component.
        :param input_artifacts: Replaces all of the component's input artifacts with the specified
        artifacts.
        :param input_artifacts_to_remove: The input artifacts to remove from the component.
        :param output_artifacts: Replaces all of the component's output artifacts with the specified
        artifacts.
        :param output_artifacts_to_remove: The output artifacts to remove from the component.
        :returns: UpdateTrialComponentResponse
        :raises ConflictException:
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("UpdateUserProfile")
    def update_user_profile(
        self,
        context: RequestContext,
        domain_id: DomainId,
        user_profile_name: UserProfileName,
        user_settings: UserSettings = None,
    ) -> UpdateUserProfileResponse:
        """Updates a user profile.

        :param domain_id: The domain ID.
        :param user_profile_name: The user profile name.
        :param user_settings: A collection of settings.
        :returns: UpdateUserProfileResponse
        :raises ResourceLimitExceeded:
        :raises ResourceInUse:
        :raises ResourceNotFound:
        """
        raise NotImplementedError

    @handler("UpdateWorkforce")
    def update_workforce(
        self,
        context: RequestContext,
        workforce_name: WorkforceName,
        source_ip_config: SourceIpConfig = None,
        oidc_config: OidcConfig = None,
    ) -> UpdateWorkforceResponse:
        """Use this operation to update your workforce. You can use this operation
        to require that workers use specific IP addresses to work on tasks and
        to update your OpenID Connect (OIDC) Identity Provider (IdP) workforce
        configuration.

        Use ``SourceIpConfig`` to restrict worker access to tasks to a specific
        range of IP addresses. You specify allowed IP addresses by creating a
        list of up to ten
        `CIDRs <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html>`__.
        By default, a workforce isn't restricted to specific IP addresses. If
        you specify a range of IP addresses, workers who attempt to access tasks
        using any IP address outside the specified range are denied and get a
        ``Not Found`` error message on the worker portal.

        Use ``OidcConfig`` to update the configuration of a workforce created
        using your own OIDC IdP.

        You can only update your OIDC IdP configuration when there are no work
        teams associated with your workforce. You can delete work teams using
        the operation.

        After restricting access to a range of IP addresses or updating your
        OIDC IdP configuration with this operation, you can view details about
        your update workforce using the operation.

        This operation only applies to private workforces.

        :param workforce_name: The name of the private workforce that you want to update.
        :param source_ip_config: A list of one to ten worker IP address ranges
        (`CIDRs <https://docs.
        :param oidc_config: Use this parameter to update your OIDC Identity Provider (IdP)
        configuration for a workforce made using your own IdP.
        :returns: UpdateWorkforceResponse
        """
        raise NotImplementedError

    @handler("UpdateWorkteam")
    def update_workteam(
        self,
        context: RequestContext,
        workteam_name: WorkteamName,
        member_definitions: MemberDefinitions = None,
        description: String200 = None,
        notification_configuration: NotificationConfiguration = None,
    ) -> UpdateWorkteamResponse:
        """Updates an existing work team with new member definitions or
        description.

        :param workteam_name: The name of the work team to update.
        :param member_definitions: A list of ``MemberDefinition`` objects that contains objects that
        identify the workers that make up the work team.
        :param description: An updated description for the work team.
        :param notification_configuration: Configures SNS topic notifications for available or expiring work items.
        :returns: UpdateWorkteamResponse
        :raises ResourceLimitExceeded:
        """
        raise NotImplementedError
