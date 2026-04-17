import json
import re
import shutil
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

import runner
import uninstaller
from catalog import (
    full_catalog,
    load_default_catalog,
    load_user_catalog,
    save_user_catalog,
)
from paths import (
    BIN_DIR,
    CONFIG_DIR,
    INSTALLED_EXE,
    SELECTED_FILE,
    STARTUP_DIR,
    STARTUP_VBS,
)
from version import APP_VERSION


APP_TITLE = "Hotaru's Daily Attendance"


def _slugify(text: str) -> str:
    s = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE).strip().lower()
    s = re.sub(r"[\s-]+", "_", s)
    return s or "game"


class _AddGameDialog(tk.Toplevel):
    def __init__(self, parent: tk.Misc):
        super().__init__(parent)
        self.title("Add Custom Game")
        self.resizable(False, False)
        self.transient(parent)

        self.result: tuple[str, str] | None = None

        frm = ttk.Frame(self, padding=14)
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="Game name").grid(row=0, column=0, sticky="w", pady=(0, 6))
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(frm, textvariable=self.name_var, width=42)
        name_entry.grid(row=0, column=1, sticky="ew", padx=(8, 0), pady=(0, 6))

        ttk.Label(frm, text="Attendance URL").grid(row=1, column=0, sticky="w", pady=(0, 12))
        self.url_var = tk.StringVar()
        url_entry = ttk.Entry(frm, textvariable=self.url_var, width=42)
        url_entry.grid(row=1, column=1, sticky="ew", padx=(8, 0), pady=(0, 12))

        btn_row = ttk.Frame(frm)
        btn_row.grid(row=2, column=0, columnspan=2, sticky="e")
        ttk.Button(btn_row, text="Cancel", command=self._cancel).pack(side="right", padx=(6, 0))
        ttk.Button(btn_row, text="Add", command=self._ok).pack(side="right")

        self.bind("<Return>", lambda _e: self._ok())
        self.bind("<Escape>", lambda _e: self._cancel())
        self.protocol("WM_DELETE_WINDOW", self._cancel)

        self.update_idletasks()
        try:
            px, py = parent.winfo_rootx(), parent.winfo_rooty()
            pw, ph = parent.winfo_width(), parent.winfo_height()
            w, h = self.winfo_reqwidth(), self.winfo_reqheight()
            self.geometry(f"+{px + (pw - w) // 2}+{py + (ph - h) // 2}")
        except tk.TclError:
            pass

        name_entry.focus_set()
        self.grab_set()
        self.wait_window()

    def _ok(self) -> None:
        name = self.name_var.get().strip()
        url = self.url_var.get().strip()
        if not name or not url:
            messagebox.showwarning(
                "Add Custom Game", "Both name and URL are required.", parent=self
            )
            return
        self.result = (name, url)
        self.destroy()

    def _cancel(self) -> None:
        self.result = None
        self.destroy()


class InstallerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title(f"{APP_TITLE}  v{APP_VERSION}")
        root.geometry("520x480")
        root.minsize(480, 400)

        self.vars: dict[str, tk.BooleanVar] = {}
        self._default_ids: set[str] = set()

        self._build_ui()
        self._reload_games()

        root.lift()
        root.focus_force()

    def _build_ui(self) -> None:
        header = ttk.Label(
            self.root,
            text="Select the attendance pages to open automatically on each daily first login.",
            padding=(12, 10, 12, 2),
        )
        header.pack(fill="x")

        version_label = ttk.Label(
            self.root,
            text=f"v{APP_VERSION}",
            padding=(12, 0, 12, 6),
            foreground="#888",
        )
        version_label.pack(fill="x")

        container = ttk.Frame(self.root, padding=(12, 4))
        container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(container, highlightthickness=0, borderwidth=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.list_frame = ttk.Frame(self.canvas)
        self.list_frame.bind(
            "<Configure>",
            lambda _e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.create_window((0, 0), window=self.list_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        btn_row = ttk.Frame(self.root, padding=(12, 6))
        btn_row.pack(fill="x")
        ttk.Button(btn_row, text="+ Add Custom Game", command=self._add_custom).pack(side="left")
        ttk.Button(btn_row, text="Uninstall", command=self._uninstall).pack(side="right")
        ttk.Button(btn_row, text="Install / Update", command=self._install).pack(side="right", padx=6)

        self.status = ttk.Label(self.root, text="", padding=(12, 4), foreground="#666")
        self.status.pack(fill="x")

    def _reload_games(
        self,
        *,
        preserve_current: bool = False,
        extra_checked: set[str] | None = None,
    ) -> None:
        carry_over: set[str] = set()
        if preserve_current:
            carry_over = {gid for gid, var in self.vars.items() if var.get()}
        if extra_checked:
            carry_over |= extra_checked

        for child in self.list_frame.winfo_children():
            child.destroy()
        self.vars.clear()

        self._default_ids = {g["id"] for g in load_default_catalog()}

        if preserve_current:
            initially_checked = carry_over
        else:
            initially_checked = set()
            if SELECTED_FILE.exists():
                try:
                    with open(SELECTED_FILE, encoding="utf-8") as f:
                        initially_checked = set(json.load(f))
                except (OSError, json.JSONDecodeError):
                    pass
            initially_checked |= carry_over

        games = full_catalog()
        if not games:
            ttk.Label(
                self.list_frame,
                text="No games registered. Add a custom game.",
            ).pack(pady=20)
            self._update_scrollregion()
            return

        for game in games:
            var = tk.BooleanVar(value=game["id"] in initially_checked)
            self.vars[game["id"]] = var

            row = ttk.Frame(self.list_frame)
            row.pack(fill="x", pady=3, padx=2)

            is_custom = game["id"] not in self._default_ids
            label = game["name"] + ("  [custom]" if is_custom else "")
            ttk.Checkbutton(row, text=label, variable=var).pack(side="left", anchor="w")

            if is_custom:
                ttk.Button(
                    row,
                    text="×",
                    width=2,
                    command=lambda gid=game["id"]: self._remove_custom(gid),
                ).pack(side="right", padx=(4, 0))

            url_disp = game["url"]
            if len(url_disp) > 46:
                url_disp = url_disp[:43] + "..."
            ttk.Label(row, text=url_disp, foreground="#888").pack(side="right", padx=6)

        self._update_scrollregion()

    def _update_scrollregion(self) -> None:
        self.list_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event: tk.Event) -> None:
        try:
            self.canvas.yview_scroll(-1 * (event.delta // 120), "units")
        except tk.TclError:
            pass

    def _add_custom(self) -> None:
        dialog = _AddGameDialog(self.root)
        if dialog.result is None:
            return
        name, url = dialog.result

        defaults = load_default_catalog()
        users = load_user_catalog()
        all_games = defaults + users

        if any(g.get("url", "").strip().lower() == url.lower() for g in all_games):
            messagebox.showinfo(APP_TITLE, "A game with this URL already exists.")
            return

        base_id = f"custom_{_slugify(name)}"
        existing_ids = {g["id"] for g in all_games}
        gid = base_id
        suffix = 2
        while gid in existing_ids:
            gid = f"{base_id}_{suffix}"
            suffix += 1

        users.append({"id": gid, "name": name, "url": url})
        save_user_catalog(users)
        self._reload_games(preserve_current=True, extra_checked={gid})
        self._set_status(f"Added: {name}")

    def _remove_custom(self, gid: str) -> None:
        users = [g for g in load_user_catalog() if g["id"] != gid]
        save_user_catalog(users)
        self._reload_games(preserve_current=True)
        self._set_status("Custom game removed.")

    def _install(self) -> None:
        selected = [gid for gid, var in self.vars.items() if var.get()]
        if not selected:
            messagebox.showwarning(APP_TITLE, "Select at least one game.")
            return

        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        BIN_DIR.mkdir(parents=True, exist_ok=True)
        STARTUP_DIR.mkdir(parents=True, exist_ok=True)

        with open(SELECTED_FILE, "w", encoding="utf-8") as f:
            json.dump(selected, f, ensure_ascii=False, indent=2)

        if getattr(sys, "frozen", False):
            src_exe = Path(sys.executable).resolve()
            if src_exe != INSTALLED_EXE.resolve() or not INSTALLED_EXE.exists():
                try:
                    shutil.copy2(src_exe, INSTALLED_EXE)
                except shutil.SameFileError:
                    pass
            target_cmd = f'"{INSTALLED_EXE}" --run'
        else:
            python_exe = sys.executable
            main_py = Path(__file__).resolve().parent / "main.py"
            target_cmd = f'"{python_exe}" "{main_py}" --run'

        vbs_line = 'CreateObject("Wscript.Shell").Run "{}", 0, False\r\n'.format(
            target_cmd.replace('"', '""')
        )
        STARTUP_VBS.write_text(vbs_line, encoding="utf-8")

        try:
            runner.run()
        except Exception:
            pass

        self._set_status("Installation complete.")
        messagebox.showinfo(
            APP_TITLE,
            "Installation complete.\nThe selected pages have been opened once as a test.",
        )

    def _uninstall(self) -> None:
        if not messagebox.askyesno(
            APP_TITLE,
            "Are you sure you want to uninstall?\nAll settings and history will be deleted.",
        ):
            return
        removed = uninstaller.run()
        if removed:
            self._set_status("Uninstalled.")
            messagebox.showinfo(
                APP_TITLE,
                "Uninstalled.\nSome files may still be in use. Close this window and verify that no files remain.",
            )
        else:
            self._set_status("No installation found to remove.")
        self._reload_games()

    def _set_status(self, text: str) -> None:
        self.status.config(text=text)


def run() -> None:
    root = tk.Tk()
    InstallerApp(root)
    root.mainloop()
