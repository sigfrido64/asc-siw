# coding=utf-8
"""siw URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
# from boards import views
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views
from accounts.forms import LoginForm, MyPasswordResetForm, MySetPasswordForm, MyPasswordChangeForm
from .views import si_home


urlpatterns = [
    path('', si_home, name='home'),
    
    # Abilito il routing verso gli strumenti di amministrazione del sito.
    path('admin/', admin.site.urls),
    
    # Login e Logout, per semplicità li lascio sotto la home anche se sono gestiti in accounts.
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', form_class=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Gestione degli accounts.
    # ATTENZIONE : Siccome la gestione degli account con le viste di sistema ha una forte rigidità nel nome
    # dell'url che è scritto nel codice di Django non posso spostarla in accounts/ perchè poi gli url avrebbero
    # il prefisso accounts: che non viene recepito nelle viste di sistema.
    # Quindi anche se è una schifezza a livello di refactoring lo lascio qui.
    #
    #
    # Reset della password
    #
    path('reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
    re_path('^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            auth_views.PasswordResetConfirmView.as_view(
                template_name='accounts/password_reset_confirm.html', form_class=MySetPasswordForm),
            name='password_reset_confirm'),
    path('reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html',
         form_class=MyPasswordResetForm, email_template_name='accounts/password_reset_email.html',
         subject_template_name='accounts/password_reset_subject.txt'), name='password_reset'),
    
    #
    # Registrazione dell'utente.
    #
    path('signup/', accounts_views.signup, name='signup', ),
    
    #
    # Dati utente.
    #
    re_path(r'^settings/account/$', accounts_views.UserUpdateView.as_view(template_name='accounts/my_account.html'),
            name='my_account'),
    re_path(r'^settings/password/$',
            auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html',
                                                  form_class=MyPasswordChangeForm),
            name='password_change'),
    re_path(r'^settings/password/done/$',
            auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
            name='password_change_done'),
    #
    # Inclusione app 'attesta'.
    #
    path('attesta/', include('attesta.urls', 'attesta')),

    #
    # Inclusione app 'amm'.
    #
    path('amm/', include('amm.urls', 'amm')),
    path('anagrafe/', include('anagrafe.urls', 'anagrafe')),
    path('collaboratori/', include('collaboratori.urls', 'collaboratori')),
    path('corsi/', include('corsi.urls', 'corsi')),
]

"""
# path('', views.BoardListView.as_view(), name='home'),


#
# TODO : Vecchi path che probabilmente posso eliminare !
#
re_path(r'^boards/(?P<pk>\d+)/$', views.TopicListView.as_view(), name='board_topics'),
re_path(r'^boards/(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),
re_path(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', views.PostListView.as_view(), name='topic_posts'),
re_path(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', views.reply_topic, name='reply_topic'),
re_path(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$',
        views.PostUpdateView.as_view(), name='edit_post')

"""