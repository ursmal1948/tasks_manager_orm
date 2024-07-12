add_task_schema = {
    "type": "object",
    "properties": {
        "status": {"type": "string", "enum": ["NEW", "IN_PROGRESS", "COMPLETED"], "default": "NEW"},
        "project_id": {"type": "integer"},
    },
    "required": ["project_id"],
}