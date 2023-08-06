# simple_rss_reader

As an happy customer of Alfred 4 APP, i was in a need for simplest RSS parser.
I decided to write the simplest one for my needs. 

Then i said to myself, why not to make it open source as a package for anyone who need it. 
Although its 2022, and XML should be an no more then  (not so great) history, i know that if i need it, i can only assume i am not the only one. 

Feel free to use, fork, and learn (although it is as minimal and simple as possible)


## INSTALL
run: 
```
pip install  yet-another-simple-rss-parser
```

## Usage

```

from simple_rss_reader.reader import SimpleRssReader


r = SimpleRssReader(url) # url of source or xml string

# load as dict
v = r.to_dict()

#  get as json
v = r.to_json()

# get list of items (without header)
v = r.get_tiems()
```

The package homepage in pypi: https://www.pypi.org/project/yet-another-simple-rss-parser/
Source code is hosted in github: https://github.com/barakbl/simple_rss_reader
