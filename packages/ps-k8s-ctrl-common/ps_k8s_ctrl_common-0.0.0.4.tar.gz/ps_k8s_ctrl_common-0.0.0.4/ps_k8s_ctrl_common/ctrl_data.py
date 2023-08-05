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

ctrl_data.py - Data structures for defining a controller
"""
from typing import List, Optional, Dict

import kubernetes


class CRData:
    """
    CRData - Data for a Custom Resource
    """

    def __init__(self,
                 name: str,
                 namespace: str,
                 group_name: str,
                 version: str,
                 plural: str,
                 primary_cr: bool,
                 optional: bool = False,
                 data: Optional[dict] = None):
        """
        Constructor for the Custom Resource Class
        :param name: Name of the Custom Resources
        :param namespace: Namespace for the Custom Resource
        :param group_name: Group Name for the CR (eg. a CR of Kind acds.mrp.viasat, has a group name mrp.viasat)
        :param version: Version of the CR (eg. an apiVersion of mrp.viasat/v1alpha1 has a version v1alpha1)
        :param plural: Plural of the Kind (eg. if Kind is Acd, plural is acds)
        :param primary_cr: True if this is the primary CR for the target (eg. an acd CR is the primary for ACD)
        :param optional: True if this CR is not required for the controller
        :param data: A kubernetes custom resource dictionary containing all of the fields
                    for the custom resource definition as well as all of the custom resource data
        """
        self.name = name
        self.namespace = namespace
        self.group_name = group_name
        self.version = version
        self.plural = plural
        self.primary_cr = primary_cr
        self.optional = optional
        self.data = data


class CMData:
    """
    CMData - Data for the Config Map
    """

    def __init__(self,
                 name: str,
                 filename: str,
                 namespace: str,
                 data_current: Optional[kubernetes.client.V1ConfigMap] = None,
                 data_desired: Optional[kubernetes.client.V1ConfigMap] = None):
        """
        Constructor for the Config Map class
        :param name: Name of the config map
        :param filename: Filename (key in config map) for the data
        :param namespace: Namespace for the config map
        :param data_current: Current state of the config map
        :param data_desired: Desired state of the config map
        """
        self.name = name
        self.filename = filename
        self.namespace = namespace
        self.data_current = data_current
        self.data_desired = data_desired


class CtrlJob:
    """
    CtrlJob - Data for launching the controller job
    """

    def __init__(self,
                 name: str,
                 namespace: str,
                 image: str,
                 pull_policy: str,
                 pod_name: str,
                 job_name: str,
                 command: List[str],
                 service_account: str = ""):
        """
        Constructor for the Controller Job class
        :param name: Name of the controller container
        :param namespace: Namespace of the controller job
        :param image: Container image for the controller
        :param pull_policy: Pull policy for the job (eg. Always, IfNotPresent, Never)
        :param pod_name: Name of the pod running the controller
        :param job_name: Name of the controller job
        :param command: Command used when the container starts up as List of str
        :param service_account: Service account for the pod ("" if outside of cluster)
        """
        self.name = name
        self.namespace = namespace
        self.image = image
        self.pull_policy = pull_policy
        self.pod_name = pod_name
        self.job_name = job_name
        self.command = command
        self.service_account = service_account


class DeployData:
    """
    DeployData - Deployment information used by the controller to launch the
                target application
    """

    def __init__(self,
                 name: str,
                 namespace: str,
                 container_name: str,
                 container_image: str,
                 env: List[kubernetes.client.V1EnvVar],
                 ports: List[kubernetes.client.V1ContainerPort],
                 volumes: List[kubernetes.client.V1Volume],
                 volume_mounts: List[kubernetes.client.V1VolumeMount],
                 deployment_replicas: int = 1,
                 pod_service_account: str = "",
                 data: Optional[kubernetes.client.V1Deployment] = None):
        """
        Constructor for the Deploy Data class
        :param name: Name of the deployment
        :param namespace: Namespace of the deployment
        :param container_name: Name of the container
        :param container_image: Container image name
        :param env: List of environment variables
        :param ports: List of ports for the container
        :param volumes: List of volumes (eg. config maps)
        :param volume_mounts: List of volume mounts (where config map mounted)
        :param deployment_replicas: Replicas of target process (typically 1)
        :param pod_service_account: Pod Service account
        :param data:
        """
        self.name = name
        self.namespace = namespace
        self.container_name = container_name
        self.container_image = container_image
        self.env = env
        self.ports = ports
        self.volumes = volumes
        self.volume_mounts = volume_mounts
        self.deployment_replicas = deployment_replicas
        self.pod_service_account = pod_service_account
        self.data = data


class ServiceData:
    """
    ServiceData - Information for any services associated with the deployment
    """

    def __init__(self,
                 name: str,
                 namespace: str,
                 service_type: str,
                 ports: List[kubernetes.client.V1ServicePort],
                 selector: Dict[str, str]):
        """
        Constructor for the Service Data class
        :param name: Name of the service
        :param namespace: Namespace of the service
        :param service_type: Type of service (eg. NodePort, ClusterIP, ...)
        :param ports: List of V1ServicePorts for the service
        :param selector: Selector for the service (which pod uses service)
        """
        self.name = name
        self.namespace = namespace
        self.service_type = service_type
        self.ports = ports
        self.selector = selector


class ControllerData:
    """
    ControllerData - All of the data for a single controller
    """

    def __init__(self,
                 name: str,
                 input_cr: List[CRData],
                 output_cm: List[CMData],
                 controller_job: CtrlJob,
                 deployments: List[DeployData],
                 services: List[ServiceData],
                 is_active: bool = False):
        """
        Constructor for the ControllerData class
        :param name: Name of the controller (eg. "sla", "acd", "wmgr"...)
        :param input_cr: List of input Custom Resources
        :param output_cm: list of output Config Maps
        :param controller_job: Info needed to launch the controller job
        :param deployments: List of deployments to start in the controller job
        :param services: List of Services needed by the target process
        :param is_active: True if primary CR is available and target running
        """
        self.name: str = name
        self.input_cr: List[CRData] = input_cr
        self.output_cm: List[CMData] = output_cm
        self.controller_job: CtrlJob = controller_job
        self.deployments: List[DeployData] = deployments
        self.services: List[ServiceData] = services
        self.is_active = is_active  # controller is not active till the primary cr is created

    def get_cr_by_plural(self, cr_plural: str) -> Optional[CRData]:
        """
        get_cr_by_plural - Get a custom resource by the plural name of CRD
        :param cr_plural: Custom Resource plural name
        :return: The custom resource, or None if not available
        """
        for custom_resource in self.input_cr:
            if custom_resource.plural == cr_plural:
                return custom_resource

        return None

    def get_cm_by_name(self, cm_name: str) -> Optional[CMData]:
        """
        get_cm_by_name - Get a config map by name
        :param cm_name: Config Map name
        :return: A config map, or None if not available
        """
        for config_map in self.output_cm:
            if config_map.name == cm_name:
                return config_map

        return None

    def get_deploy_by_name(self, deploy_name) -> Optional[DeployData]:
        """
        get_deploy_by_name - Get a deployment by name
        :param deploy_name: name of deployment to retrieve
        :return: Deployment, or None if not available
        """
        for deploy in self.deployments:
            if deploy.name == deploy_name:
                return deploy

        return None
