from flask import render_template, request,flash
from flask_login import current_user,login_required
from db_manager import db
from sqlalchemy import desc
from models import Comment,Service


class Home:
    def __init__(self, *args, **kwargs):
        pass
    def home(self):
        services=db.session.query(Service.Services).all()
        comments=db.session.query(Comment.Comments).filter(Comment.Comments.published==True).order_by(desc(Comment.Comments.created_at)).limit(3).all()
        return render_template('index.html',services=services,comments=comments)
    @login_required
    def send_comment(self):
        if request.method == 'POST' and request.form['text'] is not '':
            db.session.add(Comment.Comments(text=request.form['text'],
                                            user_id=current_user.id))
            db.session.commit()
            flash('نظر شما ارسال شد , پس از تایید در سایت به نمایش خواهد گذاشته شد','success')
        return render_template('comment.html')
        