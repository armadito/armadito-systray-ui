#ifndef APP_H_
#define APP_H_

struct a6o_indicator_app;

struct a6o_indicator_app *a6o_indicator_app_new(void);

int a6o_indicator_app_run(struct a6o_indicator_app *app);

void a6o_indicator_app_free(struct a6o_indicator_app *app);

#endif
