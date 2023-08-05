
[![Stable Version](https://img.shields.io/pypi/v/pip-compile-cross-platform?label=stable)](https://pypi.org/project/pip-compile-cross-platform/)

# `pip-compile-cross-platform`

Pin your Python dependencies as you would with [`pip-compile`](https://github.com/jazzband/pip-tools#example-usage-for-pip-compile), except in a cross-platform way.

## Usage

1. `pip install --user pip-compile-cross-platform`
2. `pip-compile-cross-platform requirements.in`

#### What is "pinning"?

"Pinning" your Python dependencies makes them predictable and deterministic by resolving all transitive dependencies
(dependencies of dependencies) and hard-coding them up-front.

For example, you can define a `requirements.in` file with the top-level requirements that _you_ have:

```
requests==2.27.1
```

Then, you run `pip-compile-cross-platform`, which produces a `requirements.txt` file with the "pinned" packages:

```
certifi==2022.5.18.1 ; python_full_version >= "3.6.0" \
    --hash=sha256:f1d53542ee8cbedbe2118b5686372fb33c297fcd6379b050cca0ef13a597382a \
    --hash=sha256:9c5705e395cd70084351dd8ad5c41e65655e08ce46f2ec9cf6c2c08390f71eb7
charset-normalizer==2.0.12 ; python_full_version >= "3.6.0" \
    --hash=sha256:2857e29ff0d34db842cd7ca3230549d1a697f96ee6d3fb071cfa6c7393832597 \
    --hash=sha256:6881edbebdb17b39b4eaaa821b438bf6eddffb4468cf344f09f89def34a8b1df
idna==3.3 ; python_full_version >= "3.6.0" \
    --hash=sha256:84d9dd047ffa80596e0f246e2eab0b391788b0503584e8945f2368256d2735ff \
    --hash=sha256:9d643ff0a55b762d5cdb124b8eaa99c66322e2157b69160bc32796e824360e6d
requests==2.27.1 \
    --hash=sha256:f22fa1e554c9ddfd16e6e41ac79759e17be9e492b3587efa038054674760e72d \
    --hash=sha256:68d7c56fd5a8999887728ef304a6d12edc7be74f1cfa47714fc8b414525c9a61
urllib3==1.26.9 ; python_version >= "2.7" and python_full_version < "3.0.0" or python_full_version >= "3.6.0" and python_version < "4" \
    --hash=sha256:44ece4d53fb1706f667c9bd1c648f5469a2ec925fcf3a776667042d645472c14 \
    --hash=sha256:aabaf16477806a5e1dd19aa41f8c2b7950dd3c746362d7e3223dbe6de6ac448e
```

Now, when developers install dependencies into their environment, they use the `requirements.txt`
file: `pip install -r requirements.txt`.

Since they're using this "lockfile" rather than the simpler `requirements.in`, they're guaranteed to have the exact
same packages installed as everyone else working on your project. This sidesteps a major cause of "works on my machine, but for
some reason not on yours" issues that aren't fun to diagnose 😎

## How does this compare to `pip-compile`?

[`pip-compile`](https://github.com/jazzband/pip-tools) is an incredible tool built by
[the Jazzband crew](https://jazzband.co/) that pins dependencies exactly as described above.
It can comfortably be described as a primary solution to the "pinning" problem in the Python ecosystem over the last
half-decade. In summary: `pip-compile` is great :)

However, there's one main limitation: [cross-environment usage is
unsupported](https://github.com/jazzband/pip-tools#cross-environment-usage-of-requirementsinrequirementstxt-and-pip-compile).
This means that conditional dependencies (such as Windows-only dependencies like [`colorama`](https://pypi.org/project/colorama/),
or backport libraries like [`iso8601`](https://pypi.org/project/iso8601/) which are only needed for Python < 3.7) aren't
properly captured by `pip-compile`.

![`pip-compile` misses environment-specific dependencies](pip-compile-missed-requirements.png)

`pip-compile` recommends creating a separate `requirements.txt` for each environment, but this
can lead to a lot of `requirements-$python-version-$os.txt` files:

lockfiles|
---|
requirements-3.7-windows.txt|
requirements-3.7-linux.txt|
requirements-3.7-macos.txt|
requirements-3.8-windows.txt|
...|

This has a few downsides:

* Developers have to consider which `requirements-...txt` file to install, and if the wrong one is chosen, the error
  message (pip complaining about missing hashes) doesn't make the root cause clear.
* Generating lockfiles requires many operating system environments, which can be a hassle to set up. There's [a GitHub
  Actions workflow template](https://github.com/zzzeid/compile-requirements) that can be used to lower this cost, but
  it's still a time-consuming (and perhaps eventually expensive) solution.
    * There's a minor, but possible other concern: there's a race condition where a new version of a transitive
      dependency is published in between lockfiles being created, causing different `requirements...txt` files to
      have _different versions of the same package_.

`pip-compile-cross-platform` sidesteps these downsides by generating a single `requirements.txt` lockfile that
is valid for all environments.

### Usage compared to `pip-compile`

`pip-compile-cross-platform` is planned to be compatible with the same command-line usage as `pip-compile`. However,
many flags and options are missing so far, so [help to improve this compatibility would be much appreciated](https://gitlab.com/mitchhentges/pip-compile-cross-platform/-/issues/1).

## How it works under-the-hood

Environment-specific dependencies are defined using [environment markers](https://peps.python.org/pep-0496/).
`pip-compile` evaluates environment markers up-front according to the current environment, which is why packages not
needed for the lockfile-generating machine are dropped.
`pip-compile-cross-platform` "carries forward" the environment markers into the created lockfile, which is why it is
able to work in all environments.

![`pip-compile` evaluates environment markers up-front](environment-marker-evaluation.png)

_How_ `pip-compile-cross-platform` is able to do this is by leveraging the fantastic [`poetry`](https://github.com/python-poetry/poetry)
tool. `poetry` is a "dependency management" tool for Python projects, whose main downside is that it requires that all
developers/environments working with a project have `poetry` installed. This isn't a _large_ cost, but it still carries
migration risk, which is (my theory about) why many projects still use `pip-compile` today instead.

So, part of `poetry`'s core logic requires carefully resolving dependencies and keeping track of environment markers.
`pip-compile-cross-platform` wraps around this logic, feeding in your project's top-level requirements and extracting
out a `pip`-compatible `requirements.txt` file.

-----

The best way to visualize `pip-compile-cross-platform` is that it's a thin wrapper around `poetry` that mimicks the
interface of `pip-compile`: this allows projects that still use `pip-compile` to get the benefits of `poetry` without
having to make a significant time investment.