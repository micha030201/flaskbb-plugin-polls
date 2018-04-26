polls
=====


Poll functionality for flaskBB.


Installation
------------

Install *flaskbb-plugin-polls* with
``pip install flaskbb-plugin-polls``

And run the migrations:
``flaskbb db upgrade``


Usage
-----

Polls are created inline inside posts using BBcode-style tags, like this:

```
[poll
max_votes_allowed=3
close_after=2d
votes_public=y
changing_votes_allowed=y
result_visible_before_voting=n
result_visible_before_closed=y
]
Option one
Option two
Option three - pick this one!
Option four
[/poll]
```

Multiple polls are allowed per post, they can also be quoted.


License
-------
This project is licensed under the terms of the [BSD License](/LICENSE).
