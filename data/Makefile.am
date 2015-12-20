# I chose to use recursive automake so I can use nobase_ and avoid
# 5 different directory declarations
SUBDIRS = icons

resource_files = $(shell $(GLIB_COMPILE_RESOURCES) --sourcedir=$(srcdir) --generate-dependencies $(srcdir)/org.madbob.Assetxplorer.data.gresource.xml)
org.madbob.Assetxplorer.data.gresource: org.madbob.Assetxplorer.data.gresource.xml $(resource_files)
	$(AM_V_GEN) $(GLIB_COMPILE_RESOURCES) --target=$@ --sourcedir=$(srcdir) $<

resourcedir = $(pkgdatadir)
resource_DATA = org.madbob.Assetxplorer.data.gresource

appsdir = $(datadir)/applications
apps_DATA = org.madbob.Assetxplorer.desktop

@INTLTOOL_DESKTOP_RULE@

gsettings_SCHEMAS = org.madbob.Assetxplorer.gschema.xml

@GSETTINGS_RULES@

appdatadir = $(datadir)/appdata
appdata_DATA = org.madbob.Assetxplorer.appdata.xml

@INTLTOOL_XML_RULE@

org.madbob.Assetxplorer.service: org.madbob.Assetxplorer.service.in
	$(AM_V_GEN) sed \
		-e "s|[@]pkgdatadir@|$(pkgdatadir)|g" \
		-e "s|[@]pkglibdir@|$(pkglibdir)|g" \
		-e "s|[@]bindir@|$(bindir)|g" \
		$< > $@

servicedir = $(datadir)/dbus-1/services
service_DATA = org.madbob.Assetxplorer.service

EXTRA_DIST = \
	org.madbob.Assetxplorer.desktop.in \
	org.madbob.Assetxplorer.service.in \
	org.madbob.Assetxplorer.data.gresource.xml \
	$(gsettings_SCHEMAS) \
	org.madbob.Assetxplorer.appdata.xml.in \
	$(resource_files)

CLEANFILES = \
	org.madbob.Assetxplorer.service \
	org.madbob.Assetxplorer.data.gresource \
	org.madbob.Assetxplorer.appdata.xml \
	$(apps_DATA) \
	*.valid \
	gschemas.compiled

# For uninstalled use
all-local:
	$(GLIB_COMPILE_SCHEMAS) $(builddir)

-include $(top_srcdir)/git.mk
