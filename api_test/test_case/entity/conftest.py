import pytest
from api_test.api.entity.organization_api import OrganizationApi


@pytest.fixture(name="organization", scope="module")
def init_organization():
    organization = OrganizationApi()
    yield organization
    # organization.delete_organization()
