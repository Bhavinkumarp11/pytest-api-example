# Bugs Found 

### 1. File: `schemas.py`

**Issue:**  
- The schema was incorrectly defining the `'name'` property as an `'integer'`.

**Fix:**  
- Updated the schema to define `'name'` as a `'string'`.

**Before:**
```json
{
    "type": "object",
    "properties": {
        "name": {
            "type": "integer"
        }
    }
}
```

**After:**
```json
{
    "type": "object",
    "properties": {
        "name": {
            "type": "string"
        }
    }
}
```

---

### 2. File: `app.py`

**Issue:**  
- The abort message was not using an f-string, so the variable `'status'` was not being interpolated.

**Fix:**  
- Updated the line to use an f-string for dynamic error messaging.

**Before:**
```python
api.abort(400, 'Invalid pet status {status}')
```

**After:**
```python
api.abort(400, f'Invalid pet status {status}')
```

---

### 3. File: `test_pet.py`

**Issue:**  
- Incorrect use of a string inside a tuple. The parametrize list had a single string that wasn't correctly formatted as a list of values.

**Fix:**  
- Replaced with a proper list of strings.

**Before:**
```python
@pytest.mark.parametrize("status", [("available")])
```

**After:**
```python
@pytest.mark.parametrize("status", ["available", "sold", "pending"])