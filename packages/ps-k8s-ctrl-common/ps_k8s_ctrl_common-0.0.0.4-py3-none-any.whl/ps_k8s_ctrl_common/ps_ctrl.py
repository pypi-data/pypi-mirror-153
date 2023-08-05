"""
Copyright (C) 2022 Viasat, Inc.
All rights reserved.
The information in this software is subject to change without notice and
should not be construed as a commitment by Viasat, Inc.

Viasat Proprietary
The Proprietary Information provided herein is proprietary to Viasat and
must be protected from further distribution and use.  Disclosure to others,
use or copying without express written authorization of Viasat, is strictly
prohibited.

ps_ctrl - common functions for configuration controllers
"""
import logging
from typing import Tuple, Optional

import kubernetes
from ps_k8s_api_wrapper.api_connect import ConfigType
from ps_k8s_api_wrapper.ps_k8s import PsK8s

from ps_k8s_ctrl_common import ctrl_data

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class PsCtrl:
    """
    PsCtrl - a collection of kubernetes configuration controller functions
    """

    def __init__(self, controller_data: ctrl_data.ControllerData):
        """
        Constructor for the PsCtrl class:
        """
        # Store the controller data
        self.controller_data = controller_data

        # Get the kubernetes api wrapper object
        self.ps_k8s = PsK8s()

        # Get the kube api config from service account (in-cluster) or ~/.kube/config
        self.config_type: ConfigType = self.ps_k8s.get_config_type()

    def get_config_type(self) -> ConfigType:
        """
        Get the type of config (in cluster or external (.kube/config))
        :return: ConfigType
        """
        return self.config_type

    def get_controller_data(self) -> ctrl_data.ControllerData:
        """
        Return the controller data structure
        :return: ctrl_data.ControllerData
        """
        return self.controller_data

    def read_crs(self) -> Tuple[bool, bool]:
        """
        Read through the Custom Resources this controller is monitoring
        and read it if available, or mark it as None.  Keep counts
        of how many primary CR, and primary CR read, and required CR,
        and required CR read, so it can return True if primary and/or
        required CRs are all there
        :return: Tuple, True if all primary available, True if all required available
        """
        # Setup counters for tracking primary/required available, and in monitor list
        primary_cr_found: int = 0
        primary_cr_cnt: int = 0
        required_cr_found: int = 0
        required_cr_cnt: int = 0
        is_primary: bool
        is_required: bool

        # Loop through the controllers in the input list
        for custom_resource in self.controller_data.input_cr:
            # See if the custom resource is a primary resource, and count if it is
            if custom_resource.primary_cr:
                primary_cr_cnt += 1
                is_primary = True
            else:
                is_primary = False

            # See if the custom resource is optional, and count if it is
            if custom_resource.optional:
                is_required = False
            else:
                is_required = True
                required_cr_cnt += 1

            LOGGER.info(f"Reading CR: {custom_resource.name}")
            # Read the custom resource
            cr_data = self.ps_k8s.read_cr(
                cr_group_name=custom_resource.group_name,
                cr_version=custom_resource.version,
                cr_namespace=custom_resource.namespace,
                cr_plural=custom_resource.plural,
                cr_name=custom_resource.name)
            # See if the read was successful
            if cr_data:
                # Store the read custom resource
                custom_resource.data = cr_data
                if is_primary:
                    primary_cr_found += 1
                if is_required:
                    required_cr_found += 1
            else:
                LOGGER.info(f"Could not read CR: {custom_resource.name}")
                custom_resource.data = None

        # Return True if all primary CRs available, True if all required CRs available
        return primary_cr_found == primary_cr_cnt, required_cr_found == required_cr_cnt

    def read_cms(self) -> bool:
        """
        Read the Config Maps for the controller
        :return: True if all config maps read
        """
        # Count the number of config maps read
        cm_read: int = 0

        # Loop through the configmaps in the controller configmap list
        for config_map in self.controller_data.output_cm:
            LOGGER.info(f"Reading CM: {config_map.name}")
            # Read the config map
            cm_data = self.ps_k8s.read_config_map(
                name=config_map.name,
                namespace=config_map.namespace
            )
            # See if the config map read was successful, if so, store it and count it
            if cm_data:
                config_map.data_current = cm_data
                cm_read += 1
            else:
                config_map.data_current = None

        # True if all config maps read, False otherwise
        return len(self.controller_data.output_cm) == cm_read

    def read_current_deployment(self) -> bool:
        """
        Read the current deployments
        :return: True if all deployments read successfully, False otherwise
        """
        # Count the deployments read
        deployment_read: int = 0

        # Loop through the deployments in the list
        for deployment in self.controller_data.deployments:
            # Read the deployment
            deploy_data: Optional[kubernetes.client.V1Deployment] = \
                self.ps_k8s.read_deployment(
                    name=deployment.name,
                    namespace=deployment.namespace)
            # If the deployment read was successful, store it and count it
            if deploy_data:
                deployment.data = deploy_data
                deployment_read += 1
            else:
                deployment.data = None

        # True if all deployments read successfully, False otherwise
        return len(self.controller_data.deployments) == deployment_read

    def config_maps_match(self) -> bool:
        """
        See if all of the current config maps match the desired config maps
        :return: True if all config maps match, False otherwise
        """
        # Count the number of config maps that match
        configmap_match: int = 0

        # Loop through the list of config maps
        for config_map in self.controller_data.output_cm:
            # If both current and desired don't exist count it as a match
            if not config_map.data_current and not config_map.data_desired:
                configmap_match += 1
            else:
                # Only compare if both desired and current CMs are good
                if config_map.data_current and config_map.data_desired:
                    # See if the config maps match
                    if self.ps_k8s.diff_config_map(config_map.data_current, config_map.data_desired):
                        # Count it if they match
                        configmap_match += 1

        # True if the # of config maps in the list match the matching CM count
        return len(self.controller_data.output_cm) == configmap_match

    def deploy_desired_configmaps(self) -> bool:
        """
        Deploy the desired config maps
        :return: True if all config maps deployed successfully, False otherwise
        """
        # Count the number of successful deploys of config maps
        configmap_ok: int = 0

        # Loop through the config maps in the list
        for config_map in self.controller_data.output_cm:
            # Try to update the config map
            if self.ps_k8s.upsert_config_map(
                    config_map=config_map.data_desired
            ):
                # Increment the successful config map count
                configmap_ok += 1

        # True if all config maps ok, False otherwise
        return len(self.controller_data.output_cm) == configmap_ok

    def deploy_services(self):
        """
        Deploy services to the cluster
        :return: True if all service deployed ok, False otherwise
        """
        # Count the number of services successfully created
        services_ok: int = 0

        # Loop through the services in the list
        for service in self.controller_data.services:
            # Create a service object (manifest)
            service_obj = self.ps_k8s.create_service_object(
                name=service.name,
                namespace=service.namespace,
                service_type=service.service_type,
                ports=service.ports,
                selector=service.selector
            )

            # Upsert the service
            if self.ps_k8s.upsert_service(service=service_obj):
                # Increment the number of services that are ok
                services_ok += 1

        # Are all the services in the list ok, return True
        return len(self.controller_data.services) == services_ok

    def restart_deployed_pods(self):
        """
        Restart the deployed pods to get them to read the configs
        :return: True if all pods restarted ok
        """
        # Count the number of deployments that went ok
        deployments_ok: int = 0

        # Loop through the deployments for this controller
        for deployment in self.controller_data.deployments:
            # If we could read the deployment, create one
            if not deployment.data:
                # Create a deployment
                deployment.data = \
                    self.ps_k8s.create_deployment_object(
                        name=deployment.name,
                        namespace=deployment.namespace,
                        deployment_replicas=deployment.deployment_replicas,
                        container_image=deployment.container_image,
                        container_name=deployment.container_name,
                        env=deployment.env,
                        ports=deployment.ports,
                        volumes=deployment.volumes,
                        volume_mounts=deployment.volume_mounts,
                        pod_service_account=deployment.pod_service_account
                        if self.config_type == ConfigType.INCLUSTER_CONFIG else "")
            # Upsert the deployment
            if self.ps_k8s.upsert_deployment(deployment=deployment.data):
                # Increment the successful deployments counter if this worked
                deployments_ok += 1

        # True if all deployments in the list were ok
        return len(self.controller_data.deployments) == deployments_ok

    def delete_configmaps(self):
        """
        Delete configmaps
        :return: True if all config maps deleted ok
        """
        # Count the number of configmaps deleted successfully
        configmap_deleted_ok: int = 0

        # Loop through config maps in the list
        for config_map in self.controller_data.output_cm:
            # Delete the config map
            if self.ps_k8s.delete_config_map(
                    name=config_map.name,
                    namespace=config_map.namespace
            ):
                # Increment the config maps delete ok counter
                configmap_deleted_ok += 1

        # True if all config maps deleted ok
        return len(self.controller_data.output_cm) == configmap_deleted_ok

    def delete_services(self):
        """
        Delete the services
        :return: True if all services deleted ok, False otherwise
        """
        # Count the number of services deleted successfully
        services_ok: int = 0

        # Loop through the services in the list
        for service in self.controller_data.services:
            # Delete the service
            if self.ps_k8s.delete_service(
                    name=service.name,
                    namespace=service.namespace):
                # Increment the services deleted successfully counter
                services_ok += 1

        # True if all services deleted ok, False otherwise
        return len(self.controller_data.services) == services_ok

    def delete_deployments(self):
        """
        Delete deployments
        :return: True if all deployments deleted ok, False otherwise
        """
        # Count the number of successful deployments
        deployments_ok: int = 0

        # Loop through the deployments
        for deployment in self.controller_data.deployments:
            # Delete the deployment
            if self.ps_k8s.delete_deployment(
                    name=deployment.name,
                    namespace=deployment.namespace):
                # Increment the deployments ok counter
                deployments_ok += 1

        # True if all deployments ok, False otherwise
        return len(self.controller_data.deployments) == deployments_ok
