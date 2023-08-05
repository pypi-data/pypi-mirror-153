"""
    Module for interacting with the Gab.com website.
"""

# pylint: disable=too-many-arguments

import os
import tempfile
import time
from typing import Optional, Tuple

from download import download  # type: ignore
from open_webdriver import Driver, open_webdriver  # type: ignore
from pyjpgclipboard import clipboard_load_jpg  # type: ignore
from selenium.webdriver.common.action_chains import ActionChains  # type: ignore
from selenium.webdriver.common.keys import Keys  # type: ignore

# Simulate a phone screen orientation.
WIDTH = 400
HEIGHT = 800

TIMEOUT_IMAGE_UPLOAD = 60  # Wait upto 60 seconds to upload the image.

DEFAULT_DRIVER_NAME = "chrome"


def _action_login(driver: Driver, username: str, password: str) -> None:
    """Logs into Gab.com and posts the given content."""
    # clear the web driver's local storage.
    driver.delete_all_cookies()  # Delete any cookies, otherwise sign in breaks.
    driver.set_window_size(WIDTH, HEIGHT)  # Yes this is needed tool, or it breaks.
    # Do a hard refresh to get the sign in page.
    # Handle Page sign in, where the user and password are entered.
    driver.get("https://gab.com/")
    driver.execute_script("localStorage.clear();")
    driver.execute_script("sessionStorage.clear();")
    driver.refresh()
    # driver.get("https://gab.com/auth/sign_in")
    # Wait for the page to load.
    time.sleep(1)
    # Find the login button and click it
    el_login_btn = driver.find_element_by_xpath('//*[contains(text(), "Log in")]')
    el_login_btn.click()
    el_email = driver.find_element_by_id("user_email")
    el_email.click()
    el_email.send_keys(username)
    el_password = driver.find_element_by_id("user_password")
    el_password.click()
    el_password.send_keys(password)
    el_submit_btn = driver.find_element_by_name("button")
    el_submit_btn.click()


def _action_make_post(
    driver: Driver,
    content: str,
    jpg_path: Optional[str] = None,
    dry_run: Optional[bool] = False,
) -> None:
    """Makes a social media post"""
    driver.get("https://gab.com/compose")
    el_compose_window = driver.find_element_by_id("main-composer")
    el_compose_window.click()
    # Now use the keyboard to enter in the content.
    actions = ActionChains(driver)
    actions.send_keys(content)
    actions.perform()
    # Upload the image if it's been specified.
    if jpg_path is not None:
        # Assert file has jpeg extension.
        assert jpg_path.lower().endswith(".jpg"), f"{__file__}: {jpg_path} is not a jpeg file."
        # Copy the image to the clipboard and then paste it into the post.
        if "http" in jpg_path:
            # download the image url to a local temp file and then put it on the clipboard.
            with tempfile.NamedTemporaryFile(delete=False) as temp:
                try:
                    temp.close()
                    download(jpg_path, temp.name, replace=True, timeout=60.0)
                    clipboard_load_jpg(temp.name)
                finally:
                    os.remove(temp.name)
        else:
            clipboard_load_jpg(jpg_path)
        # Send a paste command to the keyboard.
        actions = ActionChains(driver)
        actions.key_down(Keys.META)
        actions.send_keys("v")
        actions.perform()
        timeout = time.time() + TIMEOUT_IMAGE_UPLOAD
        while True:
            try:
                # Wait for the image to upload.
                # Find the element with the xpath that includes an image source
                driver.find_element_by_xpath('//img[contains(@src, "media_attachments")]')
                break
            except Exception:  # pylint: disable=broad-except
                if time.time() > timeout:
                    print(
                        f"{__file__}: Failed to upload image, because timed out waiting for "
                        f"{jpg_path} to upload for {TIMEOUT_IMAGE_UPLOAD} seconds."
                    )
                    break
                time.sleep(0.5)
    # Perform the post action.
    # Find an element that contains "Post"
    time.sleep(1)
    el_post_btn = driver.find_element_by_xpath('//*[contains(text(), "Post")]')
    # put the mouse over the button of el_post_btn and click it.
    actions = ActionChains(driver)
    actions.move_to_element(el_post_btn)
    actions.click()
    if not dry_run:
        actions.perform()
    # Give 1 second for the post to succeed. Otherwise it can sometimes fail.
    time.sleep(1)


def gab_post(
    username: str,
    password: str,
    content: str,
    jpg_path: Optional[str] = None,
    dry_run: bool = False,
    headless: bool = False,
) -> None:
    """Logs into Gab.com and posts the given content."""
    leaks_session = True  # True for chrome.
    if leaks_session:
        # What the heck is this a bug in chromium or gab? Session id leaks ACROSS
        # sessions.
        with open_webdriver(headless=headless) as driver:
            # Deep clean the local device storage and session id which for some reason
            # is cached.
            driver.session_id = None

    with open_webdriver(headless=headless) as driver:
        try:
            _action_login(driver, username, password)
            _action_make_post(driver, content, jpg_path=jpg_path, dry_run=dry_run)
        finally:
            try:
                driver.delete_all_cookies()
                driver.execute_script("window.localStorage.clear();")
                driver.execute_script("window.sessionStorage.clear();")
                driver.session_id = None
            except Exception:  # pylint: disable=broad-except
                print(f"{__file__}: Failed to clear local/session storage.")


def gab_test(headless: bool = False) -> Tuple[bool, Optional[Exception]]:
    """Tests if the gab driver works."""
    try:
        with open_webdriver(headless=headless) as driver:
            driver.get("https://gab.com")
        return True, None
    except Exception as err:  # pylint: disable=broad-except
        return False, err


if __name__ == "__main__":
    gab_test()
