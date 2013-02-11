faroo.py
========

Python bindings to the [FAROO API](http://www.faroo.com/hp/api/api.html "FAROO - Free Search API").


Usage
-----

### Importing

```python
import faroo
````

### Querying

```python
freq = faroo.Faroo()
fres = freq.param('length', 8).query('lolcats')
````

```python
freq = faroo.Faroo()
fres = freq.param('src', 'news').query()
````


![FAROO Web Search](http://www.faroo.com/hp/api/faroo_attribution.png "FAROO Web Search")
