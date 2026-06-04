#!/usr/bin/env python3
"""
WakeKeeper — 防止 Mac 休眠的菜单栏工具
类似 Amphetamine，使用系统内置 caffeinate 命令。
"""

import subprocess
import time

import rumps

# 定时选项：(菜单文字, 秒数)
DURATIONS = [
    ("15 分钟", 15 * 60),
    ("30 分钟", 30 * 60),
    ("1 小时",  60 * 60),
    ("2 小时",  120 * 60),
    ("4 小时",  240 * 60),
]

STATUS_OFF = "状态: 关闭"
STATUS_ON  = "状态: 开启 ✓  （点击停止）"


class WakeKeeperApp(rumps.App):
    def __init__(self):
        super().__init__(
            name="WakeKeeper",
            title="☕",
            quit_button=None,   # 自定义退出项，以便清理进程
        )

        self._process: subprocess.Popen | None = None  # caffeinate 子进程
        self._session_timer: rumps.Timer | None = None  # 定时自动停止
        self._session_end_time: float = 0.0            # 会话到期时间戳
        self._active = False
        self.allow_screen_sleep = False                # 是否允许屏幕休眠

        # ── 菜单项 ──────────────────────────────────────
        self._status_item = rumps.MenuItem(STATUS_OFF, callback=self.on_toggle)

        # 定时子菜单
        timed_menu = rumps.MenuItem("定时防休眠")
        for label, secs in DURATIONS:
            item = rumps.MenuItem(label, callback=self._make_timed_cb(secs))
            timed_menu.add(item)

        self._screen_sleep_item = rumps.MenuItem(
            "允许屏幕休眠", callback=self.on_toggle_screen_sleep
        )
        self._screen_sleep_item.state = False  # 默认不勾选

        quit_item = rumps.MenuItem("退出", callback=self.on_quit)

        self.menu = [
            self._status_item,
            None,
            timed_menu,
            rumps.MenuItem("无限期防休眠", callback=self.on_indefinite),
            None,
            self._screen_sleep_item,
            None,
            quit_item,
        ]

    # ── 内部启停 ─────────────────────────────────────────

    def _caffeinate_flag(self) -> str:
        """
        -d  防止显示器休眠（屏幕保持亮）
        -i  只防系统 idle sleep，允许屏幕变暗/锁屏
        """
        return "-i" if self.allow_screen_sleep else "-d"

    def _start(self, duration_sec: int | None = None):
        """启动 caffeinate，可选限时（秒）。"""
        self._stop()  # 先清理旧会话

        flag = self._caffeinate_flag()
        cmd = ["caffeinate", flag]
        if duration_sec:
            cmd += ["-t", str(duration_sec)]
            # 用 rumps.Timer（主线程）监控到期，自动更新 UI
            self._session_end_time = time.time() + duration_sec
            self._session_timer = rumps.Timer(self._check_session, 2)
            self._session_timer.start()

        self._process = subprocess.Popen(cmd)
        self._active = True
        self.title = "⚡"
        self._status_item.title = STATUS_ON

    def _stop(self):
        """终止 caffeinate 并重置 UI。"""
        if self._session_timer:
            self._session_timer.stop()
            self._session_timer = None

        if self._process:
            self._process.terminate()
            self._process = None

        self._active = False
        self.title = "☕"
        self._status_item.title = STATUS_OFF

    def _check_session(self, timer: rumps.Timer):
        """每 2 秒检查定时是否到期（在主线程执行）。"""
        if time.time() >= self._session_end_time:
            timer.stop()
            self._stop()

    def _make_timed_cb(self, secs: int):
        """为定时菜单项生成回调闭包。"""
        def callback(_sender):
            self._start(duration_sec=secs)
        return callback

    # ── 菜单回调 ─────────────────────────────────────────

    def on_toggle(self, _sender):
        """点击状态行：开→关，关→无限期开。"""
        if self._active:
            self._stop()
        else:
            self._start()

    def on_indefinite(self, _sender):
        """无限期防休眠。"""
        self._start()

    def on_toggle_screen_sleep(self, sender):
        """切换"允许屏幕休眠"开关。"""
        self.allow_screen_sleep = not self.allow_screen_sleep
        sender.state = self.allow_screen_sleep
        # 如果正在运行，重启以应用新的 caffeinate 参数
        if self._active:
            self._start()

    def on_quit(self, _sender):
        """退出时先杀掉 caffeinate。"""
        self._stop()
        rumps.quit_application()


if __name__ == "__main__":
    WakeKeeperApp().run()
