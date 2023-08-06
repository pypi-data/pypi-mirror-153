import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import cdktf
import constructs


class AgentToken(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="buildkite_buildkite.AgentToken",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/buildkite/r/agent_token buildkite_agent_token}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/buildkite/r/agent_token buildkite_agent_token} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/agent_token#description AgentToken#description}.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = AgentTokenConfig(
            description=description,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="token")
    def token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "token"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="uuid")
    def uuid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uuid"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)


@jsii.data_type(
    jsii_type="buildkite_buildkite.AgentTokenConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "description": "description",
    },
)
class AgentTokenConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/agent_token#description AgentToken#description}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/agent_token#description AgentToken#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AgentTokenConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BuildkiteProvider(
    cdktf.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="buildkite_buildkite.BuildkiteProvider",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/buildkite buildkite}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        api_token: builtins.str,
        organization: builtins.str,
        alias: typing.Optional[builtins.str] = None,
        graphql_url: typing.Optional[builtins.str] = None,
        rest_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/buildkite buildkite} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param api_token: API token with GraphQL access and ``write_pipelines, read_pipelines`` scopes. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite#api_token BuildkiteProvider#api_token}
        :param organization: The Buildkite organization ID. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite#organization BuildkiteProvider#organization}
        :param alias: Alias name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite#alias BuildkiteProvider#alias}
        :param graphql_url: Base URL for the GraphQL API to use. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite#graphql_url BuildkiteProvider#graphql_url}
        :param rest_url: Base URL for the REST API to use. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite#rest_url BuildkiteProvider#rest_url}
        '''
        config = BuildkiteProviderConfig(
            api_token=api_token,
            organization=organization,
            alias=alias,
            graphql_url=graphql_url,
            rest_url=rest_url,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="resetGraphqlUrl")
    def reset_graphql_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGraphqlUrl", []))

    @jsii.member(jsii_name="resetRestUrl")
    def reset_rest_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestUrl", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="apiTokenInput")
    def api_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiTokenInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="graphqlUrlInput")
    def graphql_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "graphqlUrlInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="restUrlInput")
    def rest_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "restUrlInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "alias", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="apiToken")
    def api_token(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiToken"))

    @api_token.setter
    def api_token(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "apiToken", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="graphqlUrl")
    def graphql_url(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "graphqlUrl"))

    @graphql_url.setter
    def graphql_url(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "graphqlUrl", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organization")
    def organization(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "organization", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="restUrl")
    def rest_url(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "restUrl"))

    @rest_url.setter
    def rest_url(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "restUrl", value)


@jsii.data_type(
    jsii_type="buildkite_buildkite.BuildkiteProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "api_token": "apiToken",
        "organization": "organization",
        "alias": "alias",
        "graphql_url": "graphqlUrl",
        "rest_url": "restUrl",
    },
)
class BuildkiteProviderConfig:
    def __init__(
        self,
        *,
        api_token: builtins.str,
        organization: builtins.str,
        alias: typing.Optional[builtins.str] = None,
        graphql_url: typing.Optional[builtins.str] = None,
        rest_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param api_token: API token with GraphQL access and ``write_pipelines, read_pipelines`` scopes. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite#api_token BuildkiteProvider#api_token}
        :param organization: The Buildkite organization ID. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite#organization BuildkiteProvider#organization}
        :param alias: Alias name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite#alias BuildkiteProvider#alias}
        :param graphql_url: Base URL for the GraphQL API to use. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite#graphql_url BuildkiteProvider#graphql_url}
        :param rest_url: Base URL for the REST API to use. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite#rest_url BuildkiteProvider#rest_url}
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "api_token": api_token,
            "organization": organization,
        }
        if alias is not None:
            self._values["alias"] = alias
        if graphql_url is not None:
            self._values["graphql_url"] = graphql_url
        if rest_url is not None:
            self._values["rest_url"] = rest_url

    @builtins.property
    def api_token(self) -> builtins.str:
        '''API token with GraphQL access and ``write_pipelines, read_pipelines`` scopes.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite#api_token BuildkiteProvider#api_token}
        '''
        result = self._values.get("api_token")
        assert result is not None, "Required property 'api_token' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def organization(self) -> builtins.str:
        '''The Buildkite organization ID.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite#organization BuildkiteProvider#organization}
        '''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite#alias BuildkiteProvider#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def graphql_url(self) -> typing.Optional[builtins.str]:
        '''Base URL for the GraphQL API to use.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite#graphql_url BuildkiteProvider#graphql_url}
        '''
        result = self._values.get("graphql_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rest_url(self) -> typing.Optional[builtins.str]:
        '''Base URL for the REST API to use.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite#rest_url BuildkiteProvider#rest_url}
        '''
        result = self._values.get("rest_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BuildkiteProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataBuildkiteMeta(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="buildkite_buildkite.DataBuildkiteMeta",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/buildkite/d/meta buildkite_meta}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/buildkite/d/meta buildkite_meta} Data Source.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = DataBuildkiteMetaConfig(
            count=count, depends_on=depends_on, lifecycle=lifecycle, provider=provider
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="webhookIps")
    def webhook_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "webhookIps"))


@jsii.data_type(
    jsii_type="buildkite_buildkite.DataBuildkiteMetaConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
    },
)
class DataBuildkiteMetaConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataBuildkiteMetaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataBuildkitePipeline(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="buildkite_buildkite.DataBuildkitePipeline",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/buildkite/d/pipeline buildkite_pipeline}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        slug: builtins.str,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/buildkite/d/pipeline buildkite_pipeline} Data Source.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param slug: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/d/pipeline#slug DataBuildkitePipeline#slug}.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = DataBuildkitePipelineConfig(
            slug=slug,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="defaultBranch")
    def default_branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultBranch"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="webhookUrl")
    def webhook_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webhookUrl"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="slugInput")
    def slug_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "slugInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="slug")
    def slug(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "slug"))

    @slug.setter
    def slug(self, value: builtins.str) -> None:
        jsii.set(self, "slug", value)


@jsii.data_type(
    jsii_type="buildkite_buildkite.DataBuildkitePipelineConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "slug": "slug",
    },
)
class DataBuildkitePipelineConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        slug: builtins.str,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param slug: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/d/pipeline#slug DataBuildkitePipeline#slug}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "slug": slug,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def slug(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/d/pipeline#slug DataBuildkitePipeline#slug}.'''
        result = self._values.get("slug")
        assert result is not None, "Required property 'slug' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataBuildkitePipelineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataBuildkiteTeam(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="buildkite_buildkite.DataBuildkiteTeam",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/buildkite/d/team buildkite_team}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        slug: builtins.str,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/buildkite/d/team buildkite_team} Data Source.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param slug: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/d/team#slug DataBuildkiteTeam#slug}.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = DataBuildkiteTeamConfig(
            slug=slug,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="defaultMemberRole")
    def default_member_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultMemberRole"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="defaultTeam")
    def default_team(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "defaultTeam"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="membersCanCreatePipelines")
    def members_can_create_pipelines(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "membersCanCreatePipelines"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="privacy")
    def privacy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privacy"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="uuid")
    def uuid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uuid"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="slugInput")
    def slug_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "slugInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="slug")
    def slug(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "slug"))

    @slug.setter
    def slug(self, value: builtins.str) -> None:
        jsii.set(self, "slug", value)


