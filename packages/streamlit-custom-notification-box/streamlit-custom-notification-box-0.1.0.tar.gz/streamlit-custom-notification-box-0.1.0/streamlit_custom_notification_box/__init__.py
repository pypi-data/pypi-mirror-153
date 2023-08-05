import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _custom_notification_box = components.declare_component(
        
        "custom_notification_box",

        url="http://localhost:3001",
    )
else:

    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _custom_notification_box = components.declare_component("custom_notification_box", path=build_dir)

def custom_notification_box(icon, textDisplay, externalLink, url, styles, key=None, defaultIndex=0):

    return _custom_notification_box(icon=icon, 
                                    textDisplay=textDisplay, 
                                    externalLink=externalLink, 
                                    url=url, 
                                    styles=styles,
                                    key=key, 
                                    default=defaultIndex)

if not _RELEASE:
    import streamlit as st


    custom_notification_box(icon='info', textDisplay='We are almost done with your registration.', externalLink='more info', url='#', styles=None, key="foo")
   
