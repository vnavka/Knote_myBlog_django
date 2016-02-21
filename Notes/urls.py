from django.conf.urls import patterns, include, url
import views

urlpatterns = [
    url(r'^$','Notes.views.landing_page'),
    url(r'^statistic/$','Notes.views.statistic_page'),

    url(r'^registration/$','Notes.views.register'),
    url(r'^registration/reg_user/$','Notes.views.register_user_post'),
    url(r'^registration_test/$','Notes.views.test_registr'),
    url(r'^login/$','Notes.views.login_user'),
    url(r'^logout/$','Notes.views.logout_user'),

    url(r'^home/$','Notes.views.show_user'),
    url(r'^home/knote/(?P<knote_id>\d+)/$','Notes.views.process_knote_comment'),
    url(r'^home/knote_del/(?P<knote_id>\d+)/$','Notes.views.process_knote_del'),
    url(r'^home/knote_edit/(?P<knote_id>\d+)/$','Notes.views.edit_knote'),
    url(r'^home/knote_edit/save/$','Notes.views.edit_knote_save'),

    url(r'^home/add_comment/$','Notes.views.add_comment'),

    url(r'^ImgEdit/$','Notes.views.imgUpload'),
    url(r'^upload/$','Notes.views.upload'),

    url(r'^AddNote/$','Notes.views.add_knote'),
    url(r'^AddNote/adding_note/$','Notes.views.process_knote'),

    url(r'^dump_db/$','Notes.views.dump_db'),
    url(r'^load_db/$','Notes.views.load_db'),
    url(r'^fill_db/$','Notes.views.fill_db'),

    url(r'^people/$','Notes.views.show_users'),
    url(r'^people/view/(?P<person_id>\d+)/$','Notes.views.person_notes'),
    url(r'^knotes/$','Notes.views.show_knotes'),
    url(r'^knotes/search/$','Notes.views.search_knotes'),







]

