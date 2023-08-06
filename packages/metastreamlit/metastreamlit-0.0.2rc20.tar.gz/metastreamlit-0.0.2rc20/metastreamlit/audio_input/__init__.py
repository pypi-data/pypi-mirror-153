import os
import streamlit.components.v1 as components
import base64
from typing import Optional
from dataclasses import dataclass


# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = True

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

_COMPONENT_NAME = os.path.splitext(os.path.basename(__file__))[0]

if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("my_component"
        # does not fit this bill, so please choose something better for your
        # own component :)
        _COMPONENT_NAME,
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3000",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "build")
    _component_func = components.declare_component(_COMPONENT_NAME, path=build_dir)


@dataclass
class AudioInputComponentOutput:
    data: bytes
    mime_type: str

# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def audio_input(key=None) -> Optional[AudioInputComponentOutput]:
    """TODO: DOC
    """

    component_data = _component_func(key=key, default=None)
    if component_data is None:
        return None
    message_bytes = component_data['b64'].encode('ascii')
    base64_bytes = base64.b64decode(message_bytes)
    return AudioInputComponentOutput(
        data=base64_bytes,
        mime_type=component_data['mime_type']
    )


# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run template_component/__init__.py`
if __name__ == "__main__":
    import streamlit as st

    audio_data = audio_input(key=0)
    if audio_data is None:
        st.write("Please record something above")
    else:
        st.write(f"This is what you recorded (len={len(audio_data.data)}) - type={audio_data.mime_type}")
        st.audio(audio_data.data)
