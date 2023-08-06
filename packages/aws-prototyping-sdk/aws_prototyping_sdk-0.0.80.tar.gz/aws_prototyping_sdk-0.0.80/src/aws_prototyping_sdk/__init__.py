'''
The aws-prototyping-sdk provides stable CDK and Projen constructs, allowing developers to have access to higher level abstractions than provided by the CDK or Projen alone.

For detailed documentation, please refer to the [documentation website](https://aws.github.io/aws-prototyping-sdk/).

## Bundling

This package simply bundles various packages from the `@aws-prototyping-sdk` namespace which have been marked as `stable`. As such, not all constructs or classes may be exported from this package and will need to be explicitly imported by creating a dependency on the individual packages.

To illustrate, at the time of writing the following individual packages are published:

```
@aws-prototyping-sdk
        |_ pipeline       : [stable]
        |_ nx-monorepo    : [stable]
        |_ static-website : [experimental]
        |_ identity       : [experimental]
```

The aws-prototyping-sdk package will bundle all stable packages and export them as namespaces as follows:

```
aws-prototyping-sdk
        |_ pipeline
        |_ nx_monorepo
```

This means if you wanted to access the PDKPipeline which is a stable construct, you simply add a dependency on the `aws-prototyping-sdk` and import it as follows:

```python
import { nx_monorepo, pipeline } from "aws-prototyping-sdk";
```

To import `experimental` constructs, a dependency on the individual package is required. In the case of `static-website`, a dependency on `@aws-prototyping-sdk/static-website` is required. The constructs can then be imported as follows:

```python
import { StaticWebsite } from "@aws-prototyping-sdk/static-website";
```

## nx-monorepo

The nx-monorepo package vends a NxMonorepoProject Projen construct that adds [NX](https://nx.dev/getting-started/intro) monorepo support and manages your yarn/npm/pnpm workspaces on your behalf. This construct enables polygot builds (and inter language build dependencies), build caching, dependency visualization and much, much more.

The PDK itself uses the nx-monorepo project itself and is a good reference for seeing how a complex, polygot monorepo can be set up.

To get started simply run the following command in an empty directory:

```bash
npx projen new --from aws-prototyping-sdk nx-monorepo
```

This will boostrap a new Projen monorepo and contain the following in the .projenrc.ts:

```python
import { nx_monorepo } from "aws-prototyping-sdk";

const project = new nx_monorepo.NxMonorepoProject({
  defaultReleaseBranch: "main",
  devDeps: ["aws-prototyping-sdk"],
  name: "my-package",
});

project.synth();
```

To add new packages to the monorepo, you can simply add them as a child to the monorepo. To demonstrate, lets add a PDK Pipeline TS Project as a child as follows:

```python
import { nx_monorepo } from "aws-prototyping-sdk";

const project = new nx_monorepo.NxMonorepoProject({
  defaultReleaseBranch: "main",
  devDeps: ["aws-prototyping-sdk"],
  name: "my-package",
});

new PDKPipelineTsProject({
  parent: project,
  outdir: "packages/cicd",
  defaultReleaseBranch: "mainline",
  name: "cicd",
  cdkVersion: "2.1.0"
});

project.synth();
```

Once added, run `npx projen` from the root directory. You will now notice a new TS package has been created under the packages/cicd path.

Now lets add a python project to the monorepo and add a inter-language build dependency.

```python
import { nx_monorepo } from "aws-prototyping-sdk";
import { PDKPipelineTsProject } from "aws-prototyping-sdk/pipeline";
import { PythonProject } from "projen/lib/python";

const project = new nx_monorepo.NxMonorepoProject({
  defaultReleaseBranch: "main",
  devDeps: ["aws-prototyping-sdk"],
  name: "test",
});

const pipelineProject = new PDKPipelineTsProject({
  parent: project,
  outdir: "packages/cicd",
  defaultReleaseBranch: "mainline",
  name: "cicd",
  cdkVersion: "2.1.0"
});

// Standard Projen projects also work here
const pythonlib = new PythonProject({
  parent: project,
  outdir: "packages/pythonlib",
  authorEmail: "",
  authorName: "",
  moduleName: "pythonlib",
  name: "pythonlib",
  version: "0.0.0"
});

// Pipeline project depends on pythonlib to build first
project.addImplicitDependency(pipelineProject, pythonlib);

project.synth();
```

Run `npx projen` from the root directory. You will now notice a new Python package has been created under packages/pythonlib.

To visualize our dependency graph, run the following command from the root directory: `npx nx graph`.

Now lets test building our project, from the root directory run `npx nx run-many --target=build --all`. As you can see, the pythonlib was built first followed by the cicd package.

The NxMonorepoProject also manages your yarn/pnpm workspaces for you and synthesizes these into your package.json pnpm-workspace.yml respectively.

For more information on NX commands, refer to this [documentation](https://nx.dev/using-nx/nx-cli).

## pipeline

The pipeline module vends an extension to CDK's CodePipeline construct, named PDKPipeline. It additionally creates a CodeCommit repository and by default is configured to build the project assumming nx-monorepo is being used (although this can be changed). A Sonarqube Scanner can also be configured to trigger a scan whenever the synth build job completes successfully. This Scanner is non-blocking and as such is not instrumented as part of the pipeline.

The architecture for the PDKPipeline is as follows:

```
CodeCommit repository -> CodePipeline
                             |-> EventBridge Rule (On Build Succeded) -> CodeBuild (Sonar Scan)
                             |-> Secret (sonarqube token)
```

This module additionally vends multiple Projen Projects, one for each of the supported languages. These projects aim to bootstrap your project by providing sample code which uses the PDKPipeline construct.

For example, in .projenrc.ts:

```python
new PDKPipelineTsProject({
    cdkVersion: "2.1.0",
    defaultReleaseBranch: "mainline",
    devDeps: ["aws-prototyping-sdk"],
    name: "my-pipeline",
});
```

This will generate a package in typescript containing CDK boilerplate for a pipeline stack (which instantiates PDKPipeline), sets up a Dev stage with an Application Stage containing an empty ApplicationStack (to be implemented). Once this package is synthesized, you can run `npx projen` and projen will synthesize your cloudformation.

Alternatively, you can initialize a project using the cli (in an empty directory) for each of the supported languages as follows:

```bash
# Typescript
npx projen new --from aws-prototyping-sdk pdk-pipeline-ts
```

```bash
# Python
npx projen new --from aws-prototyping-sdk pdk-pipeline-py
```

```bash
# Java
npx projen new --from aws-prototyping-sdk pdk-pipeline-java
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

__all__ = [
    "nx_monorepo",
    "pipeline",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import nx_monorepo
from . import pipeline
