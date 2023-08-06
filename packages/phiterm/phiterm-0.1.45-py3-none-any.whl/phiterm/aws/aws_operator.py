from typing import Optional

from phidata.infra.aws.config import AwsConfig
from phidata.infra.aws.exceptions import AwsConfigException
from phidata.infra.aws.manager import AwsManager

from phiterm.utils.cli_console import (
    print_error,
    print_heading,
    print_subheading,
    print_info,
)
from phidata.utils.log import logger


def deploy_aws_config(
    config: AwsConfig,
    name_filter: Optional[str] = None,
    type_filter: Optional[str] = None,
    app_filter: Optional[str] = None,
    dry_run: Optional[bool] = False,
    auto_confirm: Optional[bool] = False,
) -> bool:

    # Step 1: Get the AwsManager
    aws_manager: AwsManager = config.get_aws_manager()
    if aws_manager is None:
        raise AwsConfigException("AwsManager unavailable")
    print_heading(f"--**-- Aws env: {config.env}\n")

    # Step 2: If dry_run, print the resources and return True
    if dry_run:
        aws_manager.create_resources_dry_run(
            name_filter=name_filter,
            type_filter=type_filter,
            app_filter=app_filter,
            auto_confirm=auto_confirm,
        )
        return True

    # Step 3: Create resources
    try:
        success: bool = aws_manager.create_resources(
            name_filter=name_filter,
            type_filter=type_filter,
            app_filter=app_filter,
            auto_confirm=auto_confirm,
        )
        if not success:
            return False
    except Exception as e:
        logger.error(e)
        return False

    # Step 4: Validate resources are created
    resource_creation_valid: bool = aws_manager.validate_resources_are_created(
        name_filter=name_filter,
        type_filter=type_filter,
        app_filter=app_filter,
    )
    if not resource_creation_valid:
        logger.error("AwsResource creation could not be validated")
        return False

    print_info("Aws config deployed")
    return True


def shutdown_aws_config(
    config: AwsConfig,
    name_filter: Optional[str] = None,
    type_filter: Optional[str] = None,
    app_filter: Optional[str] = None,
    dry_run: Optional[bool] = False,
    auto_confirm: Optional[bool] = False,
) -> bool:

    # Step 1: Get the AwsManager
    aws_manager: AwsManager = config.get_aws_manager()
    if aws_manager is None:
        raise AwsConfigException("AwsManager unavailable")
    print_heading(f"--**-- Aws env: {config.env}\n")

    # Step 2: If dry_run, print the resources and return True
    if dry_run:
        aws_manager.delete_resources_dry_run(
            name_filter=name_filter,
            type_filter=type_filter,
            app_filter=app_filter,
            auto_confirm=auto_confirm,
        )
        return True

    # Step 3: Delete resources
    try:
        success: bool = aws_manager.delete_resources(
            name_filter=name_filter,
            type_filter=type_filter,
            app_filter=app_filter,
            auto_confirm=auto_confirm,
        )
        if not success:
            return False
    except Exception as e:
        logger.error(e)
        return False

    # Step 4: Validate resources are deleted
    resources_deletion_valid: bool = aws_manager.validate_resources_are_deleted(
        name_filter=name_filter,
        type_filter=type_filter,
        app_filter=app_filter,
    )
    if not resources_deletion_valid:
        logger.error("AwsResource deletion could not be validated")
        return False

    print_info("Aws config shutdown")
    return True


def patch_aws_config(
    config: AwsConfig,
    name_filter: Optional[str] = None,
    type_filter: Optional[str] = None,
    app_filter: Optional[str] = None,
    dry_run: Optional[bool] = False,
    auto_confirm: Optional[bool] = False,
) -> bool:

    # Step 1: Get the AwsManager
    aws_manager: AwsManager = config.get_aws_manager()
    if aws_manager is None:
        raise AwsConfigException("AwsManager unavailable")
    print_heading(f"--**-- Aws env: {config.env}\n")

    # Step 2: If dry_run, print the resources and return True
    if dry_run:
        aws_manager.patch_resources_dry_run(
            name_filter=name_filter,
            type_filter=type_filter,
            app_filter=app_filter,
            auto_confirm=auto_confirm,
        )
        return True

    # Step 3: Delete resources
    try:
        success: bool = aws_manager.patch_resources(
            name_filter=name_filter, type_filter=type_filter
        )
        if not success:
            return False
    except Exception as e:
        logger.error(e)
        return False

    # Step 4: Validate resources are patched
    resources_deletion_valid: bool = aws_manager.validate_resources_are_patched(
        name_filter=name_filter,
        type_filter=type_filter,
        app_filter=app_filter,
    )
    if not resources_deletion_valid:
        logger.error("AwsResource patch could not be validated")
        return False

    print_info("Aws config patched")
    return True
