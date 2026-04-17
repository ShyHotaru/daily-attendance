# Hotaru's Daily Attendance

**English** | [한국어](README.ko.md) | [日本語](README.ja.md)

A small Windows utility that automatically opens your chosen game attendance pages **once per day** at first login.

## Features

- Registered in the Windows Startup folder — runs automatically at login
- **Runs only once per day** — logging out and back in won't re-open the pages
- Simple GUI for picking games and adding custom URLs

## Install

1. Download the latest `HTR_DA.exe` from [Releases](../../releases)
2. Run `HTR_DA.exe` → check the games you want → click **Install / Update**
3. The selected pages will open automatically from your next Windows login

## Adding a Custom Game

In the GUI, click **+ Add Custom Game** and enter a name and URL.

To remove a custom game, click the small **×** next to its row.

## Uninstall

- Open the GUI and click **Uninstall**, or
- From the command line: `HTR_DA.exe --uninstall`

## File Locations

| Purpose | Path |
|---------|------|
| Configuration | `%APPDATA%\HTR_AttendanceAuto\config\` |
| Daily-run flags | `%APPDATA%\HTR_AttendanceAuto\flags\` |
| Installed executable | `%APPDATA%\HTR_AttendanceAuto\bin\HTR_DA.exe` |
| Startup entry | `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\HTR_daily_attendance.vbs` |

## How It Works

At Windows login, the program first checks **whether it has already opened the attendance pages today**.

- If not yet → opens the configured pages in your default browser.
- If already → exits immediately without re-opening.

No background services or task schedulers — the "once per day" behavior is guaranteed through a simple file-based flag.

## Policy Notice

This tool only opens attendance pages in your default browser — it does **not** log in, click buttons, or submit data on your behalf.

Still, if you believe that opening a particular page through this tool conflicts with the site's terms of service or operational policy, please [open an issue](../../issues). The game will be removed from the default catalog.

## License

MIT

## Contributing

Contributions are always welcome. Please follow these steps:

1. Fork this repository
2. Create a new branch
3. Commit your changes
4. Open a Pull Request

For larger changes such as new features or structural modifications, please open an Issue first to discuss — it helps things move more smoothly.
