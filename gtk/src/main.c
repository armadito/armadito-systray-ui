/***

Copyright (C) 2015, 2016 Teclib'

This file is part of Armadito gui.

Armadito gui is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Armadito gui is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Armadito gui.  If not, see <http://www.gnu.org/licenses/>.

***/

#include <glib/gi18n.h>
#include "app.h"

static void i18n_init(void)
{
	bindtextdomain(GETTEXT_PACKAGE, INDICATOR_ARMADITO_LOCALEDIR);
	bind_textdomain_codeset(GETTEXT_PACKAGE, "UTF-8");
	textdomain(GETTEXT_PACKAGE);
}

int main()
{
	struct a6o_indicator_app *indicator_app;

	i18n_init();

	indicator_app = a6o_indicator_app_new();

	return a6o_indicator_app_run(indicator_app);
}
