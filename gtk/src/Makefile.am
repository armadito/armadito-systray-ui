AUTOMAKE_OPTIONS=subdir-objects

bin_PROGRAMS= indicator-armadito

AM_CFLAGS= @GLIB2_CFLAGS@ @GMODULE2_CFLAGS@ @GIO2_CFLAGS@ 
LIBS     = @GLIB2_LIBS@ @GMODULE2_LIBS@ @GIO2_LIBS@

indicator_armadito_CFLAGS= $(AM_CFLAGS) -DSVG_ICON_PATH=\"$(datarootdir)/icons/hicolor/scalable/apps\" -DPROGRAMNAME_LOCALEDIR=\"${PROGRAMNAME_LOCALEDIR}\"
indicator_armadito_LDADD=
if USE_GTK3
indicator_armadito_CFLAGS+= $(GTK3_CFLAGS)
indicator_armadito_LDADD+= $(GTK3_LIBS)
else
if USE_GTK2
indicator_armadito_CFLAGS+= $(GTK2_CFLAGS)
indicator_armadito_LDADD+= $(GTK2_LIBS)
endif
endif

if USE_APPINDICATOR_3
indicator_armadito_CFLAGS+= $(APPINDICATOR3_CFLAGS)
indicator_armadito_LDADD+= $(APPINDICATOR3_LIBS)
else
if USE_APPINDICATOR
indicator_armadito_CFLAGS+= $(APPINDICATOR_CFLAGS)
indicator_armadito_LDADD+= $(APPINDICATOR_LIBS)
endif
endif

indicator_armadito_CFLAGS+= $(LIBNOTIFY_CFLAGS)
indicator_armadito_LDADD+= $(LIBNOTIFY_LIBS)

nodist_indicator_armadito_SOURCES = \
	resource.h \
	resource.c

indicator_armadito_SOURCES = \
	app.c \
	app.h \
	main.c

BUILT_SOURCES = $(nodist_indicator_armadito_SOURCES)
CLEANFILES = $(nodist_indicator_armadito_SOURCES)

UI_RESOURCES = \
	$(top_srcdir)/resource/indicator-armadito.gresource.xml \
	$(top_srcdir)/ui/indicator-armadito.ui

GLIB_COMPILE_RESOURCES=glib-compile-resources --sourcedir=$(top_srcdir) --internal --c-name indicator_armadito

resource.c: Makefile $(UI_RESOURCES)
	$(GLIB_COMPILE_RESOURCES) --generate-source --target=$@ $(top_srcdir)/resource/indicator-armadito.gresource.xml

resource.h: Makefile $(UI_RESOURCES)
	$(GLIB_COMPILE_RESOURCES) --generate-header --target=$@ $(top_srcdir)/resource/indicator-armadito.gresource.xml
