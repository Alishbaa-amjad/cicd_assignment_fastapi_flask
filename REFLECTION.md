Each stage of the pipeline protects against a different kind of mistake.
The lint stage (flake8 + black) catches style and formatting problems --
inconsistent code that would make the codebase harder to read and maintain,
even if it technically still runs. The test stage catches actual logic
errors -- broken endpoints, wrong status codes, or features that no longer
behave as expected -- before that broken code reaches anyone else. The
deploy stage is the final action that ships the new version to production,
so it should only happen after we are confident the code is both clean and
correct.

The order matters because each stage builds confidence for the next one.
If deploy ran before test, a broken or buggy version of the API could go
live in production immediately, and real users (or other services depending
on this API) would be affected before anyone even noticed a test had failed.
Running deploy first defeats the entire purpose of having a test stage --
the whole point of `needs: test` is to act as a gatekeeper so deploy is
physically incapable of running on top of failing code.

One thing I would add to make this pipeline closer to a real production
setup is a proper rollback mechanism -- for example, keeping the previous
deployed version tagged so that if something still slips through and causes
issues in production, we can immediately revert to the last known-good
version instead of debugging under pressure while the app is down.