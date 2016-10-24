#include <stdlib.h>
#include <gio/gio.h>
#include <gtk/gtk.h>
#include <gdk-pixbuf/gdk-pixbuf.h>
#include <libappindicator/app-indicator.h>
#include <libnotify/notify.h>
#include <glib/gi18n.h>

#include "app.h"
#include "resource.h"

#define APP_ID "org.armadito.indicator"
#define NOTIFICATION_ID "notification-armadito"
#define INDICATOR_NAME "Armadito indicator"
#define PROGRAM_NAME "indicator-armadito"
#define INDICATOR_ICON PROGRAM_NAME ".svg"
#define ICON_FILE  SVG_ICON_PATH "/" PROGRAM_NAME ".svg"
#define RESOURCE_ROOT "/org/armadito/indicator"
#define UI_RESOURCE_PATH RESOURCE_ROOT "/ui/indicator-armadito.ui"

#if (!(GTK_MAJOR_VERSION >= 3 && GTK_MINOR_VERSION >= 10))
#error you need at least Gtk 3.10 to compile
#endif

struct a6o_indicator_app {
	GtkApplication *gtk_app;
	AppIndicator *indicator;
	NotifyNotification *notification;
};

static void a6o_indicator_app_notify(struct a6o_indicator_app *app, const char *summary, const char *body);

static GtkBuilder *get_builder(struct a6o_indicator_app *app)
{
	GtkBuilder *builder;

	builder = gtk_builder_new_from_resource(UI_RESOURCE_PATH);
	if (!builder) {
		g_message("Failed to get UI builder");
		g_application_quit(G_APPLICATION(app->gtk_app));

		return NULL;
	}

	gtk_builder_connect_signals(builder, app);

	g_debug("Loaded UI builder");

	return builder;
}

static GtkWidget *get_menu(struct a6o_indicator_app *app, GtkBuilder *builder)
{
	GtkWidget *menu;

	menu = GTK_WIDGET(gtk_builder_get_object(builder, "indicator-menu"));

	if (!menu) {
		g_message("Failed to get indicator menu");
		g_application_quit(G_APPLICATION(app->gtk_app));

		return NULL;
	}

	g_debug("Loaded indicator menu");

	return menu;
}

static AppIndicator *create_indicator(GtkWidget *menu)
{
	AppIndicator *indicator;

	indicator = app_indicator_new(INDICATOR_NAME, INDICATOR_ICON, APP_INDICATOR_CATEGORY_SYSTEM_SERVICES);

	app_indicator_set_icon_full(indicator,
				ICON_FILE,
				INDICATOR_NAME);
	app_indicator_set_menu(indicator, GTK_MENU(menu));
	app_indicator_set_status(indicator, APP_INDICATOR_STATUS_ACTIVE);

	return indicator;
}


static NotifyNotification *create_notification(const char *title)
{
	NotifyNotification *notification;
	GdkPixbuf *pixbuf;

	notification = notify_notification_new(title, "", NULL);
	pixbuf = gdk_pixbuf_new_from_file(ICON_FILE, NULL);

	if (pixbuf != NULL)
		notify_notification_set_image_from_pixbuf(notification, pixbuf);
	else
		g_warning("cannot load pixbuf from %s", ICON_FILE);

	g_debug("Notification: %s", title);

	return notification;
}

static void a6o_indicator_app_init(struct a6o_indicator_app *app)
{
	GtkBuilder *builder;
	GtkWidget *menu;

	if ((builder = get_builder(app)) == NULL)
		return;

	if ((menu = get_menu(app, builder)) == NULL)
		return;

	app->indicator = create_indicator(menu);

	app->notification = create_notification("Armadito");

	g_object_unref (builder);

	g_application_hold(G_APPLICATION(app->gtk_app));
}


static void startup_cb(GApplication *g_app, gpointer user_data)
{
	a6o_indicator_app_init((struct a6o_indicator_app *)user_data);
}

static void shutdown_cb(GApplication *g_app, gpointer user_data)
{
	struct a6o_indicator_app *app = (struct a6o_indicator_app *)user_data;
}

struct a6o_indicator_app *a6o_indicator_app_new(void)
{
	struct a6o_indicator_app *app;
	GApplicationFlags flags = G_APPLICATION_IS_SERVICE;

	notify_init(PROGRAM_NAME);

	app = malloc(sizeof(struct a6o_indicator_app));

	app->gtk_app = gtk_application_new(APP_ID, flags);

	if (app->gtk_app != NULL) {
		g_signal_connect(app->gtk_app, "startup", G_CALLBACK(startup_cb), app);
		g_signal_connect(app->gtk_app, "shutdown", G_CALLBACK(shutdown_cb), app);

		if (!g_application_register(G_APPLICATION(app->gtk_app), NULL, NULL))
			g_message(PROGRAM_NAME " cannot register");
	}

	return app;
}

G_MODULE_EXPORT void indicator_title(GtkAction *action, gpointer user_data)
{
	struct a6o_indicator_app *app = (struct a6o_indicator_app *)user_data;

	g_debug("indicator_title");

	a6o_indicator_app_notify(app, "user-action", "title");
}

G_MODULE_EXPORT void indicator_status(GtkAction *action, gpointer user_data)
{
	struct a6o_indicator_app *app = (struct a6o_indicator_app *)user_data;

	g_debug("indicator_status");

	a6o_indicator_app_notify(app, "user-action", "status");
}

G_MODULE_EXPORT void indicator_toggle(GtkAction *action, gpointer user_data)
{
	struct a6o_indicator_app *app = (struct a6o_indicator_app *)user_data;

	g_debug("indicator_toggle");

	a6o_indicator_app_notify(app, "user-action", "toggle");
}

static void a6o_indicator_app_notify(struct a6o_indicator_app *app, const char *summary, const char *body)
{
	if (!notify_notification_update(app->notification, summary, body, NULL)) {
		g_debug("cannot update notification");
	}

	if (!notify_notification_show(app->notification, NULL)) {
		g_debug("cannot show notification");
	}
}

int a6o_indicator_app_run(struct a6o_indicator_app *app)
{
	return g_application_run(G_APPLICATION(app->gtk_app), 0, NULL);
}

void a6o_indicator_app_free(struct a6o_indicator_app *app)
{
	g_object_unref(app->gtk_app);
	free(app);
}
