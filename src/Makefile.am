## Process this file with automake to produce Makefile.in
## Created by Anjuta




## Directory where .class files will be installed
open_electronic_workbenchdir = $(pythondir)/open_electronic_workbench


open_electronic_workbench_PYTHON = \
	open_electronic_workbench.py \
	open_electronic_workbench.ui


EXTRA_DIST = $(ui_DATA)


# Remove ui directory on uninstall
uninstall-local:

	-rm -r $(uidir)

	-rm -r $(pkgdatadir)
