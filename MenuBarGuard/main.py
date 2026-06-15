#!/usr/bin/env python3
"""
MenuBarGuard - macOS menu bar notch/spacer helper.

This app intentionally uses public AppKit status items only. macOS does not
allow ordinary apps to directly move or hide other apps' menu bar items, so the
tool creates an adjustable empty status item that can be positioned and sized.
"""

from __future__ import annotations

import subprocess

from AppKit import (
    NSApp,
    NSApplication,
    NSApplicationActivationPolicyAccessory,
    NSMenu,
    NSMenuItem,
    NSScreen,
    NSStatusBar,
    NSVariableStatusItemLength,
)
from Foundation import NSObject, NSUserDefaults
from PyObjCTools import AppHelper


APP_NAME = "MenuBarGuard"
APP_VERSION = "1.0"
BUNDLE_ID = "com.zhuchichi.menubarguard"

DEFAULT_WIDTH = 220
MIN_WIDTH = 0
MAX_WIDTH = 640
STEP = 20
WIDTH_PRESETS = [0, 80, 120, 160, 200, 240, 280, 320, 400, 480]

KEY_ENABLED = "enabled"
KEY_WIDTH = "width"


def clamp(value: int, low: int = MIN_WIDTH, high: int = MAX_WIDTH) -> int:
    return max(low, min(high, int(value)))


class MenuBarGuardApp(NSObject):
    def applicationDidFinishLaunching_(self, _notification):
        self.defaults = NSUserDefaults.standardUserDefaults()
        self.status_bar = NSStatusBar.systemStatusBar()

        stored_enabled = self.defaults.objectForKey_(KEY_ENABLED)
        self.enabled = (
            self.defaults.boolForKey_(KEY_ENABLED)
            if stored_enabled is not None
            else True
        )

        stored_width = self.defaults.integerForKey_(KEY_WIDTH)
        self.width = clamp(stored_width or self.recommended_width())

        # Create the spacer first and the control second. Users can still
        # Command-drag status items to position the guard where it helps most.
        self.spacer_item = self.status_bar.statusItemWithLength_(self.active_width())
        self.control_item = self.status_bar.statusItemWithLength_(NSVariableStatusItemLength)

        spacer_button = self.spacer_item.button()
        if spacer_button is not None:
            spacer_button.setTitle_("")
            spacer_button.setToolTip_("MenuBarGuard spacer")

        control_button = self.control_item.button()
        if control_button is not None:
            control_button.setTitle_("MBG")
            control_button.setToolTip_("MenuBarGuard")

        self.menu = NSMenu.alloc().initWithTitle_(APP_NAME)
        self.control_item.setMenu_(self.menu)
        self.rebuild_menu()

    def active_width(self) -> float:
        return float(self.width if self.enabled else 0)

    def recommended_width(self) -> int:
        screen = NSScreen.mainScreen()
        if screen is None:
            return DEFAULT_WIDTH

        try:
            if (
                screen.respondsToSelector_("auxiliaryTopLeftArea")
                and screen.respondsToSelector_("auxiliaryTopRightArea")
            ):
                frame = screen.frame()
                left = screen.auxiliaryTopLeftArea()
                right = screen.auxiliaryTopRightArea()
                notch_width = frame.size.width - left.size.width - right.size.width
                if 60 <= notch_width <= 420:
                    return clamp(round(notch_width + 40))
        except Exception:
            pass

        return DEFAULT_WIDTH

    def save_settings(self):
        self.defaults.setBool_forKey_(self.enabled, KEY_ENABLED)
        self.defaults.setInteger_forKey_(self.width, KEY_WIDTH)
        self.defaults.synchronize()

    def apply_layout(self):
        self.spacer_item.setLength_(self.active_width())
        self.save_settings()
        self.rebuild_menu()

    def menu_item(self, title: str, action: str | None = None, enabled: bool = True):
        item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            title,
            action,
            "",
        )
        item.setEnabled_(enabled)
        if action is not None:
            item.setTarget_(self)
        return item

    def add_separator(self):
        self.menu.addItem_(NSMenuItem.separatorItem())

    def rebuild_menu(self):
        self.menu.removeAllItems()

        self.menu.addItem_(self.menu_item(f"{APP_NAME} {APP_VERSION}", None, False))
        self.menu.addItem_(
            self.menu_item(
                f"防遮挡空白区: {'开启' if self.enabled else '关闭'}",
                None,
                False,
            )
        )
        self.menu.addItem_(self.menu_item(f"当前宽度: {self.width} px", None, False))

        self.add_separator()

        toggle_title = "关闭空白区" if self.enabled else "开启空白区"
        self.menu.addItem_(self.menu_item(toggle_title, "toggleGuard:"))
        self.menu.addItem_(self.menu_item("自动估算刘海宽度", "useRecommendedWidth:"))

        self.add_separator()

        width_menu = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "空白区宽度",
            None,
            "",
        )
        submenu = NSMenu.alloc().initWithTitle_("空白区宽度")
        for preset in WIDTH_PRESETS:
            item = self.menu_item(f"{preset} px", "setPresetWidth:")
            item.setTag_(preset)
            item.setState_(1 if self.width == preset else 0)
            submenu.addItem_(item)
        width_menu.setSubmenu_(submenu)
        self.menu.addItem_(width_menu)

        smaller = self.menu_item(f"缩小 {STEP} px", "decreaseWidth:")
        smaller.setEnabled_(self.width > MIN_WIDTH)
        self.menu.addItem_(smaller)

        larger = self.menu_item(f"增大 {STEP} px", "increaseWidth:")
        larger.setEnabled_(self.width < MAX_WIDTH)
        self.menu.addItem_(larger)

        self.add_separator()

        self.menu.addItem_(self.menu_item("打开显示器设置", "openDisplaySettings:"))
        self.menu.addItem_(self.menu_item("退出", "quit:"))

    def toggleGuard_(self, _sender):
        if self.enabled:
            self.enabled = False
        else:
            self.enabled = True
            if self.width == 0:
                self.width = self.recommended_width()
        self.apply_layout()

    def useRecommendedWidth_(self, _sender):
        self.width = self.recommended_width()
        self.enabled = True
        self.apply_layout()

    def setPresetWidth_(self, sender):
        self.width = clamp(sender.tag())
        self.enabled = self.width > 0
        self.apply_layout()

    def decreaseWidth_(self, _sender):
        self.width = clamp(self.width - STEP)
        self.enabled = self.width > 0
        self.apply_layout()

    def increaseWidth_(self, _sender):
        self.width = clamp(self.width + STEP)
        self.enabled = True
        self.apply_layout()

    def openDisplaySettings_(self, _sender):
        subprocess.Popen(
            ["open", "x-apple.systempreferences:com.apple.Displays-Settings.extension"]
        )

    def quit_(self, _sender):
        NSApp.terminate_(self)


def main():
    app = NSApplication.sharedApplication()
    app.setActivationPolicy_(NSApplicationActivationPolicyAccessory)
    delegate = MenuBarGuardApp.alloc().init()
    app.setDelegate_(delegate)
    AppHelper.runEventLoop()


if __name__ == "__main__":
    main()
