'''
The static-website module is able to deploy your pre-packaged static website content into an S3 Bucket, fronted by Cloudfront. This module uses an Origin Access Identity to ensure your Bucket can only be accessed via Cloudfront and is configured to only allow HTTPS requests by default. Custom runtime configurations can also be specified which will emit a runtime-config.json file along with your website content. Typically this includes resource Arns, Id's etc which may need to be referenced from your website. This package uses sane defaults and at a minimum only requires the path to your website assets.

Below is a conceptual view of the default architecture this module creates:

```
Cloudfront Distribution (HTTPS only) -> S3 Bucket (Private via OAI)
|_ WAF V2 ACL                                |_ index.html (+ other website files and assets)
                                             |_ runtime-config.json
```
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

import aws_cdk.aws_certificatemanager
import aws_cdk.aws_cloudfront
import aws_cdk.aws_s3
import aws_cdk.aws_s3_deployment
import constructs


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/static-website.CloudFrontWebAclProps",
    jsii_struct_bases=[],
    name_mapping={"managed_rules": "managedRules"},
)
class CloudFrontWebAclProps:
    def __init__(self, *, managed_rules: typing.Sequence["ManagedRule"]) -> None:
        '''(experimental) Properties to configure the web acl.

        :param managed_rules: (experimental) List of managed rules to apply to the web acl.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "managed_rules": managed_rules,
        }

    @builtins.property
    def managed_rules(self) -> typing.List["ManagedRule"]:
        '''(experimental) List of managed rules to apply to the web acl.

        :stability: experimental
        '''
        result = self._values.get("managed_rules")
        assert result is not None, "Required property 'managed_rules' is missing"
        return typing.cast(typing.List["ManagedRule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudFrontWebAclProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/static-website.CloudfrontDomainOptions",
    jsii_struct_bases=[],
    name_mapping={"certificate": "certificate", "domain_names": "domainNames"},
)
class CloudfrontDomainOptions:
    def __init__(
        self,
        *,
        certificate: aws_cdk.aws_certificatemanager.ICertificate,
        domain_names: typing.Sequence[builtins.str],
    ) -> None:
        '''(experimental) Configuration related to using custom domain names/certificates in Cloudfront.

        :param certificate: (experimental) A certificate to associate with the distribution. The certificate must be located in N. Virginia (us-east-1). Default: - the CloudFront wildcard certificate (*.cloudfront.net) will be used.
        :param domain_names: (experimental) Alternative domain names for this distribution. If you want to use your own domain name, such as www.example.com, instead of the cloudfront.net domain name, you can add an alternate domain name to your distribution. If you attach a certificate to the distribution, you must add (at least one of) the domain names of the certificate to this list. Default: - The distribution will only support the default generated name (e.g., d111111abcdef8.cloudfront.net)

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "certificate": certificate,
            "domain_names": domain_names,
        }

    @builtins.property
    def certificate(self) -> aws_cdk.aws_certificatemanager.ICertificate:
        '''(experimental) A certificate to associate with the distribution.

        The certificate must be located in N. Virginia (us-east-1).

        :default: - the CloudFront wildcard certificate (*.cloudfront.net) will be used.

        :stability: experimental
        '''
        result = self._values.get("certificate")
        assert result is not None, "Required property 'certificate' is missing"
        return typing.cast(aws_cdk.aws_certificatemanager.ICertificate, result)

    @builtins.property
    def domain_names(self) -> typing.List[builtins.str]:
        '''(experimental) Alternative domain names for this distribution.

        If you want to use your own domain name, such as www.example.com, instead of the cloudfront.net domain name,
        you can add an alternate domain name to your distribution. If you attach a certificate to the distribution,
        you must add (at least one of) the domain names of the certificate to this list.

        :default: - The distribution will only support the default generated name (e.g., d111111abcdef8.cloudfront.net)

        :stability: experimental
        '''
        result = self._values.get("domain_names")
        assert result is not None, "Required property 'domain_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDomainOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/static-website.CloudfrontLoggingOptions",
    jsii_struct_bases=[],
    name_mapping={
        "enable_logging": "enableLogging",
        "log_bucket": "logBucket",
        "log_file_prefix": "logFilePrefix",
        "log_includes_cookies": "logIncludesCookies",
    },
)
class CloudfrontLoggingOptions:
    def __init__(
        self,
        *,
        enable_logging: typing.Optional[builtins.bool] = None,
        log_bucket: typing.Optional[aws_cdk.aws_s3.IBucket] = None,
        log_file_prefix: typing.Optional[builtins.str] = None,
        log_includes_cookies: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Configuration related to Cloudfront Logging.

        :param enable_logging: (experimental) Enable access logging for the distribution. Default: - false, unless ``logBucket`` is specified.
        :param log_bucket: (experimental) The Amazon S3 bucket to store the access logs in. Default: - A bucket is created if ``enableLogging`` is true
        :param log_file_prefix: (experimental) An optional string that you want CloudFront to prefix to the access log filenames for this distribution. Default: - no prefix
        :param log_includes_cookies: (experimental) Specifies whether you want CloudFront to include cookies in access logs. Default: false

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if enable_logging is not None:
            self._values["enable_logging"] = enable_logging
        if log_bucket is not None:
            self._values["log_bucket"] = log_bucket
        if log_file_prefix is not None:
            self._values["log_file_prefix"] = log_file_prefix
        if log_includes_cookies is not None:
            self._values["log_includes_cookies"] = log_includes_cookies

    @builtins.property
    def enable_logging(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable access logging for the distribution.

        :default: - false, unless ``logBucket`` is specified.

        :stability: experimental
        '''
        result = self._values.get("enable_logging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def log_bucket(self) -> typing.Optional[aws_cdk.aws_s3.IBucket]:
        '''(experimental) The Amazon S3 bucket to store the access logs in.

        :default: - A bucket is created if ``enableLogging`` is true

        :stability: experimental
        '''
        result = self._values.get("log_bucket")
        return typing.cast(typing.Optional[aws_cdk.aws_s3.IBucket], result)

    @builtins.property
    def log_file_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) An optional string that you want CloudFront to prefix to the access log filenames for this distribution.

        :default: - no prefix

        :stability: experimental
        '''
        result = self._values.get("log_file_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_includes_cookies(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether you want CloudFront to include cookies in access logs.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("log_includes_cookies")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontLoggingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontWebAcl(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/static-website.CloudfrontWebAcl",
):
    '''(experimental) This construct creates a WAFv2 Web ACL for cloudfront in the us-east-1 region (required for cloudfront) no matter the region of the parent cdk stack.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        managed_rules: typing.Sequence["ManagedRule"],
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param managed_rules: (experimental) List of managed rules to apply to the web acl.

        :stability: experimental
        '''
        props = CloudFrontWebAclProps(managed_rules=managed_rules)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="webAclArn")
    def web_acl_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "webAclArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="webAclId")
    def web_acl_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "webAclId"))


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/static-website.ManagedRule",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "vendor": "vendor"},
)
class ManagedRule:
    def __init__(self, *, name: builtins.str, vendor: builtins.str) -> None:
        '''(experimental) Represents a WAF V2 managed rule.

        :param name: (experimental) The name of the managed rule group. You use this, along with the vendor name, to identify the rule group.
        :param vendor: (experimental) The name of the managed rule group vendor. You use this, along with the rule group name, to identify the rule group.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "vendor": vendor,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The name of the managed rule group.

        You use this, along with the vendor name, to identify the rule group.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vendor(self) -> builtins.str:
        '''(experimental) The name of the managed rule group vendor.

        You use this, along with the rule group name, to identify the rule group.

        :stability: experimental
        '''
        result = self._values.get("vendor")
        assert result is not None, "Required property 'vendor' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagedRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/static-website.OriginBehaviourOptions",
    jsii_struct_bases=[aws_cdk.aws_cloudfront.AddBehaviorOptions],
    name_mapping={
        "allowed_methods": "allowedMethods",
        "cached_methods": "cachedMethods",
        "cache_policy": "cachePolicy",
        "compress": "compress",
        "edge_lambdas": "edgeLambdas",
        "function_associations": "functionAssociations",
        "origin_request_policy": "originRequestPolicy",
        "response_headers_policy": "responseHeadersPolicy",
        "smooth_streaming": "smoothStreaming",
        "trusted_key_groups": "trustedKeyGroups",
        "viewer_protocol_policy": "viewerProtocolPolicy",
    },
)
class OriginBehaviourOptions(aws_cdk.aws_cloudfront.AddBehaviorOptions):
    def __init__(
        self,
        *,
        allowed_methods: typing.Optional[aws_cdk.aws_cloudfront.AllowedMethods] = None,
        cached_methods: typing.Optional[aws_cdk.aws_cloudfront.CachedMethods] = None,
        cache_policy: typing.Optional[aws_cdk.aws_cloudfront.ICachePolicy] = None,
        compress: typing.Optional[builtins.bool] = None,
        edge_lambdas: typing.Optional[typing.Sequence[aws_cdk.aws_cloudfront.EdgeLambda]] = None,
        function_associations: typing.Optional[typing.Sequence[aws_cdk.aws_cloudfront.FunctionAssociation]] = None,
        origin_request_policy: typing.Optional[aws_cdk.aws_cloudfront.IOriginRequestPolicy] = None,
        response_headers_policy: typing.Optional[aws_cdk.aws_cloudfront.IResponseHeadersPolicy] = None,
        smooth_streaming: typing.Optional[builtins.bool] = None,
        trusted_key_groups: typing.Optional[typing.Sequence[aws_cdk.aws_cloudfront.IKeyGroup]] = None,
        viewer_protocol_policy: typing.Optional[aws_cdk.aws_cloudfront.ViewerProtocolPolicy] = None,
    ) -> None:
        '''(experimental) Options for configuring the default origin behavior.

        :param allowed_methods: HTTP methods to allow for this behavior. Default: AllowedMethods.ALLOW_GET_HEAD
        :param cached_methods: HTTP methods to cache for this behavior. Default: CachedMethods.CACHE_GET_HEAD
        :param cache_policy: The cache policy for this behavior. The cache policy determines what values are included in the cache key, and the time-to-live (TTL) values for the cache. Default: CachePolicy.CACHING_OPTIMIZED
        :param compress: Whether you want CloudFront to automatically compress certain files for this cache behavior. See https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/ServingCompressedFiles.html#compressed-content-cloudfront-file-types for file types CloudFront will compress. Default: true
        :param edge_lambdas: The Lambda@Edge functions to invoke before serving the contents. Default: - no Lambda functions will be invoked
        :param function_associations: The CloudFront functions to invoke before serving the contents. Default: - no functions will be invoked
        :param origin_request_policy: The origin request policy for this behavior. The origin request policy determines which values (e.g., headers, cookies) are included in requests that CloudFront sends to the origin. Default: - none
        :param response_headers_policy: The response headers policy for this behavior. The response headers policy determines which headers are included in responses Default: - none
        :param smooth_streaming: Set this to true to indicate you want to distribute media files in the Microsoft Smooth Streaming format using this behavior. Default: false
        :param trusted_key_groups: A list of Key Groups that CloudFront can use to validate signed URLs or signed cookies. Default: - no KeyGroups are associated with cache behavior
        :param viewer_protocol_policy: The protocol that viewers can use to access the files controlled by this behavior. Default: ViewerProtocolPolicy.ALLOW_ALL

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if allowed_methods is not None:
            self._values["allowed_methods"] = allowed_methods
        if cached_methods is not None:
            self._values["cached_methods"] = cached_methods
        if cache_policy is not None:
            self._values["cache_policy"] = cache_policy
        if compress is not None:
            self._values["compress"] = compress
        if edge_lambdas is not None:
            self._values["edge_lambdas"] = edge_lambdas
        if function_associations is not None:
            self._values["function_associations"] = function_associations
        if origin_request_policy is not None:
            self._values["origin_request_policy"] = origin_request_policy
        if response_headers_policy is not None:
            self._values["response_headers_policy"] = response_headers_policy
        if smooth_streaming is not None:
            self._values["smooth_streaming"] = smooth_streaming
        if trusted_key_groups is not None:
            self._values["trusted_key_groups"] = trusted_key_groups
        if viewer_protocol_policy is not None:
            self._values["viewer_protocol_policy"] = viewer_protocol_policy

    @builtins.property
    def allowed_methods(self) -> typing.Optional[aws_cdk.aws_cloudfront.AllowedMethods]:
        '''HTTP methods to allow for this behavior.

        :default: AllowedMethods.ALLOW_GET_HEAD
        '''
        result = self._values.get("allowed_methods")
        return typing.cast(typing.Optional[aws_cdk.aws_cloudfront.AllowedMethods], result)

    @builtins.property
    def cached_methods(self) -> typing.Optional[aws_cdk.aws_cloudfront.CachedMethods]:
        '''HTTP methods to cache for this behavior.

        :default: CachedMethods.CACHE_GET_HEAD
        '''
        result = self._values.get("cached_methods")
        return typing.cast(typing.Optional[aws_cdk.aws_cloudfront.CachedMethods], result)

    @builtins.property
    def cache_policy(self) -> typing.Optional[aws_cdk.aws_cloudfront.ICachePolicy]:
        '''The cache policy for this behavior.

        The cache policy determines what values are included in the cache key,
        and the time-to-live (TTL) values for the cache.

        :default: CachePolicy.CACHING_OPTIMIZED

        :see: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/controlling-the-cache-key.html.
        '''
        result = self._values.get("cache_policy")
        return typing.cast(typing.Optional[aws_cdk.aws_cloudfront.ICachePolicy], result)

    @builtins.property
    def compress(self) -> typing.Optional[builtins.bool]:
        '''Whether you want CloudFront to automatically compress certain files for this cache behavior.

        See https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/ServingCompressedFiles.html#compressed-content-cloudfront-file-types
        for file types CloudFront will compress.

        :default: true
        '''
        result = self._values.get("compress")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def edge_lambdas(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_cloudfront.EdgeLambda]]:
        '''The Lambda@Edge functions to invoke before serving the contents.

        :default: - no Lambda functions will be invoked

        :see: https://aws.amazon.com/lambda/edge
        '''
        result = self._values.get("edge_lambdas")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_cloudfront.EdgeLambda]], result)

    @builtins.property
    def function_associations(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_cloudfront.FunctionAssociation]]:
        '''The CloudFront functions to invoke before serving the contents.

        :default: - no functions will be invoked
        '''
        result = self._values.get("function_associations")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_cloudfront.FunctionAssociation]], result)

    @builtins.property
    def origin_request_policy(
        self,
    ) -> typing.Optional[aws_cdk.aws_cloudfront.IOriginRequestPolicy]:
        '''The origin request policy for this behavior.

        The origin request policy determines which values (e.g., headers, cookies)
        are included in requests that CloudFront sends to the origin.

        :default: - none
        '''
        result = self._values.get("origin_request_policy")
        return typing.cast(typing.Optional[aws_cdk.aws_cloudfront.IOriginRequestPolicy], result)

    @builtins.property
    def response_headers_policy(
        self,
    ) -> typing.Optional[aws_cdk.aws_cloudfront.IResponseHeadersPolicy]:
        '''The response headers policy for this behavior.

        The response headers policy determines which headers are included in responses

        :default: - none
        '''
        result = self._values.get("response_headers_policy")
        return typing.cast(typing.Optional[aws_cdk.aws_cloudfront.IResponseHeadersPolicy], result)

    @builtins.property
    def smooth_streaming(self) -> typing.Optional[builtins.bool]:
        '''Set this to true to indicate you want to distribute media files in the Microsoft Smooth Streaming format using this behavior.

        :default: false
        '''
        result = self._values.get("smooth_streaming")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def trusted_key_groups(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_cloudfront.IKeyGroup]]:
        '''A list of Key Groups that CloudFront can use to validate signed URLs or signed cookies.

        :default: - no KeyGroups are associated with cache behavior

        :see: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/PrivateContent.html
        '''
        result = self._values.get("trusted_key_groups")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_cloudfront.IKeyGroup]], result)

    @builtins.property
    def viewer_protocol_policy(
        self,
    ) -> typing.Optional[aws_cdk.aws_cloudfront.ViewerProtocolPolicy]:
        '''The protocol that viewers can use to access the files controlled by this behavior.

        :default: ViewerProtocolPolicy.ALLOW_ALL
        '''
        result = self._values.get("viewer_protocol_policy")
        return typing.cast(typing.Optional[aws_cdk.aws_cloudfront.ViewerProtocolPolicy], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OriginBehaviourOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/static-website.RuntimeOptions",
    jsii_struct_bases=[],
    name_mapping={"json_payload": "jsonPayload", "json_file_name": "jsonFileName"},
)
class RuntimeOptions:
    def __init__(
        self,
        *,
        json_payload: typing.Any,
        json_file_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Dynamic configuration which gets resolved only during deployment.

        :param json_payload: (experimental) Arbitrary JSON payload containing runtime values to deploy. Typically this contains resourceArns, etc which are only known at deploy time.
        :param json_file_name: (experimental) File name to store runtime configuration (jsonPayload). Must follow pattern: '*.json' Default: "runtime-config.json"

        :stability: experimental

        Example::

            // Will store a JSON file called runtime-config.json in the root of the StaticWebsite S3 bucket containing any
            // and all resolved values.
            const runtimeConfig = {jsonPayload: {bucketArn: s3Bucket.bucketArn}};
            new StaticWebsite(scope, 'StaticWebsite', {websiteContentPath: 'path/to/website', runtimeConfig});
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "json_payload": json_payload,
        }
        if json_file_name is not None:
            self._values["json_file_name"] = json_file_name

    @builtins.property
    def json_payload(self) -> typing.Any:
        '''(experimental) Arbitrary JSON payload containing runtime values to deploy.

        Typically this contains resourceArns, etc which
        are only known at deploy time.

        :stability: experimental

        Example::

            { userPoolId: some.userPool.userPoolId, someResourceArn: some.resource.Arn }
        '''
        result = self._values.get("json_payload")
        assert result is not None, "Required property 'json_payload' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def json_file_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) File name to store runtime configuration (jsonPayload).

        Must follow pattern: '*.json'

        :default: "runtime-config.json"

        :stability: experimental
        '''
        result = self._values.get("json_file_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RuntimeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StaticWebsite(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/static-website.StaticWebsite",
):
    '''(experimental) Deploys a Static Website using a private S3 bucket as an origin and Cloudfront as the entrypoint.

    This construct configures a webAcl containing rules that are generally applicable to web applications. This
    provides protection against exploitation of a wide range of vulnerabilities, including some of the high risk
    and commonly occurring vulnerabilities described in OWASP publications such as OWASP Top 10.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        website_content_path: builtins.str,
        domain_options: typing.Optional[CloudfrontDomainOptions] = None,
        error_responses: typing.Optional[typing.Sequence[aws_cdk.aws_cloudfront.ErrorResponse]] = None,
        logging_options: typing.Optional[CloudfrontLoggingOptions] = None,
        origin_behaviour_options: typing.Optional[OriginBehaviourOptions] = None,
        runtime_options: typing.Optional[RuntimeOptions] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param website_content_path: (experimental) Path to the directory containing the static website files and assets. This directory must contain an index.html file.
        :param domain_options: (experimental) Configuration related to using custom domain names/certificates.
        :param error_responses: (experimental) How CloudFront should handle requests that are not successful (e.g., PageNotFound). Default: - [{httpStatus: 404,responseHttpStatus: 200,responsePagePath: '/index.html'}]
        :param logging_options: (experimental) Configuration related to Cloudfront Logging.
        :param origin_behaviour_options: (experimental) Options for configuring the default origin behavior.
        :param runtime_options: (experimental) Dynamic configuration which gets resolved only during deployment.

        :stability: experimental
        '''
        props = StaticWebsiteProps(
            website_content_path=website_content_path,
            domain_options=domain_options,
            error_responses=error_responses,
            logging_options=logging_options,
            origin_behaviour_options=origin_behaviour_options,
            runtime_options=runtime_options,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucketDeployment")
    def bucket_deployment(self) -> aws_cdk.aws_s3_deployment.BucketDeployment:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_s3_deployment.BucketDeployment, jsii.get(self, "bucketDeployment"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cloudFrontDistribution")
    def cloud_front_distribution(self) -> aws_cdk.aws_cloudfront.Distribution:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_cloudfront.Distribution, jsii.get(self, "cloudFrontDistribution"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="websiteBucket")
    def website_bucket(self) -> aws_cdk.aws_s3.Bucket:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_s3.Bucket, jsii.get(self, "websiteBucket"))


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/static-website.StaticWebsiteProps",
    jsii_struct_bases=[],
    name_mapping={
        "website_content_path": "websiteContentPath",
        "domain_options": "domainOptions",
        "error_responses": "errorResponses",
        "logging_options": "loggingOptions",
        "origin_behaviour_options": "originBehaviourOptions",
        "runtime_options": "runtimeOptions",
    },
)
class StaticWebsiteProps:
    def __init__(
        self,
        *,
        website_content_path: builtins.str,
        domain_options: typing.Optional[CloudfrontDomainOptions] = None,
        error_responses: typing.Optional[typing.Sequence[aws_cdk.aws_cloudfront.ErrorResponse]] = None,
        logging_options: typing.Optional[CloudfrontLoggingOptions] = None,
        origin_behaviour_options: typing.Optional[OriginBehaviourOptions] = None,
        runtime_options: typing.Optional[RuntimeOptions] = None,
    ) -> None:
        '''(experimental) Properties for configuring the StaticWebsite.

        :param website_content_path: (experimental) Path to the directory containing the static website files and assets. This directory must contain an index.html file.
        :param domain_options: (experimental) Configuration related to using custom domain names/certificates.
        :param error_responses: (experimental) How CloudFront should handle requests that are not successful (e.g., PageNotFound). Default: - [{httpStatus: 404,responseHttpStatus: 200,responsePagePath: '/index.html'}]
        :param logging_options: (experimental) Configuration related to Cloudfront Logging.
        :param origin_behaviour_options: (experimental) Options for configuring the default origin behavior.
        :param runtime_options: (experimental) Dynamic configuration which gets resolved only during deployment.

        :stability: experimental
        '''
        if isinstance(domain_options, dict):
            domain_options = CloudfrontDomainOptions(**domain_options)
        if isinstance(logging_options, dict):
            logging_options = CloudfrontLoggingOptions(**logging_options)
        if isinstance(origin_behaviour_options, dict):
            origin_behaviour_options = OriginBehaviourOptions(**origin_behaviour_options)
        if isinstance(runtime_options, dict):
            runtime_options = RuntimeOptions(**runtime_options)
        self._values: typing.Dict[str, typing.Any] = {
            "website_content_path": website_content_path,
        }
        if domain_options is not None:
            self._values["domain_options"] = domain_options
        if error_responses is not None:
            self._values["error_responses"] = error_responses
        if logging_options is not None:
            self._values["logging_options"] = logging_options
        if origin_behaviour_options is not None:
            self._values["origin_behaviour_options"] = origin_behaviour_options
        if runtime_options is not None:
            self._values["runtime_options"] = runtime_options

    @builtins.property
    def website_content_path(self) -> builtins.str:
        '''(experimental) Path to the directory containing the static website files and assets.

        This directory must contain an index.html file.

        :stability: experimental
        '''
        result = self._values.get("website_content_path")
        assert result is not None, "Required property 'website_content_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_options(self) -> typing.Optional[CloudfrontDomainOptions]:
        '''(experimental) Configuration related to using custom domain names/certificates.

        :stability: experimental
        '''
        result = self._values.get("domain_options")
        return typing.cast(typing.Optional[CloudfrontDomainOptions], result)

    @builtins.property
    def error_responses(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_cloudfront.ErrorResponse]]:
        '''(experimental) How CloudFront should handle requests that are not successful (e.g., PageNotFound).

        :default: - [{httpStatus: 404,responseHttpStatus: 200,responsePagePath: '/index.html'}]

        :stability: experimental
        '''
        result = self._values.get("error_responses")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_cloudfront.ErrorResponse]], result)

    @builtins.property
    def logging_options(self) -> typing.Optional[CloudfrontLoggingOptions]:
        '''(experimental) Configuration related to Cloudfront Logging.

        :stability: experimental
        '''
        result = self._values.get("logging_options")
        return typing.cast(typing.Optional[CloudfrontLoggingOptions], result)

    @builtins.property
    def origin_behaviour_options(self) -> typing.Optional[OriginBehaviourOptions]:
        '''(experimental) Options for configuring the default origin behavior.

        :stability: experimental
        '''
        result = self._values.get("origin_behaviour_options")
        return typing.cast(typing.Optional[OriginBehaviourOptions], result)

    @builtins.property
    def runtime_options(self) -> typing.Optional[RuntimeOptions]:
        '''(experimental) Dynamic configuration which gets resolved only during deployment.

        :stability: experimental
        '''
        result = self._values.get("runtime_options")
        return typing.cast(typing.Optional[RuntimeOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StaticWebsiteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CloudFrontWebAclProps",
    "CloudfrontDomainOptions",
    "CloudfrontLoggingOptions",
    "CloudfrontWebAcl",
    "ManagedRule",
    "OriginBehaviourOptions",
    "RuntimeOptions",
    "StaticWebsite",
    "StaticWebsiteProps",
]

publication.publish()
