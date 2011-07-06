// This file is part of Fleeting Password Manager (FleetingPM).
// Copyright (C) 2011 Jussi Lind <jussi.lind@iki.fi>
//
// FleetingPM is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// FleetingPM is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with FleetingPM. If not, see <http://www.gnu.org/licenses/>.
//

#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

class SettingsDlg;
class QPushButton;
class QComboBox;
class QLineEdit;
class QTimeLine;

//! The main window.
class MainWindow : public QMainWindow
{
    Q_OBJECT

public:

    //! Constructor
    explicit MainWindow(QWidget * parent = 0);

    //! Destructor
    ~MainWindow();

private:

    //! Init the background image.
    void initBackground();

    //! Init the widgets.
    void initWidgets();

    //! Create menus and actions.
    void initMenu();

    //! Load settings by using QSettings.
    void loadSettings();

    //! Save settings by using QSettings.
    void saveSettings();

    //! Show the password for this long.
    int m_defaultDelay;

    //! Default lenght of the password.
    int m_defaultLength;

    //! "Remove.." text of the remove/remember button.
    QString m_removeText;

    //! "Remember.." text of the remove/remember button.
    QString m_rememberText;

    //! "Remember.."-tooltip of the remove/remember button.
    QString m_rememberToolTip;

    //! "Remove.."-tooltip of the remove/remember button.
    QString m_removeToolTip;

    //! Current delay.
    int m_delay;

    //! Current password length.
    int m_length;

    //! Copy generated password to the clip-board if true.
    bool m_autoCopy;

    //! Master password edit field
    QLineEdit * m_masterEdit;

    //! User name edit field
    QLineEdit * m_userEdit;

    //! Password edit field
    QLineEdit * m_passwdEdit;

    //! Url combo box
    QComboBox * m_urlCombo;

    //! Generate button
    QPushButton * m_genButton;

    //! Remember/remove button
    QPushButton * m_rmbButton;

    //! Time line used when showing the password.
    QTimeLine * m_timeLine;

    //! Settings dialog
    SettingsDlg * m_settingsDlg;

private slots:

    //! Generate the password.
    void doGenerate();

    //! Decrease the alpha of the color of the password by one.
    void decreasePasswordAlpha(int frame);

    //! Clear the generated password and disable the text field.
    void invalidate();

    //! Enable the generate-button.
    void enableGenButton();

    //! Enable the remember-button.
    void enableRmbButton();

    //! Remember or remove the active url/user-pair depending
    //! on the button state.
    void rememberOrRemoveLogin();

    //! Update the user field if the url/user-pair is known.
    void updateUser(const QString & url);

    //! Set the text for remember-button.
    void setRmbButtonText(const QString & url);

    //! Show the settings dialog.
    void showSettingsDlg();

    //! Show the about dialog.
    void showAboutDlg();

    //! Show the about Qt dialog.
    void showAboutQtDlg();
};

#endif // MAINWINDOW_H
