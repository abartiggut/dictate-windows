# Dictate Windows

**Sprache lokal in Text umwandeln und direkt in ein beliebiges Eingabefeld diktieren.**

Windows-Version von [winidi/dictate](https://github.com/winidi/dictate), gepflegt von [abartiggut](https://github.com/abartiggut).

**Dieser Fork wird ausschliesslich für Windows gepflegt, getestet und unterstützt.** Für macOS findest du die Hinweise im [Originalrepo von winidi/dictate](https://github.com/winidi/dictate#readme). Mac-Anleitungen und Mac-Support werden in diesem Fork nicht angeboten. Auch die ursprüngliche Linux-Dokumentation findest du direkt im Originalrepo.

Die deutsche Spracherkennung läuft mit Parakeet auf deiner CPU. Nach dem einmaligen Download ist sie offline nutzbar: keine GPU, kein API-Key und kein Audio-Upload. Ein Chatdienst wie Codex verarbeitet den anschliessend gesendeten Text weiterhin über seinen eigenen Dienst.

## Installation unter Windows

Voraussetzungen: Windows 10/11, **Python 3.12 in der 64-Bit-Version** und ein Mikrofon. Getestet wurde mit Python 3.12 auf Windows; andere Python-Versionen sind für diesen Installer nicht vorgesehen.

1. [Python 3.12 für Windows](https://www.python.org/downloads/windows/) installieren. Den Python-Launcher mitinstallieren.
2. Dieses Repository über **Code → Download ZIP** herunterladen und vollständig in einen beschreibbaren Ordner entpacken. Alternativ:

   ```powershell
   git clone https://github.com/abartiggut/dictate-windows.git
   cd dictate-windows
   ```

3. **install-windows.cmd** doppelklicken. Das installiert die Python-Pakete in einer eigenen `.venv` und lädt das deutsche Modell herunter, einmalig rund 640 MB. Für die Installation wird Internet benötigt.
4. **start-windows.cmd** doppelklicken.

Bei einer neuen Installation ist die lokale Erkennung voreingestellt. Vorhandene Dictate-Einstellungen bleiben erhalten. Bei Bedarf unter Settings den Anbieter **Local (Parakeet DE, CPU offline)** auswählen und mit Save speichern.

## Diktieren

1. In das gewünschte Nachrichtenfeld, Dokument oder andere Textfeld klicken.
2. **F9 gedrückt halten**, sprechen und F9 loslassen.
3. Den eingefügten Text prüfen. Die Nachricht wird nicht automatisch gesendet.

Ist beim Diktieren das **Dictate-Fenster selbst aktiv**, bleibt der Text unter **Last transcription** stehen. Mit **Text kopieren** und anschliessend **Ctrl+V** kannst du ihn im gewünschten Feld einfügen. Dictate tippt nicht in seine eigenen Bedienelemente.

Das Schliessen des Fensters lässt Dictate im Windows-Infobereich weiterlaufen. Zum Beenden das Mikrofon-Symbol rechtsklicken und **Quit** wählen. Das Windows-Standardmikrofon wird verwendet.

## Anpassungen dieser Windows-Version

- Plattformübergreifende Instanzsperre mit Qt statt Unix-`fcntl`.
- Windows-Installer und Startskript mit getrennten Python-Abhängigkeiten.
- Offline-Erkennung als Voreinstellung bei neuen Installationen.
- Die gewählte Funktionstaste wird unter Windows abgefangen, damit sie nicht gleichzeitig eine Aktion im aktiven Programm auslöst. Andere Tasten werden weitergegeben.
- Schutz gegen Einfügen in Dictates eigenes Fenster, Kopierbutton und Hinweise zum Eingabefokus.
- Lesbarer Ergebnistext auch bei dunklem Windows-Design.
- Weiterlaufen im Infobereich beim Schliessen des Fensters.

Die ursprünglichen Cloud-Anbieter Groq, OpenAI und Yorik sind weiterhin vorhanden und benötigen jeweils ihre eigene Konfiguration. Die Windows-Installation verwendet sie nicht automatisch. Maus-Seitentasten werden vom ursprünglichen Linux-evdev-Backend unterstützt; unter Windows verwende eine Funktionstaste.

## Wenn kein Text erscheint

- Im Dictate-Fenster auf **Last transcription** schauen. Ist dort Text sichtbar, funktioniert die Erkennung; das Ziel-Eingabefeld hatte möglicherweise keinen Fokus.
- Unter Settings **Local (Parakeet DE, CPU offline)** und **Installed and ready** prüfen. Für diesen Anbieter ist kein API-Key erforderlich.
- Das Windows-Standardmikrofon und den Mikrofonzugriff für Desktop-Apps in den Windows-Einstellungen prüfen.
- Dictate und das Zielprogramm mit normalen Benutzerrechten starten. Ein Zielprogramm mit Administratorrechten kann die Tastatureingabe eines nicht erhöhten Programms blockieren.
- Das Modell ist auf Deutsch ausgelegt. Eigennamen und Schweizerdeutsch können Korrekturen benötigen.

## Lokale Daten

| Inhalt | Pfad |
| --- | --- |
| Einstellungen | `%USERPROFILE%\.config\dictate\config.json` |
| Spracherkennungsmodell | `%USERPROFILE%\.local\share\dictate\models\parakeet-primeline-onnx` |
| Diagnoseprotokoll | `%USERPROFILE%\.local\state\dictate\dictate.log` |
| Bis zu drei fehlgeschlagene Audioaufnahmen | `%USERPROFILE%\.local\state\dictate\failed` |

Erfolgreiche Diktate werden nicht als Audio gespeichert. Das Protokoll enthält technische Messwerte, keinen erkannten Text. Fehlgeschlagene, nicht stumme Aufnahmen können lokal gespeichert werden. Bei Auswahl eines Cloud-Anbieters wird Audio an diesen Anbieter übertragen.

## Entwicklung und Tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Die Regressionstests prüfen die Funktionstasten-Behandlung, den Schutz vor Einfügen ins eigene Fenster, den Kopierbutton und das Beibehalten bestehender Einstellungen. Echte Mikrofonaufnahmen und die Erkennungsqualität sind nicht Teil dieser Tests. Die lokale Erkennung wurde bei der Einrichtung zusätzlich mit synthetischer deutscher Sprache und echten Diktaten geprüft; kurze Aufnahmen wurden auf dem Testrechner in rund 0,1–0,4 Sekunden transkribiert. Das ist keine Garantie für andere Rechner oder Mikrofone.

## Herkunft und Lizenz

Ausgangsstand: [`56ac487`](https://github.com/winidi/dictate/commit/56ac48730d3b206e2d1aa8ad39decf5cab9cbd6d) von **winidi**. Der ursprüngliche MIT-Lizenztext bleibt in [LICENSE](LICENSE) erhalten.

Das Modell wird nicht mit diesem Repository verteilt, sondern beim Setup aus einer festgelegten Hugging-Face-Version geladen. Attribution des Modells (CC-BY-4.0): [primeline / parakeet-primeline-onnx](https://huggingface.co/flozen1981/parakeet-primeline-onnx), basierend auf [NVIDIA Parakeet](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3). Laufzeit: [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx).
