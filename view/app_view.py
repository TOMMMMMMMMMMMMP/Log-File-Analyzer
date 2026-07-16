import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from datetime import datetime


class AppView(tk.Tk):
    """Main GUI for the Log File Analyzer."""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Log File Analyzer")
        self.geometry("950x620")
        self.resizable(True, True)
        self._build_ui()

    # ── UI construction ───────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        self.configure(padx=16, pady=16)

        # Top bar
        top = ttk.Frame(self)
        top.pack(fill="x", pady=(0, 10))

        ttk.Label(top, text="📋 Log File Analyzer",
                  font=("Segoe UI", 13, "bold")).pack(side="left")

        ttk.Button(top, text="📂 Open Log File",
                   command=self._on_open).pack(side="right", padx=(6, 0))

        # File label
        self.file_var = tk.StringVar(value="No file loaded")
        ttk.Label(self, textvariable=self.file_var,
                  foreground="gray").pack(anchor="w", pady=(0, 8))

        # Filters row
        filter_frame = ttk.Frame(self)
        filter_frame.pack(fill="x", pady=(0, 8))

        ttk.Label(filter_frame, text="Level:").pack(side="left")
        self.level_var = tk.StringVar(value="ALL")
        level_cb = ttk.Combobox(filter_frame, textvariable=self.level_var,
                                values=["ALL", "INFO", "WARNING", "ERROR"],
                                state="readonly", width=10)
        level_cb.pack(side="left", padx=(4, 16))
        level_cb.bind("<<ComboboxSelected>>", lambda e: self._refresh_table())

        ttk.Label(filter_frame, text="Search:").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._refresh_table())
        ttk.Entry(filter_frame, textvariable=self.search_var,
                  width=30).pack(side="left", padx=(4, 0))

        # Table
        cols = ("Timestamp", "Level", "Message")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=16)
        self.tree.heading("Timestamp", text="Timestamp")
        self.tree.heading("Level",     text="Level")
        self.tree.heading("Message",   text="Message")
        self.tree.column("Timestamp", width=160, anchor="center")
        self.tree.column("Level",     width=90,  anchor="center")
        self.tree.column("Message",   width=650)

        # Color tags
        self.tree.tag_configure("INFO",    foreground="#2196F3")
        self.tree.tag_configure("WARNING", foreground="#FF9800")
        self.tree.tag_configure("ERROR",   foreground="#F44336")

        scrollbar = ttk.Scrollbar(self, orient="vertical",
                                  command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="left", fill="y")

        # Bottom buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", pady=(10, 0))

        ttk.Button(btn_frame, text="📊 Bar Chart",
                   command=self._on_chart).pack(side="left", padx=(0, 6))
        ttk.Button(btn_frame, text="📈 Timeline",
                   command=self._on_timeline).pack(side="left", padx=(0, 6))
        ttk.Button(btn_frame, text="📄 Report",
                   command=self._on_report).pack(side="left", padx=(0, 6))
        ttk.Button(btn_frame, text="💾 Export JSON",
                   command=self._on_export).pack(side="left")

        # Status bar
        self.status_var = tk.StringVar(value="Ready.")
        ttk.Label(self, textvariable=self.status_var,
                  foreground="gray").pack(anchor="w", pady=(8, 0))

    # ── Actions ───────────────────────────────────────────────────────────────

    def _on_open(self) -> None:
        filepath = filedialog.askopenfilename(
            title="Select a log file",
            filetypes=[("Log files", "*.log"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not filepath:
            return
        ok, msg = self.controller.load_file(filepath)
        if ok:
            self.file_var.set(filepath)
            self.status_var.set(msg)
            self._refresh_table()
        else:
            messagebox.showerror("Error", msg)

    def _refresh_table(self) -> None:
        """Reload the table with current filters."""
        self.tree.delete(*self.tree.get_children())
        if not self.controller.has_data():
            return

        level = self.level_var.get()
        keyword = self.search_var.get()
        entries = self.controller.get_entries(level, keyword)

        for e in entries:
            self.tree.insert("", "end", values=(
                e.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                e.level,
                e.message,
            ), tags=(e.level,))

        self.status_var.set(f"Showing {len(entries)} entries.")

    def _on_chart(self) -> None:
        if not self.controller.has_data():
            messagebox.showwarning("Warning", "No data loaded.")
            return
        self.controller.show_chart()

    def _on_timeline(self) -> None:
        if not self.controller.has_data():
            messagebox.showwarning("Warning", "No data loaded.")
            return
        self.controller.show_timeline()

    def _on_report(self) -> None:
        if not self.controller.has_data():
            messagebox.showwarning("Warning", "No data loaded.")
            return
        report = self.controller.get_report()
        win = tk.Toplevel(self)
        win.title("Summary Report")
        win.geometry("500x400")
        text = scrolledtext.ScrolledText(win, font=("Courier", 10), padx=12, pady=12)
        text.pack(fill="both", expand=True)
        text.insert("1.0", report)
        text.config(state="disabled")

    def _on_export(self) -> None:
        if not self.controller.has_data():
            messagebox.showwarning("Warning", "No data loaded.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile="export.json"
        )
        if not path:
            return
        ok, msg = self.controller.export_json(path)
        if ok:
            messagebox.showinfo("Export", msg)
        else:
            messagebox.showerror("Error", msg)
