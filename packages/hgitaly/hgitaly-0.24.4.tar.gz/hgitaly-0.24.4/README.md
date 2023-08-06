# HGitaly

HGitaly is Gitaly server for Mercurial.

## Automated tests and Continuous Integration

### How to run the tests

Usually, that would be in a virtualenv, but it's not necessary.

```
  python3 -m pip install -r test-requirements.txt
  ./run-all-tests
```

Hint: Check the contents of `run-all-tests`, it's just `pytest` with
a standard set of options (mostly for coverage, see below).

### Unit and Mercurial integration tests

These are the main tests. They lie inside the `hgitaly`
and `hgext3rd.hgitaly` Python packages. The layout follows the style where
each subpackage has its own tests package, to facilitate future refactorings.

The Mercurial integration tests are written with the [mercurial-testhelpers]
library. Their duty is to assert that HGitaly works as expected and maintains
compatibility with several versions of Mercurial and possibly other
dependencies, such as [grpcio].

The implicit assumption with these tests is that the test authors actually
knew what was expected. HGitaly being meant to be a direct replacement, or
rather a translation of Gitaly in Mercurial terms, those expectation are
actually a mix of:

- Design choices, such as mapping rules between branch/topic combinations
  and GitLab branches.
- Gitaly documentation and source code.
- sampling of Gitaly responses.

### Gitaly comparison tests

If an appropriate Gitaly installation is found, `run-all-tests` will also
run the tests from the `tests_with_gitaly` package. This happens automatically
from within a [HDK] workspace.

These are precisely meant for what the Mercurial integration tests can't do:
check that HGitaly responses take the form expected by the various Gitaly
clients, by comparing directly with the reference Gitaly implementation.

The comparisons work by using the conversions to Git provided by
`py-heptapod`, which are precisely what HGitaly aims to replace as a mean
to expose Mercurial content to GitLab.

Once there is no ambiguity with what Gitaly clients expect, the correctness
of the implementation, with its various corner cases,
should be left to the Mercurial integration tests.

### Test coverage

This project is being developed with a strong test coverage policy, enforced by
CI: without the Gitaly comparison tests, the coverage has to stay at 100%.

This does not mean that a contribution has to meet this goal to be worthwile,
or even considered. Contributors can expect Maintainers to help them
achieving the required 100% coverage mark, especially if they are newcomers.
Of course, Contributors cannot expect Maintainers to go
as far as write missing tests for them, even if that can still happen
for critical urgent issues.

Selected statements can of course be excluded for good reasons, using
`# pragma no cover`.

Coverage exclusions depending on the Mercurial version are
provided by the coverage plugin of [mercurial-testhelpers].

Unexpected drop of coverage in different Mercurial versions is a powerful
warning system that something not obvious is getting wrong, but the
Gitaly comparison tests are run in CI against a fixed set of
dependencies, hence 100% coverage must be achieved without the Gitaly
comparison tests.

On the other hand, Gitaly comparison tests will warn us when we bump upstream
GitLab if some critical behaviour has changed.

### Tests Q&A and development hints

#### Doesn't the 100% coverage rule without the Gitaly comparison tests mean writing the same tests twice?

In some cases, yes, but it's limited.

For example, the comparison tests
can tell us that the `FindAllBranchNames` is actually expected to return
GitLab refs (`refs/heads/some-branch`), not GitLab branch names. That can
be settled with a few, very basic, test cases. There is no need to test all
the mapping rules for topics, and even less the various related corner cases
in the comparison tests. These, on the other hand depend strongly on Mercurial
internals, and absolutely have to be fully tested continuously against various
Mercurial versions.

Also, it is possible to deduplicate scenarios that are almost identical in
Mercurial integration tests and Gitaly comparison tests: factorize out the
common code in a helper function made available for both. The question is if
it is worth the effort.

Finally, comparison tests should focus on the fact that Gitaly and HGitaly
results agree, not on what they contain. In the above example,
a comparison for `FindAllBranchNames` could simply assert equality of the
returned sets of branch names. This is a bit less cumbersome, and easier
to maintain.

