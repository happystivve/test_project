from cefpython3 import cefpython as cef
import base64
import platform
import sys, os
import threading
import json

def main():
    assert cef.__version__ >= "57.0", "CEF Python v57.0+ required to run this"
    sys.excepthook = cef.ExceptHook
    settings = {
        "product_version": "MyProduct/10.00",
        "user_agent": "MyAgent/20.00 MyProduct/10.00"
    }
    cef.Initialize(settings=settings)
    set_global_handler()

    url="file://"+os.path.dirname(__file__)+'/site/index.html'

    browser = cef.CreateBrowserSync(
        navigateUrl=url,
        window_title="Tutorial")
    set_client_handlers(browser)
    # set_javascript_bindings(browser)
    cef.MessageLoop()
    cef.Shutdown()

def set_global_handler():
    # A global handler is a special handler for callbacks that
    # must be set before Browser is created using
    # SetGlobalClientCallback() method.
    global_handler = GlobalHandler()
    cef.SetGlobalClientCallback("OnAfterCreated",
                                global_handler.OnAfterCreated)


def set_client_handlers(browser):
    client_handlers = [LoadHandler(), DisplayHandler()]
    for handler in client_handlers:
        browser.SetClientHandler(handler)


# def set_javascript_bindings(browser):
#     external = External(browser)
#     bindings = cef.JavascriptBindings(
#             bindToFrames=False, bindToPopups=False)
#     bindings.SetProperty("python_property", "This property was set in Python")
#     bindings.SetProperty("cefpython_version", cef.GetVersion())
#     bindings.SetFunction("html_to_data_uri", html_to_data_uri)
#     bindings.SetObject("external", external)
#     browser.SetJavascriptBindings(bindings)


# def js_print(browser, lang, event, msg):
#     # Execute Javascript function "js_print"
#     browser.ExecuteFunction("js_print", lang, event, msg)


class GlobalHandler(object):
    def OnAfterCreated(self, browser, **_):
        """Called after a new browser is created."""
        pass

class LoadHandler(object):
    def OnLoadingStateChange(self, browser, is_loading, **_):
        """Called when the loading state has changed."""
        if not is_loading:
            print('OnLoadingStateChange...')
            # страничка загрузилась - заполняем контент
            browser.GetUrl()
            browser.ExecuteFunction("addButtons", '[{"caption":"one","code":1}]')


class DisplayHandler(object):
    def OnConsoleMessage(self, browser, message, **_):
        """Called to display a console message."""
        print(message)
        try:
            a=json.loads(message)
            if a ['method']=='select-item' :
                open_next(browser)
        except Exception:
            pass

def open_next(browser, **_):
    url="file://"+os.path.dirname(__file__)+'/site/index2.html'
    browser.LoadUrl(url)

def exit_app(browser):
    # Important note:
    #   Do not close browser nor exit app from OnLoadingStateChange
    #   OnLoadError or OnPaint events. Closing browser during these
    #   events may result in unexpected behavior. Use cef.PostTask
    #   function to call exit_app from these events.
    print("[test_cef.py] Close browser and exit app")
    browser.CloseBrowser()
    cef.QuitMessageLoop()

if __name__ == '__main__':
    main()
# Javascript.callbacks()