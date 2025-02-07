# DO NOT EDIT: This file is auto-generated by generate-schema/index.ts
from typing import Union
import msgspec

class Size(msgspec.Struct, omit_defaults=True): 
    height: float
    """The height of the window in logical pixels.""" 
    width: float
    """The width of the window in logical pixels.""" 

class GetVersionRequest(msgspec.Struct, tag_field="$type", tag="getVersion"): 
    id: str
    """The id of the request.""" 

class EvalRequest(msgspec.Struct, tag_field="$type", tag="eval"): 
    id: str
    """The id of the request.""" 
    js: str
    """The javascript to evaluate.""" 

class SetTitleRequest(msgspec.Struct, tag_field="$type", tag="setTitle"): 
    id: str
    """The id of the request.""" 
    title: str
    """The title to set.""" 

class GetTitleRequest(msgspec.Struct, tag_field="$type", tag="getTitle"): 
    id: str
    """The id of the request.""" 

class SetVisibilityRequest(msgspec.Struct, tag_field="$type", tag="setVisibility"): 
    id: str
    """The id of the request.""" 
    visible: bool
    """Whether the window should be visible or hidden.""" 

class IsVisibleRequest(msgspec.Struct, tag_field="$type", tag="isVisible"): 
    id: str
    """The id of the request.""" 

class OpenDevToolsRequest(msgspec.Struct, tag_field="$type", tag="openDevTools"): 
    id: str
    """The id of the request.""" 

class GetSizeRequest(msgspec.Struct, tag_field="$type", tag="getSize"): 
    id: str
    """The id of the request.""" 
    include_decorations: Union[bool | None] = None
    """Whether to include the title bar and borders in the size measurement.""" 

class SetSizeRequest(msgspec.Struct, tag_field="$type", tag="setSize"): 
    id: str
    """The id of the request.""" 
    size: Size
    """The size to set.""" 

class FullscreenRequest(msgspec.Struct, tag_field="$type", tag="fullscreen"): 
    id: str
    """The id of the request.""" 
    fullscreen: Union[bool | None] = None
    """Whether to enter fullscreen mode. If left unspecified, the window will enter fullscreen mode if it is not already in fullscreen mode or exit fullscreen mode if it is currently in fullscreen mode.""" 

class MaximizeRequest(msgspec.Struct, tag_field="$type", tag="maximize"): 
    id: str
    """The id of the request.""" 
    maximized: Union[bool | None] = None
    """Whether to maximize the window. If left unspecified, the window will be maximized if it is not already maximized or restored if it was previously maximized.""" 

class MinimizeRequest(msgspec.Struct, tag_field="$type", tag="minimize"): 
    id: str
    """The id of the request.""" 
    minimized: Union[bool | None] = None
    """Whether to minimize the window. If left unspecified, the window will be minimized if it is not already minimized or restored if it was previously minimized.""" 

class LoadHtmlRequest(msgspec.Struct, tag_field="$type", tag="loadHtml"): 
    html: str
    """HTML to set as the content of the webview.""" 
    id: str
    """The id of the request.""" 
    origin: Union[str | None] = None
    """What to set as the origin of the webview when loading html. If not specified, the origin will be set to the value of the `origin` field when the webview was created.""" 

class LoadUrlRequest(msgspec.Struct, tag_field="$type", tag="loadUrl"): 
    id: str
    """The id of the request.""" 
    url: str
    """URL to load in the webview.""" 
    headers: Union[dict[str, str] | None] = None
    """Optional headers to send with the request.""" 

WebViewRequest  = Union[GetVersionRequest, EvalRequest, SetTitleRequest, GetTitleRequest, SetVisibilityRequest, IsVisibleRequest, OpenDevToolsRequest, GetSizeRequest, SetSizeRequest, FullscreenRequest, MaximizeRequest, MinimizeRequest, LoadHtmlRequest, LoadUrlRequest] 
""" 
Explicit requests from the client to the webview. 
""" 
