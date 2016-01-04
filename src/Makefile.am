nodist_bin_SCRIPTS = assetxplorer
nodist_pkgdata_SCRIPTS = org.madbob.Assetxplorer

pydir = $(pkgdatadir)
dist_py_PYTHON = \
	main.py		\
	package.py	\
	util.py		\
	window.py

assetxplorer: assetxplorer.in
	$(AM_V_GEN) sed \
		-e "s|[@]PYTHON@|$(PYTHON)|g" \
		-e "s|[@]PACKAGE_VERSION@|$(PACKAGE_VERSION)|g" \
		-e "s|[@]prefix@|$(prefix)|g" \
		-e "s|[@]libdir@|$(libdir)|g" \
		-e "s|[@]pkgdatadir@|$(pkgdatadir)|g" \
		$< > $@
	@chmod +x $@

org.madbob.Assetxplorer: org.madbob.Assetxplorer.in
	$(AM_V_GEN) sed \
		-e "s|[@]PYTHON@|$(PYTHON)|g" \
		-e "s|[@]PACKAGE_VERSION@|$(PACKAGE_VERSION)|g" \
		-e "s|[@]prefix@|$(prefix)|g" \
		-e "s|[@]libdir@|$(libdir)|g" \
		-e "s|[@]pkgdatadir@|$(pkgdatadir)|g" \
		$< > $@
	@chmod +x $@

EXTRA_DIST = org.madbob.Assetxplorer.in assetxplorer.in
CLEANFILES = org.madbob.Assetxplorer assetxplorer

-include $(top_srcdir)/git.mk