@jsii.data_type(
    jsii_type="buildkite_buildkite.DataBuildkiteTeamConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "slug": "slug",
    },
)
class DataBuildkiteTeamConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        slug: builtins.str,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param slug: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/d/team#slug DataBuildkiteTeam#slug}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "slug": slug,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def slug(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/d/team#slug DataBuildkiteTeam#slug}.'''
        result = self._values.get("slug")
        assert result is not None, "Required property 'slug' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataBuildkiteTeamConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Pipeline(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="buildkite_buildkite.Pipeline",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline buildkite_pipeline}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        repository: builtins.str,
        steps: builtins.str,
        allow_rebuilds: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        branch_configuration: typing.Optional[builtins.str] = None,
        cancel_intermediate_builds: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        cancel_intermediate_builds_branch_filter: typing.Optional[builtins.str] = None,
        cluster_id: typing.Optional[builtins.str] = None,
        default_branch: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        provider_settings: typing.Optional["PipelineProviderSettings"] = None,
        skip_intermediate_builds: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        skip_intermediate_builds_branch_filter: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        team: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence["PipelineTeam"]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline buildkite_pipeline} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#name Pipeline#name}.
        :param repository: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#repository Pipeline#repository}.
        :param steps: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#steps Pipeline#steps}.
        :param allow_rebuilds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#allow_rebuilds Pipeline#allow_rebuilds}.
        :param branch_configuration: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#branch_configuration Pipeline#branch_configuration}.
        :param cancel_intermediate_builds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#cancel_intermediate_builds Pipeline#cancel_intermediate_builds}.
        :param cancel_intermediate_builds_branch_filter: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#cancel_intermediate_builds_branch_filter Pipeline#cancel_intermediate_builds_branch_filter}.
        :param cluster_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#cluster_id Pipeline#cluster_id}.
        :param default_branch: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#default_branch Pipeline#default_branch}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#description Pipeline#description}.
        :param provider_settings: provider_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#provider_settings Pipeline#provider_settings}
        :param skip_intermediate_builds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#skip_intermediate_builds Pipeline#skip_intermediate_builds}.
        :param skip_intermediate_builds_branch_filter: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#skip_intermediate_builds_branch_filter Pipeline#skip_intermediate_builds_branch_filter}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#tags Pipeline#tags}.
        :param team: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#team Pipeline#team}.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = PipelineConfig(
            name=name,
            repository=repository,
            steps=steps,
            allow_rebuilds=allow_rebuilds,
            branch_configuration=branch_configuration,
            cancel_intermediate_builds=cancel_intermediate_builds,
            cancel_intermediate_builds_branch_filter=cancel_intermediate_builds_branch_filter,
            cluster_id=cluster_id,
            default_branch=default_branch,
            description=description,
            provider_settings=provider_settings,
            skip_intermediate_builds=skip_intermediate_builds,
            skip_intermediate_builds_branch_filter=skip_intermediate_builds_branch_filter,
            tags=tags,
            team=team,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="putProviderSettings")
    def put_provider_settings(
        self,
        *,
        build_branches: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        build_pull_request_forks: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        build_pull_request_labels_changed: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        build_pull_request_ready_for_review: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        build_pull_requests: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        build_tags: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        cancel_deleted_branch_builds: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        filter_condition: typing.Optional[builtins.str] = None,
        filter_enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        prefix_pull_request_fork_branch_names: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        publish_blocked_as_pending: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        publish_commit_status: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        publish_commit_status_per_step: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        pull_request_branch_filter_configuration: typing.Optional[builtins.str] = None,
        pull_request_branch_filter_enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        separate_pull_request_statuses: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        skip_pull_request_builds_for_existing_commits: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        trigger_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param build_branches: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#build_branches Pipeline#build_branches}.
        :param build_pull_request_forks: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#build_pull_request_forks Pipeline#build_pull_request_forks}.
        :param build_pull_request_labels_changed: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#build_pull_request_labels_changed Pipeline#build_pull_request_labels_changed}.
        :param build_pull_request_ready_for_review: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#build_pull_request_ready_for_review Pipeline#build_pull_request_ready_for_review}.
        :param build_pull_requests: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#build_pull_requests Pipeline#build_pull_requests}.
        :param build_tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#build_tags Pipeline#build_tags}.
        :param cancel_deleted_branch_builds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#cancel_deleted_branch_builds Pipeline#cancel_deleted_branch_builds}.
        :param filter_condition: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#filter_condition Pipeline#filter_condition}.
        :param filter_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#filter_enabled Pipeline#filter_enabled}.
        :param prefix_pull_request_fork_branch_names: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#prefix_pull_request_fork_branch_names Pipeline#prefix_pull_request_fork_branch_names}.
        :param publish_blocked_as_pending: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#publish_blocked_as_pending Pipeline#publish_blocked_as_pending}.
        :param publish_commit_status: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#publish_commit_status Pipeline#publish_commit_status}.
        :param publish_commit_status_per_step: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#publish_commit_status_per_step Pipeline#publish_commit_status_per_step}.
        :param pull_request_branch_filter_configuration: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#pull_request_branch_filter_configuration Pipeline#pull_request_branch_filter_configuration}.
        :param pull_request_branch_filter_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#pull_request_branch_filter_enabled Pipeline#pull_request_branch_filter_enabled}.
        :param separate_pull_request_statuses: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#separate_pull_request_statuses Pipeline#separate_pull_request_statuses}.
        :param skip_pull_request_builds_for_existing_commits: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#skip_pull_request_builds_for_existing_commits Pipeline#skip_pull_request_builds_for_existing_commits}.
        :param trigger_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#trigger_mode Pipeline#trigger_mode}.
        '''
        value = PipelineProviderSettings(
            build_branches=build_branches,
            build_pull_request_forks=build_pull_request_forks,
            build_pull_request_labels_changed=build_pull_request_labels_changed,
            build_pull_request_ready_for_review=build_pull_request_ready_for_review,
            build_pull_requests=build_pull_requests,
            build_tags=build_tags,
            cancel_deleted_branch_builds=cancel_deleted_branch_builds,
            filter_condition=filter_condition,
            filter_enabled=filter_enabled,
            prefix_pull_request_fork_branch_names=prefix_pull_request_fork_branch_names,
            publish_blocked_as_pending=publish_blocked_as_pending,
            publish_commit_status=publish_commit_status,
            publish_commit_status_per_step=publish_commit_status_per_step,
            pull_request_branch_filter_configuration=pull_request_branch_filter_configuration,
            pull_request_branch_filter_enabled=pull_request_branch_filter_enabled,
            separate_pull_request_statuses=separate_pull_request_statuses,
            skip_pull_request_builds_for_existing_commits=skip_pull_request_builds_for_existing_commits,
            trigger_mode=trigger_mode,
        )

        return typing.cast(None, jsii.invoke(self, "putProviderSettings", [value]))

    @jsii.member(jsii_name="resetAllowRebuilds")
    def reset_allow_rebuilds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowRebuilds", []))

    @jsii.member(jsii_name="resetBranchConfiguration")
    def reset_branch_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBranchConfiguration", []))

    @jsii.member(jsii_name="resetCancelIntermediateBuilds")
    def reset_cancel_intermediate_builds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCancelIntermediateBuilds", []))

    @jsii.member(jsii_name="resetCancelIntermediateBuildsBranchFilter")
    def reset_cancel_intermediate_builds_branch_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCancelIntermediateBuildsBranchFilter", []))

    @jsii.member(jsii_name="resetClusterId")
    def reset_cluster_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterId", []))

    @jsii.member(jsii_name="resetDefaultBranch")
    def reset_default_branch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultBranch", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetProviderSettings")
    def reset_provider_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProviderSettings", []))

    @jsii.member(jsii_name="resetSkipIntermediateBuilds")
    def reset_skip_intermediate_builds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipIntermediateBuilds", []))

    @jsii.member(jsii_name="resetSkipIntermediateBuildsBranchFilter")
    def reset_skip_intermediate_builds_branch_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipIntermediateBuildsBranchFilter", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTeam")
    def reset_team(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTeam", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="badgeUrl")
    def badge_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "badgeUrl"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="providerSettings")
    def provider_settings(self) -> "PipelineProviderSettingsOutputReference":
        return typing.cast("PipelineProviderSettingsOutputReference", jsii.get(self, "providerSettings"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="slug")
    def slug(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "slug"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="webhookUrl")
    def webhook_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webhookUrl"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="allowRebuildsInput")
    def allow_rebuilds_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "allowRebuildsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="branchConfigurationInput")
    def branch_configuration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "branchConfigurationInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cancelIntermediateBuildsBranchFilterInput")
    def cancel_intermediate_builds_branch_filter_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cancelIntermediateBuildsBranchFilterInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cancelIntermediateBuildsInput")
    def cancel_intermediate_builds_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "cancelIntermediateBuildsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterIdInput")
    def cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="defaultBranchInput")
    def default_branch_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultBranchInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="providerSettingsInput")
    def provider_settings_input(self) -> typing.Optional["PipelineProviderSettings"]:
        return typing.cast(typing.Optional["PipelineProviderSettings"], jsii.get(self, "providerSettingsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="repositoryInput")
    def repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="skipIntermediateBuildsBranchFilterInput")
    def skip_intermediate_builds_branch_filter_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "skipIntermediateBuildsBranchFilterInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="skipIntermediateBuildsInput")
    def skip_intermediate_builds_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "skipIntermediateBuildsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="stepsInput")
    def steps_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stepsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="teamInput")
    def team_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["PipelineTeam"]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["PipelineTeam"]]], jsii.get(self, "teamInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="allowRebuilds")
    def allow_rebuilds(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "allowRebuilds"))

    @allow_rebuilds.setter
    def allow_rebuilds(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "allowRebuilds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="branchConfiguration")
    def branch_configuration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "branchConfiguration"))

    @branch_configuration.setter
    def branch_configuration(self, value: builtins.str) -> None:
        jsii.set(self, "branchConfiguration", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cancelIntermediateBuilds")
    def cancel_intermediate_builds(
        self,
    ) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "cancelIntermediateBuilds"))

    @cancel_intermediate_builds.setter
    def cancel_intermediate_builds(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "cancelIntermediateBuilds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cancelIntermediateBuildsBranchFilter")
    def cancel_intermediate_builds_branch_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cancelIntermediateBuildsBranchFilter"))

    @cancel_intermediate_builds_branch_filter.setter
    def cancel_intermediate_builds_branch_filter(self, value: builtins.str) -> None:
        jsii.set(self, "cancelIntermediateBuildsBranchFilter", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @cluster_id.setter
    def cluster_id(self, value: builtins.str) -> None:
        jsii.set(self, "clusterId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="defaultBranch")
    def default_branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultBranch"))

    @default_branch.setter
    def default_branch(self, value: builtins.str) -> None:
        jsii.set(self, "defaultBranch", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        jsii.set(self, "repository", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="skipIntermediateBuilds")
    def skip_intermediate_builds(
        self,
    ) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "skipIntermediateBuilds"))

    @skip_intermediate_builds.setter
    def skip_intermediate_builds(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "skipIntermediateBuilds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="skipIntermediateBuildsBranchFilter")
    def skip_intermediate_builds_branch_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "skipIntermediateBuildsBranchFilter"))

    @skip_intermediate_builds_branch_filter.setter
    def skip_intermediate_builds_branch_filter(self, value: builtins.str) -> None:
        jsii.set(self, "skipIntermediateBuildsBranchFilter", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="steps")
    def steps(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "steps"))

    @steps.setter
    def steps(self, value: builtins.str) -> None:
        jsii.set(self, "steps", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "tags", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="team")
    def team(self) -> typing.Union[cdktf.IResolvable, typing.List["PipelineTeam"]]:
        return typing.cast(typing.Union[cdktf.IResolvable, typing.List["PipelineTeam"]], jsii.get(self, "team"))

    @team.setter
    def team(
        self,
        value: typing.Union[cdktf.IResolvable, typing.List["PipelineTeam"]],
    ) -> None:
        jsii.set(self, "team", value)


@jsii.data_type(
    jsii_type="buildkite_buildkite.PipelineConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "name": "name",
        "repository": "repository",
        "steps": "steps",
        "allow_rebuilds": "allowRebuilds",
        "branch_configuration": "branchConfiguration",
        "cancel_intermediate_builds": "cancelIntermediateBuilds",
        "cancel_intermediate_builds_branch_filter": "cancelIntermediateBuildsBranchFilter",
        "cluster_id": "clusterId",
        "default_branch": "defaultBranch",
        "description": "description",
        "provider_settings": "providerSettings",
        "skip_intermediate_builds": "skipIntermediateBuilds",
        "skip_intermediate_builds_branch_filter": "skipIntermediateBuildsBranchFilter",
        "tags": "tags",
        "team": "team",
    },
)
class PipelineConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        name: builtins.str,
        repository: builtins.str,
        steps: builtins.str,
        allow_rebuilds: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        branch_configuration: typing.Optional[builtins.str] = None,
        cancel_intermediate_builds: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        cancel_intermediate_builds_branch_filter: typing.Optional[builtins.str] = None,
        cluster_id: typing.Optional[builtins.str] = None,
        default_branch: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        provider_settings: typing.Optional["PipelineProviderSettings"] = None,
        skip_intermediate_builds: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        skip_intermediate_builds_branch_filter: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        team: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence["PipelineTeam"]]] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#name Pipeline#name}.
        :param repository: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#repository Pipeline#repository}.
        :param steps: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#steps Pipeline#steps}.
        :param allow_rebuilds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#allow_rebuilds Pipeline#allow_rebuilds}.
        :param branch_configuration: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#branch_configuration Pipeline#branch_configuration}.
        :param cancel_intermediate_builds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#cancel_intermediate_builds Pipeline#cancel_intermediate_builds}.
        :param cancel_intermediate_builds_branch_filter: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#cancel_intermediate_builds_branch_filter Pipeline#cancel_intermediate_builds_branch_filter}.
        :param cluster_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#cluster_id Pipeline#cluster_id}.
        :param default_branch: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#default_branch Pipeline#default_branch}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#description Pipeline#description}.
        :param provider_settings: provider_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#provider_settings Pipeline#provider_settings}
        :param skip_intermediate_builds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#skip_intermediate_builds Pipeline#skip_intermediate_builds}.
        :param skip_intermediate_builds_branch_filter: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#skip_intermediate_builds_branch_filter Pipeline#skip_intermediate_builds_branch_filter}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#tags Pipeline#tags}.
        :param team: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#team Pipeline#team}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(provider_settings, dict):
            provider_settings = PipelineProviderSettings(**provider_settings)
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "repository": repository,
            "steps": steps,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if allow_rebuilds is not None:
            self._values["allow_rebuilds"] = allow_rebuilds
        if branch_configuration is not None:
            self._values["branch_configuration"] = branch_configuration
        if cancel_intermediate_builds is not None:
            self._values["cancel_intermediate_builds"] = cancel_intermediate_builds
        if cancel_intermediate_builds_branch_filter is not None:
            self._values["cancel_intermediate_builds_branch_filter"] = cancel_intermediate_builds_branch_filter
        if cluster_id is not None:
            self._values["cluster_id"] = cluster_id
        if default_branch is not None:
            self._values["default_branch"] = default_branch
        if description is not None:
            self._values["description"] = description
        if provider_settings is not None:
            self._values["provider_settings"] = provider_settings
        if skip_intermediate_builds is not None:
            self._values["skip_intermediate_builds"] = skip_intermediate_builds
        if skip_intermediate_builds_branch_filter is not None:
            self._values["skip_intermediate_builds_branch_filter"] = skip_intermediate_builds_branch_filter
        if tags is not None:
            self._values["tags"] = tags
        if team is not None:
            self._values["team"] = team

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#name Pipeline#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#repository Pipeline#repository}.'''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def steps(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#steps Pipeline#steps}.'''
        result = self._values.get("steps")
        assert result is not None, "Required property 'steps' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_rebuilds(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#allow_rebuilds Pipeline#allow_rebuilds}.'''
        result = self._values.get("allow_rebuilds")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def branch_configuration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#branch_configuration Pipeline#branch_configuration}.'''
        result = self._values.get("branch_configuration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cancel_intermediate_builds(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#cancel_intermediate_builds Pipeline#cancel_intermediate_builds}.'''
        result = self._values.get("cancel_intermediate_builds")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def cancel_intermediate_builds_branch_filter(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#cancel_intermediate_builds_branch_filter Pipeline#cancel_intermediate_builds_branch_filter}.'''
        result = self._values.get("cancel_intermediate_builds_branch_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#cluster_id Pipeline#cluster_id}.'''
        result = self._values.get("cluster_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_branch(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#default_branch Pipeline#default_branch}.'''
        result = self._values.get("default_branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#description Pipeline#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provider_settings(self) -> typing.Optional["PipelineProviderSettings"]:
        '''provider_settings block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#provider_settings Pipeline#provider_settings}
        '''
        result = self._values.get("provider_settings")
        return typing.cast(typing.Optional["PipelineProviderSettings"], result)

    @builtins.property
    def skip_intermediate_builds(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#skip_intermediate_builds Pipeline#skip_intermediate_builds}.'''
        result = self._values.get("skip_intermediate_builds")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def skip_intermediate_builds_branch_filter(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#skip_intermediate_builds_branch_filter Pipeline#skip_intermediate_builds_branch_filter}.'''
        result = self._values.get("skip_intermediate_builds_branch_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#tags Pipeline#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def team(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["PipelineTeam"]]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#team Pipeline#team}.'''
        result = self._values.get("team")
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["PipelineTeam"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipelineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="buildkite_buildkite.PipelineProviderSettings",
    jsii_struct_bases=[],
    name_mapping={
        "build_branches": "buildBranches",
        "build_pull_request_forks": "buildPullRequestForks",
        "build_pull_request_labels_changed": "buildPullRequestLabelsChanged",
        "build_pull_request_ready_for_review": "buildPullRequestReadyForReview",
        "build_pull_requests": "buildPullRequests",
        "build_tags": "buildTags",
        "cancel_deleted_branch_builds": "cancelDeletedBranchBuilds",
        "filter_condition": "filterCondition",
        "filter_enabled": "filterEnabled",
        "prefix_pull_request_fork_branch_names": "prefixPullRequestForkBranchNames",
        "publish_blocked_as_pending": "publishBlockedAsPending",
        "publish_commit_status": "publishCommitStatus",
        "publish_commit_status_per_step": "publishCommitStatusPerStep",
        "pull_request_branch_filter_configuration": "pullRequestBranchFilterConfiguration",
        "pull_request_branch_filter_enabled": "pullRequestBranchFilterEnabled",
        "separate_pull_request_statuses": "separatePullRequestStatuses",
        "skip_pull_request_builds_for_existing_commits": "skipPullRequestBuildsForExistingCommits",
        "trigger_mode": "triggerMode",
    },
)
class PipelineProviderSettings:
    def __init__(
        self,
        *,
        build_branches: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        build_pull_request_forks: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        build_pull_request_labels_changed: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        build_pull_request_ready_for_review: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        build_pull_requests: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        build_tags: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        cancel_deleted_branch_builds: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        filter_condition: typing.Optional[builtins.str] = None,
        filter_enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        prefix_pull_request_fork_branch_names: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        publish_blocked_as_pending: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        publish_commit_status: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        publish_commit_status_per_step: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        pull_request_branch_filter_configuration: typing.Optional[builtins.str] = None,
        pull_request_branch_filter_enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        separate_pull_request_statuses: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        skip_pull_request_builds_for_existing_commits: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        trigger_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param build_branches: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#build_branches Pipeline#build_branches}.
        :param build_pull_request_forks: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#build_pull_request_forks Pipeline#build_pull_request_forks}.
        :param build_pull_request_labels_changed: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#build_pull_request_labels_changed Pipeline#build_pull_request_labels_changed}.
        :param build_pull_request_ready_for_review: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#build_pull_request_ready_for_review Pipeline#build_pull_request_ready_for_review}.
        :param build_pull_requests: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#build_pull_requests Pipeline#build_pull_requests}.
        :param build_tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#build_tags Pipeline#build_tags}.
        :param cancel_deleted_branch_builds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#cancel_deleted_branch_builds Pipeline#cancel_deleted_branch_builds}.
        :param filter_condition: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#filter_condition Pipeline#filter_condition}.
        :param filter_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#filter_enabled Pipeline#filter_enabled}.
        :param prefix_pull_request_fork_branch_names: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#prefix_pull_request_fork_branch_names Pipeline#prefix_pull_request_fork_branch_names}.
        :param publish_blocked_as_pending: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#publish_blocked_as_pending Pipeline#publish_blocked_as_pending}.
        :param publish_commit_status: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#publish_commit_status Pipeline#publish_commit_status}.
        :param publish_commit_status_per_step: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#publish_commit_status_per_step Pipeline#publish_commit_status_per_step}.
        :param pull_request_branch_filter_configuration: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#pull_request_branch_filter_configuration Pipeline#pull_request_branch_filter_configuration}.
        :param pull_request_branch_filter_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#pull_request_branch_filter_enabled Pipeline#pull_request_branch_filter_enabled}.
        :param separate_pull_request_statuses: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#separate_pull_request_statuses Pipeline#separate_pull_request_statuses}.
        :param skip_pull_request_builds_for_existing_commits: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#skip_pull_request_builds_for_existing_commits Pipeline#skip_pull_request_builds_for_existing_commits}.
        :param trigger_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#trigger_mode Pipeline#trigger_mode}.
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if build_branches is not None:
            self._values["build_branches"] = build_branches
        if build_pull_request_forks is not None:
            self._values["build_pull_request_forks"] = build_pull_request_forks
        if build_pull_request_labels_changed is not None:
            self._values["build_pull_request_labels_changed"] = build_pull_request_labels_changed
        if build_pull_request_ready_for_review is not None:
            self._values["build_pull_request_ready_for_review"] = build_pull_request_ready_for_review
        if build_pull_requests is not None:
            self._values["build_pull_requests"] = build_pull_requests
        if build_tags is not None:
            self._values["build_tags"] = build_tags
        if cancel_deleted_branch_builds is not None:
            self._values["cancel_deleted_branch_builds"] = cancel_deleted_branch_builds
        if filter_condition is not None:
            self._values["filter_condition"] = filter_condition
        if filter_enabled is not None:
            self._values["filter_enabled"] = filter_enabled
        if prefix_pull_request_fork_branch_names is not None:
            self._values["prefix_pull_request_fork_branch_names"] = prefix_pull_request_fork_branch_names
        if publish_blocked_as_pending is not None:
            self._values["publish_blocked_as_pending"] = publish_blocked_as_pending
        if publish_commit_status is not None:
            self._values["publish_commit_status"] = publish_commit_status
        if publish_commit_status_per_step is not None:
            self._values["publish_commit_status_per_step"] = publish_commit_status_per_step
        if pull_request_branch_filter_configuration is not None:
            self._values["pull_request_branch_filter_configuration"] = pull_request_branch_filter_configuration
        if pull_request_branch_filter_enabled is not None:
            self._values["pull_request_branch_filter_enabled"] = pull_request_branch_filter_enabled
        if separate_pull_request_statuses is not None:
            self._values["separate_pull_request_statuses"] = separate_pull_request_statuses
        if skip_pull_request_builds_for_existing_commits is not None:
            self._values["skip_pull_request_builds_for_existing_commits"] = skip_pull_request_builds_for_existing_commits
        if trigger_mode is not None:
            self._values["trigger_mode"] = trigger_mode

    @builtins.property
    def build_branches(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#build_branches Pipeline#build_branches}.'''
        result = self._values.get("build_branches")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def build_pull_request_forks(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#build_pull_request_forks Pipeline#build_pull_request_forks}.'''
        result = self._values.get("build_pull_request_forks")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def build_pull_request_labels_changed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#build_pull_request_labels_changed Pipeline#build_pull_request_labels_changed}.'''
        result = self._values.get("build_pull_request_labels_changed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def build_pull_request_ready_for_review(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#build_pull_request_ready_for_review Pipeline#build_pull_request_ready_for_review}.'''
        result = self._values.get("build_pull_request_ready_for_review")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def build_pull_requests(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#build_pull_requests Pipeline#build_pull_requests}.'''
        result = self._values.get("build_pull_requests")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def build_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#build_tags Pipeline#build_tags}.'''
        result = self._values.get("build_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def cancel_deleted_branch_builds(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#cancel_deleted_branch_builds Pipeline#cancel_deleted_branch_builds}.'''
        result = self._values.get("cancel_deleted_branch_builds")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def filter_condition(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#filter_condition Pipeline#filter_condition}.'''
        result = self._values.get("filter_condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#filter_enabled Pipeline#filter_enabled}.'''
        result = self._values.get("filter_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def prefix_pull_request_fork_branch_names(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#prefix_pull_request_fork_branch_names Pipeline#prefix_pull_request_fork_branch_names}.'''
        result = self._values.get("prefix_pull_request_fork_branch_names")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def publish_blocked_as_pending(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#publish_blocked_as_pending Pipeline#publish_blocked_as_pending}.'''
        result = self._values.get("publish_blocked_as_pending")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def publish_commit_status(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#publish_commit_status Pipeline#publish_commit_status}.'''
        result = self._values.get("publish_commit_status")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def publish_commit_status_per_step(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#publish_commit_status_per_step Pipeline#publish_commit_status_per_step}.'''
        result = self._values.get("publish_commit_status_per_step")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def pull_request_branch_filter_configuration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#pull_request_branch_filter_configuration Pipeline#pull_request_branch_filter_configuration}.'''
        result = self._values.get("pull_request_branch_filter_configuration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pull_request_branch_filter_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#pull_request_branch_filter_enabled Pipeline#pull_request_branch_filter_enabled}.'''
        result = self._values.get("pull_request_branch_filter_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def separate_pull_request_statuses(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#separate_pull_request_statuses Pipeline#separate_pull_request_statuses}.'''
        result = self._values.get("separate_pull_request_statuses")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def skip_pull_request_builds_for_existing_commits(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#skip_pull_request_builds_for_existing_commits Pipeline#skip_pull_request_builds_for_existing_commits}.'''
        result = self._values.get("skip_pull_request_builds_for_existing_commits")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def trigger_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#trigger_mode Pipeline#trigger_mode}.'''
        result = self._values.get("trigger_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipelineProviderSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipelineProviderSettingsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="buildkite_buildkite.PipelineProviderSettingsOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBuildBranches")
    def reset_build_branches(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildBranches", []))

    @jsii.member(jsii_name="resetBuildPullRequestForks")
    def reset_build_pull_request_forks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildPullRequestForks", []))

    @jsii.member(jsii_name="resetBuildPullRequestLabelsChanged")
    def reset_build_pull_request_labels_changed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildPullRequestLabelsChanged", []))

    @jsii.member(jsii_name="resetBuildPullRequestReadyForReview")
    def reset_build_pull_request_ready_for_review(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildPullRequestReadyForReview", []))

    @jsii.member(jsii_name="resetBuildPullRequests")
    def reset_build_pull_requests(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildPullRequests", []))

    @jsii.member(jsii_name="resetBuildTags")
    def reset_build_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildTags", []))

    @jsii.member(jsii_name="resetCancelDeletedBranchBuilds")
    def reset_cancel_deleted_branch_builds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCancelDeletedBranchBuilds", []))

    @jsii.member(jsii_name="resetFilterCondition")
    def reset_filter_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterCondition", []))

    @jsii.member(jsii_name="resetFilterEnabled")
    def reset_filter_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterEnabled", []))

    @jsii.member(jsii_name="resetPrefixPullRequestForkBranchNames")
    def reset_prefix_pull_request_fork_branch_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefixPullRequestForkBranchNames", []))

    @jsii.member(jsii_name="resetPublishBlockedAsPending")
    def reset_publish_blocked_as_pending(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublishBlockedAsPending", []))

    @jsii.member(jsii_name="resetPublishCommitStatus")
    def reset_publish_commit_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublishCommitStatus", []))

    @jsii.member(jsii_name="resetPublishCommitStatusPerStep")
    def reset_publish_commit_status_per_step(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublishCommitStatusPerStep", []))

    @jsii.member(jsii_name="resetPullRequestBranchFilterConfiguration")
    def reset_pull_request_branch_filter_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPullRequestBranchFilterConfiguration", []))

    @jsii.member(jsii_name="resetPullRequestBranchFilterEnabled")
    def reset_pull_request_branch_filter_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPullRequestBranchFilterEnabled", []))

    @jsii.member(jsii_name="resetSeparatePullRequestStatuses")
    def reset_separate_pull_request_statuses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeparatePullRequestStatuses", []))

    @jsii.member(jsii_name="resetSkipPullRequestBuildsForExistingCommits")
    def reset_skip_pull_request_builds_for_existing_commits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipPullRequestBuildsForExistingCommits", []))

    @jsii.member(jsii_name="resetTriggerMode")
    def reset_trigger_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTriggerMode", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="buildBranchesInput")
    def build_branches_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "buildBranchesInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="buildPullRequestForksInput")
    def build_pull_request_forks_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "buildPullRequestForksInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="buildPullRequestLabelsChangedInput")
    def build_pull_request_labels_changed_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "buildPullRequestLabelsChangedInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="buildPullRequestReadyForReviewInput")
    def build_pull_request_ready_for_review_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "buildPullRequestReadyForReviewInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="buildPullRequestsInput")
    def build_pull_requests_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "buildPullRequestsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="buildTagsInput")
    def build_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "buildTagsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cancelDeletedBranchBuildsInput")
    def cancel_deleted_branch_builds_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "cancelDeletedBranchBuildsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="filterConditionInput")
    def filter_condition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterConditionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="filterEnabledInput")
    def filter_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "filterEnabledInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="prefixPullRequestForkBranchNamesInput")
    def prefix_pull_request_fork_branch_names_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "prefixPullRequestForkBranchNamesInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="publishBlockedAsPendingInput")
    def publish_blocked_as_pending_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "publishBlockedAsPendingInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="publishCommitStatusInput")
    def publish_commit_status_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "publishCommitStatusInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="publishCommitStatusPerStepInput")
    def publish_commit_status_per_step_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "publishCommitStatusPerStepInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="pullRequestBranchFilterConfigurationInput")
    def pull_request_branch_filter_configuration_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pullRequestBranchFilterConfigurationInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="pullRequestBranchFilterEnabledInput")
    def pull_request_branch_filter_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "pullRequestBranchFilterEnabledInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="separatePullRequestStatusesInput")
    def separate_pull_request_statuses_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "separatePullRequestStatusesInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="skipPullRequestBuildsForExistingCommitsInput")
    def skip_pull_request_builds_for_existing_commits_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "skipPullRequestBuildsForExistingCommitsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="triggerModeInput")
    def trigger_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "triggerModeInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="buildBranches")
    def build_branches(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "buildBranches"))

    @build_branches.setter
    def build_branches(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "buildBranches", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="buildPullRequestForks")
    def build_pull_request_forks(
        self,
    ) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "buildPullRequestForks"))

    @build_pull_request_forks.setter
    def build_pull_request_forks(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "buildPullRequestForks", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="buildPullRequestLabelsChanged")
    def build_pull_request_labels_changed(
        self,
    ) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "buildPullRequestLabelsChanged"))

    @build_pull_request_labels_changed.setter
    def build_pull_request_labels_changed(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "buildPullRequestLabelsChanged", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="buildPullRequestReadyForReview")
    def build_pull_request_ready_for_review(
        self,
    ) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "buildPullRequestReadyForReview"))

    @build_pull_request_ready_for_review.setter
    def build_pull_request_ready_for_review(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "buildPullRequestReadyForReview", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="buildPullRequests")
    def build_pull_requests(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "buildPullRequests"))

    @build_pull_requests.setter
    def build_pull_requests(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "buildPullRequests", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="buildTags")
    def build_tags(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "buildTags"))

    @build_tags.setter
    def build_tags(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        jsii.set(self, "buildTags", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cancelDeletedBranchBuilds")
    def cancel_deleted_branch_builds(
        self,
    ) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "cancelDeletedBranchBuilds"))

    @cancel_deleted_branch_builds.setter
    def cancel_deleted_branch_builds(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "cancelDeletedBranchBuilds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="filterCondition")
    def filter_condition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filterCondition"))

    @filter_condition.setter
    def filter_condition(self, value: builtins.str) -> None:
        jsii.set(self, "filterCondition", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="filterEnabled")
    def filter_enabled(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "filterEnabled"))

    @filter_enabled.setter
    def filter_enabled(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "filterEnabled", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="prefixPullRequestForkBranchNames")
    def prefix_pull_request_fork_branch_names(
        self,
    ) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "prefixPullRequestForkBranchNames"))

    @prefix_pull_request_fork_branch_names.setter
    def prefix_pull_request_fork_branch_names(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "prefixPullRequestForkBranchNames", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="publishBlockedAsPending")
    def publish_blocked_as_pending(
        self,
    ) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "publishBlockedAsPending"))

    @publish_blocked_as_pending.setter
    def publish_blocked_as_pending(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "publishBlockedAsPending", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="publishCommitStatus")
    def publish_commit_status(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "publishCommitStatus"))

    @publish_commit_status.setter
    def publish_commit_status(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "publishCommitStatus", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="publishCommitStatusPerStep")
    def publish_commit_status_per_step(
        self,
    ) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "publishCommitStatusPerStep"))

    @publish_commit_status_per_step.setter
    def publish_commit_status_per_step(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "publishCommitStatusPerStep", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="pullRequestBranchFilterConfiguration")
    def pull_request_branch_filter_configuration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pullRequestBranchFilterConfiguration"))

    @pull_request_branch_filter_configuration.setter
    def pull_request_branch_filter_configuration(self, value: builtins.str) -> None:
        jsii.set(self, "pullRequestBranchFilterConfiguration", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="pullRequestBranchFilterEnabled")
    def pull_request_branch_filter_enabled(
        self,
    ) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "pullRequestBranchFilterEnabled"))

    @pull_request_branch_filter_enabled.setter
    def pull_request_branch_filter_enabled(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "pullRequestBranchFilterEnabled", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="separatePullRequestStatuses")
    def separate_pull_request_statuses(
        self,
    ) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "separatePullRequestStatuses"))

    @separate_pull_request_statuses.setter
    def separate_pull_request_statuses(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "separatePullRequestStatuses", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="skipPullRequestBuildsForExistingCommits")
    def skip_pull_request_builds_for_existing_commits(
        self,
    ) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "skipPullRequestBuildsForExistingCommits"))

    @skip_pull_request_builds_for_existing_commits.setter
    def skip_pull_request_builds_for_existing_commits(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "skipPullRequestBuildsForExistingCommits", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="triggerMode")
    def trigger_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "triggerMode"))

    @trigger_mode.setter
    def trigger_mode(self, value: builtins.str) -> None:
        jsii.set(self, "triggerMode", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PipelineProviderSettings]:
        return typing.cast(typing.Optional[PipelineProviderSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[PipelineProviderSettings]) -> None:
        jsii.set(self, "internalValue", value)


class PipelineSchedule(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="buildkite_buildkite.PipelineSchedule",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline_schedule buildkite_pipeline_schedule}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        branch: builtins.str,
        cronline: builtins.str,
        label: builtins.str,
        pipeline_id: builtins.str,
        commit: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        message: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline_schedule buildkite_pipeline_schedule} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param branch: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline_schedule#branch PipelineSchedule#branch}.
        :param cronline: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline_schedule#cronline PipelineSchedule#cronline}.
        :param label: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline_schedule#label PipelineSchedule#label}.
        :param pipeline_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline_schedule#pipeline_id PipelineSchedule#pipeline_id}.
        :param commit: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline_schedule#commit PipelineSchedule#commit}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline_schedule#enabled PipelineSchedule#enabled}.
        :param env: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline_schedule#env PipelineSchedule#env}.
        :param message: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline_schedule#message PipelineSchedule#message}.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = PipelineScheduleConfig(
            branch=branch,
            cronline=cronline,
            label=label,
            pipeline_id=pipeline_id,
            commit=commit,
            enabled=enabled,
            env=env,
            message=message,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetCommit")
    def reset_commit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommit", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetEnv")
    def reset_env(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnv", []))

    @jsii.member(jsii_name="resetMessage")
    def reset_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessage", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="uuid")
    def uuid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uuid"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="branchInput")
    def branch_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "branchInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="commitInput")
    def commit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commitInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cronlineInput")
    def cronline_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cronlineInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="envInput")
    def env_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "envInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="labelInput")
    def label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labelInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="messageInput")
    def message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="pipelineIdInput")
    def pipeline_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pipelineIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="branch")
    def branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "branch"))

    @branch.setter
    def branch(self, value: builtins.str) -> None:
        jsii.set(self, "branch", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="commit")
    def commit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commit"))

    @commit.setter
    def commit(self, value: builtins.str) -> None:
        jsii.set(self, "commit", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cronline")
    def cronline(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cronline"))

    @cronline.setter
    def cronline(self, value: builtins.str) -> None:
        jsii.set(self, "cronline", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        jsii.set(self, "enabled", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="env")
    def env(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "env"))

    @env.setter
    def env(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        jsii.set(self, "env", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "label"))

    @label.setter
    def label(self, value: builtins.str) -> None:
        jsii.set(self, "label", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @message.setter
    def message(self, value: builtins.str) -> None:
        jsii.set(self, "message", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="pipelineId")
    def pipeline_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pipelineId"))

    @pipeline_id.setter
    def pipeline_id(self, value: builtins.str) -> None:
        jsii.set(self, "pipelineId", value)


@jsii.data_type(
    jsii_type="buildkite_buildkite.PipelineScheduleConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "branch": "branch",
        "cronline": "cronline",
        "label": "label",
        "pipeline_id": "pipelineId",
        "commit": "commit",
        "enabled": "enabled",
        "env": "env",
        "message": "message",
    },
)
class PipelineScheduleConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        branch: builtins.str,
        cronline: builtins.str,
        label: builtins.str,
        pipeline_id: builtins.str,
        commit: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        message: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param branch: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline_schedule#branch PipelineSchedule#branch}.
        :param cronline: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline_schedule#cronline PipelineSchedule#cronline}.
        :param label: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline_schedule#label PipelineSchedule#label}.
        :param pipeline_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline_schedule#pipeline_id PipelineSchedule#pipeline_id}.
        :param commit: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline_schedule#commit PipelineSchedule#commit}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline_schedule#enabled PipelineSchedule#enabled}.
        :param env: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline_schedule#env PipelineSchedule#env}.
        :param message: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline_schedule#message PipelineSchedule#message}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "branch": branch,
            "cronline": cronline,
            "label": label,
            "pipeline_id": pipeline_id,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if commit is not None:
            self._values["commit"] = commit
        if enabled is not None:
            self._values["enabled"] = enabled
        if env is not None:
            self._values["env"] = env
        if message is not None:
            self._values["message"] = message

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def branch(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline_schedule#branch PipelineSchedule#branch}.'''
        result = self._values.get("branch")
        assert result is not None, "Required property 'branch' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cronline(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline_schedule#cronline PipelineSchedule#cronline}.'''
        result = self._values.get("cronline")
        assert result is not None, "Required property 'cronline' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def label(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline_schedule#label PipelineSchedule#label}.'''
        result = self._values.get("label")
        assert result is not None, "Required property 'label' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pipeline_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline_schedule#pipeline_id PipelineSchedule#pipeline_id}.'''
        result = self._values.get("pipeline_id")
        assert result is not None, "Required property 'pipeline_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def commit(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline_schedule#commit PipelineSchedule#commit}.'''
        result = self._values.get("commit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline_schedule#enabled PipelineSchedule#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline_schedule#env PipelineSchedule#env}.'''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline_schedule#message PipelineSchedule#message}.'''
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipelineScheduleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="buildkite_buildkite.PipelineTeam",
    jsii_struct_bases=[],
    name_mapping={"access_level": "accessLevel", "slug": "slug"},
)
class PipelineTeam:
    def __init__(
        self,
        *,
        access_level: typing.Optional[builtins.str] = None,
        slug: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_level: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#access_level Pipeline#access_level}.
        :param slug: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#slug Pipeline#slug}.
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if access_level is not None:
            self._values["access_level"] = access_level
        if slug is not None:
            self._values["slug"] = slug

    @builtins.property
    def access_level(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#access_level Pipeline#access_level}.'''
        result = self._values.get("access_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def slug(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/pipeline#slug Pipeline#slug}.'''
        result = self._values.get("slug")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipelineTeam(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Team(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="buildkite_buildkite.Team",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/buildkite/r/team buildkite_team}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        default_member_role: builtins.str,
        default_team: typing.Union[builtins.bool, cdktf.IResolvable],
        name: builtins.str,
        privacy: builtins.str,
        description: typing.Optional[builtins.str] = None,
        members_can_create_pipelines: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/buildkite/r/team buildkite_team} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param default_member_role: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/team#default_member_role Team#default_member_role}.
        :param default_team: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/team#default_team Team#default_team}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/team#name Team#name}.
        :param privacy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/team#privacy Team#privacy}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/team#description Team#description}.
        :param members_can_create_pipelines: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/team#members_can_create_pipelines Team#members_can_create_pipelines}.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = TeamConfig(
            default_member_role=default_member_role,
            default_team=default_team,
            name=name,
            privacy=privacy,
            description=description,
            members_can_create_pipelines=members_can_create_pipelines,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetMembersCanCreatePipelines")
    def reset_members_can_create_pipelines(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMembersCanCreatePipelines", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="slug")
    def slug(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "slug"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="uuid")
    def uuid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uuid"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="defaultMemberRoleInput")
    def default_member_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultMemberRoleInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="defaultTeamInput")
    def default_team_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "defaultTeamInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="membersCanCreatePipelinesInput")
    def members_can_create_pipelines_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "membersCanCreatePipelinesInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="privacyInput")
    def privacy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privacyInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="defaultMemberRole")
    def default_member_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultMemberRole"))

    @default_member_role.setter
    def default_member_role(self, value: builtins.str) -> None:
        jsii.set(self, "defaultMemberRole", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="defaultTeam")
    def default_team(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "defaultTeam"))

    @default_team.setter
    def default_team(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "defaultTeam", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="membersCanCreatePipelines")
    def members_can_create_pipelines(
        self,
    ) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "membersCanCreatePipelines"))

    @members_can_create_pipelines.setter
    def members_can_create_pipelines(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "membersCanCreatePipelines", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="privacy")
    def privacy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privacy"))

    @privacy.setter
    def privacy(self, value: builtins.str) -> None:
        jsii.set(self, "privacy", value)


@jsii.data_type(
    jsii_type="buildkite_buildkite.TeamConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "default_member_role": "defaultMemberRole",
        "default_team": "defaultTeam",
        "name": "name",
        "privacy": "privacy",
        "description": "description",
        "members_can_create_pipelines": "membersCanCreatePipelines",
    },
)
class TeamConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        default_member_role: builtins.str,
        default_team: typing.Union[builtins.bool, cdktf.IResolvable],
        name: builtins.str,
        privacy: builtins.str,
        description: typing.Optional[builtins.str] = None,
        members_can_create_pipelines: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param default_member_role: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/team#default_member_role Team#default_member_role}.
        :param default_team: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/team#default_team Team#default_team}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/team#name Team#name}.
        :param privacy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/team#privacy Team#privacy}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/team#description Team#description}.
        :param members_can_create_pipelines: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/team#members_can_create_pipelines Team#members_can_create_pipelines}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "default_member_role": default_member_role,
            "default_team": default_team,
            "name": name,
            "privacy": privacy,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if description is not None:
            self._values["description"] = description
        if members_can_create_pipelines is not None:
            self._values["members_can_create_pipelines"] = members_can_create_pipelines

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def default_member_role(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/team#default_member_role Team#default_member_role}.'''
        result = self._values.get("default_member_role")
        assert result is not None, "Required property 'default_member_role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_team(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/team#default_team Team#default_team}.'''
        result = self._values.get("default_team")
        assert result is not None, "Required property 'default_team' is missing"
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/team#name Team#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def privacy(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/team#privacy Team#privacy}.'''
        result = self._values.get("privacy")
        assert result is not None, "Required property 'privacy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/team#description Team#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def members_can_create_pipelines(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/team#members_can_create_pipelines Team#members_can_create_pipelines}.'''
        result = self._values.get("members_can_create_pipelines")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TeamMember(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="buildkite_buildkite.TeamMember",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/buildkite/r/team_member buildkite_team_member}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        role: builtins.str,
        team_id: builtins.str,
        user_id: builtins.str,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/buildkite/r/team_member buildkite_team_member} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param role: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/team_member#role TeamMember#role}.
        :param team_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/team_member#team_id TeamMember#team_id}.
        :param user_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/team_member#user_id TeamMember#user_id}.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = TeamMemberConfig(
            role=role,
            team_id=team_id,
            user_id=user_id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="uuid")
    def uuid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uuid"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="roleInput")
    def role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="teamIdInput")
    def team_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "teamIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="userIdInput")
    def user_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @role.setter
    def role(self, value: builtins.str) -> None:
        jsii.set(self, "role", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="teamId")
    def team_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "teamId"))

    @team_id.setter
    def team_id(self, value: builtins.str) -> None:
        jsii.set(self, "teamId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="userId")
    def user_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userId"))

    @user_id.setter
    def user_id(self, value: builtins.str) -> None:
        jsii.set(self, "userId", value)


@jsii.data_type(
    jsii_type="buildkite_buildkite.TeamMemberConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "role": "role",
        "team_id": "teamId",
        "user_id": "userId",
    },
)
class TeamMemberConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        role: builtins.str,
        team_id: builtins.str,
        user_id: builtins.str,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param role: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/team_member#role TeamMember#role}.
        :param team_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/team_member#team_id TeamMember#team_id}.
        :param user_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/team_member#user_id TeamMember#user_id}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "role": role,
            "team_id": team_id,
            "user_id": user_id,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def role(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/team_member#role TeamMember#role}.'''
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def team_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/team_member#team_id TeamMember#team_id}.'''
        result = self._values.get("team_id")
        assert result is not None, "Required property 'team_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/buildkite/r/team_member#user_id TeamMember#user_id}.'''
        result = self._values.get("user_id")
        assert result is not None, "Required property 'user_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamMemberConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AgentToken",
    "AgentTokenConfig",
    "BuildkiteProvider",
    "BuildkiteProviderConfig",
    "DataBuildkiteMeta",
    "DataBuildkiteMetaConfig",
    "DataBuildkitePipeline",
    "DataBuildkitePipelineConfig",
    "DataBuildkiteTeam",
    "DataBuildkiteTeamConfig",
    "Pipeline",
    "PipelineConfig",
    "PipelineProviderSettings",
    "PipelineProviderSettingsOutputReference",
    "PipelineSchedule",
    "PipelineScheduleConfig",
    "PipelineTeam",
    "Team",
    "TeamConfig",
    "TeamMember",
    "TeamMemberConfig",
]

publication.publish()
