AC_INIT(indicator-armadito, 0.12.0-exp, armadito-av-dev@gna.org,, https://github.com/armadito/armadito-gui)

AM_INIT_AUTOMAKE([foreign])

# collect arguments
# debug
AC_ARG_ENABLE([debug],
	AS_HELP_STRING([--enable-debug],[enable debugging @<:@default is no@:>@]),
	,
	enable_debug="no")
# gtk version
AC_ARG_WITH([gtk],
	[AS_HELP_STRING([--with-gtk=gtk2|gtk3|check], [gtk2 or gtk3 support @<:@default=check@:>@])],
	,
	with_gtk="check")
# appindicator version
AC_ARG_WITH([appindicator],
	[AS_HELP_STRING([--with-appindicator=appindicator|appindicator3|check], [appindicator or appindicator3 support @<:@default=check@:>@])],
	,
	with_appindicator="check")

# check for needed programs
AC_PROG_CC([gcc])
AC_PROG_LIBTOOL

# start with clean CFLAGS
CFLAGS=

# check for debug
AC_MSG_CHECKING(for debug)
AC_MSG_RESULT($enable_debug)
AM_CONDITIONAL([DEBUG], [test "$enable_debug" = "yes"])
if test "$enable_debug" = "yes"; then
   	AC_DEFINE(DEBUG,1,[Define DEBUG to enable debug messages])
	CFLAGS="${CFLAGS} -g"
fi

PKG_PROG_PKG_CONFIG

# check for libcurl
PKG_CHECK_MODULES(LIBCURL, libcurl, [HAVE_LIBCURL=yes], [HAVE_LIBCURL=no])
if test "$HAVE_LIBCURL" = "no"; then
   	AC_MSG_ERROR("cannot find libcurl library")
fi

# check for json-c library
PKG_CHECK_MODULES(LIBJSONC, json-c, [HAVE_LIBJSONC=yes], [HAVE_LIBJSONC=no])
if test "$HAVE_LIBJSONC" = "no"; then
   	AC_MSG_ERROR("cannot find json-c library")
fi

# check for glib stuff
PKG_CHECK_MODULES(GLIB2, glib-2.0, [HAVE_GLIB2=yes], [HAVE_GLIB2=no])
if test "$HAVE_GLIB2" = "no"; then
   	AC_MSG_ERROR("cannot find glib2 library")
fi
PKG_CHECK_MODULES(GMODULE2, gmodule-2.0, [HAVE_GMODULE2=yes], [HAVE_GMODULE2=no])
if test "$HAVE_GMODULE2" = "no"; then
   	AC_MSG_ERROR("cannot find gmodule2 library")
fi
PKG_CHECK_MODULES(GIO2, gio-2.0 gio-unix-2.0, [HAVE_GIO2=yes], [HAVE_GIO2=no])
if test "$HAVE_GIO2" = "no"; then
   AC_MSG_ERROR("cannot find glib gio library")
fi

# check for gtk
AC_MSG_CHECKING(for Gtk required version)
AC_MSG_RESULT($with_gtk)
gtk_version="none"
case $with_gtk in
gtk2)
	PKG_CHECK_MODULES(GTK2, gtk+-2.0, [HAVE_GTK2=yes], [HAVE_GTK2=no])
	if test "$HAVE_GTK2" = "no" ; then
	   	AC_MSG_ERROR([--with-gtk=gtk2 required but gtk2 library not found])
	else
		gtk_version=gtk2
	fi
	;;
gtk3)
	PKG_CHECK_MODULES(GTK3, gtk+-3.0, [HAVE_GTK3=yes], [HAVE_GTK3=no])
	if test "$HAVE_GTK3" = "no" ; then
	   	AC_MSG_ERROR([--with-gtk=gtk3 required but gtk3 library not found])
	else
		gtk_version=gtk3
	fi
	;;
check)
	PKG_CHECK_MODULES(GTK3, gtk+-3.0, [HAVE_GTK3=yes], [HAVE_GTK3=no])
	if test "$HAVE_GTK3" = "yes" ; then
	   	gtk_version=gtk3
	else
		PKG_CHECK_MODULES(GTK2, gtk+-2.0, [HAVE_GTK2=yes], [HAVE_GTK2=no])
		if test "$HAVE_GTK2" = "no" ; then
		   	AC_MSG_ERROR([neither gtk3 nor gtk2 library found])
		else
			gtk_version=gtk2
		fi
	fi
	;;
*)
	AC_MSG_ERROR([unknown gtk version $with_gtk])
	;;
esac

AM_CONDITIONAL([USE_GTK3], [test "$gtk_version" = "gtk3"])
AM_CONDITIONAL([USE_GTK2], [test "$gtk_version" = "gtk2"])

# check for appindicator
AC_MSG_CHECKING(for appindicator required version)
AC_MSG_RESULT($with_appindicator)
appindicator_version="none"
case $with_appindicator in
appindicator)
	PKG_CHECK_MODULES(APPINDICATOR, appindicator-0.1, [HAVE_APPINDICATOR=yes], [HAVE_APPINDICATOR=no])
	if test "$HAVE_APPINDICATOR" = "no" ; then
	   	AC_MSG_ERROR([--with-appindicator=appindicator required but appindicator library not found])
	else
		appindicator_version=appindicator
	fi
	;;
appindicator3)
	PKG_CHECK_MODULES(APPINDICATOR3, appindicator3-0.1, [HAVE_APPINDICATOR3=yes], [HAVE_APPINDICATOR3=no])
	if test "$HAVE_APPINDICATOR3" = "no" ; then
	   	AC_MSG_ERROR([--with-appindicator=appindicator3 required but appindicator3 library not found])
	else
		appindicator_version=appindicator3
	fi
	;;
check)
	PKG_CHECK_MODULES(APPINDICATOR3, appindicator3-0.1, [HAVE_APPINDICATOR3=yes], [HAVE_APPINDICATOR3=no])
	if test "$HAVE_APPINDICATOR3" = "yes" ; then
	   	appindicator_version=appindicator3
	else
		PKG_CHECK_MODULES(APPINDICATOR, appindicator-0.1, [HAVE_APPINDICATOR=yes], [HAVE_APPINDICATOR=no])
		if test "$HAVE_APPINDICATOR" = "no" ; then
		   	AC_MSG_ERROR([neither appindicator3 nor appindicator library found])
		else
			appindicator_version=appindicator
		fi
	fi
	;;
*)
	AC_MSG_ERROR([unknown appindicator version $with_appindicator])
	;;
esac

AM_CONDITIONAL([USE_APPINDICATOR_3], [test "$appindicator_version" = "appindicator3"])
AM_CONDITIONAL([USE_APPINDICATOR], [test "$appindicator_version" = "appindicator"])


# Output files
AC_CONFIG_FILES([
Makefile
src/Makefile
])
AC_OUTPUT
