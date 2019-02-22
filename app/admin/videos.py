from flask import render_template, redirect, request, flash, url_for
from flask_login import login_required, current_user
from slugify import slugify

from app.entity.Article import Category
from app.entity.Video import Video
from app.repository.Repository import Repository
from . import admin
from .forms import Video as VideoForm


@admin.route('/videos')
@login_required
def videos():
    form = VideoForm()
    categories = Category.query.all()
    page = request.args.get('page', 1, type=int)
    if current_user.is_admin:
        videos = Video.query.order_by(Video.created_at.desc()).paginate(page, Video.VIDEO_PER_PAGE, False)
    else:
        videos = Video.query.filter_by(user_id=current_user.id).order_by(Video.created_at.desc()).paginate(page, Video.VIDEO_PER_PAGE, False)
    next_url = url_for('admin.videos', page=videos.next_num) if videos.has_next else None
    prev_url = url_for('admin.videos', page=videos.prev_num) if videos.has_prev else None
    return render_template('admin/videos/videos.html', form=form, videos=videos.items, categories=categories, next_url=next_url, prev_url=prev_url, url=url_for('admin.add_video'))


@admin.route('/videos/add', methods=['POST'])
@login_required
def add_video():
    form = VideoForm()

    if request.method == 'POST':
        if form.validate_on_submit:
            video = Video(title=form.title.data, slug=slugify(form.title.data), user_id=current_user.id, category_id=form.category.data)
            video.video = form.video.data
            video.description = form.description.data
            video.published = form.published.data
            Repository.save(video)
            flash("Vidéo ajoutée avec succès", 'success')
            return redirect(url_for('admin.videos'))
        else:
            flash('Formulaire incorrect', 'error')
    else:
        return redirect(url_for('admin.add_video'))


@admin.route('/videos/edit/<uid>', methods=['GET', 'POST'])
@login_required
def edit_video(uid):
    page = request.args.get('page', 1, type=int)
    if current_user.is_admin:
        videos = Video.query.order_by(Video.created_at.desc()).paginate(page, Video.VIDEO_PER_PAGE, False)
    else:
        videos = Video.query.filter_by(user_id=current_user.id).order_by(Video.created_at.desc()).paginate(page, Video.VIDEO_PER_PAGE, False)
    next_url = url_for('admin.videos', page=videos.next_num) if videos.has_next else None
    prev_url = url_for('admin.videos', page=videos.prev_num) if videos.has_prev else None
    video = Video.query.filter_by(uid=uid).first()
    form = VideoForm(obj=video)
    categories = Category.query.all()
    if request.method == 'POST':
        if form.validate_on_submit:
            video.title = form.title.data
            video.video = form.video.data
            slug_title = slugify(form.title.data)
            video.slug = slug_title
            video.description = form.description.data
            video.category_id = form.category.data
            video.published = form.published.data
            Repository.save(video)
            flash("Vidéo modifiée avec succès", 'success')
            return redirect(url_for('admin.videos'))
        else:
            flash('Formulaire incorrect', 'error')
    return render_template('admin/videos/videos.html', form=form, videos=videos.items, categories=categories, next_url=next_url, prev_url=prev_url, url=url_for('admin.edit_video', uid=uid), video=video)


@admin.route('/videos/delete/<uid>')
@login_required
def delete_video(uid):
    video = Video.query.filter_by(uid=uid).first()
    Repository.delete(video)
    flash("Vidéo supprimée avec succès", 'success')
    return redirect(url_for('admin.videos'))
