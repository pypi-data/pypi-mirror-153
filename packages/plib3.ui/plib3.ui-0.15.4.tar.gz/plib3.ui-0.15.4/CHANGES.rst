plib3.ui Change Log
===================

Version 0.15.4
--------------

- Add support for widgets from user-defined modules: in
  widget specs, any module with a dot "." in its name is
  treated as user-defined and looked up by its name directly
  instead of the module name being taken from the toolkit
  sub-package in use.

Version 0.15.3
--------------

- Change signature of ``truncate`` method of ``PTextOutput``
  to have ``size`` default to ``0``. Update ``pyidserver-ui``
  example program to use new default signature.

- Move sentinel object for signaling untitled file to
  ``PTextFile`` base class so it is commonly available.

Version 0.15.2
--------------

- Size dialogs to their controls immediately before display
  to ensure correct sizing (since control sizes may change
  when the dialog is populated with data).

Version 0.15.1
--------------

- Add ``dialogs`` module with base ``DialogRunner`` class
  and some standard dialogs. Update the preferences manager
  in the ``prefs`` module to inherit from ``DialogRunner``.

- Add support for naming container widgets (group box, panel,
  label box) and padding instead of using automatic names
  computed by number.

Version 0.15
------------

- Switch to ``setuputils_build`` PEP 517 build backend.

Version 0.14.2
--------------

- Add ``example`` module that uses the auto-construction facility
  for entry points from ``plib3.stdlib.postinstall`` for the
  example programs shipped with ``plib3.ui``. Remove the
  ``scripts`` source directory since the wrapper scripts for the
  example programs are now auto-constructed as entry points.

Version 0.14.1
--------------

- Fix importing of wrapped example modules from ``plib.stdlib``
  in ``pyidserver-ui3`` and ``scrips-edit3`` example programs.

Version 0.14
------------

- Add ``PImageView`` image view widget.

- Moved basic file open/save functionality into separate
  ``PFileAware`` class.

- Add support for multiple file filters in file open/save dialogs.

- Set parent widget correctly in application file dialogs.

- Add support for passing file names to open on command line
  of notepad and XML viewer example programs.

Version 0.13
------------

- Make ``plib`` an implicit namespace package per PEP 420.

- Update to PEP 517 build compatibility using ``setuputils``
  version 2.0 to build setup.cfg.

Version 0.12.1
--------------

- Update bug fix to correctly handle older PySide2 versions.

Version 0.12
------------

- Fix bug created by Qt5/PySide2 changing ``QSocketNotifier`` to pass
  a ``QSocketDescriptor`` object to notification handlers (instead of
  an ``int`` representing the socket's ``fileno``).

Version 0.11
------------

- Initial release, version numbering continued from ``plib3.gui``.
