#
# rules taken from: https://blog.kevin-brown.com/programming/2014/09/24/combining-autotools-and-setuptools.html
#

all-local:
	(\
		cd $(srcdir) ; \
		$(PYTHON) setup.py build \
			--build-base $(shell readlink -f $(builddir))/build \
			--verbose ; \
	)

install-exec-local:
	(\
		cd $(srcdir) ; \
		$(PYTHON) setup.py install \
			--prefix $(DESTDIR)$(prefix) \
			--single-version-externally-managed \
			--record /dev/null \
			--verbose ; \
	)
