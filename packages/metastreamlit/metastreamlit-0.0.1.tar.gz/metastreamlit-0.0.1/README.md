# MetaAI Streamlit components

Install with `pip install metastreamlit`

## Components
### `template_component`

This is a basic components aimed at demonstrating how to create custom components in streamlit - taken from [streamlit's custom component template](https://github.com/streamlit/component-template).

```python
import streamlit as st
import metastreamlit as mst

num_clicks = mst.template_component("World", key=0)
st.markdown("You've clicked %s times!" % int(num_clicks))
```

## Developping components

### Adding a new component

To create a new component `my_component`, follow these steps:
1. Copy `metastreamlit/template_component` to `metastreamlit/my_component`
2. Edit `metastreamlit/__init__.py` to add an import for your component, so users can call it from `metastreamlit.template_component` directly

### Developping a component

To develop a component `my_component`, follow these steps:
1. run npm:
```bash
cd metastreamlit/my_component
npm install
npm run start
```
2. Test it by running it within streamlit:
```bash
cd metastreamlit/my_component
# Set `_RELEASE = False` in the __init__.py file
streamlit run __init__.py
```
