# DO NOT EDIT: This file is auto-generated by generate-schema/index.ts
from enum import Enum
from typing import Union
import msgspec

class Size(msgspec.Struct, omit_defaults=True): 
    height: float
    """The height of the window in logical pixels.""" 
    width: float
    """The width of the window in logical pixels.""" 

class WebViewContentUrl(msgspec.Struct, kw_only=True, omit_defaults=True): 
    url: str
    """Url to load in the webview. Note: Don't use data URLs here, as they are not supported. Use the `html` field instead.""" 
    headers: Union[dict[str, str] | None] = None
    """Optional headers to send with the request.""" 

class WebViewContentHtml(msgspec.Struct, kw_only=True, omit_defaults=True): 
    html: str
    """Html to load in the webview.""" 
    origin: Union[str | None] = None
    """What to set as the origin of the webview when loading html.""" 

WebViewContent = Union[WebViewContentUrl, WebViewContentHtml] 
""" 
The content to load into the webview. 
""" 
class WindowSizeStates(str, Enum): 
    maximized = "maximized" 
    fullscreen = "fullscreen" 

WindowSize = Union[WindowSizeStates, Size] 
class WebViewOptions(msgspec.Struct, omit_defaults=True): 
    """ 
    Options for creating a webview. 
    """ 
    title: str
    """Sets the title of the window.""" 
    acceptFirstMouse: Union[bool | None] = None
    """Sets whether clicking an inactive window also clicks through to the webview. Default is false.""" 
    autoplay: Union[bool | None] = None
    """When true, all media can be played without user interaction. Default is false.""" 
    clipboard: Union[bool | None] = None
    """Enables clipboard access for the page rendered on Linux and Windows.

macOS doesn’t provide such method and is always enabled by default. But your app will still need to add menu item accelerators to use the clipboard shortcuts.""" 
    decorations: Union[bool | None] = None
    """When true, the window will have a border, a title bar, etc. Default is true.""" 
    devtools: Union[bool | None] = None
    """Enable or disable webview devtools.

Note this only enables devtools to the webview. To open it, you can call `webview.open_devtools()`, or right click the page and open it from the context menu.""" 
    focused: Union[bool | None] = None
    """Sets whether the webview should be focused when created. Default is false.""" 
    incognito: Union[bool | None] = None
    """Run the WebView with incognito mode. Note that WebContext will be ingored if incognito is enabled.

Platform-specific: - Windows: Requires WebView2 Runtime version 101.0.1210.39 or higher, does nothing on older versions, see https://learn.microsoft.com/en-us/microsoft-edge/webview2/release-notes/archive?tabs=dotnetcsharp#10121039""" 
    initializationScript: Union[str | None] = None
    """Run JavaScript code when loading new pages. When the webview loads a new page, this code will be executed. It is guaranteed that the code is executed before window.onload.""" 
    ipc: Union[bool | None] = None
    """Sets whether host should be able to receive messages from the webview via `window.ipc.postMessage`.""" 
    load: Union[WebViewContent | None] = None
    """The content to load into the webview.""" 
    size: Union[WindowSize | None] = None
    """The size of the window.""" 
    transparent: Union[bool | None] = None
    """Sets whether the window should be transparent.""" 
    userAgent: Union[str | None] = None
    """Sets the user agent to use when loading pages.""" 

