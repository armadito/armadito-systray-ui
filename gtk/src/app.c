#include <stdlib.h>
#include <gio/gio.h>
#include <gtk/gtk.h>
#include <libappindicator/app-indicator.h>

#include "app.h"
#include "resource.h"

#define APP_ID "org.armadito.indicator"
#define PROGRAM_NAME "indicator-armadito"
#define RESOURCE_ROOT "/org/armadito/indicator"
#define UI_RESOURCE_PATH RESOURCE_ROOT "/ui/indicator-armadito.ui"

struct a6o_indicator_app {
	GtkApplication *gtk_app;
};

static GResource *load_resource(struct a6o_indicator_app *app)
{
	GResource *resource;

	resource = indicator_armadito_get_resource();
	if (!resource) {
		g_message("Failed to load resources");
		g_application_quit(G_APPLICATION(app->gtk_app));

		return NULL;
	}

	g_message("Loaded resources");

	return resource;
}

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

	g_message("Loaded UI builder");

	return builder;
}

#if 0
	GtkWidget *indicator_menu
	indicator_menu = GTK_WIDGET(gtk_builder_get_object(builder, "indicator-menu"));
#endif

static void a6o_indicator_app_init(struct a6o_indicator_app *app)
{
	GResource *resource;
	GtkBuilder *builder;
	GtkWidget *indicator_menu;

	if ((resource = load_resource(app)) == NULL)
		return;

	if ((builder = get_builder(app)) == NULL)
		return;

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
	g_debug("indicator_title");
}

G_MODULE_EXPORT void indicator_toggle(GtkAction *action, gpointer user_data)
{
	g_debug("indicator_toggle");
}

G_MODULE_EXPORT void indicator_status(GtkAction *action, gpointer user_data)
{
	g_debug("indicator_status");
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