### How to reproduce a drop in coverage found by the `compat` CI stage?

These are often due to statements being covered by the Gitaly comparison
tests only, leading to 100% coverage in the `main` stage, but not in the
`compat` stage.

The first thing to do is to run without the Gitaly comparison tests:

```
SKIP_GITALY_COMPARISON_TESTS=yes ./run-all-tests
```

(any non empty value in that environment variable, even `no` or `false` will
trigger the skipping)

In some rare cases, the drop in coverage could be due to an actual change
between Mercurial versions. If that happens, there are good chances that an
actual bug is lurking around.

### How to run the tests with coverage of the Gitaly comparison tests

```
./run-all-tests --cov tests_with_gitaly --cov-report html
```

The HTML report will be nice if you don't have 100% coverage. To display it,
just do

```
firefox htmlcov/index.html
```

By default, the Gitaly comparison tests themselves are not covered, indeed.
This is because `run-all-tests` does not know whether they will be skipped for
lack of a Gitaly installation – which would be legitimate.

But they *are* covered in the CI jobs that launch them, because Gitaly is
assumed to be available. For these, the coverage would tell us that something
was broken, preventing the tests to run.

### How to poke into Gitaly protocol?

The Gitaly comparison tests provide exactly a harness for that: take a test,
modify it as needed, insert a `pdb` breakpoint, and get going.

The big advantage here is that startup of the Gitaly comparison tests is
almost instantaneous, especially compared with RSpec, wich takes about a minute
to start even a completely trivial test.

Of course that will raise the question whether it'll be useful to make true
tests of these experiments.

### When is a Gitaly comparison test required?

Each time there's a need to be sure of what's expected and it can help answer
that question. It doesn't have to do more than that.

### When to prefer writing RSpec tests in Heptapod Rails over Gitaly comparison tests in HGitaly?

If you need to make sure that Heptapod Rails, as a Gitaly client, sends
the proper requests, because that can depend on specific dispatch code.

For instance, we are currently still converting to Git on the Rails side.
A source of bugs would be to send Git commit ids to HGitaly.

Apart from that, it is expected to be vastly more efficient to use
Gitaly comparison tests.

The more Heptapod progresses, the less complicated all of this should be.

## Updating the Gitaly gRPC protocol

The virtualenv has to be activated

1. `pip install -r dev-requirements.txt`

2. Copy the new `proto` files from a Gitaly checkout with
   version matching the wanted GitLab upstream version.
   Example in a HDK context:

   ```
   cp ../gitaly/proto/*.proto protos/  # we dont want the `go` subdir
   ```

3. run `./generate-stubs`

4. run the tests: `./run-all-tests`

5. perform necessary `hg add` after close inspection of `hg status`

## Updating the HGitaly specific gRPC protocol

This package defines and implements an additional gRPC protocol, with
gRPC services and methods that are specific to Mercurial, or more generally
Heptapod.

### Protocol specification

The sources are `proto` files in the `protos/` directory, same as for the
Gitaly protocol.

They distinguish themselves by this declaration:

```
package hgitaly;
```

Each time a change is made to the protocol, the libraries for all
provided programming languages have to be regenerated and committed, ideally
together with the protocol change.

### Python library

It has a special status, being versioned together with the protocol and the
server implementation. It is provided as the [hgitaly.stub](hgitaly/stub)
package.

The Python stubs are produced by the same script that takes care of Gitaly
`proto` files:

```
./generate-stubs
```

### Ruby library

See [the separate documentation](ruby/README.md)

### Other languages

A Go library will probably be necessary quite soon for Workhorse or perhaps
Heptapod Shell.

A Rust library would be nice to have

[mercurial-testhelpers]: https://pypi.org/project/mercurial-testhelpers/
[grpcio]: https://pypi.org/project/grpcio/
[HDK]: https://foss.heptapod.net/heptapod/heptapod-development-kit


