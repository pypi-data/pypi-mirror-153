# Chameleon fetcher

A small wrapper for chameleon (page templates) to easily fetch and render
templates.

## Installation

```bash
pip install chameleon_fetcher
```

## Usage

E.g. you have in template dir `my_template_dir` a file `simple.pt` with
the following content:

```html

<test>${template_name} ${myvar} ${some_var}</test>
```

You can then do:

```python
from chameleon_fetcher import ChameleonFetcher

cf = ChameleonFetcher('my_template_dir', some_var=42)
output = cf('simple', myvar='test')
assert output == '<test>simple test 42</test>'
```

Please note how `some_var` is set "globally", while for the specific template also a
variable `myvar` is used.

The following parameters are accepted by ChameleonFetcher:

- **template_dir**: the directory where the templates are located

And optionally:

- _extension_: extension of the template files, defaults to '.pt'
- _boolean_attributes_: what boolean attributes should be supported, defaults to {'selected', 'checked'}
- _auto_reload_: if the templates should be reloaded on change, defaults to True
- **kwargs: other params you want to have available in all templates, e.g. flask=flask