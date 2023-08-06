'''
# cdk-eks-karpenter

This construct configures the necessary dependencies and installs [Karpenter](https://karpenter.sh)
on an EKS cluster managed by AWS CDK.

## Prerequisites

### Usage with EC2 Spot Capacity

If you have not used EC2 spot in your AWS account before, follow the instructions
[here](https://karpenter.sh/v0.6.3/getting-started/#create-the-ec2-spot-service-linked-role) to create
the service linked role in your account allowing Karpenter to provision EC2 Spot Capacity.

## Using

In your CDK project, initialize a new Karpenter construct for your EKS cluster, like this:

```python
const cluster = new Cluster(this, 'testCluster', {
  vpc: vpc,
  role: clusterRole,
  version: KubernetesVersion.V1_21,
  defaultCapacity: 1
});

const karpenter = new Karpenter(this, 'Karpenter', {
  cluster: cluster
});
```

This will install and configure Karpenter in your cluster. To have Karpenter do something useful, you
also need to create a [provisioner for AWS](https://karpenter.sh/v0.6.3/aws/provisioning/). You can
do that from CDK using `addProvisioner()`, similar to the example below:

```python
karpenter.addProvisioner('spot-provisioner', {
  requirements: [{
    key: 'karpenter.sh/capacity-type',
    operator: 'In',
    values: ['spot']
  }],
  limits: {
    resources: {
      cpu: 20
    }
  },
  provider: {
    subnetSelector: {
      Name: 'PublicSubnet*'
    },
    securityGroupSelector: {
      'aws:eks:cluster-name': cluster.clusterName
    }
  }
});
```

## Known issues

### Versions earlier than v0.6.1 fails to install

As of [aws/karpenter#1145](https://github.com/aws/karpenter/pull/1145) the Karpenter Helm chart is
refactored to specify `clusterEndpoint` and `clusterName` on the root level of the chart values, previously
these values was specified under the key `controller`.

## Testing

This construct adds a custom task to [projen](https://projen.io/), so you can test a full deployment
of an EKS cluster with Karpenter installed as specified in `test/integ.karpenter.ts` by running the
following:

```sh
export CDK_DEFAULT_REGION=<aws region>
export CDK_DEFAULT_ACCOUNT=<account id>
npx projen test:deploy
```

As the above will create a cluster without EC2 capacity, with CoreDNS and Karpenter running as Fargate
pods, you can test out the functionality of Karpenter by deploying an inflation deployment, which will
spin up a number of pods that will trigger Karpenter creation of worker nodes:

```sh
kubectl apply -f test/inflater-deployment.yml
```

You can clean things up by deleting the deployment and the CDK test stack:

```sh
kubectl delete -f test/inflater-deployment.yml
npx projen test:destroy
```

## FAQ

### I'm not able to launch spot instances

1. Ensure you have the appropriate linked role available in your account, for more details,
   see [the karpenter documentation](https://karpenter.sh/v0.6.3/getting-started/#create-the-ec2-spot-service-linked-role)
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_eks
import aws_cdk.aws_iam
import constructs


class Karpenter(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-eks-karpenter.Karpenter",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster: aws_cdk.aws_eks.Cluster,
        namespace: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cluster: The EKS Cluster to attach to.
        :param namespace: The Kubernetes namespace to install to. Default: karpenter
        :param version: The helm chart version to install. Default: - latest
        '''
        props = KarpenterProps(cluster=cluster, namespace=namespace, version=version)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addProvisioner")
    def add_provisioner(
        self,
        id: builtins.str,
        provisioner_spec: typing.Mapping[builtins.str, typing.Any],
    ) -> None:
        '''addProvisioner adds a provisioner manifest to the cluster.

        Currently the provisioner spec
        parameter is relatively free form.

        :param id: - must consist of lower case alphanumeric characters, '-' or '.', and must start and end with an alphanumeric character.
        :param provisioner_spec: - spec of Karpenters Provisioner object.
        '''
        return typing.cast(None, jsii.invoke(self, "addProvisioner", [id, provisioner_spec]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> aws_cdk.aws_eks.Cluster:
        return typing.cast(aws_cdk.aws_eks.Cluster, jsii.get(self, "cluster"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nodeRole")
    def node_role(self) -> aws_cdk.aws_iam.Role:
        return typing.cast(aws_cdk.aws_iam.Role, jsii.get(self, "nodeRole"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="version")
    def version(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "version"))


@jsii.data_type(
    jsii_type="cdk-eks-karpenter.KarpenterProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster": "cluster",
        "namespace": "namespace",
        "version": "version",
    },
)
class KarpenterProps:
    def __init__(
        self,
        *,
        cluster: aws_cdk.aws_eks.Cluster,
        namespace: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cluster: The EKS Cluster to attach to.
        :param namespace: The Kubernetes namespace to install to. Default: karpenter
        :param version: The helm chart version to install. Default: - latest
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "cluster": cluster,
        }
        if namespace is not None:
            self._values["namespace"] = namespace
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def cluster(self) -> aws_cdk.aws_eks.Cluster:
        '''The EKS Cluster to attach to.'''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(aws_cdk.aws_eks.Cluster, result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The Kubernetes namespace to install to.

        :default: karpenter
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''The helm chart version to install.

        :default: - latest
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KarpenterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Karpenter",
    "KarpenterProps",
]

publication.publish()
