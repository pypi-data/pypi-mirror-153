# sain
A pure Python package that implements standard Rust core types for Python.


## Install
You'll need Python 3.8 or higher.

Still not on PyPI
```rs
$ pip install git+https://github.com/nxtlo/sain
```

## Example
```py
import sain

#[cfg_attr(target_os = unix)]
@sain.cfg_attr(target_os="unix")
def run_when_unix() -> None:
    import uvloop
    uvloop.install()

# If this returns True, run_when_unix will run, otherwise returns.
if sain.cfg(requires_modules=("dotenv", ...), python_version=(3, 9, 6)):
    # Stright up replace typing.Optional[int]
    def inner() -> sain.Some[int]:
        return sain.Some(1)

# If the Some[T] contained value is `None`, This raises RuntimeError.
value: int = inner().expect("Still None")

as_none: sain.Some[str] = sain.Some(None)  # type hint is fine.
assert as_none.is_none()
```

### Defaults
A protocol that types can implement which have a default value.

```py
import sain

class DefaultCache(sain.Default[dict[str, int]]):
    # One staticmethod must be implemented and must return the same type.
    @staticmethod
    def default() -> dict[str, int]:
        return {'yo': 999}
```


### Iter
Turns normal iterables into `Iter` type.

```py
import sain

f = sain.Iter([1,2,3])
# or f = sain.into_iter([1,2,3])
assert 1 in f

for item in f.take_while(lambda i: i > 1):
    print(item)
```

### Why
i like Rust coding style :p

### Notes
Since Rust is a compiled language, Whatever predict returns False will not compile.

But there's no such thing as this in Python, So `RuntimeError` will be raised and whatever was predicated will not run.
