# Pull Request

## Description

Provide a brief description of the changes in this PR.

Fixes #(issue number)

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement
- [ ] Test improvements

## Changes Made

List the main changes in this PR:

- Change 1
- Change 2
- Change 3

## Testing

Describe the tests you ran to verify your changes:

- [ ] All existing tests pass (`pytest`)
- [ ] Added new tests for new functionality
- [ ] Manual testing performed
- [ ] Tested on multiple Python versions (if applicable)
- [ ] Tested on multiple operating systems (if applicable)

### Test Commands Run

```bash
pytest
pytest --cov=prozes
black --check prozes tests
ruff check prozes tests
mypy prozes
```

## Checklist

- [ ] My code follows the project's code style (Black, Ruff)
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published
- [ ] I have updated the CHANGELOG.md (if applicable)

## Breaking Changes

If this PR introduces breaking changes, describe them here and how users should update their code:

- Breaking change 1
- Migration guide: ...

## Additional Notes

Add any additional notes, screenshots, or context about the PR here.

## Related Issues

- Closes #
- Related to #

## Screenshots (if applicable)

Add screenshots to help explain your changes.

---

**For Maintainers:**

- [ ] Code review completed
- [ ] Tests pass on CI
- [ ] Documentation is up to date
- [ ] CHANGELOG updated
- [ ] Ready to merge
