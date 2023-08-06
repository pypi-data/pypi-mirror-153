'''
The aws-prototyping-sdk provides stable CDK and Projen constructs, allowing developers to have access to higher level abstractions than provided by the CDK or Projen alone.

For detailed documentation, please refer to the [documentation website](TODO).

## Bundling

This package simply bundles various packages from the `@aws-prototyping-sdk` namespace which have been marked as stable. As such, not all constructs or projen packages may be exported from this package and as such may need to be explicitly imported by creating a dependency on the individual packages.

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

To import experimental constructs, a dependency on the individual package is required. In the case of `static-website` a dependency on `@aws-prototyping-sdk/static-website` is required. The constructs can then be imported as follows:

```python
import { StaticWebsite } from "@aws-prototyping-sdk/static-website";
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
