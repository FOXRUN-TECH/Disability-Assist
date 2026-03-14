# New API Endpoint Scaffold Command

Scaffold a new Python cloud API endpoint with Pydantic models, consent lane annotation, and tests. [TS][CON]

## Usage

```text
/new-api <endpoint-name>
```

Example: `/new-api intent` creates an intent processing endpoint.

## What It Creates

### 1. Pydantic Models (`cloud/api/models/<name>.py`)

```python
"""<Endpoint> models.

Pydantic models for the <endpoint> API.
"""

from pydantic import BaseModel, constr


class <Name>Request(BaseModel):
    """Request model for <endpoint>."""

    # Fields with type annotations and validators
    pass


class <Name>Response(BaseModel):
    """Response model for <endpoint>.

    Data classification: sensitive
    """

    # Fields with type annotations
    pass
```

### 2. Router File (`cloud/api/routes/<name>.py`)

```python
"""<Endpoint> API routes.

Handles <description>.
"""

from fastapi import APIRouter

# consent-lane: core-cloud
router = APIRouter(prefix="/api/v1/<name>", tags=["<name>"])


@router.get("/")
async def get_<name>() -> <Name>Response:
    """Get <name> data.

    Returns:
        <Name>Response with current state.
    """
    pass
```

### 3. Constants (`cloud/constants/<name>.py`)

```python
"""<Endpoint> constants."""

from typing import Final

<NAME>_DEFAULT: Final[str] = "value"
```

### 4. Test File (`tests/unit/test_<name>.py`)

```python
"""Tests for <endpoint> API."""

import pytest
from httpx import AsyncClient


class TestGet<Name>:
    """Tests for GET /api/v1/<name>."""

    async def test_returns_200(self, client: AsyncClient) -> None:
        """Returns 200 with valid response."""
        response = await client.get("/api/v1/<name>")
        assert response.status_code == 200
```

### 5. Register Router

Add to main app file:

```python
from cloud.api.routes.<name> import router as <name>_router
app.include_router(<name>_router)
```

## Checklist

- [ ] Pydantic models with field validators [TS]
- [ ] Google-style docstrings on all functions
- [ ] Constants in `cloud/constants/` (no magic numbers)
- [ ] Custom exceptions subclassing `AssistError`
- [ ] Router registered in main app
- [ ] Test file with behavior-driven names [TF]
- [ ] **Consent lane annotation** on router (`# consent-lane: <lane>`)
- [ ] **Data classification** on response models
- [ ] File-scoped quality check on new files

## Related Commands

- `/review` -- Review before committing
- `/commit` -- Commit the new endpoint
- `/privacy-audit` -- Verify consent lanes
