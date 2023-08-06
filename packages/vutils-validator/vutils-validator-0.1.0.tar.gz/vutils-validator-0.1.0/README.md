[![Coverage Status](https://coveralls.io/repos/github/i386x/vutils-validator/badge.svg?branch=main)](https://coveralls.io/github/i386x/vutils-validator?branch=main)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/i386x/vutils-validator.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/i386x/vutils-validator/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/i386x/vutils-validator.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/i386x/vutils-validator/context:python)

# vutils-validator: Data Validation Utilities

This package provides a set of tools that helps with validation of input data.

## Installation

To get the package on your system, type
```sh
$ pip install vutils-validator
```

## How to Use

Please, read the following subsections to get more info about particular use
case.

### Basic Validations

Module `vutils.validator.basic` provides a set of functions for validation of
simple input data forms, like email addresses:
* `verify_not_empty(value)` fails if `value` is empty.
* `verify_matches(value, regex, message="")` fails if `value` does not match
  regular expression `regex`. Since many regular expressions describe entities
  that have a name (identifier, number, email address, etc.) the default error
  message can be overridden by `message` argument.
* `verify_email(value)` fails if `value` is not an email address (currently
  described by simple `^\S+@\S+\.[A-Za-z]+$` regular expression).

The `value` passed to all validation functions can be either `str` or a
`ValueHolder` (from `vutils.validator.value`) object. A `ValueHolder` object
can be used to store additional information about value, like its name and
origin. The synopsis of `ValueHolder`'s constructor is
`__init__(self, value, name="The value", location=None)`, where `value`,
`name`, and `location` are value, its name, and the location of its origin,
respectively. `location` is a `Location` (from `vutils.validator.value`) object
that holds path, line, and column of the value/token origin. `ValueHolder`
serves to provide more detail about value in error messages issued by
validation functions by raising `ValidationError` (from
`vutils.validator.errors`) when the validation fails, example:
```python
from vutils.validator.basic import verify_email
from vutils.validator.errors import ValidationError
from vutils.validator.value import ValueHolder


def get_input(name):
    return ValueHolder(input(f"Enter {name}: "), name)


try:
    verify_email(get_input("email"))
except ValidationError as exc:
    print(exc)
```

On ill-formed input, the example prints `email must be an email address!`,
since `get_input` names a value as `email`.
