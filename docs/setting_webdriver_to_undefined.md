# Setting webdriver to undefined

The variable `navigator.webdriver` returns `true` in selenium. To avoid this, whenever the browser performs action, the following code is run:

```python
self.browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
```

Because every action resets the variable to `true`, it is necessary to run the script after every `.get()` and `.click()` at least. To that effect, three new methods on the `IgBot` class are creted:
- `click()`
- `click_with_script()`
- `get()`

`click()` and `click_with_script()` take as a parameter the element on which the browser is to click. `click_with_script()` is a wrapper around `self.browser.execute_script("arguments[0].click();", element)`

`get()` takes as a parameter the URL.
