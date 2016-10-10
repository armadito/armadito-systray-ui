#include <stdlib.h>
#include <gio/gio.h>
#include <gtk/gtk.h>
#include <libappindicator/app-indicator.h>

#include "app.h"
#include "resource.h"

#define APP_ID "org.armadito.indicator"

#define PROGRAM_NAME "indicator-armadito"

struct a6o_indicator_app {
	GtkApplication *gtk_app;
};

static void startup_cb(GApplication *g_app, gpointer user_data)
{
	struct a6o_indicator_app *app = (struct a6o_indicator_app *)user_data;
	GResource *resource;

	resource = indicator_armadito_get_resource();
	if (!resource){
		g_message("Failed to load resources");
		g_application_quit(G_APPLICATION(app->gtk_app));

		return;
	}

	g_message("Loaded resources OK");
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
		g_signal_connect(app->gtk_app, "startup", G_CALLBACK(startup_cb), NULL);
		g_signal_connect(app->gtk_app, "shutdown", G_CALLBACK(shutdown_cb), NULL);

		if (!g_application_register(G_APPLICATION(app->gtk_app), NULL, NULL))
			g_message(PROGRAM_NAME " cannot register");
	}

	return app;
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
