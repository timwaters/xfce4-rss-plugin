plugindir = $(libexecdir)/xfce4/panel-plugins
dist_plugin_SCRIPTS = xfce4-rss-plugin.py

rssplugindir = $(pythondir)/xfce4/rssplugin
dist_rssplugin_PYTHON =		\
	__init__.py		\
	plugin.py		\
	props.py		\
	config.py
nodist_rssplugin_PYTHON =	\
	globals.py

globals.py: globals.py.in
	sed -e "s^%name%^@PACKAGE@^" \
	    -e "s^%version%^@VERSION@^" \
	    -e "s^%localedir%^${localedir}^" \
	    < $< > $@

EXTRA_DIST = globals.py.in

# .desktop file
#
# Some automake trickery here. Because we cannot use $(libexecdir) in the
# automake stage, we'll use sed to get the full path into the .desktop file.
# We also need to let intltool merge the translated fields, so we add an
# additional level of indirection: a <name>.desktop.in.in file.
# 
desktop_in_in_files = rss.desktop.in.in
desktop_in_files = $(desktop_in_in_files:.desktop.in.in=.desktop.in)

desktopdir = $(datadir)/xfce4/panel-plugins
desktop_DATA = $(desktop_in_files:.desktop.in=.desktop)
@INTLTOOL_DESKTOP_RULE@

EXTRA_DIST += $(desktop_in_in_files)

DISTCLEANFILES = \
	$(desktop_DATA) $(desktop_in_files)

# get full path into .desktop file
%.desktop.in: %.desktop.in.in
	sed -e "s^@PLUGIN_PATH@^$(libexecdir)/xfce4/panel-plugins^" \
		$< > $@
