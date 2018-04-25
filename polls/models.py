from flaskbb.extensions import db
from flaskbb.utils.database import CRUDMixin


association_table = db.Table(
    'polls_association', db.Model.metadata,
    db.Column('option_id', db.Integer, db.ForeignKey('polls_options.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
)


class Poll(db.Model, CRUDMixin):
    __tablename__ = 'polls_polls'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id'),
        nullable=True
    )
    post = db.relationship("Post")

    options = db.relationship("Option", back_populates="poll", lazy="joined")

    @property
    def users_voted(self):
        return [
            voted_user
            for option in self.options
            for voted_user in option.users_voted
        ]

    def allowed_to_vote(self, user):
        return all((
            self.post,
            self.post.topic,
            not self.post.topic.locked,
            not self.post.topic.forum.locked,
            not user.is_anonymous,
            ({g.id for g in self.post.topic.forum.groups} &
             {g.id for g in user.groups})
        ))


class Option(db.Model, CRUDMixin):
    __tablename__ = 'polls_options'

    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(
        db.Integer,
        db.ForeignKey('polls_polls.id'),
        nullable=False
    )
    poll = db.relationship("Poll", back_populates="options")

    text = db.Column(db.String, nullable=False)

    users_voted = db.relationship(
        "User", secondary=association_table, lazy="joined")
