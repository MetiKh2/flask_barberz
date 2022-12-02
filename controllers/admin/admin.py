from flask import render_template, request, flash, abort, redirect, url_for
from flask_login import current_user, login_required
from db_manager import db
from sqlalchemy import desc
from models import Comment, Service


class Admin:
    def __init__(self, *args, **kwargs):
        pass

    @login_required
    def admin(self):
        if not current_user.admin:
            abort(403)
        return render_template('/admin/index.html')

    @login_required
    def comments_list(self):
        if not current_user.admin:
            abort(403)
        if request.method == 'POST':
            db.session.query(Comment.Comments).filter(
                Comment.Comments.id==request.args.get('id')).delete()
            db.session.commit()
        comments = db.session.query(Comment.Comments).order_by(
            desc(Comment.Comments.created_at)).all()
        return render_template('/admin/comments.html', comments=comments)

    @login_required
    def approve_comment(self, comment_id, status):
        if not current_user.admin:
            abort(403)
        status=True if status == 'True' else False
        comment = db.session.query(Comment.Comments).filter(
            Comment.Comments.id == comment_id).first()
        if comment:
            comment.published = status
            db.session.add(comment)
            db.session.commit()
        return redirect(url_for('comments_list'))
