
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from .api.api_application_api import APIApplicationApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from onshape_client.oas.api.api_application_api import APIApplicationApi
from onshape_client.oas.api.account_api import AccountApi
from onshape_client.oas.api.alias_api import AliasApi
from onshape_client.oas.api.app_associative_data_api import AppAssociativeDataApi
from onshape_client.oas.api.app_element_api import AppElementApi
from onshape_client.oas.api.assembly_api import AssemblyApi
from onshape_client.oas.api.billing_api import BillingApi
from onshape_client.oas.api.blob_element_api import BlobElementApi
from onshape_client.oas.api.classroom_api import ClassroomApi
from onshape_client.oas.api.comment_api import CommentApi
from onshape_client.oas.api.company_api import CompanyApi
from onshape_client.oas.api.document_api import DocumentApi
from onshape_client.oas.api.drawing_api import DrawingApi
from onshape_client.oas.api.element_api import ElementApi
from onshape_client.oas.api.export_rule_api import ExportRuleApi
from onshape_client.oas.api.feature_studio_api import FeatureStudioApi
from onshape_client.oas.api.folder_api import FolderApi
from onshape_client.oas.api.insertable_api import InsertableApi
from onshape_client.oas.api.metadata_api import MetadataApi
from onshape_client.oas.api.metadata_category_api import MetadataCategoryApi
from onshape_client.oas.api.open_api_api import OpenApiApi
from onshape_client.oas.api.part_api import PartApi
from onshape_client.oas.api.part_number_api import PartNumberApi
from onshape_client.oas.api.part_studio_api import PartStudioApi
from onshape_client.oas.api.publication_api import PublicationApi
from onshape_client.oas.api.release_package_api import ReleasePackageApi
from onshape_client.oas.api.revision_api import RevisionApi
from onshape_client.oas.api.sketch_api import SketchApi
from onshape_client.oas.api.team_api import TeamApi
from onshape_client.oas.api.thumbnail_api import ThumbnailApi
from onshape_client.oas.api.translation_api import TranslationApi
from onshape_client.oas.api.user_api import UserApi
from onshape_client.oas.api.version_api import VersionApi
from onshape_client.oas.api.webhook_api import WebhookApi
from onshape_client.oas.api.workflow_api import WorkflowApi
from onshape_client.oas.api.workflowable_test_object_api import WorkflowableTestObjectApi
