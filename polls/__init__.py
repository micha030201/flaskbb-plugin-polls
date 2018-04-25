# -*- coding: utf-8 -*-
"""
    polls
    ~~~~~

    A polls Plugin for FlaskBB.

    :copyright: (c) 2018 by Михаил Лебедев.
    :license: BSD License, see LICENSE for more details.
"""
import re
import os
from contextlib import suppress
from functools import partial

from flask import (
    Blueprint, request, abort, render_template, url_for, redirect)
from flask_login import current_user

from .models import Poll, Option


__version__ = "0.0.1"


# connect the hooks
def flaskbb_load_migrations():
    return os.path.join(os.path.dirname(__file__), "migrations")


def flaskbb_load_translations():
    return os.path.join(os.path.dirname(__file__), "translations")


def flaskbb_load_blueprints(app):
    app.register_blueprint(
        bp,
        url_prefix="/polls"
    )


# Poll creation:

_re_poll_definition = re.compile(
    r'\[poll\](.+?)\[/poll\]',
    flags=re.DOTALL
)


def create_poll(post, match):
    options = map(str.strip, match.group(1).strip().split('\n'))

    poll = Poll()
    poll.post = post
    poll.options = [Option(text=option) for option in options]
    poll.save()

    return '[poll={}]'.format(poll.id)


def flaskbb_event_post_save_after(post):
    new_content = _re_poll_definition.sub(
        partial(create_poll, post), post.content)
    if not new_content == post.content:
        post.content = new_content
        post.save()


# Voting:

def redirect_back():
    next_url = request.referrer
    if next_url:
        return redirect(next_url)
    else:
        return redirect(url_for('forum.index'))


bp = Blueprint("polls", __name__, template_folder="templates")


@bp.route('/vote/<int:id>', methods=['POST'])
def vote(id):
    poll = Poll.query.filter(Poll.id == id).first_or_404()
    if not poll.allowed_to_vote(current_user):
        abort(403)
    option_ids = request.form.getlist('options-selected', type=int)
    options = Option.query.filter(Option.id.in_(option_ids)).all()
    for option in options:
        assert option.poll == poll
        option.users_voted.append(current_user)
    poll.save()
    return redirect_back()


@bp.route('/withdraw_vote/<int:id>', methods=['POST'])
def withdraw_vote(id):
    poll = Poll.query.filter(Poll.id == id).first_or_404()
    if not poll.allowed_to_vote(current_user):
        abort(403)
    for option in poll.options:
        with suppress(ValueError):
            option.users_voted.remove(current_user)
    poll.save()
    return redirect_back()


# Poll rendering:

_re_poll = re.compile(r'\[poll=(\d)\]')


def render_poll(match):
    id = match.group(1)
    poll = Poll.query.filter(Poll.id == id).first()
    if not poll:
        return '[invalid-poll]'
    else:
        return render_template('poll.html', poll=poll)


class Renderer:
    def paragraph(self, text):
        text = _re_poll.sub(render_poll, text)
        return super().paragraph(text)


def flaskbb_load_post_markdown_class():
    return Renderer


SETTINGS = {}
