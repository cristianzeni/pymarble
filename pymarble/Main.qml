import QtQuick
import QtQuick.Controls

Window {
    id: root
    width: 640; height: 540
    visible: true
    title: "SameGame PySide - Cristian Zeni"
    color: "#1a1a1a"

    // Funzione di traduzione REATTIVA
    function tr(key) {
        // Referenziando esplicitamente la proprietà, QML attiva il binding
        var dummy = lang ? lang.currentLanguage : ""
        return lang ? lang.text(key) : key
    }

    Column {
        anchors.fill: parent
        anchors.margins: 15
        spacing: 15

        Text {
            text: root.tr("score") + ": " + (gameBoard ? gameBoard.score : 0)
            font.pixelSize: 30; font.bold: true; color: "#ffffff"
            anchors.horizontalCenter: parent.horizontalCenter
        }

        GridView {
            id: gameGrid
            width: parent.width; height: parent.height - 160
            interactive: false
            cellWidth: Math.floor(width / 15); cellHeight: Math.floor(height / 10)
            model: gameBoard

            delegate: Item {
                id: delegateItem
                width: gameGrid.cellWidth; height: gameGrid.cellHeight

                property color ballColor: {
                    if (blockColor === 1) return "#ff4d4d"
                    if (blockColor === 2) return "#4dff4d"
                    if (blockColor === 3) return "#4d4dff"
                    return "transparent"
                }

                Rectangle {
                    anchors.centerIn: parent
                    anchors.verticalCenterOffset: 3
                    width: Math.min(parent.width, parent.height) * 0.7
                    height: width; radius: width / 2; color: "black"; opacity: 0.4
                    visible: blockColor !== 0
                }

                Rectangle {
                    id: sphere
                    anchors.centerIn: parent
                    width: Math.min(parent.width, parent.height) * 0.85; height: width
                    radius: width / 2; antialiasing: true; visible: blockColor !== 0
                    gradient: Gradient {
                        GradientStop { position: 0.0; color: Qt.lighter(delegateItem.ballColor, 1.4) }
                        GradientStop { position: 1.0; color: Qt.darker(delegateItem.ballColor, 1.6) }
                    }

                    MouseArea { id: ma; anchors.fill: parent; onClicked: gameBoard.handleBlockClick(index) }
                    scale: ma.pressed ? 0.85 : 1.0
                    Behavior on scale { NumberAnimation { duration: 100 } }
                }
            }
        }

        Row {
            anchors.horizontalCenter: parent.horizontalCenter
            spacing: 20

            Button {
                text: root.tr("restart")
                font.bold: true
                onClicked: {
                    gameBoard.resetGame()
                    gameOverOverlay.visible = false
                }
            }

            ComboBox {
                id: langSelector
                model: ["English", "Italian"]
                currentIndex: (lang && lang.currentLanguage === "English") ? 0 : 1
                width: 130

                // Cambio lingua istantaneo alla selezione
                onActivated: {
                    lang.currentLanguage = currentText
                }
            }
        }
    }

    Text {
        text: root.tr("made_by")
        font.pixelSize: 11; font.italic: true; color: "#666666"
        anchors.right: parent.right; anchors.bottom: parent.bottom; anchors.margins: 8
    }

    Rectangle {
        id: gameOverOverlay
        anchors.fill: parent; color: "#cc000000"; visible: false; z: 100
        MouseArea {
            anchors.fill: parent
            onClicked: (mouse) => mouse.accepted = true
        }

        Column {
            anchors.centerIn: parent; spacing: 25
            Text {
                text: root.tr("game_over")
                color: "white"; font.pixelSize: 48; font.bold: true; anchors.horizontalCenter: parent.horizontalCenter
            }
            Text {
                text: root.tr("final_score") + ": " + (gameBoard ? gameBoard.score : 0)
                color: "#4dff4d"; font.pixelSize: 24; anchors.horizontalCenter: parent.horizontalCenter
            }
            Button {
                text: root.tr("play_again")
                anchors.horizontalCenter: parent.horizontalCenter
                onClicked: {
                    gameBoard.resetGame()
                    gameOverOverlay.visible = false
                }
            }
        }
    }

    Connections {
        target: gameBoard
        function onGameOver() { gameOverOverlay.visible = true }
    }
}