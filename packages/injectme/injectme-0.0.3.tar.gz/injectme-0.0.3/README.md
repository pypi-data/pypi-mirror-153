# injectme

Simple Dependency Injection library in pure Python.

If you have never heard about DI it's probably useless.

If you are struggling to tame all of your dependencies running wildly through your code and have a hard time passing high-level dependencies down the abstracion layers you might have found a solution.

It's small. It's simple. Does not enforce complex abstractions. Does not pollute the code.

## Installation
This project is available as python package:

```
pip install injectme
```

## Simple Example

```python
from injectme import inject, register


class Dependency:
    def do_stuff(self):
        print("I'm useful")


@inject
class App:
    dependency: Dependency

    def run(self):
        self.dependency.do_stuff()


register(Dependency, Dependency())

app = App()
app.run()
```
```
I'm useful
```

## Links

- docs: https://github.com/zuczekgnojak/injectme
- pypi: https://pypi.org/project/injectme
- code: https://github.com/zuczekgnojak/injectme
