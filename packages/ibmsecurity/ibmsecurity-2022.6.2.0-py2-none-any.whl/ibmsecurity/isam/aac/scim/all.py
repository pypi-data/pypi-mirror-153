import logging
from ibmsecurity.utilities.tools import json_sort

logger = logging.getLogger(__name__)

uri = "/mga/scim/configuration"
requires_modules = ["mga", "federation"]
requires_version = "9.0.2"

def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the complete list of SCIM configuration settings
    """
    return isamAppliance.invoke_get("Retrieving the complete list of SCIM configuration settings",
                                    "/mga/scim/configuration", requires_modules=requires_modules,
                                    requires_version=requires_version)


def set(isamAppliance, settings, check_mode=False, force=False):
    """
    Updating the complete SCIM configuration settings

    """
    obj = get(isamAppliance)
    obj = obj['data']
    sorted_new = json_sort(settings)
    sorted_old = json_sort(obj)
    if sorted_new == sorted_old:
        update_required = False
    else:
        update_required = True

    if force is True or update_required is True:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_put("Updating the complete SCIM configuration settings",
                                            "{0}".format(uri),
                                            settings,
                                            requires_modules=requires_modules,
                                            requires_version=requires_version
                                            )

    return isamAppliance.create_return_object(changed=False)
