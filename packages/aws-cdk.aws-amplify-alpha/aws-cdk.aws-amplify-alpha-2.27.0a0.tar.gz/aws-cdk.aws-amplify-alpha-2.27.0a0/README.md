# AWS Amplify Construct Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

The AWS Amplify Console provides a Git-based workflow for deploying and hosting fullstack serverless web applications. A fullstack serverless app consists of a backend built with cloud resources such as GraphQL or REST APIs, file and data storage, and a frontend built with single page application frameworks such as React, Angular, Vue, or Gatsby.

## Setting up an app with branches, custom rules and a domain

To set up an Amplify Console app, define an `App`:

```python
import aws_cdk.aws_codebuild as codebuild


amplify_app = amplify.App(self, "MyApp",
    source_code_provider=amplify.GitHubSourceCodeProvider(
        owner="<user>",
        repository="<repo>",
        oauth_token=SecretValue.secrets_manager("my-github-token")
    ),
    build_spec=codebuild.BuildSpec.from_object_to_yaml({
        # Alternatively add a `amplify.yml` to the repo
        "version": "1.0",
        "frontend": {
            "phases": {
                "pre_build": {
                    "commands": ["yarn"
                    ]
                },
                "build": {
                    "commands": ["yarn build"
                    ]
                }
            },
            "artifacts": {
                "base_directory": "public",
                "files": -"**/*"
            }
        }
    })
)
```

To connect your `App` to GitLab, use the `GitLabSourceCodeProvider`:

```python
amplify_app = amplify.App(self, "MyApp",
    source_code_provider=amplify.GitLabSourceCodeProvider(
        owner="<user>",
        repository="<repo>",
        oauth_token=SecretValue.secrets_manager("my-gitlab-token")
    )
)
```

To connect your `App` to CodeCommit, use the `CodeCommitSourceCodeProvider`:

```python
import aws_cdk.aws_codecommit as codecommit


repository = codecommit.Repository(self, "Repo",
    repository_name="my-repo"
)

amplify_app = amplify.App(self, "App",
    source_code_provider=amplify.CodeCommitSourceCodeProvider(repository=repository)
)
```

The IAM role associated with the `App` will automatically be granted the permission
to pull the CodeCommit repository.

Add branches:

```python
# amplify_app: amplify.App


main = amplify_app.add_branch("main") # `id` will be used as repo branch name
dev = amplify_app.add_branch("dev",
    performance_mode=True
)
dev.add_environment("STAGE", "dev")
```

Auto build and pull request preview are enabled by default.

Add custom rules for redirection:

```python
# amplify_app: amplify.App

amplify_app.add_custom_rule({
    "source": "/docs/specific-filename.html",
    "target": "/documents/different-filename.html",
    "status": amplify.RedirectStatus.TEMPORARY_REDIRECT
})
```

When working with a single page application (SPA), use the
`CustomRule.SINGLE_PAGE_APPLICATION_REDIRECT` to set up a 200
rewrite for all files to `index.html` except for the following
file extensions: css, gif, ico, jpg, js, png, txt, svg, woff,
ttf, map, json, webmanifest.

```python
# my_single_page_app: amplify.App


my_single_page_app.add_custom_rule(amplify.CustomRule.SINGLE_PAGE_APPLICATION_REDIRECT)
```

Add a domain and map sub domains to branches:

```python
# amplify_app: amplify.App
# main: amplify.Branch
# dev: amplify.Branch


domain = amplify_app.add_domain("example.com",
    enable_auto_subdomain=True,  # in case subdomains should be auto registered for branches
    auto_subdomain_creation_patterns=["*", "pr*"]
)
domain.map_root(main) # map main branch to domain root
domain.map_sub_domain(main, "www")
domain.map_sub_domain(dev)
```

## Restricting access

Password protect the app with basic auth by specifying the `basicAuth` prop.

Use `BasicAuth.fromCredentials` when referencing an existing secret:

```python
amplify_app = amplify.App(self, "MyApp",
    source_code_provider=amplify.GitHubSourceCodeProvider(
        owner="<user>",
        repository="<repo>",
        oauth_token=SecretValue.secrets_manager("my-github-token")
    ),
    basic_auth=amplify.BasicAuth.from_credentials("username", SecretValue.secrets_manager("my-github-token"))
)
```

Use `BasicAuth.fromGeneratedPassword` to generate a password in Secrets Manager:

```python
amplify_app = amplify.App(self, "MyApp",
    source_code_provider=amplify.GitHubSourceCodeProvider(
        owner="<user>",
        repository="<repo>",
        oauth_token=SecretValue.secrets_manager("my-github-token")
    ),
    basic_auth=amplify.BasicAuth.from_generated_password("username")
)
```

Basic auth can be added to specific branches:

```python
# amplify_app: amplify.App

amplify_app.add_branch("feature/next",
    basic_auth=amplify.BasicAuth.from_generated_password("username")
)
```

## Automatically creating and deleting branches

Use the `autoBranchCreation` and `autoBranchDeletion` props to control creation/deletion
of branches:

```python
amplify_app = amplify.App(self, "MyApp",
    source_code_provider=amplify.GitHubSourceCodeProvider(
        owner="<user>",
        repository="<repo>",
        oauth_token=SecretValue.secrets_manager("my-github-token")
    ),
    auto_branch_creation=amplify.AutoBranchCreation( # Automatically connect branches that match a pattern set
        patterns=["feature/*", "test/*"]),
    auto_branch_deletion=True
)
```

## Adding custom response headers

Use the `customResponseHeaders` prop to configure custom response headers for an Amplify app:

```python
amplify_app = amplify.App(self, "App",
    source_code_provider=amplify.GitHubSourceCodeProvider(
        owner="<user>",
        repository="<repo>",
        oauth_token=SecretValue.secrets_manager("my-github-token")
    ),
    custom_response_headers=[amplify.CustomResponseHeader(
        pattern="*.json",
        headers={
            "custom-header-name-1": "custom-header-value-1",
            "custom-header-name-2": "custom-header-value-2"
        }
    ), amplify.CustomResponseHeader(
        pattern="/path/*",
        headers={
            "custom-header-name-1": "custom-header-value-2"
        }
    )
    ]
)
```

## Deploying Assets

`sourceCodeProvider` is optional; when this is not specified the Amplify app can be deployed to using `.zip` packages. The `asset` property can be used to deploy S3 assets to Amplify as part of the CDK:

```python
import aws_cdk.aws_s3_assets as assets

# asset: assets.Asset
# amplify_app: amplify.App

branch = amplify_app.add_branch("dev", asset=asset)
```
